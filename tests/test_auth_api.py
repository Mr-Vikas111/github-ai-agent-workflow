"""API tests for authentication endpoints."""

import pytest
from httpx import AsyncClient

from app.schemas.auth import UserRegister


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "full_name": "Example User",
            "password": "Str0ngPassw0rd!",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "user@example.com"
    assert body["full_name"] == "Example User"
    assert body["role"] == "user"
    assert body["is_active"] is True


@pytest.mark.asyncio
async def test_register_user_rejects_duplicate_email(client: AsyncClient) -> None:
    payload = {
        "email": "user@example.com",
        "full_name": "Example User",
        "password": "Str0ngPassw0rd!",
    }

    first_response = await client.post("/api/v1/auth/register", json=payload)
    second_response = await client.post("/api/v1/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_login_user_returns_access_token(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "user@example.com",
            "full_name": "Example User",
            "password": "Str0ngPassw0rd!",
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "Str0ngPassw0rd!"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


@pytest.mark.asyncio
async def test_login_user_rejects_invalid_credentials(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "Str0ngPassw0rd!"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_returns_authenticated_user(
    client: AsyncClient,
    fake_auth_service,
) -> None:
    user = await fake_auth_service.register_user(
        UserRegister(
            email="user@example.com",
            full_name="Example User",
            password="Str0ngPassw0rd!",
        )
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "Str0ngPassw0rd!"},
    )

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(user.id)


@pytest.mark.asyncio
async def test_inactive_user_cannot_login(
    client: AsyncClient,
    fake_auth_service,
) -> None:
    user = await fake_auth_service.register_user(
        UserRegister(
            email="user@example.com",
            full_name="Example User",
            password="Str0ngPassw0rd!",
        )
    )
    await fake_auth_service.deactivate_user(user.id)

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "Str0ngPassw0rd!"},
    )

    assert response.status_code == 403
