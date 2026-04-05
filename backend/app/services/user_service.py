"""
app/services/user_service.py
────────────────────────────
Business logic for User CRUD operations.

WHY no password logic here?
  Hashing lives in core/security.py (single responsibility).
  This service only orchestrates DB operations.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Return the User row matching email, or None."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Return the User row by primary key, or raise 404."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        """
        Register a new user.

        Raises 400 if the email is already taken.
        Passwords are hashed here — plain text is NEVER stored.
        """
        if UserService.get_user_by_email(db, user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        db_user = User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),  # ✅ Hashed
            full_name=user_in.full_name,
            skin_type=user_in.skin_type,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
        """Patch a user — only updates fields that were explicitly sent."""
        db_user = UserService.get_user_by_id(db, user_id)
        update_data = user_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

