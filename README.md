# AutoFlow-RAG — Autonomous AI Task Execution Engine

AutoFlow-RAG is a deployment-ready document intelligence and retrieval application built around a robust RAG architecture: React frontend, FastAPI backend, FAISS vector store, JWT authentication, local Sentence Transformer embeddings, and Google Gemini 2.5 Flash for grounded answer generation.

The system supports end-to-end question answering over uploaded documents (PDF, DOCX, TXT, CSV, XLSX) with user-scoped isolation, transparent retrieval score tracking, document metadata extraction, persistent chat memory, and operational analytics.

Repository: [https://github.com/Varunpv2005/AutoFlow-RAG](https://github.com/Varunpv2005/AutoFlow-RAG)

---

## Key Features

- **Document Processing & Chunking**: Upload and parse PDF, DOCX, TXT, CSV, and XLSX files with adaptive header/character chunking.
- **Local Embeddings & FAISS Vector Search**: High-performance embedding generation via `sentence-transformers/all-MiniLM-L6-v2` stored in a disk-persisted FAISS index.
- **User Data Isolation**: Implemented user-scoped retrieval by attaching `user_id` metadata to FAISS chunks and filtering retrieved candidates against the authenticated user's identity.
- **Scored Retrieval & Source Citations**: Real retrieval similarity scores calculated from FAISS distance (`1 / (1 + distance)`) presented alongside chunk previews and document page references.
- **Grounded Gemini LLM Answers**: Prompt-constrained Gemini 2.5 Flash completions that refuse out-of-context queries to prevent AI hallucinations.
- **JWT Authentication & Security**: Password hashing with bcrypt, stateless JWT authorization headers, configurable CORS, and upload file size validation (`MAX_UPLOAD_SIZE_MB`).
- **User Analytics & Observability**: Scoped workspace telemetry tracking user document allocation, chat history, latency metrics, and infrastructure health.
- **SSE Incremental Delivery**: Server-Sent Events endpoint (`/api/chat/stream`) delivering answer tokens with done/error event metadata.

---

## Technology Stack

- **Frontend**: React, TypeScript, Vite, Chakra UI, Zustand
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Pydantic, Pytest
- **Database & Storage**: SQLite (local metadata), FAISS (vector index persistence), Local Filesystem
- **LLM & Embeddings**: Google Gemini 2.5 Flash (`google-genai` SDK), Sentence Transformers (`all-MiniLM-L6-v2`) via `HuggingFaceEmbeddings`
- **Infrastructure**: Docker, Docker Compose, Nginx

---

## Architecture Overview

```
[ React + Vite Frontend ]
           │ (HTTP / SSE with JWT Bearer Token)
           ▼
   [ FastAPI Backend ]
    ├── Auth & Security (JWT, bcrypt)
    ├── User Isolation Middleware & Scoped Analytics
    ├── Document Ingestion & Adaptive Chunker
    ├── FAISS Vectorstore (all-MiniLM-L6-v2 embeddings)
    └── Gemini Service (Google GenAI SDK)
           │
           ▼
[ SQLite DB & FAISS Index ]
```

---

## Quick Start (Local Development)

### 1. Environment Setup

Copy `.env.example` to `backend/.env`:

```bash
cp .env.example backend/.env
```

Configure `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
CHAT_RAG_ADMIN_TOKEN=your_admin_token_here
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173
GEMINI_MODEL=gemini-2.5-flash
MAX_UPLOAD_SIZE_MB=25
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend API: `http://localhost:8000/api`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend UI: `http://localhost:5173`

---

## Docker Setup & Deployment

Run using Docker Compose:

```bash
docker compose build --no-cache
docker compose up -d
```

- **Frontend UI**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000/api`
- **Backend Health Check**: `http://localhost:8000/api/health`


## Cloud Production Deployment

AutoFlow-RAG includes a `render.yaml` Blueprint for 1-click cloud deployment on platforms like Render or Fly.io:

### 1. Environment Variable Requirements
Set the following environment variables on your cloud backend service:
- `GEMINI_API_KEY`: Your Google Gemini API Key.
- `JWT_SECRET_KEY`: High-entropy random secret key for signing JWT tokens.
- `CHAT_RAG_ADMIN_TOKEN`: Secret token required for administrative endpoints.
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed frontend origins (e.g., `https://autoflow-rag-frontend.onrender.com`).
- `GEMINI_MODEL`: Model name, defaults to `gemini-2.5-flash`.
- `MAX_UPLOAD_SIZE_MB`: Max file upload size in MB, defaults to `25`.

### 2. Deployment via Render
1. Connect your GitHub repository (`Varunpv2005/AutoFlow-RAG`) to Render.
2. Select **New > Blueprint**.
3. Render automatically detects `render.yaml` and configures `autoflow-rag-backend` and `autoflow-rag-frontend`.
4. Enter your `GEMINI_API_KEY` when prompted in the Render Dashboard.
5. Deploy both services. Update `CORS_ALLOWED_ORIGINS` on the backend service with your frontend's live public URL once generated.

---

## Running Tests

Run the backend test suite:

```bash
cd backend
pytest
```

---

## License

[MIT](LICENSE)
