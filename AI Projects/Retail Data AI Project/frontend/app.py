import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Retail AI Analyst", page_icon="📊", layout="wide")

st.title("📊 Retail Sales Agentic AI")
st.caption("Powered by FastAPI + MySQL (73,100+ rows) + Gemini AI")

API_URL = "http://127.0.0.1:8000/chat"

# Sidebar: Clear chat & Sample Questions
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("💡 Try asking:")
    st.markdown("""
    - *Which category has the highest net revenue?*
    - *Top 5 stores by units sold in 2022*
    - *Compare sales on holiday vs non-holiday*
    - *Is it true that the weather is hot right now?*
    """)

# Chat history initialize kar
if "messages" not in st.session_state:
    st.session_state.messages = []

# Priviose Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql_queries"):
            with st.expander("🔍 View SQL Queries"):
                for q in msg["sql_queries"]:
                    st.code(q, language="sql")

# User input box
if prompt := st.chat_input("Ask Any Question About Your Data.."):
    # 1. User Quary
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. FastAPI la request 
    with st.chat_message("assistant"):
        with st.spinner("Fetching The Ans..."):
            try:
                res = requests.post(API_URL, json={"question": prompt}, timeout=60)
                if res.status_code == 200:
                    data = res.json()
                    answer = data["answer"]
                    queries = data.get("sql_queries", [])

                    st.markdown(answer)
                    if queries:
                        with st.expander("🔍 View SQL Queries"):
                            for q in queries:
                                st.code(q, language="sql")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sql_queries": queries
                    })
                else:
                    st.error(f"API Error ({res.status_code}): {res.text}")
            except requests.exceptions.ConnectionError:
                st.error("⚠️ FastAPI server is down! First, run `uvicorn api:app --reload` on the terminal..")
            except Exception as e:
                st.error(f"Error : {e}")