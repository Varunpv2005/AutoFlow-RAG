🚀 AutoFlow-RAG — Autonomous AI Task Execution Engine
AI-Powered Document Intelligence & Retrieval-Augmented Generation Platform
AutoFlow-RAG is a full-stack RAG-based document intelligence platform that allows users to upload documents and ask natural-language questions over their content.
The system automates the complete workflow:
Document Upload → Parsing → Chunking → Embeddings → FAISS Retrieval → Context Filtering → Gemini Generation → Streaming Response
It combines React, FastAPI, FAISS, Sentence Transformers, Google Gemini 2.5 Flash, JWT authentication, SQLite, and Docker into a complete end-to-end AI application.

✨ Key Features
- 📄 Multi-format document processing — PDF, DOCX, TXT, CSV, and XLSX
- 🧩 Adaptive document chunking with source metadata
- 🔎 Semantic search using Sentence Transformers
- ⚡ FAISS vector retrieval with persistent indexing
- 🔐 JWT authentication with bcrypt password hashing
- 👤 User-scoped retrieval to isolate documents between users
- 📊 Retrieval similarity scores for transparent search results
- 🤖 Grounded Gemini 2.5 Flash responses
- 💬 Persistent conversational history
- ⚡ Real-time response streaming using Server-Sent Events (SSE)
- 📈 Workspace analytics and operational telemetry
- 🐳 Docker & Docker Compose support
- ☁️ Cloud deployment configuration

🏗️ Architecture
                         ┌─────────────────────┐
                         │       User          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ React + TypeScript + Vite    │
                    │ Chakra UI + Zustand          │
                    └──────────────┬───────────────┘
                                   │
                           HTTP / SSE + JWT
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       FastAPI Backend        │
                    │                              │
                    │  Authentication & Security   │
                    │  Document Processing         │
                    │  Retrieval & Chat            │
                    │  Analytics                   │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
             ┌────────────┐ ┌────────────┐ ┌──────────────┐
             │  Document  │ │ Embeddings │ │   SQLite     │
             │  Chunking  │ │  MiniLM    │ │   Metadata   │
             └─────┬──────┘ └─────┬──────┘ └──────────────┘
                   │               │
                   └───────┬───────┘
                           ▼
                    ┌───────────────┐
                    │ FAISS Index   │
                    │ Vector Search │
                    └───────┬───────┘
                            │
                     Top-K Retrieval
                            │
                            ▼
                    ┌───────────────┐
                    │ User-Scoped   │
                    │ Filtering     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Gemini 2.5    │
                    │ Flash         │
                    └───────┬───────┘
                            │
                       SSE Streaming
                            │
                            ▼
                         Response

🔄 How It Works
1. Document Ingestion
Users upload supported documents:
PDF • DOCX • TXT • CSV • XLSX
The backend validates the file and extracts its content and metadata.
2. Chunking
Documents are divided into smaller chunks while preserving useful source information such as:
user_id
document_id
filename
page_number
chunk_id
3. Embedding Generation
Each chunk is converted into a semantic vector using:
sentence-transformers/all-MiniLM-L6-v2
The embeddings are generated locally.
4. Vector Indexing
The embeddings are stored in a persistent FAISS index for fast similarity search.
5. Query Processing
When a user asks a question:
Question
   ↓
Query Embedding
   ↓
FAISS Similarity Search
   ↓
Top-K Chunks
   ↓
User Authorization Filter
   ↓
Relevant Context
6. Grounded Generation
The retrieved context is passed to Gemini 2.5 Flash along with the user's question.
The generation prompt instructs the model to answer using the provided context and avoid unsupported information.
7. Streaming
The response is delivered progressively through:
/api/chat/stream
using Server-Sent Events (SSE).

🔐 Security & Data Isolation
Security is implemented at multiple layers.
Authentication
- JWT-based authentication
- Bearer token authorization
- bcrypt password hashing
User Isolation
Each vector chunk contains the corresponding user_id.
During retrieval:
Authenticated User
        ↓
FAISS Candidates
        ↓
user_id Filtering
        ↓
Authorized Chunks Only
This prevents documents belonging to one user from being used in another user's retrieval context.
Additional Controls
- Configurable CORS
- Upload size validation
- Protected administrative endpoints
- Environment-based secrets
- No hardcoded API credentials

📊 Retrieval Transparency
AutoFlow-RAG exposes retrieval information instead of treating vector search as a black box.
FAISS distance is converted into a similarity score:
similarity = 1 / (1 + distance)
Retrieved results can therefore provide information such as:
Document
Page
Chunk
Similarity Score
This helps understand why particular content was selected for generation.

🧠 RAG Pipeline
                 OFFLINE / INGESTION
                 ───────────────────

Document
   ↓
Parse
   ↓
Chunk
   ↓
Generate Embeddings
   ↓
Store in FAISS


                 ONLINE / QUERY
                 ──────────────

User Question
   ↓
Generate Query Embedding
   ↓
FAISS Similarity Search
   ↓
Retrieve Top-K Candidates
   ↓
Apply User Scope
   ↓
Build Context
   ↓
Gemini 2.5 Flash
   ↓
SSE Response

🛠️ Technology Stack
Layer	Technology
Frontend	React, TypeScript, Vite
UI	Chakra UI
State Management	Zustand
Backend	FastAPI, Python 3.11
API Server	Uvicorn
Validation	Pydantic
ORM	SQLAlchemy
Authentication	JWT + bcrypt
Vector Search	FAISS
Embeddings	Sentence Transformers
Embedding Model	all-MiniLM-L6-v2
LLM	Google Gemini 2.5 Flash
LLM SDK	Google GenAI
Database	SQLite
Testing	Pytest
Containerization	Docker
Orchestration	Docker Compose
Reverse Proxy	Nginx
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
└── README.md

🚀 Getting Started
Prerequisites
- Python 3.11+
- Node.js 18+
- npm
- Git
- Google Gemini API key

1. Clone Repository
git clone https://github.com/Varunpv2005/AutoFlow-RAG.git

cd AutoFlow-RAG

2. Configure Environment
Create the backend environment file:
cp .env.example backend/.env
Configure:
GEMINI_API_KEY=your_gemini_api_key
JWT_SECRET_KEY=your_secret_key
CHAT_RAG_ADMIN_TOKEN=your_admin_token

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

GEMINI_MODEL=gemini-2.5-flash
MAX_UPLOAD_SIZE_MB=25
Never commit real API keys or secrets to GitHub.

🐍 Backend
cd backend

python -m venv venv
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Run the API:
uvicorn app.main:app --reload --port 8000
Backend:
http://localhost:8000/api
Health check:
http://localhost:8000/api/health

⚛️ Frontend
Open another terminal:
cd frontend

npm install

npm run dev
Frontend:
http://localhost:5173

🐳 Docker
Build the application:
docker compose build --no-cache
Start services:
docker compose up -d
Services:
Frontend → http://localhost:3000
Backend  → http://localhost:8000/api

☁️ Deployment
The repository includes render.yaml for cloud deployment.
Required backend variables
GEMINI_API_KEY
JWT_SECRET_KEY
CHAT_RAG_ADMIN_TOKEN
CORS_ALLOWED_ORIGINS
GEMINI_MODEL
MAX_UPLOAD_SIZE_MB
After deployment, configure CORS_ALLOWED_ORIGINS with the actual frontend URL.

🧪 Testing
Run the backend test suite:
cd backend

pytest
The project uses Pytest for backend testing and validation of core application functionality.

📌 Engineering Decisions
Why FAISS?
FAISS provides efficient local vector similarity search without introducing the operational complexity of a separate vector database.
Why local embeddings?
all-MiniLM-L6-v2 allows document embeddings to be generated locally, reducing dependence on external embedding APIs.
Why FastAPI?
FastAPI provides strong request validation, automatic API documentation, asynchronous support, and natural integration with Python AI/ML libraries.
Why Gemini?
Gemini 2.5 Flash provides the generation layer for producing grounded responses from retrieved document context.
Why SSE?
SSE allows the backend to stream generated responses incrementally to the frontend instead of waiting for the complete response.

⚠️ Current Limitations
AutoFlow-RAG is designed as a deployment-oriented application, but several components can be further scaled.
- FAISS is currently locally persisted.
- SQLite is used for application metadata.
- Very large documents may require background processing.
- Retrieval quality depends on chunking and embedding configuration.
- Large-scale production deployment would benefit from PostgreSQL and a distributed vector database.

🔮 Future Improvements
- PostgreSQL for production metadata storage
- Distributed vector database
- Hybrid keyword + semantic retrieval
- Cross-encoder reranking
- Background document processing
- Automated RAG evaluation
- OpenTelemetry-based observability
- CI/CD pipeline
- Document versioning
- Advanced source citations
- Kubernetes deployment

🎯 What This Project Demonstrates
AutoFlow-RAG demonstrates practical experience with:
Full-Stack Development • RAG • Semantic Search • Vector Retrieval • LLM Integration • REST APIs • Authentication • Authorization • Streaming • Document Processing • Testing • Docker • Cloud Deployment

📜 License
MIT License

🔗 Repository
GitHub — AutoFlow-RAG
