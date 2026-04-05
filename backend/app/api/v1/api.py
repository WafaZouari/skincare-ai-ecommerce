"""
app/api/v1/api.py
─────────────────
Groups all feature routers into a single v1 router.
Enables clean versioned API paths like /api/v1/auth/login.

HOW TO ADD A NEW FEATURE:
  1. Create app/api/v1/endpoints/your_feature.py
  2. Import it here
  3. api_router.include_router(your_feature.router, prefix="/your-feature", tags=["Your Feature"])
"""

from fastapi import APIRouter
from app.api.v1.endpoints import users, ai_sessions, auth

api_router = APIRouter()

api_router.include_router(auth.router,        prefix="/auth",        tags=["Authentication"])
api_router.include_router(users.router,       prefix="/users",       tags=["Users"])
api_router.include_router(ai_sessions.router, prefix="/ai-sessions", tags=["AI Sessions"])

