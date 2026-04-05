"""
app/schemas/user.py
───────────────────
Pydantic schemas for the User resource (Interface Layer).

These schemas define what data comes IN from API requests and what
goes OUT in API responses.  They are intentionally separate from the
SQLAlchemy model so that:
  • Internal DB columns (hashed_password) are never leaked.
  • Validation rules can evolve independently of the DB schema.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ── Request schemas ──────────────────────────────────────────────

class UserCreate(BaseModel):
    """Payload to register a new user."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    skin_type: Optional[str] = None


class UserUpdate(BaseModel):
    """Payload to update an existing user (all fields optional)."""
    full_name: Optional[str] = None
    skin_type: Optional[str] = None
    is_active: Optional[bool] = None


# ── Response schemas ─────────────────────────────────────────────

class UserResponse(BaseModel):
    """Public representation of a user returned by the API."""
    id: int
    email: str
    full_name: Optional[str] = None
    skin_type: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
