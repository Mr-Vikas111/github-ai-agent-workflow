"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.db.session import dispose_engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Manage application startup and shutdown concerns."""
    configure_logging()
    yield
    await dispose_engine()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    register_exception_handlers(application)
    application.include_router(api_router, prefix="/api/v1")

    @application.get(
        "/health",
        tags=["health"],
        summary="Health check",
        description="Return a basic liveness probe response.",
    )
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
