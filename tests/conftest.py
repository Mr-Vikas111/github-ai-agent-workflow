"""Shared pytest fixtures."""

from collections.abc import AsyncIterator
from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_todo_service
from app.core.exceptions import NotFoundError
from app.main import app
from app.schemas.todo import TodoCreate, TodoListResponse, TodoRead, TodoUpdate


class InMemoryTodoService:
    """Simple in-memory todo service for API tests."""

    def __init__(self) -> None:
        self._items: dict[UUID, TodoRead] = {}

    async def create_todo(self, payload: TodoCreate) -> TodoRead:
        now = datetime.now(UTC)
        todo = TodoRead(id=uuid4(), created_at=now, updated_at=now, **payload.model_dump())
        self._items[todo.id] = todo
        return todo

    async def get_todo(self, todo_id: UUID) -> TodoRead:
        todo = self._items.get(todo_id)
        if todo is None:
            raise NotFoundError(f"Todo '{todo_id}' was not found.")
        return todo

    async def list_todos(
        self,
        *,
        limit: int,
        offset: int,
        is_completed: bool | None = None,
        search: str | None = None,
    ) -> TodoListResponse:
        items = list(self._items.values())
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

    async def update_todo(self, todo_id: UUID, payload: TodoUpdate) -> TodoRead:
        existing = await self.get_todo(todo_id)
        updated = existing.model_copy(
            update={
                **payload.model_dump(exclude_unset=True),
                "updated_at": datetime.now(UTC),
            }
        )
        self._items[todo_id] = updated
        return updated

    async def delete_todo(self, todo_id: UUID) -> None:
        await self.get_todo(todo_id)
        del self._items[todo_id]


@pytest.fixture
def fake_todo_service() -> InMemoryTodoService:
    """Return a fresh in-memory todo service."""
    return InMemoryTodoService()


@pytest.fixture
async def client(fake_todo_service: InMemoryTodoService) -> AsyncIterator[AsyncClient]:
    """Return an HTTPX async client with dependency overrides."""

    async def override_service() -> InMemoryTodoService:
        return fake_todo_service

    app.dependency_overrides[get_todo_service] = override_service
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client

    app.dependency_overrides.clear()
