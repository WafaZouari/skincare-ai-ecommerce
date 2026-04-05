"""
app/schemas/ai_session.py
─────────────────────────
Pydantic schemas for AI chat sessions stored in MongoDB.

MongoDB documents are schema-less, but we still validate with Pydantic
to enforce consistency and catch errors at the API boundary.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MessageEntry(BaseModel):
    """A single message in the AI conversation."""
    role: str = Field(..., examples=["user", "assistant"])
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AISessionCreate(BaseModel):
    """Payload to start a new AI session."""
    user_id: int
    skin_concerns: Optional[str] = None


class AISessionResponse(BaseModel):
    """Public representation of an AI session."""
    id: str = Field(..., alias="_id")
    user_id: int
    skin_concerns: Optional[str] = None
    messages: list[MessageEntry] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"populate_by_name": True}


class AIMessageAdd(BaseModel):
    """Payload to add a message to an existing session."""
    role: str = Field(..., examples=["user", "assistant"])
    content: str
