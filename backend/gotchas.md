# Gotchas & Integration Quirks

_Last updated: 2026-07-28_

## Google Gemini 2.5 Flash API Key Requirements
- Ensure `GEMINI_API_KEY` is set in `backend/.env`.
- Health check `/api/health` validates Gemini API connectivity and returns `status: ok` when valid.

## FAISS Vectorstore Persistence
- Persistence is automatic with `save_local` and `load_local` during FAISS operations.

## Hybrid Retrieval API
- `/api/chat` supports `keywords`, `metadata_filter`, `k`.
- Backwards compatible: legacy clients using `question`/`file_id` still work cleanly.
