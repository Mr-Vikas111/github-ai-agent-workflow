"""Todo request and response schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):
    """Shared todo attributes."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["Ship FastAPI CRUD service"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        examples=["Create a production-ready todo API with pagination."],
    )
    is_completed: bool = Field(default=False, examples=[False])


class TodoCreate(TodoBase):
    """Payload for creating a todo."""


class TodoUpdate(BaseModel):
    """Payload for partially updating a todo."""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["Updated title"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        examples=["Updated description"],
    )
    is_completed: bool | None = Field(default=None, examples=[True])


class TodoRead(TodoBase):
    """Todo API response model."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


class TodoListResponse(BaseModel):
    """Paginated todo response."""

    items: list[TodoRead]
    total: int = Field(examples=[1])
    limit: int = Field(examples=[20])
    offset: int = Field(examples=[0])
