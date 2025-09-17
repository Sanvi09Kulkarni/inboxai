import gradio as gr
import os
import requests

# ✅ Read Hugging Face API Key from Environment
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "facebook/bart-large-cnn"
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

def summarize_text(text, max_length=130, min_length=30):
    """Call Hugging Face Inference API to summarize text."""
    payload = {
        "inputs": text,
        "parameters": {"max_length": max_length, "min_length": min_length, "do_sample": False},
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"⚠️ API Error {response.status_code}: {response.text}"
    data = response.json()
    if isinstance(data, list) and "summary_text" in data[0]:
        return data[0]["summary_text"]
    return "⚠️ No summary generated (empty response)"

def summarizer_interface(email_text):
    if not email_text.strip():
        return "⚠️ Please enter some text!"
    return summarize_text(email_text)

# ✅ Build Gradio UI
demo = gr.Interface(
    fn=summarizer_interface,
    inputs=gr.Textbox(lines=10, placeholder="Paste your email text here..."),
    outputs="text",
    title="📩 AI Inbox Summarizer",
    description="Paste your email content and get a clean, short summary powered by Hugging Face."
)

if __name__ == "__main__":
    demo.launch()
