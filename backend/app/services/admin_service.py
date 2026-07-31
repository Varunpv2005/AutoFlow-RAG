import os
import shutil
from sqlalchemy.orm import Session
from app.db.models import File as DBFile, ChatHistory
from app.log_utils import safe_log_gotcha
from fastapi import HTTPException
from datetime import datetime
from typing import Any, Dict

def clear_all_service(admin_token: str, db: Session, rag_pipeline, admin_env_token: str) -> Dict[str, Any]:
    """
    Danger: Delete ALL files and chat history from DB and FAISS vectorstore. Requires admin-token.
    """
    if admin_token != admin_env_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Delete all chat history
    chat_count = db.query(ChatHistory).delete()
    # Delete all files
    file_count = db.query(DBFile).delete()
    db.commit()
    # Delete all FAISS embeddings from vectorstore
    try:
        if os.path.exists(rag_pipeline.vector_db_path):
            shutil.rmtree(rag_pipeline.vector_db_path, ignore_errors=True)
        rag_pipeline.vectorstore = None
        safe_log_gotcha(f"[AdminClearAll] All files, chats, and FAISS vectors deleted at {datetime.now().isoformat()}")
    except Exception as e:
        safe_log_gotcha(f"[AdminClearAll] Vectorstore clear failed: {e}")
        raise HTTPException(status_code=500, detail=f"Vectorstore clear failed: {e}")
    return {"status": "cleared", "files_deleted": file_count, "chats_deleted": chat_count}
