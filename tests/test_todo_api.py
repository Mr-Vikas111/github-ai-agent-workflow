"""API tests for todo CRUD endpoints."""

from uuid import uuid4

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/todos",
        json={
            "title": "Write tests",
            "description": "Cover the CRUD routes",
            "is_completed": False,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["description"] == "Cover the CRUD routes"
    assert body["is_completed"] is False
    assert body["id"]


@pytest.mark.asyncio
async def test_list_todos_supports_filtering_and_pagination(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/todos",
        json={"title": "Ship API", "description": "first", "is_completed": False},
    )
    await client.post(
        "/api/v1/todos",
        json={"title": "Archive docs", "description": "second", "is_completed": True},
    )

    response = await client.get(
        "/api/v1/todos",
        params={"is_completed": True, "limit": 10, "offset": 0},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "Archive docs"


@pytest.mark.asyncio
async def test_get_todo_returns_resource(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Fetch todo", "description": None, "is_completed": False},
    )
    todo_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/todos/{todo_id}")

    assert response.status_code == 200
    assert response.json()["id"] == todo_id


@pytest.mark.asyncio
async def test_update_todo_applies_partial_changes(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Before", "description": "Original", "is_completed": False},
    )
    todo_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"title": "After", "is_completed": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "After"
    assert body["description"] == "Original"
    assert body["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_todo_returns_no_content(client: AsyncClient) -> None:
    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Delete me", "description": None, "is_completed": False},
    )
    todo_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/todos/{todo_id}")
    missing_response = await client.get(f"/api/v1/todos/{todo_id}")

    assert response.status_code == 204
    assert missing_response.status_code == 404


@pytest.mark.asyncio
async def test_missing_todo_returns_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/todos/{uuid4()}")

    assert response.status_code == 404
