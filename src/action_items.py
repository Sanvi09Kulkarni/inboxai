import re

def extract_action_items(text: str):
    action_items = []

    # Normalize text
    lines = text.splitlines()
    for line in lines:
        line_clean = line.strip()

        # Match deadlines / due dates / actions
        if re.search(r"\b(due|deadline|submit|asap|complete|finish|remind|by tomorrow|by [A-Z][a-z]+day)\b", line_clean, re.IGNORECASE):
            action_items.append(f"🔴 **{line_clean}**")  # Highlight urgent ones in red/bold
        elif re.search(r"\b(meeting|call|follow up|reply|update)\b", line_clean, re.IGNORECASE):
            action_items.append(f"📌 {line_clean}")
        elif re.search(r"\b(report|plan|send|share|review)\b", line_clean, re.IGNORECASE):
            action_items.append(f"✉️ {line_clean}")

    if not action_items:
        action_items.append("✅ No actionable items detected.")

    return action_items
