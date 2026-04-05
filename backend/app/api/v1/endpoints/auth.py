"""
app/api/v1/endpoints/auth.py
────────────────────────────
Authentication endpoints: register, login, and "who am I".

Design principles applied here:
  • Routes are thin — all logic delegated to services.
  • Schemas enforce input validation before the route body runs.
  • get_current_user is the only guard needed for protected routes.

Endpoints:
  POST /auth/register  → Create account, return user profile
  POST /auth/login     → Validate credentials, return JWT
  GET  /auth/me        → Return the currently logged-in user's profile
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


# ── POST /auth/register ───────────────────────────────────────────

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Creates a new user account. "
        "The password is hashed with bcrypt before storage — "
        "plain text is never persisted."
    ),
)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    PUBLIC endpoint — no token required.

    Flow:
      1. Pydantic validates email format + required fields.
      2. UserService checks for duplicate email.
      3. Password is hashed, user is stored, user profile is returned.

    COMMON MISTAKE: Don't return the hashed_password in the response.
    UserResponse is intentionally built without that field.
    """
    return UserService.create_user(db, user_in)


# ── POST /auth/login ──────────────────────────────────────────────

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get access token",
    description=(
        "Validates email/password and returns a JWT access token. "
        "Include this token in future requests as: "
        "Authorization: Bearer <token>"
    ),
)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    PUBLIC endpoint — no token required.

    WHY not use OAuth2PasswordRequestForm?
      That form expects application/x-www-form-urlencoded.
      We use JSON (application/json) for consistency with the rest of
      the API and friendlier frontend integration.

    COMMON MISTAKE: Don't expose whether the email exists or the
    password is wrong separately — AuthService returns the same error.
    """
    return AuthService.login(db, credentials.email, credentials.password)


# ── GET /auth/me ──────────────────────────────────────────────────

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description=(
        "Returns the profile of the currently authenticated user. "
        "Requires a valid JWT in the Authorization: Bearer header."
    ),
)
def get_me(current_user: User = Depends(get_current_user)):
    """
    PROTECTED endpoint — requires a valid JWT.

    get_current_user (injected via Depends) does all the heavy lifting:
      • Parses the Authorization header
      • Decodes and validates the JWT
      • Fetches the user from the DB
      • Raises 401 if anything is invalid

    This route just returns what it's given.
    """
    return current_user
