# Quick Reference: Backend API & Service Reference

_Last updated: 2026-07-28_

## API Endpoints
- `POST   /api/upload`    (file upload and ingestion)
- `GET    /api/files`     (list uploaded files)
- `DELETE /api/files/{file_id}` (delete file and vector embeddings)
- `POST /api/chat`
  - Request body (preferred):
    ```json
    {
      "question": "What are the main findings?",
      "file_id": 1,
      "keywords": ["finding", "summary"],
      "metadata_filter": {"section": "Results"},
      "k": 4
    }
    ```
  - Query params (legacy support): `question: str`, `file_id: int (optional)`
  - Response: `{ "answer": "...", "sources": ["file.pdf"] }`
  - Supports hybrid retrieval: vector + keyword + metadata filtering.
- `GET /api/health`    (verifies DB, Chroma vectorstore, and Gemini 2.5 Flash API connectivity)
- `POST /api/admin/clear_all` (resets all files, chat history, and vector store)

## Vectorstore Persistence
- Chroma persistence is automatic with `persist_directory`.

## LLM & Service Integration
- Powered by **Google Gemini 2.5 Flash** (`gemini-2.5-flash`) via the official Google GenAI Python SDK (`google-genai`).
- Embeddings generated via `gemini-embedding-001`.
- API Key loaded securely from `backend/.env` under `GEMINI_API_KEY`.
- Single-point provider configuration managed in `backend/app/config.py`.

## Required Dependencies
- `google-genai`
- `langchain-community`, `langchain-chroma`, `langchain-core`
- `pydantic-settings`, `python-dotenv`
- `unstructured`, `pdfplumber`, `pypdf`

## Frontend Dev
- Vite proxy forwards `/api` to backend on `localhost:8000`.
