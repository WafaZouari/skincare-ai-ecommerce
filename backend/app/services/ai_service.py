"""
app/services/ai_service.py
-------------------------
Handles all business logic for AI sessions stored in MongoDB.
Each session is a record including user information and message history.
"""

from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pymongo.database import Database
from app.schemas.ai_session import AISessionCreate, AIMessageAdd, AISessionResponse, MessageEntry
from fastapi import HTTPException

class AIService:
    @staticmethod
    def create_session(db: Database, session_in: AISessionCreate):
        """Initializes a new AI consultation session in MongoDB."""
        new_session = {
            "user_id": session_in.user_id,
            "skin_concerns": session_in.skin_concerns,
            "messages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = db["ai_sessions"].insert_one(new_session)
        created_session = db["ai_sessions"].find_one({"_id": result.inserted_id})
        
        # Format MongoDB _id (ObjectId) into string for the Pydantic schema
        created_session["_id"] = str(created_session["_id"])
        return created_session

    @staticmethod
    def get_session(db: Database, session_id: str):
        """Retrieve a specific AI session by MongoDB ObjectId."""
        try:
            object_id = ObjectId(session_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid session format")
            
        session = db["ai_sessions"].find_one({"_id": object_id})
        if not session:
            raise HTTPException(status_code=404, detail="AI Session not found")
        
        session["_id"] = str(session["_id"])
        return session

    @staticmethod
    def add_message(db: Database, session_id: str, message_in: AIMessageAdd):
        """Append a new message (user or assistant) to an existing session."""
        try:
            object_id = ObjectId(session_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid session format")
            
        new_message = {
            "role": message_in.role,
            "content": message_in.content,
            "timestamp": datetime.utcnow()
        }
        
        result = db["ai_sessions"].update_one(
            {"_id": object_id},
            {
                "$push": {"messages": new_message},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Session not updated or not found")
        
        return AIService.get_session(db, session_id)

    @staticmethod
    def list_user_sessions(db: Database, user_id: int):
        """Retrieve all previous AI sessions for a specific user."""
        cursor = db["ai_sessions"].find({"user_id": user_id}).sort("created_at", -1)
        sessions = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            sessions.append(doc)
        return sessions
