import os
from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None

async def connect_db() -> None:
    global _client, db
    if _client is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        db = _client[DATABASE_NAME]

async def close_db() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if db is None:
        raise RuntimeError("Database not connected")
    data = {**data, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    res = await db[collection_name].insert_one(data)
    inserted = await db[collection_name].find_one({"_id": res.inserted_id})
    if inserted and "_id" in inserted:
        inserted["_id"] = str(inserted["_id"])  # convert ObjectId to str
    return inserted or {}

async def get_documents(collection_name: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 50) -> List[Dict[str, Any]]:
    if db is None:
        raise RuntimeError("Database not connected")
    cursor = db[collection_name].find(filter_dict or {}).limit(limit)
    results: List[Dict[str, Any]] = []
    async for doc in cursor:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])  # convert ObjectId to str
        results.append(doc)
    return results
