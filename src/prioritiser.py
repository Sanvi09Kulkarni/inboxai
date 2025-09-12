# src/prioritiser.py
import re

URGENCY_KEYWORDS = ['urgent','asap','immediately','important','priority','need by','required']

def compute_priority(action_items, body_text):
    """
    Simple scoring:
      +2 if any action_item has a deadline
      +1 if urgency keywords present
      +1 if 'please' present near a task
    Returns: 'high' | 'medium' | 'low' and numeric score
    """
    score = 0
    # deadline presence
    for ai in action_items:
        if ai.get('deadline_text') or ai.get('dates'):
            score += 2
    # urgency keywords
    for kw in URGENCY_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', body_text, flags=re.IGNORECASE):
            score += 1
            break
    # polite asks
    if re.search(r'\bplease\b', body_text, flags=re.IGNORECASE):
        score += 1

    if score >= 3:
        return 'high', score
    if score == 2:
        return 'medium', score
    return 'low', score
