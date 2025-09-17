import gradio as gr
from transformers import pipeline

# Load smaller, faster model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_email(text):
    if not text.strip():
        return "⚠️ Cannot summarize empty text."
    result = summarizer(text, max_length=80, min_length=10, do_sample=False)
    return result[0]['summary_text']

# Build a simple UI
demo = gr.Interface(
    fn=summarize_email,
    inputs=gr.Textbox(lines=8, placeholder="Paste email text here..."),
    outputs="text",
    title="AI Inbox Summarizer",
    description="Paste an email and get a quick summary using a distilled BART model."
)

if __name__ == "__main__":
    demo.launch()

