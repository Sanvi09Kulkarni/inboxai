# scripts/load_kaggle.py
import os
import sys
import argparse
import pandas as pd
import glob
import json
import time
import uuid
from email import message_from_string, policy

# ensure project root is on path when run directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.preprocess import clean_email
from src.summariser import summarize_text
from src.action_items import extract_action_items
from src.prioritiser import compute_priority
from src.reply_suggester import generate_replies
from src.db import init_db, save_email

def read_emails_from_csv(csv_path, body_columns=None):
    df = pd.read_csv(csv_path, dtype=str, encoding='utf-8', on_bad_lines='skip')
    # find likely text column
    if body_columns is None:
        body_columns = ['message','content','body','text','mail','message_text']
    candidates = [c for c in body_columns if c in df.columns]
    emails = []
    for idx, row in df.iterrows():
        text = None
        for c in candidates:
            v = row.get(c)
            if isinstance(v, str) and v.strip():
                text = v
                break
        # fallback: try to join all string columns
        if not text:
            text = " ".join([str(v) for v in row.tolist() if isinstance(v, str)])[:10000]
        emails.append({
            "id": str(row.name),
            "sender": row.get('from') or row.get('sender') or '',
            "subject": row.get('subject') or '',
            "date": row.get('date') or '',
            "body": text
        })
    return emails

def read_emails_from_maildir(folder):
    eml_files = glob.glob(os.path.join(folder, '**', '*.eml'), recursive=True)
    emails = []
    for i, path in enumerate(eml_files):
        try:
            raw = open(path, 'r', encoding='utf-8', errors='ignore').read()
            msg = message_from_string(raw, policy=policy.default)
            # extract plain text part
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_content()
                        break
            else:
                body = msg.get_content()
            emails.append({
                "id": str(i),
                "sender": msg.get('From') or '',
                "subject": msg.get('Subject') or '',
                "date": msg.get('Date') or '',
                "body": body or raw
            })
        except Exception as e:
            print("Failed to parse:", path, e)
    return emails

def anonymize_text(text):
    # simple anonymizer: replace email addresses
    import re
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', text)
    # optionally mask phone numbers
    text = re.sub(r'\+?\d[\d\-\s]{6,}\d', '[PHONE]', text)
    return text

def process_and_save(emails, out_csv='outputs/kaggle_summaries.csv', sample_limit=None, anonymize=False):
    os.makedirs(os.path.dirname(out_csv) or '.', exist_ok=True)
    conn = init_db('emails.db')
    rows = []
    total = len(emails) if sample_limit is None else min(len(emails), sample_limit)
    for i, e in enumerate(emails[:total]):
        print(f"[{i+1}/{total}] Processing id={e.get('id')}")
        raw = e.get('body') or ''
        if anonymize:
            raw_proc = anonymize_text(raw)
        else:
            raw_proc = raw
        clean = clean_email(raw_proc)
        summary = summarize_text(clean)
        action_items = extract_action_items(clean)
        priority, score = compute_priority(action_items, clean)
        try:
            replies = generate_replies(clean, n=3)
        except Exception as ex:
            print("Reply generation failed (continue):", ex)
            replies = []
        rec = {
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
        save_email(conn, rec)
        rows.append({
            "id": rec['id'],
            "sender": rec['sender'],
            "subject": rec['subject'],
            "date": rec['date'],
            "summary": rec['summary'],
            "action_items": json.dumps(rec['action_items'], ensure_ascii=False),
            "priority": rec['priority'],
            "priority_score": rec['priority_score'],
            "replies": json.dumps(rec['replies'], ensure_ascii=False)
        })
    # save CSV
    pd.DataFrame(rows).to_csv(out_csv, index=False, encoding='utf-8')
    conn.close()
    print("Saved", out_csv)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", help="Path to Kaggle CSV file (if CSV).")
    p.add_argument("--maildir", help="Path to maildir / folder with .eml files.")
    p.add_argument("--n", type=int, default=50, help="Number of emails to process (use small N first).")
    p.add_argument("--anonymize", action='store_true', help="Anonymize emails (mask addresses).")
    args = p.parse_args()

    if args.csv:
        emails = read_emails_from_csv(args.csv)
    elif args.maildir:
        emails = read_emails_from_maildir(args.maildir)
    else:
        print("Provide --csv or --maildir")
        sys.exit(1)

    # run processing (sample n)
    process_and_save(emails, out_csv='outputs/kaggle_summaries.csv', sample_limit=args.n, anonymize=args.anonymize)
