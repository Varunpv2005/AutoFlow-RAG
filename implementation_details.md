# Implementation Details: AutoFlow RAG Pipeline (Sentence Transformers + Gemini 2.5 Flash)

_Last updated: 2026-07-28_

## Architecture & Integration
- **LLM**: Google Gemini 2.5 Flash (`gemini-2.5-flash`) via `google-genai` SDK for answer generation.
- **Embeddings**: Local `sentence-transformers/all-MiniLM-L6-v2` via LangChain's `HuggingFaceEmbeddings`.
- **Vector Store**: ChromaDB (local, disk-based at `backend/app/data/chroma_db`).
- **Quota Protection**: All document parsing, chunking, and vector embedding creation happen locally on CPU/GPU without making API calls to Gemini embedding endpoints.

## Config & Service Architecture
- `backend/app/config.py`: `EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"`, `GEMINI_MODEL = "gemini-2.5-flash"`.
- `backend/app/services/gemini_service.py`: Dedicated service wrapping `google-genai` for LLM completion and health check. All Gemini embedding code removed.
- `backend/app/rag/pipeline.py`: Uses `HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)` for vector operations.
