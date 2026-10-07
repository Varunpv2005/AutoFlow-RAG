AutoFlow-RAG 🚀

Autonomous AI Task Execution & Document Intelligence Engine

AutoFlow-RAG is a production-oriented Retrieval-Augmented Generation (RAG) platform that enables users to upload documents and interact with them through grounded, context-aware AI conversations.

The system combines local semantic embeddings, FAISS vector search, FastAPI, JWT authentication, persistent chat history, and Google Gemini 2.5 Flash to provide accurate document-based question answering while maintaining strict user-level data isolation.

Unlike a basic chatbot that sends documents directly to an LLM, AutoFlow-RAG implements a complete retrieval pipeline:

Upload → Parse → Chunk → Embed → Index → Retrieve → Score → Generate → Stream

The architecture is designed to reduce hallucinations, provide retrieval transparency, isolate user data, and support containerized deployment.

🎯 Problem Statement

Traditional document-search systems often rely on keyword matching and struggle with:

Understanding the semantic meaning of questions

Finding relevant information across large documents

Maintaining conversational context

Providing grounded AI-generated answers

Preventing one user's documents from appearing in another user's results

Explaining why a particular piece of information was retrieved

Handling multiple document formats consistently

AutoFlow-RAG addresses these problems by combining semantic vector retrieval with LLM-based generation.

💡 Solution

AutoFlow-RAG follows a Retrieval-Augmented Generation architecture.

Instead of allowing the LLM to answer purely from its pretrained knowledge, the application first retrieves relevant document chunks and then provides those chunks as context to the Gemini model.

High-Level Flow

                    ┌──────────────────────┐
                    │      User            │
                    │ Upload / Ask Query   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ React + TypeScript   │
                    │ Frontend             │
                    └──────────┬───────────┘
                               │
                     HTTP / SSE + JWT
                               │
                               ▼
                    ┌──────────────────────┐
                    │ FastAPI Backend      │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │ Authentication│   │ Document    │   │ Chat /      │
      │ & Security    │   │ Processing  │   │ Analytics   │
      └─────────────┘   └──────┬──────┘   └─────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Chunking        │
                       │ + Metadata      │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Sentence        │
                       │ Transformer     │
                       │ Embeddings      │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ FAISS Vector    │
                       │ Index           │
                       └────────┬────────┘
                                │
                         Top-K Retrieval
                                │
                                ▼
                       ┌─────────────────┐
                       │ User Scope      │
                       │ Filtering       │
                       └────────┬────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Gemini 2.5      │
                       │ Flash           │
                       └────────┬────────┘
                                │
                         Grounded Answer
                                │
                                ▼
                       ┌─────────────────┐
                       │ SSE Streaming   │
                       └────────┬────────┘
                                │
                                ▼
                            User UI

✨ Key Features

1. Multi-Format Document Ingestion

Users can upload:

PDF

DOCX

TXT

CSV

XLSX

The backend extracts text and metadata from each supported format before sending the content through the chunking pipeline.

Processing Pipeline

Document
   ↓
File Validation
   ↓
Format Detection
   ↓
Text / Data Extraction
   ↓
Metadata Extraction
   ↓
Adaptive Chunking
   ↓
Embedding Generation
   ↓
FAISS Indexing

The system also validates uploaded file sizes using:

MAX_UPLOAD_SIZE_MB

to prevent uncontrolled resource consumption.

🧠 2. Adaptive Document Chunking

Large documents cannot be directly passed to the embedding model or LLM as a single block.

AutoFlow-RAG therefore divides documents into smaller semantic units.

The chunking process considers document structure such as:

Headers

Paragraphs

Character boundaries

Document structure

Metadata

Each generated chunk maintains metadata such as:

user_id
document_id
filename
page_number
chunk_id
source information

This metadata later enables source attribution and user-scoped retrieval.

🔎 3. Local Semantic Embeddings

AutoFlow-RAG uses:

sentence-transformers/all-MiniLM-L6-v2

for embedding generation.

Instead of sending document content to an external embedding API, embeddings are generated locally.

Why local embeddings?

Advantages include:

Lower external API dependency

Reduced embedding API cost

Better privacy for document processing

Predictable embedding generation

Suitable performance for a lightweight RAG system

The resulting vectors are stored in FAISS for similarity search.

⚡ 4. FAISS Vector Search

The application uses FAISS (Facebook AI Similarity Search) as its vector database/index.

When a user asks a question:

User Query
    ↓
Query Embedding
    ↓
FAISS Similarity Search
    ↓
Top-K Candidate Chunks
    ↓
User-Level Filtering
    ↓
Relevant Context

The FAISS index is persisted to disk so that the application does not need to rebuild the complete vector index every time the backend restarts.

📊 5. Transparent Retrieval Scores

AutoFlow-RAG does not treat retrieval as a black box.

FAISS distance values are converted into an interpretable similarity score:

similarity = 1 / (1 + distance)

These scores can be surfaced alongside retrieved chunks.

This provides visibility into:

Which document chunks were retrieved

How strongly they matched the query

Which document/page produced the context

What evidence was supplied to the LLM

This is particularly useful for debugging and evaluating RAG quality.

🔐 6. User-Scoped Data Isolation

One of the important architectural decisions in AutoFlow-RAG is user-level retrieval isolation.

A shared vector index can create a security problem if retrieved chunks are not associated with their owner.

To address this, each indexed chunk contains user metadata:

user_id

During retrieval:

Authenticated User
        ↓
Generate Query Embedding
        ↓
FAISS Search
        ↓
Retrieve Candidate Chunks
        ↓
Filter by user_id
        ↓
Return Authorized Context

This prevents a user's query from accidentally retrieving another user's documents.

Security Principle

User A → User A Documents
User B → User B Documents

The retrieval layer therefore enforces the same logical ownership boundary as the application layer.

🤖 7. Grounded Gemini Generation

Retrieved document chunks are passed to:

Google Gemini 2.5 Flash

using the Google GenAI SDK.

The generation prompt is designed to constrain the model to the retrieved context.

Conceptually:

User Question
      +
Retrieved Document Context
      ↓
Grounded Prompt
      ↓
Gemini 2.5 Flash
      ↓
Answer

If the required information is not available in the retrieved context, the system is designed to avoid fabricating an answer.

This makes the application more suitable for document-based question answering than a generic conversational chatbot.

💬 8. Persistent Chat Memory

AutoFlow-RAG maintains chat history so users can continue conversations instead of treating every question as an isolated request.

Example:

User:
What is the refund policy?

AI:
The document states that...

User:
What about international customers?

AI:
For international customers...

The conversation context can therefore be used to support follow-up questions.

Chat history is associated with the authenticated user.

⚡ 9. Server-Sent Events (SSE)

The backend exposes:

/api/chat/stream

for incremental response delivery.

Instead of waiting for the entire LLM response, the frontend can receive the generated response progressively.

Streaming Flow

React
  │
  │ HTTP Request
  ▼
FastAPI
  │
  │ Retrieve Context
  ▼
Gemini
  │
  │ Generated Tokens
  ▼
SSE Stream
  │
  ▼
React UI

The stream also supports completion and error event metadata.

This improves the perceived responsiveness of the application.

🔑 10. Authentication & Security

AutoFlow-RAG implements JWT-based authentication.

Authentication Flow

Register / Login
       ↓
Password Verification
       ↓
JWT Token Generated
       ↓
Frontend Stores Authentication State
       ↓
Bearer Token Sent With Requests
       ↓
FastAPI Validates JWT
       ↓
Authenticated User Identified

Security mechanisms include:

JWT authentication

Password hashing using bcrypt

Authorization headers

User-scoped data access

Configurable CORS

Upload size validation

Protected administrative endpoints

Environment-based secret configuration

Sensitive configuration is kept outside the source code.

📈 11. Analytics & Observability

AutoFlow-RAG also tracks operational information such as:

User document allocation

Chat activity

Request latency

Workspace information

Infrastructure health

Retrieval information

This makes the application easier to monitor and debug than a basic RAG prototype.

🏗️ System Architecture

┌───────────────────────────────────────────────────────────┐
│                     React Frontend                        │
│                                                           │
│ React + TypeScript + Vite + Chakra UI + Zustand          │
└──────────────────────────┬────────────────────────────────┘
                           │
                    HTTP / SSE + JWT
                           │
                           ▼
┌───────────────────────────────────────────────────────────┐
│                    FastAPI Backend                        │
│                                                           │
│ ┌──────────────┐   ┌──────────────────┐                  │
│ │ Auth/Security│   │ Document Service │                  │
│ └──────────────┘   └────────┬─────────┘                  │
│                             │                             │
│                     ┌───────▼────────┐                    │
│                     │ Chunking Engine │                    │
│                     └───────┬────────┘                    │
│                             │                             │
│                     ┌───────▼────────┐                    │
│                     │ Embedding Model│                    │
│                     │ MiniLM-L6-v2   │                    │
│                     └───────┬────────┘                    │
│                             │                             │
│                     ┌───────▼────────┐                    │
│                     │ FAISS Index    │                    │
│                     └───────┬────────┘                    │
│                             │                             │
│                     ┌───────▼────────┐                    │
│                     │ Retrieval +    │                    │
│                     │ User Filtering │                    │
│                     └───────┬────────┘                    │
│                             │                             │
│                     ┌───────▼────────┐                    │
│                     │ Gemini Service │                    │
│                     └────────────────┘                    │
└───────────────┬──────────────────────────┬────────────────┘
                │                          │
                ▼                          ▼
       ┌────────────────┐        ┌──────────────────┐
       │ SQLite         │        │ FAISS Persistent │
       │ Metadata/Chat  │        │ Vector Index     │
       └────────────────┘        └──────────────────┘

🔄 Complete RAG Workflow

Step 1 — Document Upload

The user uploads a supported document.

PDF / DOCX / TXT / CSV / XLSX

The backend validates the file type and size.

Step 2 — Document Parsing

The corresponding parser extracts usable text/data from the document.

Metadata such as filename and page information is retained where available.

Step 3 — Chunking

The extracted content is divided into smaller chunks.

Each chunk receives metadata identifying its source and owner.

Step 4 — Embedding Generation

Each chunk is converted into a numerical vector using:

all-MiniLM-L6-v2

Step 5 — Vector Indexing

The generated vectors are inserted into the FAISS index.

The index is persisted for future searches.

Step 6 — User Query

The authenticated user submits a natural-language question.

Example:

"What are the main security requirements mentioned in the document?"

Step 7 — Query Embedding

The question is converted into the same embedding space as the document chunks.

Step 8 — Similarity Search

FAISS finds the most similar document vectors.

Query Vector
     ↓
FAISS
     ↓
Top-K Candidates

Step 9 — Authorization Filtering

Retrieved candidates are filtered according to the authenticated user's user_id.

Only authorized chunks continue to the generation stage.

Step 10 — Retrieval Scoring

The system calculates an interpretable similarity score:

1 / (1 + distance)

The application can expose this information to the user.

Step 11 — Grounded Prompt Construction

The selected chunks are inserted into the prompt sent to Gemini.

Conceptually:

SYSTEM INSTRUCTIONS
        +
RETRIEVED DOCUMENT CONTEXT
        +
CONVERSATION HISTORY
        +
USER QUESTION

Step 12 — Gemini Generation

Gemini 2.5 Flash generates an answer using the retrieved context.

Step 13 — Streaming Response

The answer is streamed back through SSE.

Gemini
  ↓
FastAPI SSE
  ↓
React
  ↓
Incremental UI Rendering

🧩 Technology Stack

Layer

Technology

Frontend

React

Language

TypeScript

Build Tool

Vite

UI

Chakra UI

State Management

Zustand

Backend

FastAPI

Backend Language

Python 3.11

API Server

Uvicorn

Validation

Pydantic

ORM

SQLAlchemy

Authentication

JWT

Password Hashing

bcrypt

Vector Search

FAISS

Embeddings

Sentence Transformers

Embedding Model

all-MiniLM-L6-v2

LLM

Gemini 2.5 Flash

LLM SDK

Google GenAI

Metadata Database

SQLite

Testing

Pytest

Containerization

Docker

Orchestration

Docker Compose

Reverse Proxy

Nginx

📁 Project Structure

AutoFlow-RAG/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── core/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   └── App.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── render.yaml
├── Dockerfile
└── README.md

🚀 Getting Started

Prerequisites

Make sure the following are installed:

Python 3.11+

Node.js

npm

Docker Desktop (optional)

Git

You also need a Google Gemini API key.

⚙️ Local Development

1. Clone the Repository

git clone https://github.com/Varunpv2005/AutoFlow-RAG.git

cd AutoFlow-RAG

2. Configure Environment Variables

Copy the example environment file:

cp .env.example backend/.env

Configure:

GEMINI_API_KEY=your_gemini_api_key_here

JWT_SECRET_KEY=your_high_entropy_secret_key

CHAT_RAG_ADMIN_TOKEN=your_admin_token_here

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173

GEMINI_MODEL=gemini-2.5-flash

MAX_UPLOAD_SIZE_MB=25

Never commit actual API keys or secrets to GitHub.

🐍 Backend Setup

cd backend

Create a virtual environment:

Windows

python -m venv venv

venv\Scripts\activate

Linux/macOS

python -m venv venv

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start FastAPI:

uvicorn app.main:app --reload --port 8000

Backend:

http://localhost:8000/api

Health check:

http://localhost:8000/api/health

⚛️ Frontend Setup

Open another terminal:

cd frontend

Install dependencies:

npm install

Start development server:

npm run dev

Frontend:

http://localhost:5173

🐳 Docker Deployment

The project supports Docker Compose for containerized execution.

Build:

docker compose build --no-cache

Run:

docker compose up -d

Services:

Frontend → http://localhost:3000

Backend  → http://localhost:8000/api

Health endpoint:

http://localhost:8000/api/health

☁️ Cloud Deployment

AutoFlow-RAG includes a render.yaml deployment configuration.

The architecture can be deployed as separate frontend and backend services.

Required Environment Variables

GEMINI_API_KEY
JWT_SECRET_KEY
CHAT_RAG_ADMIN_TOKEN
CORS_ALLOWED_ORIGINS
GEMINI_MODEL
MAX_UPLOAD_SIZE_MB

Deployment Flow

GitHub Repository
       ↓
Cloud Platform
       ↓
Backend Service
       +
Frontend Service
       ↓
Configure Environment Variables
       ↓
Configure CORS
       ↓
Deploy

The frontend's public URL must be included in the backend's allowed CORS origins.

🧪 Testing

Backend tests are written using Pytest.

Run:

cd backend

pytest

The test suite covers important backend functionality and helps validate application behavior during development.

🔒 Security Considerations

AutoFlow-RAG was designed with several application-level security controls.

Authentication

JWT tokens are used to authenticate API requests.

Password Protection

Passwords are hashed using bcrypt rather than stored as plaintext.

Authorization

Authenticated identity is used to scope document and retrieval operations.

Data Isolation

Vector chunks contain ownership metadata so retrieval can be restricted to the requesting user.

CORS

Allowed frontend origins are configurable through environment variables.

Upload Validation

Uploaded files are subject to configurable size limits.

Secret Management

API keys, JWT secrets, and administrative tokens are supplied through environment variables rather than hardcoded into the repository.

🧠 Why These Technologies?

Why FastAPI?

FastAPI provides:

High-performance asynchronous API handling

Automatic OpenAPI documentation

Pydantic validation

Easy integration with Python ML/AI libraries

Clean dependency injection

Native support for streaming responses

Why FAISS?

FAISS was selected because it provides:

Efficient vector similarity search

Local execution

Low infrastructure complexity

Persistence support

Good performance for a lightweight document intelligence system

For a larger production deployment, FAISS could later be replaced by a distributed vector database.

Why Sentence Transformers?

Local Sentence Transformer embeddings provide:

Semantic representations of text

No dependency on external embedding APIs

Lower operating cost

Better control over document-processing privacy

Why Gemini 2.5 Flash?

Gemini 2.5 Flash provides a strong balance between:

Response quality

Latency

Context handling

Cost

Streaming support

The model is used only after retrieval, keeping the generation stage grounded in application-provided context.

Why SQLite?

SQLite is lightweight and appropriate for local development and smaller deployments.

It stores application metadata such as:

Users

Documents

Conversations

Chat messages

Operational information

For larger deployments, PostgreSQL would be a natural production upgrade.

🧪 RAG Design Decisions

A major design goal was to avoid building a simple:

Document → LLM → Answer

application.

Instead, AutoFlow-RAG separates the system into independent stages:

Ingestion
   ↓
Chunking
   ↓
Embedding
   ↓
Indexing
   ↓
Retrieval
   ↓
Authorization
   ↓
Context Construction
   ↓
Generation
   ↓
Streaming

This separation makes the system easier to:

Debug

Test

Optimize

Monitor

Extend

Secure

📊 Retrieval Transparency

One of the project's important features is exposing information about retrieval rather than treating the vector search layer as a black box.

For a query, the system can associate the answer with:

Document
Page
Chunk
Retrieval Score

This makes it easier to investigate questions such as:

"Why did the system answer this way?"

The retrieval layer can therefore be evaluated independently from the LLM generation layer.

🛡️ Hallucination Control

RAG does not automatically eliminate hallucinations.

AutoFlow-RAG addresses hallucination risk using several layers:

Relevant Document Retrieval
          ↓
User-Level Filtering
          ↓
Retrieved Context
          ↓
Grounded Prompt
          ↓
Gemini Generation
          ↓
Out-of-Context Refusal

The model is instructed to avoid generating unsupported information when the required information is not present in the retrieved context.

This does not mathematically guarantee zero hallucinations, but it significantly constrains the generation process.

⚠️ Current Limitations

The current architecture is intentionally lightweight and has several areas that could be improved for large-scale production.

Vector Storage

FAISS is locally persisted and is not a distributed vector database.

Metadata Database

SQLite is suitable for development and smaller deployments but PostgreSQL would be preferable for high-concurrency production workloads.

Document Processing

Very large documents may require asynchronous/background processing.

Retrieval Quality

Semantic retrieval quality depends on:

Chunk size

Chunk overlap

Embedding model

Top-K configuration

Document structure

Evaluation

A future production version could include an automated RAG evaluation framework measuring:

Retrieval precision

Retrieval recall

Context relevance

Faithfulness

Answer correctness

Latency

🔮 Future Improvements

Potential next steps include:

PostgreSQL migration

Redis-based caching

Distributed vector database

Hybrid keyword + semantic retrieval

Reranking models

Background document processing with Celery/RQ

Document-level access-control policies

Automated RAG evaluation

Observability with OpenTelemetry

Prometheus/Grafana metrics

Multi-model support

Conversation summarization

Document versioning

Advanced citation generation

Kubernetes deployment

CI/CD pipeline

Automated security scanning

📌 Example Use Cases

AutoFlow-RAG can be adapted for:

📚 Education

Upload lecture notes, textbooks, and question papers and ask contextual questions.

🏢 Enterprise Knowledge Base

Query internal policies, manuals, and technical documentation.

⚖️ Document Analysis

Search large collections of policy or compliance documents.

💻 Technical Documentation

Ask questions about APIs, architecture documents, and engineering specifications.

📑 Business Documents

Analyze reports, spreadsheets, and structured business information.

🎯 Engineering Highlights

The project demonstrates practical implementation of:

Full-stack application architecture

REST API development

RAG architecture

Semantic search

Vector databases/indexing

Local embedding models

LLM integration

JWT authentication

User-level authorization

Secure file handling

Persistent chat systems

Server-Sent Events

Retrieval scoring

API validation

Automated testing

Docker containerization

Cloud deployment

Application observability

👨‍💻 What I Learned

Building AutoFlow-RAG involved working across multiple layers of an AI-powered production application:

Designing a complete RAG pipeline rather than directly calling an LLM.

Implementing semantic retrieval using local embeddings and FAISS.

Connecting retrieval results to grounded LLM generation.

Designing user-scoped vector retrieval.

Implementing JWT-based authentication and authorization.

Building streaming AI responses using SSE.

Managing document parsing across multiple file formats.

Containerizing frontend and backend services.

Writing backend tests with Pytest.

Designing the application for future migration from local infrastructure to scalable cloud services.

📜 License

This project is licensed under the MIT License.

🔗 Repository

GitHub:
https://github.com/Varunpv2005/AutoFlow-RAG

⭐ Project Summary

AutoFlow-RAG is a full-stack, deployment-oriented RAG platform that combines local semantic embeddings, FAISS retrieval, user-scoped authorization, Gemini 2.5 Flash generation, persistent conversation memory, retrieval transparency, and SSE streaming into a complete document intelligence workflow.
