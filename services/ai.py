import os
import pdfplumber
import pytesseract
import requests
from PIL import Image
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text(file_url):
    response = requests.get(file_url)
    file_path = "/tmp/file"

    with open(file_path, "wb") as f:
        f.write(response.content)

    if file_url.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    else:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)


def analyze_contract(text):
    prompt = f"""
You are an elite entertainment contract analyst.

Return:
- Summary
- Red flags
- Risks
- Improvements
- Rewrite in favor of artist

{text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
