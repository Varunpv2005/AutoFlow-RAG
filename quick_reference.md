# Quick Reference: AutoFlow RAG System Architecture

_Last updated: 2026-07-28_

## Purpose
This document outlines the **requirements and architecture** for the AutoFlow RAG application powered by **Sentence Transformers (`all-MiniLM-L6-v2`)** and **Google Gemini 2.5 Flash**.

---

## Key Architecture & Components

### 1. LLM & Embeddings
- LLM: Google Gemini 2.5 Flash (`gemini-2.5-flash`) via the official Google GenAI SDK (`google-genai`).
- Embeddings: Local Sentence Transformers (`sentence-transformers/all-MiniLM-L6-v2`) via LangChain's `HuggingFaceEmbeddings`.
- API Key: Securely stored in `backend/.env` under `GEMINI_API_KEY` (used only for Gemini 2.5 Flash LLM completions).
- Single-point Configuration: Centralized in `backend/app/config.py`.

### 2. Vector Store & File Processing
- Local Vector Database: ChromaDB (stored on local disk at `backend/app/data/chroma_db`).
- RAG Pipeline orchestrates:
    - File parsing (PDF, DOCX, TXT, CSV, XLSX)
    - Adaptive chunking (`MarkdownHeaderTextSplitter` / `RecursiveCharacterTextSplitter`)
    - Embedding via local `HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")`
    - Vector storage in ChromaDB
    - Hybrid retrieval (vector, keyword, metadata filter)
    - Context construction & Gemini 2.5 Flash completion

### 3. Frontend
- Built with Vite + React + TypeScript + Zustand + Chakra UI.
- Communicates with FastAPI backend via REST API at `/api`.

---

## Stack Overview
| Layer        | Technology                   | Purpose                                |
|--------------|------------------------------|----------------------------------------|
| Frontend     | Vite + React + TS            | Modern UI                              |
| UI           | Chakra UI                    | UI Component Library                   |
| Backend      | FastAPI (Python)             | Async REST API                         |
| File Storage | Local filesystem             | Storage for uploaded files             |
| User DB      | SQLite (SQLAlchemy)          | Local DB for file and chat metadata    |
| Vector Store | ChromaDB                     | Disk-backed vector database            |
| Embeddings   | `all-MiniLM-L6-v2`           | Local Sentence Transformers            |
| LLM          | Gemini 2.5 Flash             | Google GenAI LLM (`gemini-2.5-flash`)  |
