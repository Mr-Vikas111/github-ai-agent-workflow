"""Todo service layer."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.todo import Todo
from app.repositories.todo import TodoRepository
from app.schemas.todo import TodoCreate, TodoListResponse, TodoUpdate


class TodoService:
    """Business logic for todo APIs."""

    def __init__(self, session: AsyncSession, repository: TodoRepository) -> None:
        self._session = session
        self._repository = repository

    async def create_todo(self, payload: TodoCreate) -> Todo:
        """Create a todo item."""
        return await self._repository.create(self._session, payload)

    async def get_todo(self, todo_id: UUID) -> Todo:
        """Return a single todo item or raise when missing."""
        todo = await self._repository.get_by_id(self._session, todo_id)
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
        """Return paginated todo items."""
        items = await self._repository.list(
            self._session,
            limit=limit,
            offset=offset,
            is_completed=is_completed,
            search=search,
        )
        total = await self._repository.count(
            self._session,
            is_completed=is_completed,
            search=search,
        )
        return TodoListResponse(items=items, total=total, limit=limit, offset=offset)

    async def update_todo(self, todo_id: UUID, payload: TodoUpdate) -> Todo:
        """Update a todo item or raise when missing."""
        todo = await self.get_todo(todo_id)
        return await self._repository.update(self._session, todo, payload)

    async def delete_todo(self, todo_id: UUID) -> None:
        """Delete a todo item or raise when missing."""
        todo = await self.get_todo(todo_id)
        await self._repository.delete(self._session, todo)
