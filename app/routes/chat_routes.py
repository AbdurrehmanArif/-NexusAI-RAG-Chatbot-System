from fastapi import APIRouter, HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from app.schemas import ChatRequest, ChatResponse
from app.database import get_db
from app.models import chat_history_model
from app.rag_pipeline import general_chat, rag_chat
import traceback

router = APIRouter(prefix="/chat", tags=["Chat"])


def safe_object_id(id_str: str):
    """Safely convert string to ObjectId."""
    try:
        return ObjectId(id_str)
    except (InvalidId, Exception):
        return None


@router.post("/", response_model=ChatResponse)
async def chat(body: ChatRequest):
    db = get_db()
    mode = "general"
    sources = None
    response_text = ""

    try:
        if body.website_id:
            # ── Website RAG Mode ──
            oid = safe_object_id(body.website_id)
            if oid is None:
                raise HTTPException(status_code=400, detail="Invalid website_id format")

            website = await db.websites.find_one({"_id": oid})
            if not website:
                raise HTTPException(status_code=404, detail="Website not found")
            if website.get("status") != "done":
                raise HTTPException(
                    status_code=400,
                    detail=f"Website not ready. Status: {website.get('status')}"
                )

            result = rag_chat(body.message, body.website_id)
            response_text = result["response"]
            sources = result.get("sources", [])
            mode = "website"

        else:
            # ── General Mode ──
            response_text = general_chat(body.message)
            mode = "general"

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    # ✅ MongoDB mein save karo - try/except alag taake chat fail na ho
    try:
        history_doc = chat_history_model(
            user_id=str(body.user_id),        # string hi rakho
            message=body.message,
            response=response_text,
            mode=mode,
            website_id=str(body.website_id) if body.website_id else None,
        )
        result = await db.chat_history.insert_one(history_doc)
        print(f"✅ Chat saved to MongoDB: {result.inserted_id}")
    except Exception as e:
        # Save fail hone pe bhi response return karo
        print(f"⚠️  MongoDB save failed: {e}")
        traceback.print_exc()

    return ChatResponse(response=response_text, mode=mode, sources=sources)


@router.get("/history/{user_id}")
async def get_history(user_id: str, limit: int = 50):
    """User ki chat history MongoDB se lo."""
    db = get_db()
    cursor = db.chat_history.find(
        {"user_id": str(user_id)}
    ).sort("timestamp", -1).limit(limit)

    history = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        history.append(doc)

    print(f"📜 Found {len(history)} messages for user: {user_id}")
    return {"history": history, "total": len(history)}