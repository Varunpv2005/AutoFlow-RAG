from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class FileUploadResponse(BaseModel):
    id: int
    filename: str
    upload_time: Optional[datetime] = None
    file_metadata: Optional[str] = None
    file_size_bytes: Optional[int] = None
    file_type: Optional[str] = None
    chunk_count: Optional[int] = None
    is_indexed: Optional[bool] = False
    processing_status: Optional[str] = "pending"

class FileListItem(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    file_metadata: str
    file_size_bytes: Optional[int] = None
    file_type: Optional[str] = None
    chunk_count: Optional[int] = None
    is_indexed: Optional[bool] = False
    processing_status: Optional[str] = "pending"

class FileListResponse(BaseModel):
    files: List[FileListItem]

class ChatRequest(BaseModel):
    """
    Chat request for hybrid RAG retrieval.
    - question: User query
    - file_id: (optional) restrict search to a file
    - keywords: (optional) boost/filter by keywords
    - metadata_filter: (optional) dict to restrict by metadata
    - use_mmr: (optional) use MMR re-ranking
    - k: (optional) number of chunks to retrieve
    - conversation_history: (optional) prior user/assistant turns for follow-up context
    """
    question: str = Field(..., min_length=1)
    file_id: Optional[int] = None
    keywords: Optional[List[str]] = None
    metadata_filter: Optional[dict] = None
    k: Optional[int] = 4
    conversation_history: Optional[List[Dict[str, Any]]] = None

class SourceInfo(BaseModel):
    filename: str
    page: Optional[int] = None
    chunk_index: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Any]
    chat_id: Optional[int] = None
    response_time: Optional[float] = None
    chunk_count: Optional[int] = None
    retrieval_latency_ms: Optional[float] = None
    confidence_score: Optional[float] = None
    retrieved_chunks: Optional[List[Dict[str, Any]]] = None

class AdminClearAllResponse(BaseModel):
    status: str
    files_deleted: int
    chats_deleted: int

class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
