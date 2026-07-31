from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ANALYTICS_FILE = DATA_DIR / "analytics.json"


@dataclass
class AnalyticsSnapshot:
    total_queries: int = 0
    average_retrieval_latency: float = 0.0
    average_llm_response_time: float = 0.0
    uploaded_documents: int = 0
    total_chunks: int = 0
    total_retrieved_chunks: int = 0
    embedding_generation_time: float = 0.0
    total_retrieval_latency: float = 0.0
    total_llm_response_time: float = 0.0
    total_embedding_time: float = 0.0
    _retrieval_latencies: List[float] = field(default_factory=list)
    _llm_response_times: List[float] = field(default_factory=list)
    _embedding_times: List[float] = field(default_factory=list)

    def __post_init__(self):
        self._load()

    def _ensure_data_dir(self) -> None:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    def _load(self) -> None:
        if not ANALYTICS_FILE.exists():
            return
        try:
            with ANALYTICS_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            self.total_queries = int(data.get("total_queries", 0))
            self.total_retrieval_latency = float(data.get("total_retrieval_latency", 0.0))
            self.total_llm_response_time = float(data.get("total_llm_response_time", 0.0))
            self.total_embedding_time = float(data.get("total_embedding_time", 0.0))
            self.total_retrieved_chunks = int(data.get("total_retrieved_chunks", 0))
            self.uploaded_documents = int(data.get("uploaded_documents", 0))
            self.total_chunks = int(data.get("total_chunks", 0))
            self.average_retrieval_latency = float(data.get("average_retrieval_latency", 0.0))
            self.average_llm_response_time = float(data.get("average_llm_response_time", 0.0))
            self.embedding_generation_time = float(data.get("embedding_generation_time", 0.0))
        except Exception:
            pass

    def _save(self) -> None:
        self._ensure_data_dir()
        payload = {
            "total_queries": self.total_queries,
            "total_retrieval_latency": self.total_retrieval_latency,
            "total_llm_response_time": self.total_llm_response_time,
            "total_embedding_time": self.total_embedding_time,
            "average_retrieval_latency": round(self.average_retrieval_latency, 3),
            "average_llm_response_time": round(self.average_llm_response_time, 3),
            "total_retrieved_chunks": self.total_retrieved_chunks,
            "uploaded_documents": self.uploaded_documents,
            "total_chunks": self.total_chunks,
            "embedding_generation_time": round(self.embedding_generation_time, 3),
        }
        temp_file = ANALYTICS_FILE.with_suffix(".tmp")
        try:
            with temp_file.open("w", encoding="utf-8") as handle:
                json.dump(payload, handle)
            temp_file.replace(ANALYTICS_FILE)
        except Exception:
            pass

    def record_query(self, retrieval_latency: float, llm_response_time: float, retrieved_chunks: int = 0) -> None:
        self.total_queries += 1
        self.total_retrieved_chunks += retrieved_chunks
        self.total_retrieval_latency += retrieval_latency
        self.total_llm_response_time += llm_response_time
        self._retrieval_latencies.append(retrieval_latency)
        self._llm_response_times.append(llm_response_time)
        self.average_retrieval_latency = self.total_retrieval_latency / self.total_queries
        self.average_llm_response_time = self.total_llm_response_time / self.total_queries
        self._save()

    def record_upload(self, chunks_count: int, embedding_time: float) -> None:
        self.uploaded_documents += 1
        self.total_chunks += chunks_count
        self.total_embedding_time += embedding_time
        self._embedding_times.append(embedding_time)
        self.embedding_generation_time = self.total_embedding_time / self.uploaded_documents
        self._save()

    def to_dict(self) -> Dict[str, float | int]:
        return {
            "total_queries": self.total_queries,
            "average_retrieval_latency": round(self.average_retrieval_latency, 3),
            "average_llm_response_time": round(self.average_llm_response_time, 3),
            "total_retrieved_chunks": self.total_retrieved_chunks,
            "uploaded_documents": self.uploaded_documents,
            "total_chunks": self.total_chunks,
            "embedding_generation_time": round(self.embedding_generation_time, 3),
        }


analytics = AnalyticsSnapshot()
