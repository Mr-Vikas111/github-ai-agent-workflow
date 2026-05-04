"""Authentication service layer."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import TokenResponse, UserLogin, UserRegister


class AuthService:
    """Business logic for user authentication."""

    def __init__(self, session: AsyncSession, repository: UserRepository) -> None:
        self._session = session
        self._repository = repository

    async def register_user(self, payload: UserRegister) -> User:
        """Create a new user account."""
        existing_user = await self._repository.get_by_email(self._session, payload.email)
        if existing_user is not None:
            raise ConflictError(f"User '{payload.email}' already exists.")

        return await self._repository.create(
            self._session,
            email=payload.email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password),
        )

    async def login_user(self, payload: UserLogin) -> TokenResponse:
        """Authenticate a user and issue a JWT."""
        user = await self._repository.get_by_email(self._session, payload.email)
        if user is None or not verify_password(payload.password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")
        if not user.is_active:
            raise AuthorizationError("User account is inactive.")

        return TokenResponse(
            access_token=create_access_token(subject=str(user.id), role=user.role),
        )

    async def get_user(self, user_id: UUID) -> User:
        """Fetch a user by identifier or raise when missing."""
        user = await self._repository.get_by_id(self._session, user_id)
        if user is None:
            raise NotFoundError(f"User '{user_id}' was not found.")
        return user
