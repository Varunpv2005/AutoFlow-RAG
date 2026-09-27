FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for unstructured, pdfplumber, curl, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libmagic1 libpoppler-cpp-dev poppler-utils curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# ── CPU-only PyTorch pre-install ────────────────────────────────────────────
# torch==2.7.0 on PyPI resolves to the CUDA-enabled wheel (865 MB) which also
# pulls nvidia-cublas, nvidia-cudnn, nvidia-cuda-runtime, etc. (~2.5 GB total).
# This application runs sentence-transformers/all-MiniLM-L6-v2 on CPU only.
# Pre-installing from the PyTorch CPU wheel index (~180 MB) satisfies the
# torch==2.7.0 pin in requirements.txt (PEP 440: 2.7.0+cpu matches ==2.7.0)
# so pip skips the CUDA wheel when processing the full requirements.
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    torch==2.7.0 \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining application dependencies (torch already satisfied above).
# --no-deps: requirements.txt is a complete pip freeze with all transitive deps
#            pinned explicitly, so dependency resolution is unnecessary and
#            the metadata-fetch round-trips it triggers are skipped entirely.
# --timeout=300: raise per-read timeout from pip's 15s default to 300s.
# --retries=5:  retry each download up to 5 times on transient failures.
RUN pip install --no-cache-dir --no-deps --timeout=300 --retries=5 -r requirements.txt

COPY . .

# Create non-root user and directories with appropriate ownership
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data/faiss_index /data/files && \
    chown -R appuser:appuser /app /data

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
