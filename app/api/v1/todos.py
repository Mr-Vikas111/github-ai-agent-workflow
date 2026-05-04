"""Todo API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import get_todo_service
from app.schemas.todo import TodoCreate, TodoListResponse, TodoRead, TodoUpdate
from app.services.todo import TodoService

router = APIRouter()
TodoServiceDependency = Annotated[TodoService, Depends(get_todo_service)]


@router.post(
    "",
    response_model=TodoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create todo",
)
async def create_todo(
    payload: TodoCreate,
    service: TodoServiceDependency,
) -> TodoRead:
    """Create a new todo item."""
    return await service.create_todo(payload)


@router.get(
    "",
    response_model=TodoListResponse,
    summary="List todos",
)
async def list_todos(
    service: TodoServiceDependency,
    limit: int = Query(default=20, ge=1, le=100, description="Maximum number of items to return."),
    offset: int = Query(default=0, ge=0, description="Number of items to skip."),
    is_completed: bool | None = Query(
        default=None,
        description="Optional completion filter.",
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="Optional case-insensitive title or description search.",
    ),
) -> TodoListResponse:
    """List todo items with pagination and filters."""
    return await service.list_todos(
        limit=limit,
        offset=offset,
        is_completed=is_completed,
        search=search,
    )


@router.get(
    "/{todo_id}",
    response_model=TodoRead,
    summary="Get todo",
)
async def get_todo(
    todo_id: UUID,
    service: TodoServiceDependency,
) -> TodoRead:
    """Fetch a todo item by identifier."""
    return await service.get_todo(todo_id)


@router.patch(
    "/{todo_id}",
    response_model=TodoRead,
    summary="Update todo",
)
async def update_todo(
    todo_id: UUID,
    payload: TodoUpdate,
    service: TodoServiceDependency,
) -> TodoRead:
    """Update fields on an existing todo item."""
    return await service.update_todo(todo_id, payload)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete todo",
)
async def delete_todo(
    todo_id: UUID,
    service: TodoServiceDependency,
) -> Response:
    """Delete a todo item."""
    await service.delete_todo(todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
