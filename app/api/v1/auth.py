"""Authentication API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import CurrentUser, get_auth_service
from app.api.docs import (
    auth_error_response,
    conflict_error_response,
    validation_error_response,
)
from app.schemas.auth import TokenResponse, UserLogin, UserRead, UserRegister
from app.schemas.common import ErrorResponse
from app.services.auth import AuthService

router = APIRouter()
AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    description="Create a new user account with a bcrypt-hashed password.",
    response_description="Registered user profile.",
    responses={
        status.HTTP_409_CONFLICT: conflict_error_response(
            "A user with the email address already exists.",
            "User 'user@example.com' already exists.",
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: validation_error_response(
            "Registration payload validation failed."
        ),
    },
)
async def register_user(
    payload: UserRegister,
    service: AuthServiceDependency,
) -> UserRead:
    """Register a new user account."""
    return await service.register_user(payload)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate a user and issue a JWT bearer access token.",
    response_description="JWT access token for authenticated requests.",
    responses={
        status.HTTP_401_UNAUTHORIZED: auth_error_response(
            "Invalid email, password, or token state.",
            "Invalid email or password.",
        ),
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "User exists but is inactive.",
            "content": {"application/json": {"example": {"detail": "User account is inactive."}}},
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: validation_error_response(
            "Login payload validation failed."
        ),
    },
)
async def login_user(
    payload: UserLogin,
    service: AuthServiceDependency,
) -> TokenResponse:
    """Authenticate a user and return a JWT access token."""
    return await service.login_user(payload)


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user",
    description="Return the authenticated user associated with the bearer token.",
    response_description="Authenticated user profile.",
    responses={
        status.HTTP_401_UNAUTHORIZED: auth_error_response(
            "Bearer token is missing, invalid, or expired."
        ),
        status.HTTP_403_FORBIDDEN: {
            "model": ErrorResponse,
            "description": "User is authenticated but inactive.",
            "content": {"application/json": {"example": {"detail": "User account is inactive."}}},
        },
    },
)
async def get_me(current_user: CurrentUser) -> UserRead:
    """Return the currently authenticated user."""
    return current_user
