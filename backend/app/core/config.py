"""
app/core/config.py
──────────────────
Centralised application settings loaded from environment variables.

Uses pydantic-settings (BaseSettings) so every value is validated at startup.
The `.env` file is read automatically; explicit env vars always take precedence.
"""

from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "Skincare AI E-Commerce"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ── PostgreSQL (SQLAlchemy) ──────────────────────────────────
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/skincare_db"

    # ── MongoDB (AI Sessions) ───────────────────────────────────
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "skincare_ai"

    # ── Security / JWT (placeholder — extend later) ─────────────
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ── CORS ────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    """Return a cached Settings singleton so .env is parsed only once."""
    return Settings()
