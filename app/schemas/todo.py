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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Ship FastAPI CRUD service",
                "description": "Finish the first production-ready todo API.",
                "is_completed": False,
            }
        }
    )


class TodoUpdate(BaseModel):
    """Payload for partially updating a todo."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Ship updated FastAPI CRUD service",
                "description": "Todo API updated with owner-scoped access.",
                "is_completed": True,
            }
        }
    )

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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "owner_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "title": "Ship FastAPI CRUD service",
                "description": "Finish the first production-ready todo API.",
                "is_completed": False,
                "is_active": True,
                "created_at": "2026-05-04T11:00:00Z",
                "updated_at": "2026-05-04T11:00:00Z",
            }
        },
    )

    id: UUID
    owner_id: UUID | None = Field(examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"])
    is_active: bool = Field(examples=[True])
    created_at: datetime
    updated_at: datetime


class TodoListResponse(BaseModel):
    """Paginated todo response."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "owner_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                        "title": "Ship FastAPI CRUD service",
                        "description": "Finish the first production-ready todo API.",
                        "is_completed": False,
                        "is_active": True,
                        "created_at": "2026-05-04T11:00:00Z",
                        "updated_at": "2026-05-04T11:00:00Z",
                    }
                ],
                "total": 1,
                "limit": 20,
                "offset": 0,
            }
        }
    )

    items: list[TodoRead]
    total: int = Field(examples=[1])
    limit: int = Field(examples=[20])
    offset: int = Field(examples=[0])
