import re
from sqlalchemy.orm import Session
from app.db.models import File as DBFile, ChatHistory
from app.log_utils import build_log_entry, emit_observability_event, safe_log_gotcha
from datetime import datetime
import time
from typing import Optional, List, Dict, Any
from app.services.gemini_service import gemini_service
from app.analytics import analytics


def iter_response_tokens(text: str) -> List[str]:
    """Split an AI answer into small token-like chunks for streaming responses.

    Preserve whitespace tokens so the frontend can concatenate streamed chunks
    without losing spaces or markdown formatting.
    """
    if not text:
        return []
    return re.findall(r"\s+|[^\s]+", text)


def build_source_citations(docs: List[Any]) -> List[Dict[str, Any]]:
    """Create enterprise-grade citations directly from retrieved chunk metadata."""
    citations: List[Dict[str, Any]] = []
    for doc in docs:
        meta = doc.metadata or {}
        document_name = (
            meta.get("filename")
            or meta.get("source_file")
            or meta.get("source")
            or meta.get("file_name")
            or "Unknown File"
        )
        page_number = meta.get("page") or meta.get("page_number")
        chunk_id = meta.get("chunk_index") or meta.get("chunk_id")
        similarity_score = meta.get("score") or meta.get("similarity_score")
        content_preview = (doc.page_content or "")[:280].strip()
        if similarity_score is None:
            similarity_score = 0.0
        citations.append({
            "document_name": document_name,
            "page_number": page_number,
            "chunk_id": chunk_id,
            "similarity_score": similarity_score,
            "confidence": "high" if similarity_score >= 0.7 else "medium" if similarity_score >= 0.5 else "low",
            "content_preview": content_preview,
            "metadata": meta,
        })
    return citations


def chat_service(
    question: str,
    file_id: Optional[int],
    db: Session,
    rag_pipeline,
    llm=None,
    keywords: Optional[list] = None,
    metadata_filter: Optional[dict] = None,
    k: Optional[int] = 4,
    user_id: Optional[int] = None,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Handles chat logic: retrieves relevant docs (hybrid/vector/keyword/MMR), constructs prompt, calls LLM (Gemini), logs history.
    """
    llm_to_use = llm or gemini_service

    # Multi-user isolation: only retrieve files belonging to current user
    if user_id is not None:
        db_files = db.query(DBFile).filter(DBFile.user_id == user_id).all()
    else:
        db_files = db.query(DBFile).all()

    if not db_files:
        safe_log_gotcha(f"[Chat] No files in DB for user={user_id} at {datetime.now().isoformat()}")
        return {"answer": "No files are available for answering. Please upload a file first.", "sources": []}
    # Metadata filter by file_id if provided
    if file_id:
        if metadata_filter is None:
            metadata_filter = {}
        metadata_filter["file_id"] = file_id

    retrieval_started_at = time.time()
    docs = rag_pipeline.retrieve(
        question,
        k=k,
        keywords=keywords,
        metadata_filter=metadata_filter
    )
    retrieval_latency = round(time.time() - retrieval_started_at, 3)

    # Filter docs so only those whose file_id is present in the current user's DB files are used.
    # Precompute the allowed file IDs once to avoid repeated set lookups during filtering.
    current_file_ids = {str(f.id) for f in db_files}
    docs = [d for d in docs if str((d.metadata or {}).get("file_id")) in current_file_ids]

    # HALLUCINATION PREVENTION: Don't query LLM if no relevant chunks are found
    if not docs:
        return {
            "answer": "I cannot find any relevant context in the uploaded documents to answer your question.",
            "sources": []
        }

    # Construct context
    context = "\n\n".join([d.page_content for d in docs])
    history_context = ""
    if conversation_history:
        recent_history = conversation_history[-8:]
        formatted_history = []
        for entry in recent_history:
            role = entry.get("role", "user")
            content = entry.get("content", "")
            if role == "assistant":
                formatted_history.append(f"Assistant: {content}")
            else:
                formatted_history.append(f"User: {content}")
        if formatted_history:
            history_context = "Conversation history:\n" + "\n".join(formatted_history) + "\n\n"

    system_prompt = (
        "You are an intelligent AI assistant with deep expertise in analysing documents. "
        "Answer questions like a knowledgeable colleague — conversational, insightful, and direct.\n\n"
        "Formatting requirements:\n"
        "- Use clean Markdown with short paragraphs, bullet points, and headings when they improve clarity.\n"
        "- Prefer simple structure: a short opening answer, followed by bullet points or a brief section if needed.\n"
        "- Use ## headings for major sections and - bullet points for supporting details.\n"
        "- Keep formatting concise and readable; do not overuse sections for short answers.\n"
        "- Bold the single most important term or finding in each section.\n"
        "- Use inline code formatting only for package names, commands, or technical terms. Do not wrap normal prose in code blocks.\n"
        "- Do not use fenced code blocks unless the user explicitly asks for code or configuration output.\n"
        "- Never use phrases like 'The provided context', 'This document provides', 'Based on the context', or 'According to the document'.\n"
        "- Write as if you already know the material — speak with authority, not qualification.\n"
        "- End with a one-sentence conclusion or recommendation only when it adds value.\n\n"
        "STRICT RULE: Answer exclusively from the information below. "
        "If the information needed is not present, reply with exactly: "
        "'I cannot find any relevant context in the uploaded documents to answer your question.' "
        "Never speculate, infer beyond the text, or use outside knowledge.\n"
    )
    prompt = f"{system_prompt}\n---\n{history_context}{context}\n---\n\nQuestion: {question}\n\nAnswer:"
    # Call Gemini LLM — let quota errors propagate raw so main.py can catch and return HTTP 200
    t0 = time.time()
    try:
        answer = llm_to_use.invoke(prompt)
    except Exception as e:
        safe_log_gotcha(f"[Chat] LLM inference failed: {str(e)} at {datetime.now().isoformat()}")
        raise
    response_time = round(time.time() - t0, 2)
    analytics.record_query(retrieval_latency=retrieval_latency, llm_response_time=response_time, retrieved_chunks=len(docs))
    safe_log_gotcha(
        "chat_completed",
        retrieval_latency_ms=retrieval_latency,
        llm_latency_ms=response_time,
        chunk_count=len(docs),
        user_id=user_id,
    )

    
    # Check if LLM refused to answer (hallucination guard)
    if "I cannot find any relevant context in the uploaded documents to answer your question" in answer:
        answer = "I cannot find any relevant context in the uploaded documents to answer your question."
        docs = []

    # Log chat history with user isolation
    chunk_count = len(docs)
    chat = ChatHistory(
        user_id=user_id,
        file_id=file_id,
        question=question,
        answer=answer,
        timestamp=datetime.utcnow(),
        response_time=response_time,
        chunk_count=chunk_count,
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    citations = build_source_citations(docs)
    confidence_score = max(
        (citation.get("similarity_score") for citation in citations if citation.get("similarity_score") is not None),
        default=None,
    )
    retrieved_chunks = [
        {
            "chunk_id": citation.get("chunk_id"),
            "document_name": citation.get("document_name"),
            "page_number": citation.get("page_number"),
            "similarity_score": citation.get("similarity_score"),
            "content_preview": citation.get("content_preview"),
        }
        for citation in citations
    ]
    return {
        "answer": answer,
        "sources": citations,
        "chat_id": chat.id,
        "response_time": response_time,
        "chunk_count": chunk_count,
        "retrieval_latency_ms": retrieval_latency,
        "confidence_score": confidence_score,
        "retrieved_chunks": retrieved_chunks,
    }

