"""
app/models/user.py
──────────────────
SQLAlchemy ORM model for the `users` table (PostgreSQL).

This is the **Data Layer** — it defines the database schema.
Business logic does NOT belong here; it lives in app/services/.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    skin_type = Column(String(50), nullable=True)        # e.g. "oily", "dry", "combination"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
