"""Todo repository implementation."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    """Data access layer for todo persistence."""

    async def create(self, session: AsyncSession, payload: TodoCreate) -> Todo:
        """Create and persist a todo item."""
        todo = Todo(**payload.model_dump())
        session.add(todo)
        await session.commit()
        await session.refresh(todo)
        return todo

    async def get_by_id(self, session: AsyncSession, todo_id: UUID) -> Todo | None:
        """Fetch a todo by its identifier."""
        return await session.get(Todo, todo_id)

    async def list(
        self,
        session: AsyncSession,
        *,
        limit: int,
        offset: int,
        is_completed: bool | None = None,
        search: str | None = None,
    ) -> Sequence[Todo]:
        """List todo items with pagination and optional filters."""
        query = self._build_filtered_query(is_completed=is_completed, search=search)
        query = query.order_by(Todo.created_at.desc()).limit(limit).offset(offset)
        result = await session.execute(query)
        return result.scalars().all()

    async def count(
        self,
        session: AsyncSession,
        *,
        is_completed: bool | None = None,
        search: str | None = None,
    ) -> int:
        """Count todo items for the current filter set."""
        base_query = self._build_filtered_query(is_completed=is_completed, search=search)
        count_query = select(func.count()).select_from(base_query.subquery())
        result = await session.execute(count_query)
        return int(result.scalar_one())

    async def update(
        self, session: AsyncSession, todo: Todo, payload: TodoUpdate
    ) -> Todo:
        """Update an existing todo item."""
        for field_name, value in payload.model_dump(exclude_unset=True).items():
            setattr(todo, field_name, value)
        todo.updated_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(todo)
        return todo

    async def delete(self, session: AsyncSession, todo: Todo) -> None:
        """Delete a todo item."""
        await session.delete(todo)
        await session.commit()

    def _build_filtered_query(
        self, *, is_completed: bool | None, search: str | None
    ) -> Select[tuple[Todo]]:
        query = select(Todo)
        if is_completed is not None:
            query = query.where(Todo.is_completed.is_(is_completed))
        if search:
            search_term = f"%{search.strip()}%"
            query = query.where(
                Todo.title.ilike(search_term) | Todo.description.ilike(search_term)
            )
        return query
