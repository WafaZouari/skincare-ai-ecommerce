"""
app/main.py
-----------
Application entry point.
Initializes FastAPI, includes routers, and defines middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.v1.api import api_router
from app.db.database import engine, Base

# Import all models to ensure they are registered with Base.metadata
from app.models import *

# In a production environment, you would use Alembic for migrations.
# For this initial setup, we'll auto-create tables on startup.
Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS Middleware (Crucial for frontend-backend interaction)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for health check
@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "online"
    }

# Include all API v1 endpoints
app.include_router(api_router, prefix="/api/v1")
