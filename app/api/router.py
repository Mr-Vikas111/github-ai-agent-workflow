"""API router configuration."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.todos import router as todos_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(tasks_router, prefix="/users/me/tasks", tags=["tasks"])
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])
