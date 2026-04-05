"""
app/db/mongo.py
───────────────
MongoDB connection for AI session storage.

Uses synchronous pymongo (matching current requirements.txt).
The `get_mongo_db()` function is a FastAPI dependency that provides
the database handle to routers and services.
"""

from pymongo import MongoClient

from app.core.config import get_settings

settings = get_settings()

client: MongoClient = MongoClient(settings.MONGO_URL)
mongo_db = client[settings.MONGO_DB_NAME]


def get_mongo_db():
    """
    FastAPI dependency — returns the MongoDB database handle.

    Collections are accessed like:
        db = get_mongo_db()
        db["ai_sessions"].find(...)
    """
    return mongo_db