import chromadb
from sentence_transformers import SentenceTransformer
from typing import List
import os
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP


print(" Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print(" Embedding model loaded!")


CHROMA_PATH = "./chroma_storage"
os.makedirs(CHROMA_PATH, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)



def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return [c.strip() for c in chunks if len(c.strip()) > 50]



def get_embedding(text: str) -> List[float]:
    """Local model se embedding - koi API key nahi."""
    embedding = embedding_model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def get_query_embedding(text: str) -> List[float]:
    """Query embedding."""
    embedding = embedding_model.encode(text, normalize_embeddings=True)
    return embedding.tolist()



def get_or_create_collection(website_id: str):
    """Get or create collection - data persist hoga."""
    safe_id = website_id.replace("-", "_")
    collection_name = f"site_{safe_id}"
    
    
    if len(collection_name) > 63:
        collection_name = collection_name[:63]
    
    return chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def collection_exists_with_data(website_id: str) -> bool:
    """Check karo ke collection exist karti hai aur data hai."""
    try:
        safe_id = website_id.replace("-", "_")
        collection_name = f"site_{safe_id}"
        if len(collection_name) > 63:
            collection_name = collection_name[:63]
        
        col = chroma_client.get_collection(collection_name)
        count = col.count()
        print(f" Collection '{collection_name}' has {count} chunks")
        return count > 0
    except Exception as e:
        print(f" Collection check failed: {e}")
        return False


def store_chunks(website_id: str, pages: List[dict]) -> int:
    """Chunks embed karke ChromaDB mein store karo."""
    collection = get_or_create_collection(website_id)

    # Pehle se data check karo - duplicate avoid karo
    existing = collection.count()
    if existing > 0:
        print(f"  Collection already has {existing} chunks - clearing first")
        safe_id = website_id.replace("-", "_")
        collection_name = f"site_{safe_id}"
        if len(collection_name) > 63:
            collection_name = collection_name[:63]
        chroma_client.delete_collection(collection_name)
        collection = get_or_create_collection(website_id)

    total = 0
    for page in pages:
        chunks = chunk_text(page["content"])
        print(f"   {page['url']} → {len(chunks)} chunks")
        for i, chunk in enumerate(chunks):
            chunk_id = f"{website_id}_{i}_{hash(chunk) % 999999}"
            embedding = get_embedding(chunk)
            collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source_url": page["url"], "website_id": website_id}],
            )
            total += 1

    print(f" Total {total} chunks stored in ChromaDB (persistent)")
    return total


def search_similar_chunks(website_id: str, query: str, top_k: int = 5) -> List[dict]:
    """ChromaDB se similar chunks search karo."""
    try:
    
        if not collection_exists_with_data(website_id):
            print(f" No data found for website_id: {website_id}")
            return []

        collection = get_or_create_collection(website_id)
        query_emb = get_query_embedding(query)

    
        available = collection.count()
        n = min(top_k, available)
        if n == 0:
            return []

        results = collection.query(
            query_embeddings=[query_emb],
            n_results=n,
            include=["documents", "metadatas", "distances"],
        )

        chunks = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            
            if dist < 1.5:
                chunks.append({
                    "text": doc,
                    "source": meta.get("source_url", ""),
                    "score": round(1 - dist, 3)
                })
                print(f"   Score: {round(1-dist,3)} | {doc[:60]}...")

        return chunks

    except Exception as e:
        print(f" Search error: {e}")
        return []


def delete_website_collection(website_id: str):
    """Website ki collection delete karo."""
    try:
        safe_id = website_id.replace("-", "_")
        collection_name = f"site_{safe_id}"
        if len(collection_name) > 63:
            collection_name = collection_name[:63]
        chroma_client.delete_collection(collection_name)
        print(f"Deleted collection: {collection_name}")
    except Exception as e:
        print(f"Delete failed: {e}")
