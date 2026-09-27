import os
import shutil
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader, CSVLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings

import logging
import asyncio

from app.config import settings
from app.services.gemini_service import gemini_service

"""
Migrated RAG pipeline: FAISS vector database + Sentence Transformers (all-MiniLM-L6-v2) for local embeddings + Google Gemini 2.5 Flash for LLM answer generation.
"""

SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.csv', '.xlsx'}

class RAGPipeline:
    def __init__(self, vector_db_path: Optional[str] = None, chunking_strategy: str = "auto", embeddings=None, llm=None):
        """
        :param vector_db_path: Path for FAISS index persistence (defaults to settings.FAISS_PATH)
        :param chunking_strategy: 'auto', 'header', or 'character'.
        :param embeddings: Custom embeddings instance (defaults to HuggingFaceEmbeddings with all-MiniLM-L6-v2)
        :param llm: Custom LLM instance (defaults to gemini_service)
        """
        self.vector_db_path = vector_db_path or settings.FAISS_PATH
        self.embeddings = embeddings or HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        self.llm = llm or gemini_service
        self.chunking_strategy = chunking_strategy
        self.vectorstore: Optional[FAISS] = None

        # Load existing FAISS index from disk if present
        self._load_faiss_index()
        logging.info(f"Initialized RAGPipeline (FAISS at {self.vector_db_path}, embeddings={settings.EMBEDDING_MODEL}, chunking_strategy={chunking_strategy})")

    def _load_faiss_index(self):
        """
        Loads local FAISS index from disk if index file exists.
        """
        index_file = os.path.join(self.vector_db_path, "index.faiss")
        if os.path.exists(index_file):
            try:
                self.vectorstore = FAISS.load_local(
                    self.vector_db_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logging.info(f"Successfully loaded local FAISS index from {self.vector_db_path}")
            except Exception as e:
                logging.error(f"Failed to load FAISS index from {self.vector_db_path}: {e}")
                self.vectorstore = None
        else:
            self.vectorstore = None

    def save_faiss_index(self):
        """
        Saves current FAISS vector store to disk.
        """
        if self.vectorstore:
            os.makedirs(self.vector_db_path, exist_ok=True)
            self.vectorstore.save_local(self.vector_db_path)
            logging.info(f"Saved FAISS index to {self.vector_db_path}")

    def _get_text_splitter(self, docs, file_path: str):
        """
        Use MarkdownHeaderTextSplitter if markdown, else fallback to RecursiveCharacterTextSplitter.
        """
        ext = os.path.splitext(file_path)[-1].lower()
        if self.chunking_strategy == "header" or (self.chunking_strategy == "auto" and ext in ['.md', '.markdown']):
            try:
                return MarkdownHeaderTextSplitter(headers_to_split_on=["#", "##", "###"], chunk_size=1000, chunk_overlap=100)
            except Exception as e:
                logging.warning(f"Header splitter failed: {e}, falling back to character splitter.")
        # Fallback
        return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    def load_document(self, file_path: str) -> List[Document]:
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext == '.docx':
            loader = UnstructuredWordDocumentLoader(file_path)
        elif ext == '.txt':
            loader = TextLoader(file_path)
        elif ext == '.csv':
            loader = CSVLoader(file_path)
        elif ext == '.xlsx':
            loader = UnstructuredExcelLoader(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
        docs = loader.load()
        return docs

    def ingest(self, file_path: str, metadata: dict = None):
        """
        Ingests a file using adaptive chunking and stores vectors in FAISS.
        Automatically saves the FAISS index to disk.
        """
        docs = self.load_document(file_path)
        splitter = self._get_text_splitter(docs, file_path)
        splits = splitter.split_documents(docs)
        # Attach file-level metadata
        for doc in splits:
            doc.metadata = doc.metadata or {}
            if metadata:
                doc.metadata.update(metadata)
            doc.metadata['source_file'] = file_path

        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(splits, self.embeddings)
        else:
            self.vectorstore.add_documents(splits)

        self.save_faiss_index()
        logging.info(f"Ingested {len(splits)} chunks from {file_path} into FAISS using {splitter.__class__.__name__}")
        return len(splits)

    def retrieve(self, query: str, k: int = 4, keywords: Optional[list] = None, metadata_filter: Optional[dict] = None) -> List[Document]:
        """
        Semantic retrieval with keyword and metadata filtering.
        :param query: user query
        :param k: number of results
        :param keywords: list of keywords to boost/filter
        :param metadata_filter: dict of metadata filters (e.g. {"user_id": ..., "file_id": ...})
        """
        if self.vectorstore is None:
            logging.info("FAISS vectorstore is empty. Returning 0 results.")
            return []

        # Convert dictionary metadata_filter to a filter callable if dictionary is provided
        faiss_filter = None
        if metadata_filter:
            # Match metadata keys as string or int to handle serialized types
            def _filter_fn(doc_meta: dict) -> bool:
                if not doc_meta:
                    return False
                for key, val in metadata_filter.items():
                    if val is None:
                        continue
                    meta_val = doc_meta.get(key)
                    if meta_val != val and str(meta_val) != str(val):
                        return False
                return True

            faiss_filter = _filter_fn

        # Pass fetch_k to ensure FAISS retrieves an adequate candidate pool before post-filtering
        fetch_k = max(k * 10, 50)
        if faiss_filter:
            results_with_score = self.vectorstore.similarity_search_with_score(query, k=k, filter=faiss_filter, fetch_k=fetch_k)
        else:
            results_with_score = self.vectorstore.similarity_search_with_score(query, k=k)

        results: List[Document] = []
        for doc, dist in results_with_score:
            doc.metadata = doc.metadata or {}
            # Convert FAISS L2 distance to a 0.0 - 1.0 similarity score: 1 / (1 + distance)
            score = round(1.0 / (1.0 + float(dist)), 4)
            doc.metadata["score"] = score
            doc.metadata["similarity_score"] = score
            doc.metadata["faiss_distance"] = float(dist)
            results.append(doc)

        # Keyword filter/boost
        if keywords:
            keyword_results = [doc for doc in results if any(kw.lower() in doc.page_content.lower() for kw in keywords)]
            unique = {id(doc): doc for doc in keyword_results + results}
            results = list(unique.values())[:k]

        logging.info(f"Semantic retrieval for query '{query}': {len(results)} docs (FAISS top-k, keywords={keywords}, metadata={metadata_filter})")
        return results

    def reindex_all_files(self, db):
        """
        Re-indexes all active files in the database into a clean FAISS index.
        """
        from app.db.models import File as DBFile
        db_files = db.query(DBFile).all()

        # Wipe existing FAISS files
        if os.path.exists(self.vector_db_path):
            shutil.rmtree(self.vector_db_path, ignore_errors=True)
        self.vectorstore = None

        count = 0
        for db_file in db_files:
            if os.path.exists(db_file.filepath):
                self.ingest(
                    db_file.filepath,
                    metadata={
                        "file_id": db_file.id,
                        "filename": db_file.filename,
                        "user_id": db_file.user_id,
                    }
                )
                count += 1

        logging.info(f"Re-indexed {count} existing files into FAISS.")
