"""
app/api/v1/endpoints/users.py
─────────────────────────────
User resource endpoints (CRUD on the User entity).

NOTE: These routes are currently public for development.
      In production, protect them with Depends(get_current_user).
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user via the /users route (mirrors /auth/register)."""
    return UserService.create_user(db, user_in)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a user by their ID."""
    return UserService.get_user_by_id(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    """Partially update a user's profile."""
    return UserService.update_user(db, user_id, user_in)

