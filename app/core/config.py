from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "rag_chatbot")
SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 4