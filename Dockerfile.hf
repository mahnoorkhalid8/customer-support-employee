# Hugging Face Spaces Dockerfile for FastAPI Backend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY production/ ./production/
COPY .env.example .env

# Expose port (Hugging Face uses 7860 by default)
EXPOSE 7860

# Run the application
CMD ["uvicorn", "production.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
