FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for unstructured, pdfplumber, curl, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libmagic1 libpoppler-cpp-dev poppler-utils curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# ── CPU-only PyTorch pre-install ────────────────────────────────────────────
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    torch==2.7.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining application dependencies
RUN pip install --no-cache-dir --no-deps --timeout=300 --retries=5 -r requirements.txt

COPY . .

# Create non-root user and directories with appropriate ownership
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data/faiss_index /data/files && \
    chown -R appuser:appuser /app /data

USER appuser

EXPOSE 10000

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:${PORT:-10000}/api/health || exit 1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
