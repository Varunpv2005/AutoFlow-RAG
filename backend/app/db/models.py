from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    files = relationship("File", back_populates="user")
    chats = relationship("ChatHistory", back_populates="user")

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_metadata = Column(Text)
    file_size_bytes = Column(Integer, nullable=True, default=0)
    file_type = Column(String, nullable=True)
    chunk_count = Column(Integer, nullable=True, default=0)
    is_indexed = Column(Integer, nullable=True, default=0)
    processing_status = Column(String, nullable=True, default="pending")
    version = Column(Integer, nullable=False, default=1)
    is_latest = Column(Integer, nullable=False, default=1)
    user = relationship("User", back_populates="files")
    chats = relationship("ChatHistory", back_populates="file")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    feedback = Column(String, nullable=True)   # 'up' | 'down' | None
    response_time = Column(Float, nullable=True)
    chunk_count = Column(Integer, nullable=True)
    user = relationship("User", back_populates="chats")
    file = relationship("File", back_populates="chats")
