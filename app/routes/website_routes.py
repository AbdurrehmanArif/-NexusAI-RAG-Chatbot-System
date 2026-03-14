from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.schemas import AddWebsiteRequest, WebsiteResponse
from app.database import get_db
from app.models import website_model
from app.scraper import scrape_website
from app.embeddings import store_chunks
import traceback

router = APIRouter(prefix="/website", tags=["Website"])


@router.post("/add", response_model=WebsiteResponse)
async def add_website(body: AddWebsiteRequest):
    db = get_db()

    if not body.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    doc = website_model(user_id=body.user_id, url=body.url, status="processing")
    result = await db.websites.insert_one(doc)
    website_id = str(result.inserted_id)

    try:
        print(f"🌐 Starting scrape: {body.url}")
        pages = scrape_website(body.url, max_pages=10)
        print(f"✅ Scraped {len(pages)} pages")

        if not pages:
            await db.websites.update_one(
                {"_id": ObjectId(website_id)},
                {"$set": {"status": "failed"}}
            )
            raise HTTPException(status_code=422, detail="Could not scrape any content from the URL.")

        print(f"🧠 Generating embeddings...")
        chunks_stored = store_chunks(website_id, pages)
        print(f"✅ Stored {chunks_stored} chunks")

        await db.websites.update_one(
            {"_id": ObjectId(website_id)},
            {"$set": {"status": "done", "pages_scraped": len(pages)}}
        )

        return WebsiteResponse(
            message="Website processed successfully",
            pages_scraped=len(pages),
            website_id=website_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        await db.websites.update_one(
            {"_id": ObjectId(website_id)},
            {"$set": {"status": "failed"}}
        )
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")