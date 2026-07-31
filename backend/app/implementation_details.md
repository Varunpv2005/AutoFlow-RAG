# implementation_details.md

## Modularization and Service Layer
- All business logic for file, chat, and admin operations is now in dedicated service modules (`services/file_service.py`, `services/chat_service.py`, `services/admin_service.py`).
- Endpoints in `main.py` are thin, delegating to these service layers for maintainability, testability, and clarity.

## Centralized Error Handling
- Custom exception handlers for `HTTPException`, `SQLAlchemyError`, and generic `Exception` are registered in `main.py`.
- All errors return a JSON response with a `detail` key and the correct HTTP status.
- Logging for database and unhandled errors is performed for traceability.

## Health Check Endpoint
- `/api/health` checks:
  - **Database**: Uses a real SQLAlchemy session and `text("SELECT 1")` for compatibility with SQLAlchemy 2.x.
  - **Vectorstore**: Calls `.get()` on the vectorstore instance.
  - **LLM**: Calls a trivial prompt on the LLM to confirm inference is working.
- Returns a granular status for each subsystem and an overall status (`ok` or `degraded`).

## Validation
- **File Upload**: Validates file extension against `SUPPORTED_EXTENSIONS` before accepting uploads.
- **Chat**: Enforces question length (`min_length=3`, `max_length=500`) at the API level.
- **Admin Token**: Requires 8–128 characters, alphanumeric, dash, or underscore.

## Pydantic Models
- All major endpoints use Pydantic response models defined in `schemas.py` for type safety and OpenAPI documentation.

## Logging
- All operational events, errors, and gotchas are logged using `safe_log_gotcha` for compliance and debugging.

---

## RAG Pipeline Consolidation (2025-05-02)
- Removed `rag/pipeline_modular.py` and the `ModularRAGPipeline` class.
- Only `RAGPipeline` (in `rag/pipeline.py`) is used by the backend and referenced in `main.py`.
- Rationale: Avoid code duplication and ensure a single source of truth for retrieval logic.

_Last updated: 2025-05-02 22:38:49+02:00_
