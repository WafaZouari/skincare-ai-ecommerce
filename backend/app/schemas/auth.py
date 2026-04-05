"""
app/schemas/auth.py
───────────────────
Pydantic schemas for the authentication flow.

WHY separate from schemas/user.py?
  • User schemas are about the *resource* (CRUD).
  • Auth schemas are about the *session* (login, tokens).
  • Mixing them creates coupling: a user update shouldn't need token fields.
"""

from pydantic import BaseModel, EmailStr


# ── Request schemas ───────────────────────────────────────────────

class LoginRequest(BaseModel):
    """Payload the client sends to POST /auth/login."""
    email: EmailStr
    password: str


# ── Response schemas ──────────────────────────────────────────────

class TokenResponse(BaseModel):
    """
    Standard OAuth2-compatible token response.

    access_token : the signed JWT the client must include in future requests
                   via the Authorization: Bearer <token> header.
    token_type   : always "bearer" — required by the OAuth2 spec so that
                   clients know HOW to use the token.
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Internal representation of a decoded JWT payload.
    Used in get_current_user to type the decoded claims.
    """
    sub: str | None = None
