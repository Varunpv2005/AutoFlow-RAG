# AutoFlow-RAG

AutoFlow-RAG is an enterprise-grade document intelligence and retrieval platform built around the existing Autonomous RAG architecture: React frontend, FastAPI backend, FAISS vector search, JWT authentication, and Gemini-grounded answer generation.

The product is optimized for grounded question answering over uploaded enterprise documents, with explainable retrieval, document metadata, chat memory, and operational analytics all preserved inside the original architecture.

---

## What this platform now delivers

- Local vector ingestion with FAISS and sentence-transformer embeddings
- Document lifecycle management with upload, indexing, chunk counts, and processing status
- Explainable retrieval with source cards, confidence scoring, chunk previews, latency, and similarity evidence
- Multi-document retrieval support and conversational history for follow-up questions
- Analytics and system health monitoring for operational visibility
- Commercial-quality UI patterns with loading states, notifications, and responsive layouts

---

## Architecture

- Frontend: React + Vite + TypeScript + Zustand + Chakra UI
- Backend: FastAPI + SQLAlchemy + JWT + Pydantic
- Retrieval: FAISS + LangChain + local sentence-transformer embeddings
- LLM: Google Gemini via the official SDK

---

## Production readiness checklist

- Document ingestion and metadata enrichment are completed through the existing upload flow
- Retrieval metadata is exposed back to the UI as human-readable evidence
- File and chat lifecycle analytics surface meaningful operational telemetry
- The codebase is aligned with a clean service boundary and existing deployment flow

---

## Quick Start

### 1. Requirements
- Python 3.9+
- Node.js 18+
- Google Gemini API Key (`GEMINI_API_KEY`)
- Optional: `VITE_ADMIN_TOKEN` for protected admin reset actions

---

## 🚀 Quick Setup Checklist

1. **Get a Gemini API Key**: From [Google AI Studio](https://aistudio.google.com/).
2. **Configure backend environment variables** in `backend/.env`.
3. **Configure optional frontend admin token** in `frontend/.env` if you want to protect the app reset endpoint.
4. **Set up backend** (Python, FastAPI)
5. **Set up frontend** (Node.js, Vite)
6. **Open the app** in your browser: [http://localhost:5173](http://localhost:5173)

---

### 2. Backend Setup (FastAPI)
- **Create and activate a virtual environment:**
  ```bash
  cd backend
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
  ```
- **Configure backend environment variables:**
  Create or update `backend/.env` with:
  ```env
  GEMINI_API_KEY=your_gemini_api_key_here
  JWT_SECRET_KEY=super-secret-jwt-key-for-production
  CHAT_RAG_ADMIN_TOKEN=supersecret
  CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
  FAISS_PATH=./data/faiss_index
  UPLOAD_DIR=./data/files
  ```
  - `GEMINI_API_KEY` is required for the Gemini LLM.
  - `JWT_SECRET_KEY` should be changed in production.
  - `CHAT_RAG_ADMIN_TOKEN` secures admin reset calls.
  - `CORS_ALLOWED_ORIGINS` controls frontend access.
- **Install Python dependencies:**
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
- **Start the backend server:**
  ```bash
  uvicorn app.main:app --reload --reload-dir app --reload-exclude venv --reload-exclude **/site-packages/**
  ```
  - The backend API will be available at: [http://localhost:8000/api](http://localhost:8000/api)

### 3. Frontend Setup (Vite)
- **Create optional frontend `.env`:**
  ```env
  VITE_ADMIN_TOKEN=supersecret
  ```
  - This is used by the frontend admin reset UI only.
- **Install Node.js dependencies:**
  ```bash
  cd frontend
  npm install
  ```
- **Start the frontend dev server:**
  ```bash
  npm run dev
  ```
  - The frontend app will be available at: [http://localhost:5173](http://localhost:5173)

---

## 4. Docker Deployment
- **Build and start services:**
  ```bash
  docker compose up --build
  ```
- **Backend:** `http://localhost:8000/api`
- **Frontend:** `http://localhost:3000`
- **Notes:**
  - `frontend` is served from Nginx on port `3000`.
  - `backend` uses the `.env` file mounted by `docker-compose.yml`.
  - Update `docker-compose.yml` or `backend/.env` for custom production values.

## 5. Verification
- Frontend build: `cd frontend && npm run build`
- Frontend lint: `cd frontend && npm run lint`
- Backend tests: `cd backend && pytest`
- Docker: `docker compose up --build`

## Architecture

- **Frontend**: Vite + React + TypeScript + Zustand + Chakra UI
- **Backend**: FastAPI + SQLAlchemy + LangChain + ChromaDB + Google GenAI SDK
- **Embeddings**: Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`) via `HuggingFaceEmbeddings`
- **LLM**: Google Gemini 2.5 Flash (`gemini-2.5-flash`) via `google-genai`
- **RAG Pipeline**: Chunking, local embedding, hybrid retrieval, and chat with sources

---

## License
[MIT](LICENSE)
