# Gotchas & Integration Quirks

_Last updated: 2026-07-28_

## Google Gemini 2.5 Flash API Key Requirements
- Ensure `GEMINI_API_KEY` is set in `backend/.env`.
- Health check `/api/health` validates Gemini API connectivity and returns `status: ok` when valid.

## Chroma Vectorstore Persistence
- Persistence is automatic with `persist_directory` during `Chroma` instantiation.

## Hybrid Retrieval API
- `/api/chat` supports `keywords`, `metadata_filter`, `k`.
- Backwards compatible: legacy clients using `question`/`file_id` still work cleanly.
