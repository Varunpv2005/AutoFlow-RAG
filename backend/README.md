# Backend for Google Gemini RAG Chat App

_Last updated: 2026-07-28_

## Purpose
This backend implements a Retrieval-Augmented Generation (RAG) chat application powered by **Google Gemini 2.5 Flash** and the official Google GenAI Python SDK (`google-genai`).

---

## Architecture Overview

- **API Framework:** FastAPI (Python)
- **RAG Pipeline:** LangChain & ChromaDB (file parsing, chunking, embedding, hybrid retrieval, LLM orchestration)
- **LLM:** Google Gemini 2.5 Flash (`gemini-2.5-flash`) via `google-genai` SDK
- **Embeddings:** Google Gemini Embeddings (`gemini-embedding-001`)
- **Vector Store:** ChromaDB (disk-based)
- **User/File Metadata:** SQLite (via SQLAlchemy)
- **File Storage:** Local filesystem
- **Configuration:** Centralized `app/config.py` using `pydantic-settings`

---

## Folder Structure
```
/backend
├── app/
│   ├── main.py            # FastAPI entrypoint
│   ├── config.py          # Centralized configuration & single-point LLM setting
│   ├── api/               # API route modules
│   ├── db/                # DB models and session
│   ├── rag/               # RAG pipeline (LangChain, Gemini Embeddings, ChromaDB)
│   ├── error_handlers.py  # Centralized error handling
│   ├── log_utils.py       # Logging for gotchas/ops
│   ├── schemas.py         # Pydantic models
│   ├── services/          # Business logic (gemini_service, file, chat, admin)
│   │   ├── gemini_service.py # Official Google GenAI SDK wrapper
│   │   ├── chat_service.py   # RAG chat logic
│   │   ├── file_service.py   # File storage & DB operations
│   │   └── admin_service.py  # System cleanup logic
│   ├── gotchas.md         # Backend-specific gotchas
│   ├── implementation_details.md # Backend implementation notes
│   └── quick_reference.md # Backend quick reference
├── data/                  # SQLite DB and ChromaDB storage
├── requirements.txt
└── README.md
```

---

## Key Features
- High-speed inference using Google Gemini 2.5 Flash.
- Embeddings powered by `gemini-embedding-001`.
- Clean separation of concerns with `gemini_service` and `config.py`.
- Health checks verifying SQLite DB, ChromaDB vector store, and Gemini API connectivity.
- SQLite is used for user and file metadata.
- ChromaDB stores vector embeddings on disk.

---

## Endpoints
- `POST /api/upload` — Upload a document (stores file, triggers embedding & vector storage)
- `POST /api/chat` — Ask a question (retrieves relevant chunks, queries Gemini, returns answer with sources)
- `GET /api/files` — List uploaded files
- `DELETE /api/files/{file_id}` — Delete a file
- `GET /api/health` — Check health status of DB, Vectorstore, and Gemini LLM API
- `POST /api/admin/clear_all` — Reset environment and vectorstore (requires admin token)
