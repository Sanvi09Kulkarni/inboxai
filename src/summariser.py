from transformers import pipeline

# ✅ Load model locally (no API key required, will work on Railway too if dependencies installed)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=130, min_length=30):
    """
    Summarizes the given text using the BART summarization model.
    Args:
        text (str): The input text to summarize.
        max_length (int): Maximum number of tokens in summary.
        min_length (int): Minimum number of tokens in summary.
    Returns:
        str: Generated summary text.
    """
    if not text.strip():
        return "⚠️ Cannot summarize empty text."

    try:
        result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        if isinstance(result, list) and "summary_text" in result[0]:
            return result[0]["summary_text"]
        return "⚠️ No summary generated (empty response)"
    except Exception as e:
        return f"⚠️ Error during summarization: {str(e)}"
