from fastapi import UploadFile, HTTPException, File, Depends
from sqlalchemy.orm import Session
from app.db.models import File as DBFile
from app.rag.pipeline import SUPPORTED_EXTENSIONS
from app.log_utils import safe_log_gotcha
from app.analytics import analytics
from datetime import datetime
from typing import Optional
import os
import shutil
import uuid
from pathlib import Path

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/files"))
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_file_preview(file_path: str, limit: int = 4000):
    path = Path(file_path)
    ext = path.suffix.lower()
    if ext == ".txt":
        try:
            content = path.read_text(encoding="utf-8")
            return {"type": "text", "content": content[:limit]}
        except UnicodeDecodeError:
            return {"type": "text", "content": path.read_text(encoding="latin-1")[:limit]}
    if ext == ".pdf":
        return {"type": "pdf", "content": "", "path": str(path)}
    return {"type": "unsupported", "content": "Preview is not available for this file type."}


def upload_file(file: UploadFile = File(...), db: Session = Depends(), user_id: Optional[int] = None):
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    existing_files = db.query(DBFile).filter(DBFile.user_id == user_id, DBFile.filename == file.filename).all()
    if not isinstance(existing_files, list):
        existing_files = list(existing_files or [])

    next_version = 1
    if existing_files:
        version_candidates = [getattr(f, "version", None) for f in existing_files]
        version_candidates = [v for v in version_candidates if isinstance(v, int)]
        next_version = max(version_candidates, default=1) + 1

    for prior_file in existing_files:
        prior_file.is_latest = 0

    file_size_bytes = 0
    try:
        file.file.seek(0, os.SEEK_END)
        file_size_bytes = file.file.tell()
        file.file.seek(0)
    except Exception:
        file_size_bytes = 0

    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    db_file = None

    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        db_file = DBFile(
            filename=file.filename,
            filepath=save_path,
            upload_time=datetime.utcnow(),
            user_id=user_id,
            file_metadata="{}",
            file_size_bytes=file_size_bytes,
            file_type=ext,
            chunk_count=0,
            is_indexed=0,
            version=next_version,
            is_latest=1,
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
    except Exception:
        if db_file is not None:
            db.rollback()
        try:
            if os.path.exists(save_path):
                os.remove(save_path)
        except Exception:
            pass
        raise

    return db_file

def list_files(db: Session = Depends(), user_id: Optional[int] = None):
    if user_id is not None:
        return db.query(DBFile).filter(DBFile.user_id == user_id).all()
    return db.query(DBFile).all()

def delete_file(file_id: int, db: Session = Depends(), user_id: Optional[int] = None):
    query = db.query(DBFile).filter(DBFile.id == file_id)
    if user_id is not None:
        query = query.filter(DBFile.user_id == user_id)
    db_file = query.first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    errors = []
    try:
        os.remove(db_file.filepath)
    except FileNotFoundError:
        pass
    except Exception as e:
        errors.append(f"File delete error: {e}")
    db.delete(db_file)
    db.commit()
    if errors:
        for err in errors:
            safe_log_gotcha(f"[DeleteFile] {err}")
    else:
        safe_log_gotcha(f"[DeleteFile] File {file_id} deleted successfully at {datetime.now().isoformat()}")
    return {"status": "deleted", "warnings": errors}
