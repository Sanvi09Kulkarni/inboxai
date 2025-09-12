# src/db.py
import sqlite3
import json

def init_db(db_path='emails.db'):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS emails (
      id TEXT PRIMARY KEY,
      sender TEXT,
      subject TEXT,
      date TEXT,
      raw_body TEXT,
      clean_body TEXT,
      summary TEXT,
      action_items TEXT,
      priority TEXT,
      priority_score INTEGER,
      replies TEXT
    )
    ''')
    conn.commit()
    return conn

def save_email(conn, email):
    """
    email is a dict with keys:
      id, sender, subject, date, raw_body, clean_body, summary,
      action_items (list), priority (str), priority_score (int), replies (list)
    """
    cur = conn.cursor()
    cur.execute('''
      INSERT OR REPLACE INTO emails (id,sender,subject,date,raw_body,clean_body,summary,action_items,priority,priority_score,replies)
      VALUES (?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        email.get('id'),
        email.get('sender'),
        email.get('subject'),
        email.get('date'),
        email.get('raw_body'),
        email.get('clean_body'),
        email.get('summary'),
        json.dumps(email.get('action_items', [])),
        email.get('priority'),
        email.get('priority_score'),
        json.dumps(email.get('replies', []))
    ))
    conn.commit()

def get_all_emails(conn):
    cur = conn.cursor()
    cur.execute("SELECT id,sender,subject,date,summary,action_items,priority,replies FROM emails ORDER BY date DESC")
    rows = cur.fetchall()
    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "sender": r[1],
            "subject": r[2],
            "date": r[3],
            "summary": r[4],
            "action_items": json.loads(r[5]) if r[5] else [],
            "priority": r[6],
            "replies": json.loads(r[7]) if r[7] else []
        })
    return results
