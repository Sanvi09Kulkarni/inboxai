from src.preprocess import remove_quoted_text, html_to_text

# Test html_to_text
print("HTML Test:", html_to_text("<html><body><p>Hello World</p></body></html>"))

# Test remove_quoted_text
print("Quoted Text Test:", remove_quoted_text("On Monday John wrote: hi\n> quoted text\nmain content"))
