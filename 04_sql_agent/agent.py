import sqlite3
import os
from groq import Groq
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
DATABASE_PATH = Path("company.db")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
SEMANTIC_LAYER = {
    "revenue": "amount",
    "sales": "amount",
    "top customers": "ORDER BY total_purchases DESC LIMIT 10",
    "best selling": "ORDER BY quantity DESC LIMIT 10",
    "recent orders": "ORDER BY order_date DESC LIMIT 10",
    "expensive products": "ORDER BY price DESC LIMIT 10",
}
FORBIDDEN_KEYWORDS = [
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"
]
def validate_query(query: str) -> tuple[bool, str]:
    query_upper = query.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_upper:
            return False, f"'{keyword}' not allowed!"
    return True, "query is safe!"
def get_schema() -> str:
    return """
        DATABASE SCHEMA:

            Table: customers
            Columns: id, name, email, total_purchases, city

            Table: products
            Columns: id, name, price, category, stock

            Table: orders
            Columns: id, customer_id, product_id, quantity, order_date, amount    

            RELATIONSHITPS:
            orders.customer_id -> customers.id
            orders.product_id -> products.id
            """
def execute_query(query: str) -> tuple[bool, any]:
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return True, results
    except Exception as e:
        return False, str(e)
def ask_agent(user_question: str, conversation_history: list) -> str:
    schema = get_schema()
    system_prompt = f"""
    You are an expert SQL agent.
    You have access to this database:

    {schema}

    RULES:
    1. Always write SELECT queries only
    2. Always add LIMIT 10 to prevent large results
    3. Use the schema above to write correct SQL
    4. Return ONLY the SQL query - nothing else

    SEMANTIC LAYER:
    {SEMANTIC_LAYER}
    """
    messages = conversation_history.copy()
    messages.append({
        "role": "user",
        "content": user_question
        })
    for attempt in range(3):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            max_tokens=500,
            temperature=0.1
        )
        sql_query = response.choices[0].message.content.strip()
        is_safe, safety_message = validate_query(sql_query)
        if not is_safe:
            message.append({
                "role": "user",
                "content": f"Query rejected: {safety_message}. Write a safe SELECT query only."
            })
            continue
        success,result = execute_query(sql_query)
        if success:
            final_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Convert this SQL result to a friendly human readable answer."},
                    {"role": "user", "content": f"Question: {user_question}\nSQL: {sql_query}\nResult: {result}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return final_response.choices[0].message.content.strip()
        else:
            messages.append({
                "role": "user",
                "content": f"Query failed: {result}. Fix the SQL query."
            })
    return "Sorry, I couldn't process your request after 3 attempts."
def main():
    st.title("SQL AI Agent")
    st.caption("Ask questions about your database in plain English!")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    if prompt := st.chat_input("Ask about your data..."):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Thinking..."):
            response = ask_agent(prompt, st.session_state.messages)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        with st.chat_message("assistant"):
            st.write(response)
if __name__ == "__main__":
    main()