"""API tests for todo CRUD endpoints."""

from uuid import uuid4

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient, auth_identity) -> None:
    user, headers = await auth_identity()

    response = await client.post(
        "/api/v1/todos",
        json={
            "title": "Write tests",
            "description": "Cover the CRUD routes",
            "is_completed": False,
        },
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["description"] == "Cover the CRUD routes"
    assert body["is_completed"] is False
    assert body["is_active"] is True
    assert body["owner_id"] == str(user.id)
    assert body["id"]


@pytest.mark.asyncio
async def test_list_todos_supports_filtering_and_pagination(
    client: AsyncClient,
    auth_identity,
) -> None:
    _, headers = await auth_identity()
    _, other_headers = await auth_identity(email="other@example.com")

    await client.post(
        "/api/v1/todos",
        json={"title": "Ship API", "description": "first", "is_completed": False},
        headers=headers,
    )
    await client.post(
        "/api/v1/todos",
        json={"title": "Archive docs", "description": "second", "is_completed": True},
        headers=headers,
    )
    await client.post(
        "/api/v1/todos",
        json={"title": "Other user", "description": "third", "is_completed": True},
        headers=other_headers,
    )

    response = await client.get(
        "/api/v1/todos",
        params={"is_completed": True, "limit": 10, "offset": 0},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["items"][0]["title"] == "Archive docs"


@pytest.mark.asyncio
async def test_list_todos_supports_active_filter(client: AsyncClient, auth_identity) -> None:
    _, headers = await auth_identity()

    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Make inactive", "description": None, "is_completed": False},
        headers=headers,
    )
    todo_id = create_response.json()["id"]
    await client.patch(f"/api/v1/todos/{todo_id}/inactive", headers=headers)

    response = await client.get(
        "/api/v1/todos",
        params={"is_active": False, "limit": 10, "offset": 0},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == todo_id
    assert body["items"][0]["is_active"] is False


@pytest.mark.asyncio
async def test_get_todo_returns_resource(client: AsyncClient, auth_identity) -> None:
    _, headers = await auth_identity()

    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Fetch todo", "description": None, "is_completed": False},
        headers=headers,
    )
    todo_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/todos/{todo_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == todo_id


@pytest.mark.asyncio
async def test_inactivate_todo_marks_resource_inactive(client: AsyncClient, auth_identity) -> None:
    _, headers = await auth_identity()

    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Deactivate me", "description": None, "is_completed": False},
        headers=headers,
    )
    todo_id = create_response.json()["id"]

    response = await client.patch(f"/api/v1/todos/{todo_id}/inactive", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert response.json()["is_active"] is False


@pytest.mark.asyncio
async def test_update_todo_applies_partial_changes(client: AsyncClient, auth_identity) -> None:
    _, headers = await auth_identity()

    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Before", "description": "Original", "is_completed": False},
        headers=headers,
    )
    todo_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"title": "After", "is_completed": True},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "After"
    assert body["description"] == "Original"
    assert body["is_completed"] is True


@pytest.mark.asyncio
async def test_delete_todo_returns_no_content(client: AsyncClient, auth_identity) -> None:
    _, headers = await auth_identity()

    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Delete me", "description": None, "is_completed": False},
        headers=headers,
    )
    todo_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/todos/{todo_id}", headers=headers)
    missing_response = await client.get(f"/api/v1/todos/{todo_id}", headers=headers)

    assert response.status_code == 204
    assert missing_response.status_code == 404


@pytest.mark.asyncio
async def test_missing_todo_returns_not_found(client: AsyncClient, auth_identity) -> None:
    _, headers = await auth_identity()
    response = await client.get(f"/api/v1/todos/{uuid4()}", headers=headers)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_todo_endpoints_require_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/todos")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_cannot_access_another_users_todo(client: AsyncClient, auth_identity) -> None:
    _, owner_headers = await auth_identity()
    _, other_headers = await auth_identity(email="other@example.com")

    create_response = await client.post(
        "/api/v1/todos",
        json={"title": "Private todo", "description": None, "is_completed": False},
        headers=owner_headers,
    )
    todo_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/todos/{todo_id}", headers=other_headers)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_task_for_authenticated_user(client: AsyncClient, auth_identity) -> None:
    user, headers = await auth_identity()

    response = await client.post(
        "/api/v1/users/me/tasks",
        json={"title": "My task", "description": "Owned by current user", "is_completed": False},
        headers=headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "My task"
    assert body["owner_id"] == str(user.id)


@pytest.mark.asyncio
async def test_list_user_tasks_only_returns_current_user_items(
    client: AsyncClient,
    auth_identity,
) -> None:
    _, headers = await auth_identity()
    _, other_headers = await auth_identity(email="other@example.com")

    await client.post(
        "/api/v1/users/me/tasks",
        json={"title": "Mine", "description": None, "is_completed": False},
        headers=headers,
    )
    await client.post(
        "/api/v1/users/me/tasks",
        json={"title": "Not mine", "description": None, "is_completed": False},
        headers=other_headers,
    )

    response = await client.get("/api/v1/users/me/tasks", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["title"] == "Mine"


@pytest.mark.asyncio
async def test_update_and_delete_user_task(client: AsyncClient, auth_identity) -> None:
    _, headers = await auth_identity()

    create_response = await client.post(
        "/api/v1/users/me/tasks",
        json={"title": "Before", "description": "Task description", "is_completed": False},
        headers=headers,
    )
    task_id = create_response.json()["id"]

    update_response = await client.patch(
        f"/api/v1/users/me/tasks/{task_id}",
        json={"title": "After", "is_completed": True},
        headers=headers,
    )
    delete_response = await client.delete(f"/api/v1/users/me/tasks/{task_id}", headers=headers)
    missing_response = await client.get(f"/api/v1/users/me/tasks/{task_id}", headers=headers)

    assert update_response.status_code == 200
    assert update_response.json()["title"] == "After"
    assert update_response.json()["is_completed"] is True
    assert delete_response.status_code == 204
    assert missing_response.status_code == 404
