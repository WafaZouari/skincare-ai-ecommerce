"""
app/db/database.py
──────────────────
PostgreSQL connection via SQLAlchemy.

Key concepts:
  • `engine`      – manages the connection pool to Postgres.
  • `SessionLocal` – factory that produces per-request DB sessions.
  • `Base`        – declarative base class that all ORM models inherit from.
  • `get_db()`    – FastAPI dependency that yields a session and guarantees
                    cleanup (commit on success, rollback on exception).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # verify connections before reuse
    pool_size=10,             # max persistent connections
    max_overflow=20,          # extra connections under load
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency — yields a SQLAlchemy session per request.

    Usage in a router:
        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()