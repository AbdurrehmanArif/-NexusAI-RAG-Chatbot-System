# ⚡ NexusAI — RAG Chatbot System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

**An intelligent AI chatbot that answers questions from any website using RAG**

</div>

---

## 📋 Table of Contents

- [What is NexusAI?](#-what-is-nexusai)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Setup & Installation](#-setup--installation)
- [Running the Project](#-running-the-project)
- [Usage Guide](#-usage-guide)
- [RAG Pipeline Explained](#-rag-pipeline-explained)
- [Common Errors & Fixes](#-common-errors--fixes)

---

## 🤖 What is NexusAI?

NexusAI ek AI-powered chatbot hai jo **do modes** mein kaam karta hai:

### Mode 1 — General Chat
```
User: What is machine learning?
Bot:  Machine learning is a subset of AI that enables systems to learn from data...
```

### Mode 2 — Website RAG Mode
```
User: [provides https://suzukipakistan.com]
      → System scrapes & indexes website

User: What cars does Suzuki Pakistan offer?
Bot:  According to the website, Suzuki Pakistan offers Alto, Cultus, Swift...
      Sources: https://suzukipakistan.com/products/automobiles
```

---

## 🔄 How It Works

### Website Indexing Flow
```
User provides URL
       ↓
FastAPI → POST /website/add
       ↓
scraper.py → requests + BeautifulSoup → clean text
       ↓
Split into 400-char chunks (50 char overlap)
       ↓
SentenceTransformers → 384-dim embedding vectors
       ↓
ChromaDB PersistentClient → store vectors on disk
       ↓
MongoDB → save website record { status: "done" }
```

### RAG Chat Flow
```
User sends question + website_id
       ↓
SentenceTransformers → query vector
       ↓
ChromaDB cosine similarity search → top 5 chunks
       ↓
Build context from retrieved chunks
       ↓
Gemini 1.5 Flash → generate answer using context
       ↓
MongoDB → save to chat_history
       ↓
Return { response, mode: "website", sources[] }
```

### General Chat Flow
```
User sends question (no website_id)
       ↓
Gemini 1.5 Flash → direct answer
       ↓
MongoDB → save to chat_history
       ↓
Return { response, mode: "general" }
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | User Interface |
| **Backend** | FastAPI | REST API |
| **LLM** | Google Gemini 1.5 Flash | Answer generation |
| **Embeddings** | SentenceTransformers | Text to vectors (no API key!) |
| **Vector DB** | ChromaDB Persistent | Store & search embeddings |
| **App DB** | MongoDB + Motor | Users, websites, chat history |
| **Scraping** | requests + BeautifulSoup4 | Website content extraction |
| **Auth** | JWT + bcrypt | Secure authentication |

---

## 📂 Project Structure

```
task 9/
│
├── frontend.py              ← Streamlit UI
├── .env                     ← API keys & config
├── requirements.txt         ← Python packages
│
├── chroma_storage/          ← ChromaDB data (auto-created)
│
└── app/
    ├── main.py              ← FastAPI app entry point
    ├── database.py          ← MongoDB connection
    ├── models.py            ← MongoDB document builders
    ├── schemas.py           ← Pydantic validation models
    ├── scraper.py           ← Web scraping (requests + BS4)
    ├── embeddings.py        ← Chunking + vectors + ChromaDB
    ├── rag_pipeline.py      ← RAG logic + Gemini prompting
    │
    ├── core/
    │   ├── config.py        ← Load .env variables
    │   └── security.py      ← Password hash + JWT
    │
    └── routes/
        ├── auth_routes.py   ← /auth/register, /auth/login
        ├── website_routes.py← /website/add
        └── chat_routes.py   ← /chat/
```

---

## 🗄 Database Schema

### MongoDB — `rag_chatbot` Database

#### `users` Collection
```json
{
  "_id":             "ObjectId",
  "name":            "Ahmed Ali",
  "email":           "ahmed123",
  "hashed_password": "$2b$12$...",
  "created_at":      "2024-01-01T00:00:00Z"
}
```

#### `websites` Collection
```json
{
  "_id":           "ObjectId",
  "user_id":       "ahmed123",
  "url":           "https://example.com",
  "status":        "done",
  "pages_scraped": 10,
  "created_at":    "2024-01-01T00:00:00Z"
}
```

#### `chat_history` Collection
```json
{
  "_id":        "ObjectId",
  "user_id":    "ahmed123",
  "message":    "What services do you offer?",
  "response":   "According to the website...",
  "mode":       "website",
  "website_id": "507f1f77bcf86cd799439011",
  "timestamp":  "2024-01-01T12:00:00Z"
}
```

### ChromaDB — Vector Storage

```
Collection:  site_{website_id}
Dimensions:  384 (all-MiniLM-L6-v2)
Distance:    Cosine Similarity
Storage:     chroma_storage/ (persistent)

Fields:
  ids       → "{website_id}_{index}_{hash}"
  embeddings→ [0.123, -0.456, ...]  (384 floats)
  documents → "chunk text (400 chars)"
  metadatas → { source_url, website_id }
```

---

## 🔗 API Endpoints

### `POST /auth/register`
```json
// Request
{ "name": "Ahmed", "email": "ahmed123", "password": "pass123" }

// Response
{ "message": "User registered successfully", "user_id": "507f..." }
```

### `POST /auth/login`
```json
// Request
{ "email": "ahmed123", "password": "pass123" }

// Response
{ "access_token": "eyJhbGci...", "token_type": "bearer" }
```

### `POST /website/add`
```json
// Request
{ "url": "https://example.com", "user_id": "ahmed123" }

// Response
{ "message": "Website processed successfully", "pages_scraped": 10, "website_id": "507f..." }
```

### `POST /chat/`
```json
// General Mode
{ "message": "What is AI?", "user_id": "ahmed123" }

// Website RAG Mode
{ "message": "What cars do you sell?", "user_id": "ahmed123", "website_id": "507f..." }

// Response
{ "response": "According to the website...", "mode": "website", "sources": ["https://..."] }
```

---

## ⚙ Setup & Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install sentence-transformers
```

### 3. Configure `.env`
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=rag_chatbot
SECRET_KEY=your_secret_key_here
CHROMA_DB_PATH=./chroma_storage
```

> 🔑 Get Gemini API Key: https://aistudio.google.com/app/apikey

---

## 🚀 Running the Project

```bash
# Terminal 1 — Backend
uvicorn app.main:app --reload
# → http://127.0.0.1:8000
# → http://127.0.0.1:8000/docs  (API docs)

# Terminal 2 — Frontend
streamlit run frontend.py
# → http://localhost:8501
```

---

## 📖 Usage Guide

1. **Register** → Create Account tab mein naam, username, password
2. **Login** → Sign In tab se login karo
3. **General Chat** → Seedha koi bhi question poochho
4. **Website Mode:**
   - Sidebar mein URL enter karo
   - "Index Website" click karo (1-2 min wait)
   - Website ke baare mein sawal karo
   - Answer + sources milenge
5. **Remove Website** → Sidebar mein "Remove Source" click karo

---

## 🧠 RAG Pipeline Explained

```
INDEXING (one time per website):
  Text → Chunks (400 chars) → Embeddings → ChromaDB

RETRIEVAL (every question):
  Question → Query Embedding → ChromaDB Search → Top 5 Chunks

GENERATION:
  Context (chunks) + Question → Gemini → Answer + Sources
```

**Why RAG?**
- ✅ Website ka latest content use hota hai
- ✅ Specific, accurate answers
- ✅ Sources cite kiye jaate hain
- ✅ Hallucination kam hoti hai

---

## 🐛 Common Errors & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| MongoDB connection error | MongoDB service start karo |
| Gemini 429 rate limit | 1 minute wait karo (free tier: 60 req/min) |
| `"Could not find info"` | Website dobara index karo |
| bcrypt error | `pip install bcrypt==4.0.1` |
| Email validation error | `EmailStr` ko `str` se replace karo in schemas.py |
| ChromaDB `np.float_` error | `pip install "numpy<2.0"` |

---

## 📦 Key Dependencies

```
fastapi          — REST API framework
uvicorn          — ASGI server
motor            — Async MongoDB driver
chromadb         — Vector database
google-generativeai — Gemini AI
sentence-transformers — Local embeddings
beautifulsoup4   — Web scraping
streamlit        — Frontend UI
python-jose      — JWT tokens
bcrypt           — Password hashing
```

---

<div align="center">

**NexusAI v1.0** · FastAPI · Streamlit · Gemini · ChromaDB · MongoDB

</div>