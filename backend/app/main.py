import os
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query, Request, Header
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db, init_db
from app.db.models import File as DBFile, ChatHistory, User
from app.rag.pipeline import RAGPipeline, SUPPORTED_EXTENSIONS
from datetime import datetime
import time
import shutil
import uuid
from app.log_utils import build_log_entry, emit_observability_event, safe_log_gotcha
from app.schemas import (
    FileUploadResponse, FileListItem, ChatResponse, AdminClearAllResponse,
    ChatRequest, SignupRequest, LoginRequest, TokenResponse
)
from app.config import settings, parse_cors_origins
from app.services.gemini_service import gemini_service, GeminiServiceUnavailableError
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.request_context import clear_request_id, get_request_id, set_request_id
from app.rate_limiter import SimpleRateLimiter
from app.document_intelligence import enrich_file_metadata
from app.analytics import analytics

PUBLIC_ENDPOINTS = {
    "/api/health",
    "/api/auth/signup",
    "/api/auth/login",
    "/api/chat/stream",
    "/api/chat",
}

UPLOAD_DIR = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="AutoFlow-RAG Chat App (FAISS)")
allowed_origins = parse_cors_origins(settings.CORS_ALLOWED_ORIGINS)
auth_rate_limiter = SimpleRateLimiter(max_requests=10, window_seconds=60)
public_rate_limiter = SimpleRateLimiter(max_requests=30, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = set_request_id()
    request.state.request_id = request_id
    started_at = datetime.now()
    response = None
    try:
        if request.url.path in PUBLIC_ENDPOINTS:
            client_key = request.headers.get("x-forwarded-for") or request.client.host if request.client else "unknown"
            if not public_rate_limiter.allow_request(f"public:{request.url.path}:{client_key}"):
                response = JSONResponse(status_code=429, content={"detail": "Too many requests. Please try again later."})
                response.headers["X-Request-ID"] = request_id
                safe_log_gotcha("rate_limited_request", request_id=request_id, path=request.url.path, client_key=client_key, api_latency_ms=0.0)
                return response
        response = await call_next(request)
        api_latency_ms = round((datetime.now() - started_at).total_seconds() * 1000, 3)
        response.headers["X-Request-ID"] = request_id
        safe_log_gotcha("request_completed", request_id=request_id, path=request.url.path, api_latency_ms=api_latency_ms, status_code=response.status_code)
        return response
    except Exception as exc:
        api_latency_ms = round((datetime.now() - started_at).total_seconds() * 1000, 3)
        safe_log_gotcha("request_error", request_id=request_id, path=request.url.path, api_latency_ms=api_latency_ms, error=str(exc))
        raise
    finally:
        clear_request_id()

# Register centralized error handlers
from app.error_handlers import http_exception_handler, sqlalchemy_exception_handler, generic_exception_handler
from sqlalchemy.exc import SQLAlchemyError
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

FAISS_PATH = settings.FAISS_PATH
os.makedirs(FAISS_PATH, exist_ok=True)

# Initialize DB and RAG pipeline
init_db()

# SQLite migration: add new columns if they don't exist (safe no-op if already present)
with next(get_db()) as _mdb:
    for _col, _ddl in [
        ("feedback",      "ALTER TABLE chat_history ADD COLUMN feedback TEXT"),
        ("response_time", "ALTER TABLE chat_history ADD COLUMN response_time REAL"),
        ("chunk_count",   "ALTER TABLE chat_history ADD COLUMN chunk_count INTEGER"),
        ("processing_status", "ALTER TABLE files ADD COLUMN processing_status TEXT"),
    ]:
        try:
            _mdb.execute(text(_ddl))
            _mdb.commit()
        except Exception:
            pass  # Column already exists

rag_pipeline = RAGPipeline(vector_db_path=FAISS_PATH)

# Automatic re-indexing check on startup for existing files
with next(get_db()) as db_session:
    existing_file_count = db_session.query(DBFile).count()
    if existing_file_count > 0 and rag_pipeline.vectorstore is None:
        safe_log_gotcha(f"[Startup] Re-indexing {existing_file_count} existing files into FAISS index...")
        rag_pipeline.reindex_all_files(db_session)

# --- Auth endpoints ---

@app.post("/api/auth/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)) -> TokenResponse:
    normalized_username = req.username.strip().lower()
    identifier = normalized_username
    if not auth_rate_limiter.allow_request(f"signup:{identifier}"):
        raise HTTPException(status_code=429, detail="Too many signup attempts. Please try again later.")
    if db.query(User).filter(User.username == normalized_username).first():
        raise HTTPException(status_code=409, detail="Username already exists")
    user = User(username=normalized_username, password_hash=hash_password(req.password))
    db.add(user)
    db.commit()
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)


@app.post("/api/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    normalized_username = req.username.strip().lower()
    identifier = normalized_username
    if not auth_rate_limiter.allow_request(f"login:{identifier}"):
        raise HTTPException(status_code=429, detail="Too many login attempts. Please try again later.")
    user = db.query(User).filter(User.username == normalized_username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)


from app.services.admin_service import clear_all_service

@app.post("/api/admin/clear_all", response_model=AdminClearAllResponse)
def clear_all(admin_token: str = Header(..., alias="admin-token", min_length=8, max_length=128), db: Session = Depends(get_db)) -> AdminClearAllResponse:
    """
    Danger: Delete ALL files and chat history from DB and FAISS vectorstore. Delegates business logic to admin_service.
    Validates admin token length (8-128 chars).
    """
    ADMIN_TOKEN = settings.CHAT_RAG_ADMIN_TOKEN
    if not (admin_token.isalnum() or '-' in admin_token or '_' in admin_token):
        raise HTTPException(status_code=422, detail="Invalid admin token format.")
    return AdminClearAllResponse(**clear_all_service(
        admin_token=admin_token,
        db=db,
        rag_pipeline=rag_pipeline,
        admin_env_token=ADMIN_TOKEN
    ))


@app.get("/api/health")
def health_check():
    """
    Health check endpoint: verifies DB, FAISS vectorstore, and Gemini LLM connectivity.
    """
    # DB health
    try:
        db_ok = True
        db_msg = "OK"
        session_gen = get_db()
        session = next(session_gen)
        session.execute(text("SELECT 1"))
        session.close()
    except Exception as e:
        db_ok = False
        db_msg = str(e)

    # FAISS Vectorstore health
    try:
        vec_ok = True
        vec_msg = "OK"
        if rag_pipeline.vectorstore is not None:
            _ = rag_pipeline.vectorstore.index.ntotal
    except Exception as e:
        vec_ok = False
        vec_msg = str(e)

    # Gemini LLM health
    llm_ok, llm_msg, llm_model = gemini_service.health_check()

    status = "ok" if all([db_ok, vec_ok, llm_ok]) else "degraded"
    return {
        "status": status,
        "db": {"ok": db_ok, "msg": db_msg},
        "vectorstore": {"ok": vec_ok, "msg": vec_msg},
        "llm": {"ok": llm_ok, "msg": llm_msg, "model": llm_model}
    }

from app.services.file_service import upload_file as upload_file_service, get_file_preview

@app.post("/api/upload", response_model=FileUploadResponse)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileUploadResponse:
    """
    Upload a file and ingest into the RAG pipeline. Requires JWT auth.
    """
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=422, detail=f"Unsupported file type: {ext}")
    db_file = upload_file_service(file=file, db=db, user_id=current_user.id)
    db_file.processing_status = "processing"
    db.commit()
    # Ingest into RAG pipeline
    try:
        ingest_started_at = time.time()
        chunk_count = rag_pipeline.ingest(db_file.filepath, metadata={"file_id": db_file.id, "filename": db_file.filename})
        ingest_duration = round(time.time() - ingest_started_at, 3)
        db_file.chunk_count = chunk_count or 0
        db_file.is_indexed = 1
        db_file.processing_status = "indexed"
        db.commit()
        analytics.record_upload(chunks_count=db_file.chunk_count, embedding_time=ingest_duration)
        # AI Document Intelligence (Strictly 1 Gemini call, skips on failure/quota limit)
        try:
            docs = rag_pipeline.load_document(db_file.filepath)
            if docs:
                full_text = "\n".join([doc.page_content for doc in docs])[:15000]
                parsed_intel = enrich_file_metadata(full_text)
                db_file.file_metadata = json.dumps(parsed_intel)
                db.commit()
        except Exception as intel_err:
            safe_log_gotcha(f"[DocIntel] Skipped doc intelligence due to error/quota limits: {intel_err}")
            # Ensure metadata is valid JSON even on skip/failure
            try:
                db_file.file_metadata = "{}"
                db.commit()
            except Exception:
                pass
    except Exception as e:
        db_file.processing_status = "failed"
        db.commit()
        db.delete(db_file)
        db.commit()
        if os.path.exists(db_file.filepath):
            os.remove(db_file.filepath)
        raise HTTPException(status_code=500, detail=f"RAG ingestion failed: {str(e)}")
    return FileUploadResponse(
        id=db_file.id,
        filename=db_file.filename,
        upload_time=db_file.upload_time,
        file_metadata=db_file.file_metadata,
        file_size_bytes=db_file.file_size_bytes,
        file_type=db_file.file_type,
        chunk_count=db_file.chunk_count,
        is_indexed=bool(db_file.is_indexed),
        processing_status=db_file.processing_status,
    )



from app.services.file_service import list_files as list_files_service

@app.get("/api/files", response_model=list[FileListItem])
def list_files(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[FileListItem]:
    """
    List all files in the database belonging to the current user.
    """
    files = list_files_service(db=db, user_id=current_user.id)
    return [
        FileListItem(
            id=f.id,
            filename=f.filename,
            upload_time=f.upload_time,
            file_metadata=f.file_metadata or "{}",
            file_size_bytes=getattr(f, "file_size_bytes", None),
            file_type=getattr(f, "file_type", None),
            chunk_count=getattr(f, "chunk_count", None),
            is_indexed=bool(getattr(f, "is_indexed", 0)),
            processing_status=getattr(f, "processing_status", "pending")
        ) for f in files
    ]

from app.services.file_service import delete_file as delete_file_service

@app.get("/api/files/{file_id}/preview")
def preview_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    db_file = db.query(DBFile).filter(DBFile.id == file_id, DBFile.user_id == current_user.id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    return get_file_preview(db_file.filepath)

@app.delete("/api/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    """
    Delete a user's file: removes from DB and disk, re-indexes remaining files.
    """
    result = delete_file_service(file_id=file_id, db=db, user_id=current_user.id)
    errors = result.get("warnings", [])
    try:
        rag_pipeline.reindex_all_files(db)
    except Exception as e:
        errors.append(f"FAISS re-indexing error after deletion: {e}")
        safe_log_gotcha(f"[DeleteFile] FAISS re-indexing failure: {e}")
    return {"status": "deleted", "warnings": errors}


from app.services.chat_service import chat_service

@app.post("/api/chat", response_model=ChatResponse)
def chat(
    chat_req: ChatRequest = None,
    question: str = Query(None, min_length=3, max_length=500),
    file_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Chat endpoint: supports hybrid retrieval (keywords, metadata, k). Requires JWT auth.
    """
    if chat_req is not None:
        req = chat_req
    else:
        req = ChatRequest(question=question, file_id=file_id)
    try:
        return ChatResponse(**chat_service(
            question=req.question,
            file_id=req.file_id,
            db=db,
            rag_pipeline=rag_pipeline,
            llm=gemini_service,
            keywords=req.keywords,
            metadata_filter=req.metadata_filter,
            k=req.k,
            user_id=current_user.id,
            conversation_history=req.conversation_history,
        ))
    except GeminiServiceUnavailableError as chat_err:
        safe_log_gotcha(f"[Chat] Gemini service unavailable: {chat_err}")
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "error": "Gemini service is temporarily unavailable. Please try again in a few moments.",
            },
        )
    except Exception as chat_err:
        err_str = str(chat_err).lower()
        if "resource_exhausted" in err_str or "429" in err_str or "quota" in err_str:
            safe_log_gotcha(f"[Chat] Gemini quota exceeded: {chat_err}")
            return ChatResponse(
                answer=(
                    "⚠️ AI service is temporarily unavailable because the Gemini API daily quota has been reached. "
                    "Your documents remain indexed and searchable. Please try again later or use a new Gemini API key."
                ),
                sources=[]
            )
        safe_log_gotcha(f"[Chat] Unexpected error: {chat_err}")
        raise


@app.get("/api/chat/history")
def get_chat_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Load persistent chat history for the logged-in user.
    """
    history = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).order_by(ChatHistory.timestamp.asc()).all()
    messages = []
    for item in history:
        messages.append({"sender": "user", "text": item.question})
        messages.append({
            "sender": "ai",
            "text": item.answer,
            "sources": [],
            "chat_id": item.id,
            "response_time": item.response_time,
            "chunk_count": item.chunk_count,
            "feedback": item.feedback,
        })
    return messages


@app.post("/api/chat/feedback")
def submit_feedback(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Record thumbs-up / thumbs-down feedback for a chat response.
    payload: {"chat_id": int, "feedback": "up" | "down"}
    """
    chat_id = payload.get("chat_id")
    feedback = payload.get("feedback")
    if not chat_id or feedback not in ("up", "down"):
        raise HTTPException(status_code=422, detail="Invalid payload")
    chat = db.query(ChatHistory).filter(
        ChatHistory.id == chat_id,
        ChatHistory.user_id == current_user.id
    ).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat.feedback = feedback
    db.commit()
    return {"status": "ok"}


@app.get("/api/chat/stream")
async def chat_stream(
    question: str = Query(..., min_length=1, max_length=500),
    file_id: int = Query(None),
    conversation_history: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Server-Sent Events streaming chat endpoint.
    Streams answer tokens then sends a final 'done' event with sources/stats JSON.
    """
    from app.services.chat_service import chat_service as _chat_svc, iter_response_tokens
    import time

    async def event_generator():
        try:
            parsed_history = []
            if conversation_history:
                try:
                    parsed_history = json.loads(conversation_history)
                except Exception:
                    parsed_history = []
            # Run the full chat_service synchronously in executor to keep async loop free
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: _chat_svc(
                    question=question,
                    file_id=file_id,
                    db=db,
                    rag_pipeline=rag_pipeline,
                    llm=gemini_service,
                    user_id=current_user.id,
                    conversation_history=parsed_history,
                )
            )
            answer: str = result["answer"]
            for token in iter_response_tokens(answer):
                yield f"data: {json.dumps({'type': 'token', 'text': token})}\n\n"
                await asyncio.sleep(0.012)
            # Final event with metadata
            yield f"data: {json.dumps({'type': 'done', 'sources': result.get('sources', []), 'chat_id': result.get('chat_id'), 'response_time': result.get('response_time'), 'chunk_count': result.get('chunk_count'), 'retrieval_latency_ms': result.get('retrieval_latency_ms'), 'confidence_score': result.get('confidence_score'), 'retrieved_chunks': result.get('retrieved_chunks', [])})}\n\n"
        except Exception as e:
            err_str = str(e).lower()
            if "resource_exhausted" in err_str or "429" in err_str or "quota" in err_str:
                safe_log_gotcha(f"[Stream] Gemini quota: {e}")
                msg = (
                    "\u26a0\ufe0f AI service is temporarily unavailable because the Gemini API daily quota has been reached. "
                    "Your documents remain indexed and searchable. Please try again later."
                )
                yield f"data: {json.dumps({'type': 'token', 'text': msg})}\n\n"
            else:
                safe_log_gotcha(f"[Stream] Error: {e}")
                yield f"data: {json.dumps({'type': 'error', 'text': str(e)})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'sources': [], 'chat_id': None, 'response_time': None, 'chunk_count': 0, 'retrieval_latency_ms': None, 'confidence_score': None, 'retrieved_chunks': []})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.get("/api/activity")
def get_activity(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Recent activity: last 5 uploads and last 5 conversations for the current user.
    """
    recent_files = (
        db.query(DBFile)
        .filter(DBFile.user_id == current_user.id)
        .order_by(DBFile.upload_time.desc())
        .limit(5)
        .all()
    )
    recent_chats = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id)
        .order_by(ChatHistory.timestamp.desc())
        .limit(5)
        .all()
    )
    return {
        "uploads": [
            {"id": f.id, "filename": f.filename, "upload_time": f.upload_time.isoformat() if f.upload_time else None}
            for f in recent_files
        ],
        "conversations": [
            {"id": c.id, "question": c.question[:80], "timestamp": c.timestamp.isoformat() if c.timestamp else None, "feedback": c.feedback}
            for c in recent_chats
        ],
    }


@app.get("/api/analytics")
def get_analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Analytics dashboard statistics.
    """
    total_users = db.query(User).count()
    total_docs = db.query(DBFile).count()
    user_docs = db.query(DBFile).filter(DBFile.user_id == current_user.id).count()
    total_chats = db.query(ChatHistory).count()
    user_chats = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id).count()
    indexed_docs = db.query(DBFile).filter(DBFile.is_indexed == 1).count()
    pending_docs = total_docs - indexed_docs

    faiss_chunks = 0
    if rag_pipeline.vectorstore is not None:
        try:
            faiss_chunks = rag_pipeline.vectorstore.index.ntotal
        except Exception:
            pass

    llm_ok, llm_msg, llm_model = gemini_service.health_check()
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    faiss_ok = rag_pipeline.vectorstore is not None

    return {
        "users": total_users,
        "total_documents": total_docs,
        "user_documents": user_docs,
        "total_chats": total_chats,
        "user_chats": user_chats,
        "chunks": faiss_chunks,
        "indexed_documents": indexed_docs,
        "pending_documents": pending_docs,
        "total_queries": analytics.total_queries,
        "average_retrieval_latency": analytics.average_retrieval_latency,
        "average_llm_response_time": analytics.average_llm_response_time,
        "total_retrieved_chunks": analytics.total_retrieved_chunks,
        "embedding_generation_time": analytics.embedding_generation_time,
        "status": {
            "database": "OK" if db_ok else "ERROR",
            "gemini": "OK" if llm_ok else f"ERROR: {llm_msg}",
            "faiss": "OK" if faiss_ok else "NOT_INITIALIZED"
        }
    }

