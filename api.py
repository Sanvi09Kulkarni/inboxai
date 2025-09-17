from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# ✅ Load lightweight model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# ✅ Warm up once at startup to prevent first-request timeout
summarizer("This is a warmup text to load the model.", max_length=20, min_length=5)

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
