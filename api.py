from fastapi import FastAPI
from pydantic import BaseModel
from src.preprocess import clean_email
from src.summariser import summarize_text
from src.action_items import extract_action_items

# Initialize FastAPI app
app = FastAPI()

# Define request body
class EmailRequest(BaseModel):
    email: str

@app.get("/")
def home():
    return {"message": "AI Inbox Summariser API is running 🚀"}

@app.post("/summarize")
def summarize_email(request: EmailRequest):
    # Clean and summarize the email
    cleaned = clean_email(request.email)
    summary = summarize_text(cleaned)
    action_items = extract_action_items(cleaned)

    return {
        "summary": summary,
        "action_items": action_items
    }
