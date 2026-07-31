# quick_reference.md

## API Endpoints

### File Management
- **POST /api/upload**
  - Upload a file (validates extension)
  - Response: `{ id: int, filename: str }`
- **GET /api/files**
  - List all files
  - Response: `[{ id, filename, upload_time, file_metadata }]`
- **DELETE /api/files/{file_id}**
  - Delete a file by ID
  - Response: `{ status, warnings }`

### Chat
- **POST /api/chat**
  - Query with a question (3-500 chars)
  - Query params: `question: str`, `file_id: int (optional)`
  - Response: `{ answer, sources }`

### Admin
- **POST /api/admin/clear_all**
  - Danger: Clears all files and chats (admin-token required, 8-128 chars, alnum/-/_)
  - Response: `{ status, files_deleted, chats_deleted }`

### Health
- **GET /api/health**
  - Checks DB, vectorstore, and LLM health
  - Response: `{ status, db: {ok, msg}, vectorstore: {ok, msg}, llm: {ok, msg} }`

---

## Validation Rules
- File upload: Extension must be in SUPPORTED_EXTENSIONS.
- Chat: Question must be 3-500 characters.
- Admin: Token must be 8-128 chars, alphanumeric, dash, or underscore.

---

## Error Handling
- Centralized FastAPI exception handlers for HTTPException, SQLAlchemyError, and generic Exception.
- All errors return JSON with `detail` and appropriate HTTP status.

---

## Operational Notes
- All business logic is modularized in `services/`.
- Health check endpoint is production-ready and covers all critical dependencies.
- All endpoints use Pydantic response models for validation and OpenAPI docs.

---

_Last updated: 2025-04-29 22:16:48+02:00_
