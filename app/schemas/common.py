"""Shared OpenAPI response schemas."""

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    """Standard API error response."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Bearer token is missing, invalid, or expired.",
            }
        }
    )

    detail: str = Field(examples=["Resource was not found."])


class ValidationErrorItem(BaseModel):
    """Single validation error item."""

    loc: list[str | int] = Field(examples=[["body", "email"]])
    msg: str = Field(examples=["value is not a valid email address"])
    type: str = Field(examples=["value_error"])


class ValidationErrorResponse(BaseModel):
    """Validation error response payload."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error",
                    }
                ]
            }
        }
    )

    detail: list[ValidationErrorItem]


class HealthResponse(BaseModel):
    """Health check response."""

    model_config = ConfigDict(json_schema_extra={"example": {"status": "ok"}})

    status: str = Field(examples=["ok"])
