import requests
from bs4 import BeautifulSoup
import os 
from dotenv import load_dotenv
load_dotenv()
import json 
from typing import Optional
def scrape_url(url: str) -> Optional[str]:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64: x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip =True)
        return text
    except Exception as e:
        return None
def extract_links(url: str) -> list:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windosws NT 10.0: Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=jeaders, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        return links
    except:
        return[]
def clean_text(text: str) -> str:
    lines = text.split("\n")
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned[:100])