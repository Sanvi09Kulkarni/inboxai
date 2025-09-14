import os
import requests

# Read Hugging Face API token from environment variables
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum"

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def summarize_text(text):
    if not HF_API_TOKEN:
        return "[Error: Hugging Face token not set]"

    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return f"[Error: {response.status_code} - {response.text}]"

    try:
        result = response.json()
        return result[0].get("summary_text", "[Error: No summary returned]")
    except Exception as e:
        return f"[Error: Failed to parse response: {str(e)}]"


