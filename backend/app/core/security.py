"""
app/core/security.py
────────────────────
Low-level cryptography utilities.

Responsibilities (and ONLY these):
  1. Hash plain-text passwords with bcrypt.
  2. Verify a plain-text password against its hash.
  3. Create a signed JWT access token.
  4. Decode and validate an incoming JWT.

WHY a separate module?
  • Single Responsibility — auth endpoints and services should NOT care
    about HOW hashing / signing works; they just call these helpers.
  • Easy to swap algorithms later (e.g., argon2 instead of bcrypt)
    without touching half the codebase.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# ── Password hashing ──────────────────────────────────────────────
# CryptContext handles algorithm selection, deprecation, and future
# migrations automatically.  bcrypt is the industry standard.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return the bcrypt hash of a plain-text password."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if the plain password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT ───────────────────────────────────────────────────────────

def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a signed JWT access token.

    Parameters
    ----------
    subject : str | int
        Typically the user's ID or email — what the token 'represents'.
    expires_delta : timedelta | None
        Optional overriding TTL.  Falls back to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns
    -------
    str
        A compact, URL-safe JWT string.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": str(subject),   # 'sub' (subject) is a standard JWT claim
        "exp": expire,         # 'exp' (expiration) — jose validates this automatically
        "iat": datetime.now(timezone.utc),  # 'iat' (issued at) — useful for auditing
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and validate a JWT.

    Returns
    -------
    str | None
        The 'sub' claim (user ID) if the token is valid, otherwise None.
        Callers are responsible for raising HTTP 401 when None is returned.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload.get("sub")
    except JWTError:
        return None
