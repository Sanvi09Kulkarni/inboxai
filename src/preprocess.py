# src/preprocess.py
from bs4 import BeautifulSoup
import re

def html_to_text(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text('\n')

def remove_quoted_text(text):
    if not text:
        return ""
    # remove "On <date> <name> wrote:" but keep the following text
    text = re.sub(r'(?s)On .*wrote:\s*', '', text)
    # remove lines starting with '>'
    text = '\n'.join([l for l in text.splitlines() if not l.strip().startswith('>')])
    return text

def remove_signature(text):
    if not text:
        return ""
    # naive signature cut at common markers
    parts = re.split(r'(?i)\n(?:--|thanks|regards|best regards|sent from my|kind regards)\b', text)
    return parts[0].strip()

def strip_greeting(text):
    if not text:
        return ""
    lines = [l for l in text.splitlines() if l.strip()!='']
    if lines and len(lines[0].split()) <= 4 and lines[0].strip().endswith(','):
        lines = lines[1:]
    return '\n'.join(lines).strip()

def clean_email(raw):
    """
    Full cleaning pipeline: remove html, quoted text, signatures and greetings.
    """
    text = raw if isinstance(raw, str) else ""
    if '<' in text[:300] and '>' in text[:300]:
        text = html_to_text(text)
    text = remove_quoted_text(text)
    text = remove_signature(text)
    text = strip_greeting(text)
    # unify spacing
    text = re.sub(r'\n\s+\n', '\n\n', text).strip()
    return text


