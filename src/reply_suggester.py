# src/reply_suggester.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# small/flan works well for short generation, will download on first run
MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_replies(email_text, n=3):
    """
    Returns list of n reply strings (short professional replies).
    Uses different temperatures for variety.
    """
    temps = [0.0, 0.6, 0.9]
    temps = temps[:n] + [temps[-1]]*(n - len(temps))
    replies = []
    prompt_template = (
        "Write a short, professional email reply (<= 30 words) to the message below. "
        "Be polite and concise.\n\nMessage:\n" + email_text
    )
    for t in temps[:n]:
        inputs = tokenizer(prompt_template, return_tensors="pt", truncation=True, max_length=512)
        # on CPU, generation can be slow; keep max_new_tokens small
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=(t>0),
            temperature=t,
            top_k=50 if t>0 else None,
            num_return_sequences=1
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        replies.append(text)
    return replies
