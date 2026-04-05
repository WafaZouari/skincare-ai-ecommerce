"""
app/core/dependencies.py
────────────────────────
Reusable FastAPI dependency functions.

WHY a dedicated dependencies module?
  Dependencies like get_current_user are used across MANY routers.
  Centralising them here means:
    • One place to change auth logic
    • easy to unit-test in isolation
    • Clean import path: from app.core.dependencies import get_current_user

HOW FastAPI dependencies work:
  When a route declares `current_user: User = Depends(get_current_user)`,
  FastAPI calls get_current_user() before the route function runs.
  If it raises an HTTPException, the route never executes — perfect security gate.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.services.user_service import UserService

# OAuth2PasswordBearer tells FastAPI:
#   "Extract the JWT from the Authorization: Bearer <token> header."
#   tokenUrl is used by Swagger UI to know where to send login requests.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Protected route dependency.

    Validates the JWT from the Authorization header and returns the
    corresponding User from the database.

    Usage in any route:
        @router.get("/protected")
        def protected(current_user: User = Depends(get_current_user)):
            return {"email": current_user.email}

    COMMON MISTAKE: Don't catch the HTTPException here — let it propagate
    so FastAPI automatically returns a 401 to the client.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1: Decode the token and get the user ID
    user_id_str = decode_access_token(token)
    if user_id_str is None:
        raise credentials_exception

    # Step 2: Parse user ID (our tokens store it as a string)
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception

    # Step 3: Verify user still exists in the DB
    # WHY check the DB?  A token could be valid but the user deleted.
    user = UserService.get_user_by_id(db, user_id)

    # Step 4: Verify account is still active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Convenience wrapper — re-usable for routes that need an active user.
    This pattern lets you add more checks (e.g., email verified) in one place.
    """
    return current_user
