from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URL, DATABASE_NAME

client: AsyncIOMotorClient = None
db = None


async def connect_db():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    print(f" MongoDB Connected: {DATABASE_NAME}")


async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB Connection Closed")


def get_db():
    return db
