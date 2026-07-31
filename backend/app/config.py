import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# Path to backend directory containing .env
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_FILE_PATH = os.path.join(BACKEND_DIR, ".env")


def parse_cors_origins(raw_value: Optional[str] = None) -> list[str]:
    """Parse a comma-separated list of allowed CORS origins from environment/config."""
    default_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    if raw_value is None:
        return default_origins

    value = raw_value.strip()
    if not value:
        return default_origins
    if value == "*":
        return ["*"]

    origins = [origin.strip() for origin in value.split(",") if origin.strip()]
    return origins or default_origins


class Settings(BaseSettings):
    """
    Centralized Configuration for AutoFlow-RAG.
    Allows easy switching of LLM providers, embedding models, and vector stores.
    """
    # Active LLM Provider configuration
    LLM_PROVIDER: str = "gemini"
    
    # Gemini API Configuration for LLM
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Embedding Configuration (Local Sentence Transformers)
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Database and Storage Configuration (FAISS Vector Store)
    FAISS_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "./data/faiss_index"))
    UPLOAD_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/files"))

    # Admin configuration
    CHAT_RAG_ADMIN_TOKEN: str = "supersecret"
    JWT_SECRET_KEY: str = "autoflow-rag-secret-key-change-in-production"

    # CORS configuration
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
