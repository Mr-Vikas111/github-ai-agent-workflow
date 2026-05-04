"""User repository implementation."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Data access layer for user persistence."""

    async def create(
        self,
        session: AsyncSession,
        *,
        email: str,
        full_name: str,
        password_hash: str,
    ) -> User:
        """Create and persist a user."""
        user = User(email=email, full_name=full_name, password_hash=password_hash)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        """Fetch a user by email address."""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, session: AsyncSession, user_id: UUID) -> User | None:
        """Fetch a user by identifier."""
        return await session.get(User, user_id)
