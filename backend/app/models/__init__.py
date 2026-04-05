"""
app/models - SQLAlchemy ORM models (Data Layer).

Import all models here so that `Base.metadata` discovers every table
when we run migrations or call `Base.metadata.create_all()`.
"""

from app.models.user import User  # noqa: F401
