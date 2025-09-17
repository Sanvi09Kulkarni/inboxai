from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# ✅ Use a public summarization model (no token required)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

class EmailRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API is running ✅"}

@app.post("/summarize")
def summarize_email(request: EmailRequest):
    try:
        summary = summarizer(request.text, max_length=60, min_length=10, do_sample=False)
        return {"summary": summary[0]['summary_text']}
    except Exception as e:
        return {"error": str(e)}

