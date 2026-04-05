"""
app/api/v1/endpoints/ai_sessions.py
----------------------------------
Defines the endpoints for managing AI chat sessions.
Uses AIService to interact with MongoDB.
"""

from fastapi import APIRouter, Depends, status
from pymongo.database import Database
from app.db.mongo import get_mongo_db
from app.services.ai_service import AIService
from app.schemas.ai_session import AISessionCreate, AISessionResponse, AIMessageAdd
from typing import List

router = APIRouter()

@router.post("/", response_model=AISessionResponse, status_code=status.HTTP_201_CREATED)
def start_ai_session(session_in: AISessionCreate, db: Database = Depends(get_mongo_db)):
    """Initializes a new skincare AI session for a specific user ID."""
    return AIService.create_session(db, session_in)

@router.get("/{session_id}", response_model=AISessionResponse)
def get_ai_session(session_id: str, db: Database = Depends(get_mongo_db)):
    """Retrieves session details and full conversation history."""
    return AIService.get_session(db, session_id)

@router.post("/{session_id}/messages", response_model=AISessionResponse)
def add_message_to_session(session_id: str, message_in: AIMessageAdd, db: Database = Depends(get_mongo_db)):
    """Appends a new interaction (user/assistant) to an existing session."""
    return AIService.add_message(db, session_id, message_in)

@router.get("/user/{user_id}", response_model=List[AISessionResponse])
def list_user_sessions(user_id: int, db: Database = Depends(get_mongo_db)):
    """Lists all consultation history for a specific user."""
    return AIService.list_user_sessions(db, user_id)
