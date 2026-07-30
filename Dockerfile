FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn python-multipart jinja2 groq

# Copy application files
COPY . .

# Expose HuggingFace default port
EXPOSE 7860

# Run FastAPI Uvicorn Server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
