import streamlit as st
import pandas as pd
import os 
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
from excel_tools import read_excel, get_summary, filter_data, get_column_stats, search_data, to_json_str
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
def analyze_with_ai(question: str, excel_summary: dict, relevant_data: str) -> str:
    prompt = f"""
    You are an expert data analyst.
    
    Excel Summary:
    {excel_summary}

    Relevant Data:
    {relevant_data}

    User Question:
    {question}

    Answer the question based on the data above.
    Be specific and concise.
    If data is not available, say so clearly.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user","content": prompt}],
        max_tokens=500,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
def main():
    st.title("Excel AI Agent")
    st.caption("Upload Excel file and ask questions in plain English!")
    uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx', 'xls'])
    if uploaded_file is not None:
        df = read_excel(uploaded_file)
        if df is not None:
            summary = get_summary(df)
            st.success("Excel file loaded successfully!")
            st.write(f"Rows: {summary['rows']} | Columns: {len(summary['columns'])}")
            question = st.text_input("Ask a question about your data:")
            if question:
                relevant_data = to_json_str(df.head(20))
                answer = analyze_with_ai(question, summary, relevant_data)
                st.write("### Answer:")
                st.write(answer)
        else:
            st.error("Could not read the Excel file!")
if __name__ == "__main__":
    main()