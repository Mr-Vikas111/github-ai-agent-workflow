"""Shared API dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.todo import TodoRepository
from app.services.todo import TodoService

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


async def get_todo_service(session: DbSession) -> TodoService:
    """Provide the todo service instance for request handlers."""
    return TodoService(session=session, repository=TodoRepository())
