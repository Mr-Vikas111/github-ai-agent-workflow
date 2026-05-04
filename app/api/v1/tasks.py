"""User-wise task API routes."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import CurrentUser, get_todo_service
from app.api.docs import (
    auth_error_response,
    forbidden_error_response,
    not_found_error_response,
    validation_error_response,
)
from app.schemas.todo import TodoCreate, TodoListResponse, TodoRead, TodoUpdate
from app.services.todo import TodoService

router = APIRouter()
TaskServiceDependency = Annotated[TodoService, Depends(get_todo_service)]


@router.post(
    "",
    response_model=TodoRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create task",
    description="Create a task under the authenticated user's personal task namespace.",
    response_description="Created user task.",
    responses={
        status.HTTP_401_UNAUTHORIZED: auth_error_response(
            "Bearer token is missing, invalid, or expired."
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: validation_error_response(
            "Task payload validation failed."
        ),
    },
)
async def create_task(
    payload: TodoCreate,
    current_user: CurrentUser,
    service: TaskServiceDependency,
) -> TodoRead:
    """Create a task for the authenticated user."""
    return await service.create_todo(current_user.id, payload)


@router.get(
    "",
    response_model=TodoListResponse,
    summary="List user tasks",
    description="List tasks for the authenticated user with pagination and optional filters.",
    response_description="Paginated user task collection.",
    responses={
        status.HTTP_401_UNAUTHORIZED: auth_error_response(
            "Bearer token is missing, invalid, or expired."
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: validation_error_response(
            "Query parameter validation failed."
        ),
    },
)
async def list_tasks(
    service: TaskServiceDependency,
    current_user: CurrentUser,
    limit: int = Query(default=20, ge=1, le=100, description="Maximum number of items to return."),
    offset: int = Query(default=0, ge=0, description="Number of items to skip."),
    is_active: bool | None = Query(
        default=None,
        description="Optional active state filter.",
    ),
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
    """List tasks for the authenticated user."""
    return await service.list_todos(
        owner_id=current_user.id,
        limit=limit,
        offset=offset,
        is_active=is_active,
        is_completed=is_completed,
        search=search,
    )


@router.get(
    "/{task_id}",
    response_model=TodoRead,
    summary="Get user task",
    description="Fetch a single task owned by the authenticated user.",
    response_description="Requested user task.",
    responses={
        status.HTTP_401_UNAUTHORIZED: auth_error_response(
            "Bearer token is missing, invalid, or expired."
        ),
        status.HTTP_403_FORBIDDEN: forbidden_error_response(
            "Task exists but belongs to another user.",
            "You do not have permission to access this todo.",
        ),
        status.HTTP_404_NOT_FOUND: not_found_error_response(
            "Task was not found.",
            "Todo '3fa85f64-5717-4562-b3fc-2c963f66afa6' was not found.",
        ),
    },
)
async def get_task(
    task_id: UUID,
    current_user: CurrentUser,
    service: TaskServiceDependency,
) -> TodoRead:
    """Fetch a task owned by the authenticated user."""
    return await service.get_todo(task_id, current_user.id)


@router.patch(
    "/{task_id}",
    response_model=TodoRead,
    summary="Update user task",
    description="Partially update a task owned by the authenticated user.",
    response_description="Updated user task.",
    responses={
        status.HTTP_401_UNAUTHORIZED: auth_error_response(
            "Bearer token is missing, invalid, or expired."
        ),
        status.HTTP_403_FORBIDDEN: forbidden_error_response(
            "Task exists but belongs to another user.",
            "You do not have permission to access this todo.",
        ),
        status.HTTP_404_NOT_FOUND: not_found_error_response(
            "Task was not found.",
            "Todo '3fa85f64-5717-4562-b3fc-2c963f66afa6' was not found.",
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: validation_error_response(
            "Task update payload validation failed."
        ),
    },
)
async def update_task(
    task_id: UUID,
    payload: TodoUpdate,
    current_user: CurrentUser,
    service: TaskServiceDependency,
) -> TodoRead:
    """Update a task owned by the authenticated user."""
    return await service.update_todo(task_id, current_user.id, payload)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user task",
    description="Delete a task owned by the authenticated user.",
    response_description="User task deleted successfully.",
    responses={
        status.HTTP_401_UNAUTHORIZED: auth_error_response(
            "Bearer token is missing, invalid, or expired."
        ),
        status.HTTP_403_FORBIDDEN: forbidden_error_response(
            "Task exists but belongs to another user.",
            "You do not have permission to access this todo.",
        ),
        status.HTTP_404_NOT_FOUND: not_found_error_response(
            "Task was not found.",
            "Todo '3fa85f64-5717-4562-b3fc-2c963f66afa6' was not found.",
        ),
    },
)
async def delete_task(
    task_id: UUID,
    current_user: CurrentUser,
    service: TaskServiceDependency,
) -> Response:
    """Delete a task owned by the authenticated user."""
    await service.delete_todo(task_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
