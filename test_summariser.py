from src.summariser import summarize_text

test_text = """
Artificial Intelligence is transforming industries worldwide.
It is used in healthcare for faster diagnoses, in finance for fraud detection,
and in education for personalized learning. The adoption is growing every year.
"""

print("Summary:", summarize_text(test_text))
