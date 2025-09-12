# main.py
from src.summariser import summarize_text
from src.preprocess import html_to_text, remove_quoted_text

# Example email text
email_html = """
<html><body>
<p>Hi Sanvi,</p>
<p>This is a sample email. Just checking in about your project.</p>
<blockquote>On Monday John wrote: Hi</blockquote>
</body></html>
"""

# Step 1: Clean email
plain_text = html_to_text(email_html)
clean_text = remove_quoted_text(plain_text)

# Step 2: Summarize
summary = summarize_text(clean_text)

# Step 3: Show results
print("\n--- ORIGINAL TEXT ---")
print(clean_text)
print("\n--- SUMMARY ---")
print(summary)
