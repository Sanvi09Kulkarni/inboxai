import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")  # Read token from env variable
HF_MODEL = "facebook/bart-large-cnn"  # Hosted model on HuggingFace

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def summarize_text(text, max_length=130, min_length=30):
    payload = {
        "inputs": text,
        "parameters": {"max_length": max_length, "min_length": min_length, "do_sample": False},
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"⚠️ API Error: {response.status_code} - {response.text}"
    data = response.json()
    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]
    return "⚠️ No summary generated (empty response)"


