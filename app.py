import streamlit as st
from src.preprocess import clean_email
from src.summariser import summarize_text
from src.action_items import extract_action_items

st.title("AI Inbox Summariser — Demo")

# File uploader
uploaded_files = st.file_uploader(
    "Upload email files (.txt or .eml)", 
    type=["txt", "eml"],
    accept_multiple_files=True
)

emails = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        content = uploaded_file.read().decode("utf-8", errors="ignore")
        emails.append(content)

    st.success(f"{len(emails)} emails uploaded successfully ✅")

    if emails and st.button("Summarize All Emails"):
        for i, email in enumerate(emails, 1):
            st.subheader(f"📩 Email {i}")
            cleaned = clean_email(email)
            summary = summarize_text(cleaned)
            action_items = extract_action_items(cleaned)

            # Display results
            st.markdown(f"**Summary:**\n\n{summary}")
            st.markdown("**Action items detected:**")
            for item in action_items:
                st.markdown(f"- {item}")

