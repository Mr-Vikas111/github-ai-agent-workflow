"""Shared pytest fixtures."""

from collections.abc import AsyncIterator
from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_auth_service, get_todo_service
from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.main import app
from app.schemas.auth import TokenResponse, UserLogin, UserRead, UserRegister, UserRole
from app.schemas.todo import TodoCreate, TodoListResponse, TodoRead, TodoUpdate


class InMemoryTodoService:
    """Simple in-memory todo service for API tests."""

    def __init__(self) -> None:
        self._items: dict[UUID, TodoRead] = {}

    async def create_todo(self, owner_id: UUID, payload: TodoCreate) -> TodoRead:
        now = datetime.now(UTC)
        todo = TodoRead(
            id=uuid4(),
            owner_id=owner_id,
            is_active=True,
            created_at=now,
            updated_at=now,
            **payload.model_dump(),
        )
        self._items[todo.id] = todo
        return todo

    async def get_todo(self, todo_id: UUID, owner_id: UUID) -> TodoRead:
        todo = self._items.get(todo_id)
        if todo is None:
            raise NotFoundError(f"Todo '{todo_id}' was not found.")
        if todo.owner_id != owner_id:
            raise AuthorizationError("You do not have permission to access this todo.")
        return todo

    async def list_todos(
        self,
        *,
        owner_id: UUID,
        limit: int,
        offset: int,
        is_active: bool | None = None,
        is_completed: bool | None = None,
        search: str | None = None,
    ) -> TodoListResponse:
        items = [item for item in self._items.values() if item.owner_id == owner_id]
        if is_active is not None:
            items = [item for item in items if item.is_active is is_active]
        if is_completed is not None:
            items = [item for item in items if item.is_completed is is_completed]
        if search:
            term = search.lower()
            items = [
                item
                for item in items
                if term in item.title.lower() or term in (item.description or "").lower()
            ]
        paginated = items[offset : offset + limit]
        return TodoListResponse(items=paginated, total=len(items), limit=limit, offset=offset)

    async def update_todo(self, todo_id: UUID, owner_id: UUID, payload: TodoUpdate) -> TodoRead:
        existing = await self.get_todo(todo_id, owner_id)
        updated = existing.model_copy(
            update={
                **payload.model_dump(exclude_unset=True),
                "updated_at": datetime.now(UTC),
            }
        )
        self._items[todo_id] = updated
        return updated

    async def delete_todo(self, todo_id: UUID, owner_id: UUID) -> None:
        await self.get_todo(todo_id, owner_id)
        del self._items[todo_id]

    async def deactivate_todo(self, todo_id: UUID, owner_id: UUID) -> TodoRead:
        existing = await self.get_todo(todo_id, owner_id)
        updated = existing.model_copy(
            update={
                "is_active": False,
                "updated_at": datetime.now(UTC),
            }
        )
        self._items[todo_id] = updated
        return updated


class InMemoryAuthService:
    """Simple in-memory auth service for API tests."""

    def __init__(self) -> None:
        self._users: dict[UUID, dict[str, object]] = {}

    async def register_user(self, payload: UserRegister) -> UserRead:
        if any(user_data["user"].email == payload.email for user_data in self._users.values()):
            raise ConflictError(f"User '{payload.email}' already exists.")

        now = datetime.now(UTC)
        user_id = uuid4()
        user = UserRead(
            id=user_id,
            email=payload.email,
            full_name=payload.full_name,
            role=UserRole.USER,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        self._users[user_id] = {
            "user": user,
            "password_hash": hash_password(payload.password),
        }
        return user

    async def login_user(self, payload: UserLogin) -> TokenResponse:
        for user_data in self._users.values():
            user = user_data["user"]
            if user.email != payload.email:
                continue
            if not verify_password(payload.password, str(user_data["password_hash"])):
                raise AuthenticationError("Invalid email or password.")
            if not user.is_active:
                raise AuthorizationError("User account is inactive.")
            return TokenResponse(
                access_token=create_access_token(subject=str(user.id), role=user.role.value)
            )
        raise AuthenticationError("Invalid email or password.")

    async def get_user(self, user_id: UUID) -> UserRead:
        user_data = self._users.get(user_id)
        if user_data is None:
            raise NotFoundError(f"User '{user_id}' was not found.")
        return user_data["user"]

    async def deactivate_user(self, user_id: UUID) -> UserRead:
        user = await self.get_user(user_id)
        updated_user = user.model_copy(
            update={"is_active": False, "updated_at": datetime.now(UTC)}
        )
        self._users[user_id]["user"] = updated_user
        return updated_user


@pytest.fixture
def fake_todo_service() -> InMemoryTodoService:
    """Return a fresh in-memory todo service."""
    return InMemoryTodoService()


@pytest.fixture
def fake_auth_service() -> InMemoryAuthService:
    """Return a fresh in-memory auth service."""
    return InMemoryAuthService()


@pytest.fixture
def auth_identity(fake_auth_service: InMemoryAuthService):
    """Create authenticated test users and bearer headers."""

    async def factory(
        *,
        email: str = "user@example.com",
        full_name: str = "Example User",
        password: str = "Str0ngPassw0rd!",
    ) -> tuple[UserRead, dict[str, str]]:
        user = await fake_auth_service.register_user(
            UserRegister(email=email, full_name=full_name, password=password)
        )
        token = create_access_token(subject=str(user.id), role=user.role.value)
        return user, {"Authorization": f"Bearer {token}"}

    return factory


@pytest.fixture
async def client(
    fake_todo_service: InMemoryTodoService,
    fake_auth_service: InMemoryAuthService,
) -> AsyncIterator[AsyncClient]:
    """Return an HTTPX async client with dependency overrides."""

    async def override_service() -> InMemoryTodoService:
        return fake_todo_service

    async def override_auth_service() -> InMemoryAuthService:
        return fake_auth_service

    app.dependency_overrides[get_todo_service] = override_service
    app.dependency_overrides[get_auth_service] = override_auth_service
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client

    app.dependency_overrides.clear()
