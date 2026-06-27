import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
from scraper import scrape_url, extract_links, clean_text
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)
def analyze_url(url: str, question: str) -> str:
    raw_text = scrape_url(url)
    if not raw_text:
        return "could not scrape the URL. Please try another."
    cleaned = clean_text(raw_text)
    prompt = f"""
    You are a web data analyst.

    Website  Content:
    {cleaned}
    User Question: {question}
    Answer  based only on the content above.
    If answer not found, say "Not found on this page."
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
