"""Application configuration."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="Todo Service", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/todo_db",
        alias="DATABASE_URL",
    )

    @property
    def sync_database_url(self) -> str:
        """Return a synchronous PostgreSQL URL for Alembic operations."""
        return self.database_url.replace("+asyncpg", "+psycopg", 1)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
