"""Security helpers for password hashing and JWT handling."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from jwt import InvalidTokenError
from pydantic import ValidationError

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.schemas.auth import TokenPayload


def hash_password(password: str) -> str:
    """Hash a plaintext password with bcrypt."""
    password_bytes = password.encode("utf-8")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_access_token(*, subject: str, role: str) -> str:
    """Create a signed JWT access token."""
    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "role": role, "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> TokenPayload:
    """Decode and validate a JWT access token."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return TokenPayload.model_validate(payload)
    except (InvalidTokenError, ValidationError) as exc:
        raise AuthenticationError("Invalid or expired authentication token.") from exc
