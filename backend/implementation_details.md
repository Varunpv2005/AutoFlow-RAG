# Implementation Details

_Last updated: 2026-07-28_

## LLM Integration Migration (Google Gemini 2.5 Flash)

### ✅ Migration Complete & System Verified
- The backend now uses the official Google GenAI Python SDK (`google-genai`) to integrate with **Google Gemini 2.5 Flash** (`gemini-2.5-flash`).
- All Ollama dependencies (`ollama`, `langchain-ollama`, `ChatOllama`, `OllamaLLM`) have been completely removed.
- Single-point configuration management implemented in `backend/app/config.py`.
- Dedicated reusable service module created at `backend/app/services/gemini_service.py`.
- Embeddings migrated to `sentence-transformers/all-MiniLM-L6-v2`.
- Vector store migrated to FAISS.
- API endpoints (`/api/health`, `/api/chat`, `/api/upload`, `/api/files`) maintain 100% contract and frontend compatibility.

---

## Structured Markdown Output for LLM (Chat Endpoint)
- Added a `system_prompt` in `app/services/chat_service.py` instructing the LLM to always answer in well-structured markdown.

---

## Service Architecture
- `config.py`: Uses `pydantic-settings` to load `.env` variables cleanly (`GEMINI_API_KEY`, `GEMINI_MODEL`, `FAISS_PATH`, `UPLOAD_DIR`).
- `gemini_service.py`: Implements `GeminiService` (sync & async generation, health check) for Google GenAI LLM.
- `rag/pipeline.py`: Configured to use `HuggingFaceEmbeddings` and FAISS for vector operations.

---

## API Routing Consistency
- All backend API endpoints use the `/api/` prefix for seamless integration with the frontend Vite proxy.
