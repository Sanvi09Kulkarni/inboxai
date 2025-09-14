# Use slim Python base (much smaller)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (change if your app runs on a different port)
EXPOSE 8000

# Start the app (replace main.py with your entrypoint)
CMD ["python", "main.py"]
