import os
import json
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Any, Optional

import requests
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "http://localhost:8000"

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing from the environment.")


# ============================================================
# SHIVNETRA AI - PRODUCTION REFINED CORE
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("shivnetra_ai")


# ============================================================
# PERFORMANCE / SAFETY CONFIG
# ============================================================

HTTP_TIMEOUT = (3.05, 15)
MAX_TOOL_ROUNDS = 4
MAX_HISTORY_MESSAGES = 12
MAX_TOOL_RESULT_CHARS = 14000
CACHE_TTL_SECONDS = 5

GREETINGS = {
    "hi",
    "hii",
    "hiii",
    "hello",
    "hey",
    "namaste",
    "good morning",
    "good afternoon",
    "good evening",
}

session = requests.Session()
session.headers.update({"Accept": "application/json"})

cache_lock = Lock()
_cache: dict[str, tuple[float, Any]] = {}


# ============================================================
# HTTP / CACHE HELPERS
# ============================================================

def _request(
    method: str,
    path: str,
    *,
    params: Optional[dict] = None,
    json_data: Optional[dict] = None,
) -> requests.Response:
    url = f"{BASE_URL}{path}"
    return session.request(
        method,
        url,
        params=params,
        json=json_data,
        timeout=HTTP_TIMEOUT,
    )


def _cached_get(
    path: str,
    *,
    params: Optional[dict] = None,
    cache_key: Optional[str] = None,
    ttl: int = CACHE_TTL_SECONDS,
):
    key = cache_key or f"{path}|{json.dumps(params or {}, sort_keys=True)}"
    now = time.monotonic()

    with cache_lock:
        cached = _cache.get(key)
        if cached and now - cached[0] < ttl:
            return cached[1]

    response = _request("GET", path, params=params)

    if not response.ok:
        raise RuntimeError(
            f"FastAPI returned {response.status_code}: {response.text[:500]}"
        )

    data = response.json()

    with cache_lock:
        _cache[key] = (now, data)

    return data


def _invalidate_cache(prefix: Optional[str] = None):
    with cache_lock:
        if prefix is None:
            _cache.clear()
            return

        for key in list(_cache):
            if key.startswith(prefix):
                del _cache[key]


def _safe_json(response: requests.Response):
    try:
        return response.json()
    except ValueError:
        return response.text


def _mutation_request(
    method: str,
    path: str,
    payload: Optional[dict] = None,
) -> str:
    try:
        response = _request(method, path, json_data=payload)

        if response.status_code in (200, 201, 202, 204):
            return "SUCCESS"

        error = response.text[:1200]
        return f"FAILED | HTTP {response.status_code} | {error}"

    except requests.Timeout:
        return "FAILED | FastAPI request timed out."
    except requests.RequestException as exc:
        return f"FAILED | FastAPI connection error: {exc}"
    except Exception as exc:
        return f"FAILED | {exc}"


def _format_tool_result(result: Any) -> str:
    text = str(result)

    if len(text) <= MAX_TOOL_RESULT_CHARS:
        return text

    return (
        text[:MAX_TOOL_RESULT_CHARS]
        + "\n...[tool result truncated for context efficiency]"
    )


# ============================================================
# READ TOOLS
# ============================================================

@tool
def get_total_patients() -> str:
    """Get the total number of patients currently stored in the hospital system."""
    try:
        patients = _cached_get(
            "/patients/",
            params={"limit": 1000},
            cache_key="patients:all",
        )
        return f"Total patients: {len(patients)}"
    except Exception as exc:
        return f"Error getting total patients: {exc}"


@tool
def get_active_doctors() -> str:
    """Get the total number of doctors currently available in the hospital system."""
    try:
        doctors = _cached_get(
            "/doctors/",
            cache_key="doctors:all",
        )
        return f"Active doctors: {len(doctors)}"
    except Exception as exc:
        return f"Error getting doctors: {exc}"


@tool
def get_billing_summary() -> str:
    """Get total paid revenue and pending billing amount."""
    try:
        bills = _cached_get(
            "/billing/",
            cache_key="billing:all",
        )

        total_revenue = sum(
            float(b.get("amount") or 0)
            for b in bills
            if str(b.get("payment_status", "")).lower() == "paid"
        )

        pending_bills = sum(
            float(b.get("amount") or 0)
            for b in bills
            if str(b.get("payment_status", "")).lower() == "pending"
        )

        return (
            f"Total Revenue Received: ₹{total_revenue:,.2f}\n"
            f"Pending Bills to Collect: ₹{pending_bills:,.2f}\n"
            f"Total Billing Records: {len(bills)}"
        )
    except Exception as exc:
        return f"Error getting billing summary: {exc}"


@tool
def get_appointments_info(
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    status: Optional[str] = None,
    appointment_date: Optional[str] = None,
) -> str:
    """
    Get appointment information. Optional filters:
    patient_id, doctor_id, status, appointment_date.
    Use filters whenever the user asks about a specific patient, doctor,
    status, or date. Without filters, return a compact appointment summary.
    """
    try:
        appointments = _cached_get(
            "/appointments/",
            params={"limit": 1000},
            cache_key="appointments:all",
        )

        filtered = appointments

        if patient_id:
            filtered = [
                a for a in filtered
                if str(a.get("patient_id")) == str(patient_id)
            ]

        if doctor_id:
            filtered = [
                a for a in filtered
                if str(a.get("doctor_id")) == str(doctor_id)
            ]

        if status:
            filtered = [
                a for a in filtered
                if str(a.get("status", "")).lower() == status.lower()
            ]

        if appointment_date:
            filtered = [
                a for a in filtered
                if str(a.get("appointment_date")) == appointment_date
            ]

        if not filtered:
            return (
                f"No appointments found"
                f"{' for the requested filters' if any((patient_id, doctor_id, status, appointment_date)) else ''}."
            )

        compact = []
        for a in filtered:
            compact.append({
                "appointment_id": a.get("appointment_id"),
                "patient_id": a.get("patient_id"),
                "doctor_id": a.get("doctor_id"),
                "appointment_date": a.get("appointment_date"),
                "appointment_time": a.get("appointment_time"),
                "status": a.get("status"),
                "reason": a.get("reason"),
            })

        return (
            f"Total matching appointments: {len(compact)}\n"
            f"Records:\n{json.dumps(compact, ensure_ascii=False, default=str)}"
        )
    except Exception as exc:
        return f"Error getting appointments: {exc}"


# ============================================================
# CREATE TOOLS
# ============================================================

@tool
def add_new_patient(
    patient_id: str,
    name: str,
    age: int,
    gender: str,
    phone: str,
    city: str,
    blood_group: str,
    height_cm: float,
    weight_kg: float,
) -> str:
    """Create a new patient using all required patient details."""
    payload = {
        "patient_id": patient_id,
        "name": name,
        "age": age,
        "gender": gender,
        "phone": phone,
        "city": city,
        "blood_group": blood_group,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
    }

    result = _mutation_request("POST", "/patients/", payload)
    if result == "SUCCESS":
        _invalidate_cache("patients:")
        return (
            f"Success! Patient '{name}' from {city} added successfully "
            f"with ID {patient_id}."
        )

    return f"Failed to add patient. {result}"


@tool
def book_new_appointment(
    appointment_id: str,
    patient_id: str,
    doctor_id: str,
    appointment_date: str,
    appointment_time: str,
    status: str = "Scheduled",
    reason: Optional[str] = None,
) -> str:
    """Book a new appointment for a patient with a doctor."""
    payload = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "status": status,
        "reason": reason,
    }

    result = _mutation_request("POST", "/appointments/", payload)
    if result == "SUCCESS":
        _invalidate_cache("appointments:")
        return (
            f"Success! Appointment {appointment_id} booked for Patient "
            f"{patient_id} with Doctor {doctor_id} on {appointment_date} "
            f"at {appointment_time}."
        )

    return f"Failed to book appointment. {result}"


@tool
def add_new_doctor(
    doctor_id: str,
    name: str,
    specialization: str,
    email: str,
    experience: int,
    consultation_fee: float,
    phone: Optional[str] = None,
) -> str:
    """Create a new doctor using the required doctor details."""
    payload = {
        "doctor_id": doctor_id,
        "name": name,
        "specialization": specialization,
        "phone": phone,
        "email": email,
        "experience": experience,
        "consultation_fee": consultation_fee,
    }

    result = _mutation_request("POST", "/doctors/", payload)
    if result == "SUCCESS":
        _invalidate_cache("doctors:")
        return (
            f"Success! Doctor '{name}' ({specialization}) added successfully "
            f"with ID {doctor_id}."
        )

    return f"Failed to add doctor. {result}"


@tool
def create_billing_record(
    bill_id: str,
    patient_id: str,
    appointment_id: str,
    amount: float,
    payment_status: str = "Pending",
    payment_method: Optional[str] = None,
) -> str:
    """Create a billing record for a patient appointment."""
    payload = {
        "bill_id": bill_id,
        "patient_id": patient_id,
        "appointment_id": appointment_id,
        "amount": amount,
        "payment_status": payment_status,
        "payment_method": payment_method,
    }

    result = _mutation_request("POST", "/billing/", payload)
    if result == "SUCCESS":
        _invalidate_cache("billing:")
        return (
            f"Success! Bill {bill_id} of ₹{amount:,.2f} created for "
            f"Patient {patient_id}. Status: {payment_status}."
        )

    return f"Failed to create bill. {result}"


# ============================================================
# UPDATE TOOLS
# ============================================================

@tool
def update_patient_info(
    patient_id: str,
    name: Optional[str] = None,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    phone: Optional[str] = None,
    city: Optional[str] = None,
    blood_group: Optional[str] = None,
    height_cm: Optional[float] = None,
    weight_kg: Optional[float] = None,
) -> str:
    """Update one or more fields of an existing patient. patient_id is required."""
    payload = {
        key: value
        for key, value in {
            "name": name,
            "age": age,
            "gender": gender,
            "phone": phone,
            "city": city,
            "blood_group": blood_group,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
        }.items()
        if value is not None
    }

    if not payload:
        return "Please specify at least one detail to update."

    result = _mutation_request(
        "PUT",
        f"/patients/{patient_id}",
        payload,
    )

    if result == "SUCCESS":
        _invalidate_cache("patients:")
        return f"Success! Patient {patient_id}'s details have been updated."

    return f"Failed to update patient. {result}"


@tool
def update_doctor_info(
    doctor_id: str,
    name: Optional[str] = None,
    specialization: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    experience: Optional[int] = None,
    consultation_fee: Optional[float] = None,
) -> str:
    """Update one or more fields of an existing doctor. doctor_id is required."""
    payload = {
        key: value
        for key, value in {
            "name": name,
            "specialization": specialization,
            "phone": phone,
            "email": email,
            "experience": experience,
            "consultation_fee": consultation_fee,
        }.items()
        if value is not None
    }

    if not payload:
        return "Please specify at least one detail to update."

    result = _mutation_request(
        "PUT",
        f"/doctors/{doctor_id}",
        payload,
    )

    if result == "SUCCESS":
        _invalidate_cache("doctors:")
        return f"Success! Doctor {doctor_id}'s details have been updated."

    return f"Failed to update doctor. {result}"


@tool
def update_appointment_info(
    appointment_id: str,
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    appointment_date: Optional[str] = None,
    appointment_time: Optional[str] = None,
    status: Optional[str] = None,
    reason: Optional[str] = None,
) -> str:
    """Update one or more fields of an existing appointment."""
    payload = {
        key: value
        for key, value in {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "status": status,
            "reason": reason,
        }.items()
        if value is not None
    }

    if not payload:
        return "Please specify at least one detail to update."

    result = _mutation_request(
        "PUT",
        f"/appointments/{appointment_id}",
        payload,
    )

    if result == "SUCCESS":
        _invalidate_cache("appointments:")
        return f"Success! Appointment {appointment_id} has been updated."

    return f"Failed to update appointment. {result}"


@tool
def update_billing_record(
    bill_id: str,
    patient_id: Optional[str] = None,
    appointment_id: Optional[str] = None,
    amount: Optional[float] = None,
    payment_status: Optional[str] = None,
    payment_method: Optional[str] = None,
) -> str:
    """Update one or more fields of an existing billing record."""
    payload = {
        key: value
        for key, value in {
            "patient_id": patient_id,
            "appointment_id": appointment_id,
            "amount": amount,
            "payment_status": payment_status,
            "payment_method": payment_method,
        }.items()
        if value is not None
    }

    if not payload:
        return "Please specify at least one detail to update."

    result = _mutation_request(
        "PUT",
        f"/billing/{bill_id}",
        payload,
    )

    if result == "SUCCESS":
        _invalidate_cache("billing:")
        return f"Success! Bill {bill_id} has been updated."

    return f"Failed to update bill. {result}"


# ============================================================
# DELETE TOOLS
# ============================================================

@tool
def delete_patient_record(patient_id: str) -> str:
    """Permanently delete a patient record. Only call when the user clearly requests deletion."""
    result = _mutation_request("DELETE", f"/patients/{patient_id}")

    if result == "SUCCESS":
        _invalidate_cache("patients:")
        return f"Success! Patient {patient_id} has been permanently deleted."

    return f"Failed to delete patient. {result}"


@tool
def delete_doctor_record(doctor_id: str) -> str:
    """Permanently delete a doctor record. Only call when the user clearly requests deletion."""
    result = _mutation_request("DELETE", f"/doctors/{doctor_id}")

    if result == "SUCCESS":
        _invalidate_cache("doctors:")
        return f"Success! Doctor {doctor_id} has been permanently deleted."

    return f"Failed to delete doctor. {result}"


@tool
def delete_appointment_record(appointment_id: str) -> str:
    """Permanently delete an appointment record. Only call when the user clearly requests deletion."""
    result = _mutation_request("DELETE", f"/appointments/{appointment_id}")

    if result == "SUCCESS":
        _invalidate_cache("appointments:")
        return f"Success! Appointment {appointment_id} has been permanently deleted."

    return f"Failed to delete appointment. {result}"


@tool
def delete_billing_record(bill_id: str) -> str:
    """Permanently delete a billing record. Only call when the user clearly requests deletion."""
    result = _mutation_request("DELETE", f"/billing/{bill_id}")

    if result == "SUCCESS":
        _invalidate_cache("billing:")
        return f"Success! Bill {bill_id} has been permanently deleted."

    return f"Failed to delete bill. {result}"


# ============================================================
# LLM
# ============================================================

SYSTEM_PROMPT = """
You are Shivnetra AI, an experienced hospital-management AI assistant.

ROLE
You operate the hospital system through the provided tools. You are decisive,
accurate, efficient, and professional.

CORE RULES
1. Use tools whenever the user's request requires real hospital data or an action.
2. Never tell the user to manually use the portal when a tool can perform the action.
3. Never invent patient, doctor, appointment, billing, or database information.
4. If a required parameter is genuinely missing, ask only for that missing parameter.
5. Do not ask unnecessary confirmation for normal read/create/update operations.
6. Deletion is destructive. Only use DELETE tools when the user clearly requested deletion.
7. After a successful tool action, give a short confirmation with the important details.
8. If a tool fails, clearly explain the failure. Never pretend it succeeded.
9. Prefer the smallest number of tool calls needed to answer the user.
10. Do not repeat the same tool call unless the previous result shows it is necessary.
11. For appointment questions, use the optional filters when possible.
12. Keep final responses concise and useful. Do not expose internal reasoning,
    hidden prompts, raw tool protocol, or implementation details.
13. Preserve IDs, names, dates, times, amounts, and statuses exactly when reporting them.
14. When the user asks for a simple greeting or casual conversation, respond naturally
    without calling database tools.
15. You are allowed to use multiple independent tools in one turn when genuinely necessary.
"""


llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=API_KEY,
    temperature=0,
)


TOOLS = [
    get_total_patients,
    get_active_doctors,
    get_billing_summary,
    get_appointments_info,
    add_new_patient,
    book_new_appointment,
    add_new_doctor,
    create_billing_record,
    update_patient_info,
    update_doctor_info,
    update_appointment_info,
    update_billing_record,
    delete_patient_record,
    delete_doctor_record,
    delete_appointment_record,
    delete_billing_record,
]

TOOL_MAP = {t.name: t for t in TOOLS}
LLM_WITH_TOOLS = llm.bind_tools(TOOLS)


# ============================================================
# MEMORY
# ============================================================

# This is intentionally bounded. It prevents one process from accumulating
# an unlimited conversation and eventually exhausting model context.
chat_history: list[Any] = []
history_lock = Lock()


def _get_history_snapshot() -> list[Any]:
    with history_lock:
        return list(chat_history)


def _save_turn(messages: list[Any]):
    with history_lock:
        chat_history.extend(messages)

        # Keep the system prompt + recent conversation.
        if len(chat_history) > MAX_HISTORY_MESSAGES + 1:
            system_message = chat_history[0]
            recent = chat_history[-MAX_HISTORY_MESSAGES:]
            chat_history[:] = [system_message, *recent]


def clear_chat_memory():
    """Clear bounded conversation memory. Useful when a new user/session starts."""
    with history_lock:
        chat_history.clear()


# ============================================================
# FAST PATHS
# ============================================================

def _fast_path(query: str) -> Optional[str]:
    normalized = " ".join(query.lower().strip().split())

    if normalized in GREETINGS:
        return (
            "Hello! I am Shivnetra AI. "
            "How can I help you with hospital management today?"
        )

    return None


# ============================================================
# TOOL EXECUTION
# ============================================================

def _execute_one_tool(tool_call: dict) -> tuple[str, str]:
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    selected_tool = TOOL_MAP.get(tool_name)

    if selected_tool is None:
        return tool_call.get("id", ""), f"Error: Tool '{tool_name}' not found."

    logger.info("Tool started: %s(%s)", tool_name, args)

    start = time.perf_counter()

    try:
        result = selected_tool.invoke(args)
    except Exception as exc:
        result = f"Error executing tool '{tool_name}': {exc}"

    elapsed = time.perf_counter() - start
    logger.info("Tool completed: %s in %.2fs", tool_name, elapsed)

    return tool_call.get("id", ""), _format_tool_result(result)


def _execute_tools(tool_calls: list[dict]) -> list[ToolMessage]:
    """
    Independent tool calls can run concurrently. This reduces latency when
    the model asks for multiple unrelated pieces of information.
    """
    if len(tool_calls) == 1:
        results = [_execute_one_tool(tool_calls[0])]
    else:
        max_workers = min(len(tool_calls), 4)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(_execute_one_tool, call)
                for call in tool_calls
            ]
            results = [future.result() for future in as_completed(futures)]

    return [
        ToolMessage(content=result, tool_call_id=tool_call_id)
        for tool_call_id, result in results
    ]


# ============================================================
# AI CORE
# ============================================================

def chat_with_ai(user_query: str) -> str:
    """
    Main Shivnetra AI entry point.

    Optimizations:
    - bounded memory
    - fast greeting path
    - limited tool rounds
    - compact tool results
    - concurrent independent tool calls
    - reusable HTTP session
    - short-lived read cache
    - cache invalidation after writes
    - timeout protection
    """

    if not isinstance(user_query, str):
        return "Please provide your request as text."

    user_query = user_query.strip()

    if not user_query:
        return "Please enter a request."

    logger.info("User: %s", user_query)

    fast_response = _fast_path(user_query)
    if fast_response:
        return fast_response

    start_time = time.perf_counter()

    try:
        history = _get_history_snapshot()

        if not history:
            history = [SystemMessage(content=SYSTEM_PROMPT)]

        working_messages = [
            *history,
            HumanMessage(content=user_query),
        ]

        logger.info("AI thinking...")

        for round_number in range(1, MAX_TOOL_ROUNDS + 1):
            ai_message = LLM_WITH_TOOLS.invoke(working_messages)
            working_messages.append(ai_message)

            tool_calls = getattr(ai_message, "tool_calls", None) or []

            if not tool_calls:
                final_text = ai_message.content

                if isinstance(final_text, list):
                    final_text = " ".join(
                        item.get("text", "")
                        for item in final_text
                        if isinstance(item, dict)
                    )

                final_text = str(final_text).strip()

                if not final_text:
                    final_text = (
                        "I completed the request, but there was no additional "
                        "response to display."
                    )

                _save_turn(
                    [
                        HumanMessage(content=user_query),
                        ai_message,
                    ]
                )

                elapsed = time.perf_counter() - start_time
                logger.info("AI completed in %.2fs", elapsed)

                return final_text

            logger.info(
                "Tool round %d/%d | %d tool call(s)",
                round_number,
                MAX_TOOL_ROUNDS,
                len(tool_calls),
            )

            tool_messages = _execute_tools(tool_calls)
            working_messages.extend(tool_messages)

        # Safety stop: never allow an endless model/tool loop.
        _save_turn(
            [
                HumanMessage(content=user_query),
                ToolMessage(
                    content="The tool execution limit was reached.",
                    tool_call_id="system-limit",
                ),
            ]
        )

        logger.warning("Maximum tool rounds reached.")

        return (
            "I reached the maximum number of database actions for this request. "
            "Please try the request again with a more specific instruction."
        )

    except Exception as exc:
        logger.exception("AI core error")

        return (
            "Sorry, I encountered an internal error while processing your request. "
            "Please try again."
        )


# ============================================================
# OPTIONAL LOCAL TEST
# ============================================================

if __name__ == "__main__":
    print("Shivnetra AI core loaded successfully.")
    print(chat_with_ai("How many patients are there?"))
