import pytest
from fastapi.testclient import TestClient

from app.models.user import User

pytestmark = pytest.mark.integration


def test_login_returns_access_token(
    client: TestClient,
    admin_user: User,
) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "admin123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_with_invalid_credentials_returns_401(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "wrongsecret"},
    )

    assert response.status_code == 401


def test_me_with_valid_token_returns_current_user(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    response = client.get("/api/v1/auth/me", headers=admin_auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "admin@example.com"
    assert body["role_name"] == "ADMIN"
    assert "hashed_password" not in body


def test_me_without_token_returns_401(client: TestClient) -> None:
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_me_with_invalid_token_returns_401(client: TestClient) -> None:
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
