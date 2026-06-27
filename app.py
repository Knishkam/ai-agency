import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()
from agent import analyze_url
from scraper import extract_links
def main():
    st.title("Web Scraper AI Agent")
    st.caption("Enter any URL and ask questions about it!")
    url = st.text_input("Enter URL:", placeholder="https://example.com")
    question = st.text_input("Ask a question:", placeholder="What is this page about?")
    if url and question:
        if st.button("Analyze"):
            with st.spinner("Scraping and analysing..."):
                answer = analyze_url(url, question)
                st.success("Done!")
                st.write("### Answer:")
                st.write(answer)
    if url and st.button("Extract Links"):
        links = extract_links(url)
        st.write(f"Found {len(links)} links:")
        for link in links[:20]:
            st.write(link)
if __name__ == "__main__":
    main()
