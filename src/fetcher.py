# src/fetcher.py
import imaplib, email
from email.header import decode_header
import getpass

def fetch_from_imap(host, username, password, folder='INBOX', limit=50):
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select(folder)
    typ, data = mail.search(None, 'ALL')
    ids = data[0].split()[-limit:]
    emails = []
    for i in ids[::-1]:
        typ, msg_data = mail.fetch(i, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8', errors='ignore')
        from_ = msg.get('From')
        date = msg.get('Date')
        # get body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/plain' and part.get_content_disposition() is None:
                    body = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors='ignore')
        emails.append({'id': i.decode(), 'subject': subject, 'from': from_, 'date': date, 'body': body})
    return emails
