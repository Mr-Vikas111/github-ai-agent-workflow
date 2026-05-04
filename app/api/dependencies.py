"""Shared API dependencies."""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, AuthorizationError, NotFoundError
from app.core.security import decode_access_token
from app.db.session import get_db_session
from app.models.user import User
from app.repositories.todo import TodoRepository
from app.repositories.user import UserRepository
from app.schemas.auth import UserRole
from app.services.auth import AuthService
from app.services.todo import TodoService

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
bearer_scheme = HTTPBearer(auto_error=False)
TokenCredentials = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]


async def get_todo_service(session: DbSession) -> TodoService:
    """Provide the todo service instance for request handlers."""
    return TodoService(session=session, repository=TodoRepository())


async def get_auth_service(session: DbSession) -> AuthService:
    """Provide the auth service instance for request handlers."""
    return AuthService(session=session, repository=UserRepository())


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    credentials: TokenCredentials,
    service: AuthServiceDependency,
) -> User:
    """Resolve the authenticated user from a bearer token."""
    if credentials is None:
        raise AuthenticationError("Authentication credentials were not provided.")

    token_payload = decode_access_token(credentials.credentials)
    try:
        user = await service.get_user(token_payload.sub)
    except NotFoundError as exc:
        raise AuthenticationError("Invalid or expired authentication token.") from exc
    if not user.is_active:
        raise AuthorizationError("User account is inactive.")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_roles(*roles: UserRole) -> Callable[[CurrentUser], User]:
    """Build a dependency that restricts access to the provided roles."""

    async def role_dependency(current_user: CurrentUser) -> User:
        current_role = (
            current_user.role.value
            if isinstance(current_user.role, UserRole)
            else current_user.role
        )
        if current_role not in {role.value for role in roles}:
            raise AuthorizationError("You do not have permission to perform this action.")
        return current_user

    return role_dependency
