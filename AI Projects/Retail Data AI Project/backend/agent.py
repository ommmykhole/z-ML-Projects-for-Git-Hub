import os
import time
from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# MySQL Connection
password = quote_plus(os.getenv("DB_PASS"))
engine = create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{password}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
)

executed_queries = []

def run_sql_query(sql_query: str) -> str:
    """Executes a read-only MySQL SELECT query on the 'sales' table."""
    executed_queries.append(sql_query.strip())
    
    clean_q = sql_query.strip().upper()
    if not (clean_q.startswith("SELECT") or clean_q.startswith("WITH")):
        return "Error: Only SELECT queries are allowed."
    
    try:
        df_result = pd.read_sql(sql_query, con=engine)
        if df_result.empty:
            return "Query ran successfully, but returned 0 rows."
        if len(df_result) > 50:
            return f"Showing top 50 of {len(df_result)} rows:\n" + df_result.head(50).to_string(index=False)
        return df_result.to_string(index=False)
    except Exception as e:
        return f"SQL Error: {str(e)}. Please fix the MySQL syntax and call run_sql_query again."

SYSTEM_INSTRUCTION = """
You are an expert Retail Data Analyst AI connected to a MySQL database.
Table name: `sales`

Columns:
- date (DATETIME): Transaction date (YYYY-MM-DD)
- store_id (TEXT): Store identifier (e.g., S001)
- product_id (TEXT): Product identifier (e.g., P0001)
- category (TEXT): Product category (e.g., Groceries, Toys, Electronics, Clothing, Furniture)
- region (TEXT): Region (North, South, East, West)
- inventory_level (INT): Stock available
- units_sold (INT): Number of units sold
- units_ordered (INT): Units ordered from supplier
- demand_forecast (FLOAT): Predicted demand
- price (FLOAT): Unit price
- discount (INT): Discount percentage (0 to 100)
- weather_condition (TEXT): Rainy, Sunny, Cloudy, Snowy
- holiday_promotion (INT): 1 if holiday/promotion, 0 otherwise
- competitor_pricing (FLOAT): Competitor's price
- seasonality (TEXT): Autumn, Summer, Winter, Spring

Important Rules:
1. Always use the `run_sql_query` tool to get exact numbers from the database. NEVER guess.
2. Net Revenue formula: `units_sold * price * (1 - discount / 100.0)`
3. Use valid MySQL syntax (e.g., YEAR(date), MONTH(date), LIMIT).
4. Explain insights clearly and concisely.
5. Efficiency Rule: Always try to answer using a SINGLE efficient SQL query (max 2 only if strictly necessary).
"""



client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[run_sql_query],
        temperature=0.1
    )
)

# 2. ask_ai madhe exact error print kar
def ask_ai(question: str):
    executed_queries.clear()
    wait_times = [5, 8, 10]
    
    for attempt in range(3):
        try:
            response = chat.send_message(question)
            return response.text, executed_queries.copy()
        except Exception as e:
            print(f"\n[EXACT ERROR]: {e}\n")  # <-- He terminal madhe khara error dakhvel
            if "503" in str(e) or "429" in str(e):
                time.sleep(wait_times[attempt])
            else:
                raise e
                
    raise Exception("AI Server is currently busy. Please try again.")