# scripts/run_pipeline.py
from src.preprocess import clean_email
from src.summariser import summarize_text
from src.action_items import extract_action_items
from src.prioritiser import compute_priority
from src.reply_suggester import generate_replies
from src.db import init_db, save_email
import uuid
import time

# dummy data: replace with real fetcher later
DUMMY_EMAILS = [
    {
        "id": "1",
        "sender": "manager@example.com",
        "subject": "Project deliverable due next week",
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "body": "Hi Sanvi, please submit the final report by Friday. We need it for the review. Thanks!"
    },
    {
        "id": "2",
        "sender": "colleague@example.com",
        "subject": "Quick question about the demo",
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "body": "Could you review the demo slides and send feedback by Tuesday? Also, can we schedule a call?"
    }
]

def process_emails(emails):
    conn = init_db('emails.db')
    for e in emails:
        raw = e.get('body') or ''
        clean = clean_email(raw)
        summary = summarize_text(clean)
        action_items = extract_action_items(clean)
        priority, score = compute_priority(action_items, clean)
        replies = generate_replies(clean, n=3)
        email_record = {
            "id": e.get('id') or str(uuid.uuid4()),
            "sender": e.get('sender'),
            "subject": e.get('subject'),
            "date": e.get('date'),
            "raw_body": raw,
            "clean_body": clean,
            "summary": summary,
            "action_items": action_items,
            "priority": priority,
            "priority_score": score,
            "replies": replies
        }
        save_email(conn, email_record)
        print(f"Processed {email_record['id']}  priority={priority}  replies={len(replies)}")
    conn.close()

if __name__ == "__main__":
    process_emails(DUMMY_EMAILS)
