"""
app/services/auth_service.py
────────────────────────────
Business logic for authentication flows.

WHY separate from user_service.py?
  • user_service.py  → manages the User *resource* (CRUD).
  • auth_service.py  → manages *sessions* (login, token issuance).
  Mixing them would mean a single class responsible for too many things.

Flow:
  1. Client calls POST /auth/login with email + password.
  2. We look up the user by email.
  3. We verify the plain password against the stored bcrypt hash.
  4. If valid, we create and return a signed JWT.
  5. Client stores that JWT and sends it in: Authorization: Bearer <token>
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.services.user_service import UserService
from app.core.security import verify_password, create_access_token
from app.schemas.auth import TokenResponse


class AuthService:

    @staticmethod
    def login(db: Session, email: str, password: str) -> TokenResponse:
        """
        Validate credentials and return a JWT access token.

        COMMON MISTAKE: Don't give different error messages for
        'user not found' vs 'wrong password'. Always return the same
        vague message — it prevents attackers from enumerating valid emails.
        """
        # Step 1: Find the user
        user = UserService.get_user_by_email(db, email)

        # Step 2: Validate — same generic error either way (security!)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},  # Required by OAuth2 spec
            )

        # Step 3: Check account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )

        # Step 4: Issue token — subject is the user's ID (not email)
        # WHY user ID as subject?
        #   If a user changes their email, existing tokens still work.
        access_token = create_access_token(subject=user.id)

        return TokenResponse(access_token=access_token)
