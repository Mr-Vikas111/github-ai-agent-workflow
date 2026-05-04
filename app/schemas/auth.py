"""Authentication request and response schemas."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    """Supported application roles."""

    USER = "user"
    ADMIN = "admin"


class UserRegister(BaseModel):
    """Payload for user registration."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "full_name": "Example User",
                "password": "Str0ngPassw0rd!",
            }
        }
    )

    email: EmailStr = Field(examples=["user@example.com"])
    full_name: str = Field(min_length=1, max_length=255, examples=["Example User"])
    password: str = Field(min_length=8, max_length=128, examples=["Str0ngPassw0rd!"])


class UserLogin(BaseModel):
    """Payload for user login."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "Str0ngPassw0rd!",
            }
        }
    )

    email: EmailStr = Field(examples=["user@example.com"])
    password: str = Field(min_length=8, max_length=128, examples=["Str0ngPassw0rd!"])


class UserRead(BaseModel):
    """Safe user response model."""

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "email": "user@example.com",
                "full_name": "Example User",
                "role": "user",
                "is_active": True,
                "created_at": "2026-05-04T10:30:00Z",
                "updated_at": "2026-05-04T10:30:00Z",
            }
        },
    )

    id: UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    """JWT token response."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example",
                "token_type": "bearer",
            }
        }
    )

    access_token: str
    token_type: str = Field(default="bearer", examples=["bearer"])


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    sub: UUID
    role: UserRole
    exp: int
