FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for unstructured, pdfplumber, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libmagic1 libpoppler-cpp-dev poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create necessary directories
RUN mkdir -p /app/data/faiss_index /data/files

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
