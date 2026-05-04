"""Reusable OpenAPI response helpers."""


from app.schemas.common import ErrorResponse, ValidationErrorResponse


def auth_error_response(
    description: str,
    detail: str = "Bearer token is missing, invalid, or expired.",
) -> dict:
    """Return a documented authentication error response."""
    return {
        "model": ErrorResponse,
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
        "headers": {"WWW-Authenticate": {"schema": {"type": "string"}, "example": "Bearer"}},
    }


def forbidden_error_response(description: str, detail: str) -> dict:
    """Return a documented authorization error response."""
    return {
        "model": ErrorResponse,
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


def not_found_error_response(description: str, detail: str) -> dict:
    """Return a documented not-found error response."""
    return {
        "model": ErrorResponse,
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


def conflict_error_response(description: str, detail: str) -> dict:
    """Return a documented conflict error response."""
    return {
        "model": ErrorResponse,
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


def validation_error_response(description: str) -> dict:
    """Return a documented validation error response."""
    return {
        "model": ValidationErrorResponse,
        "description": description,
    }
