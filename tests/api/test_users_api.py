from fastapi.testclient import TestClient

from app.models.role import Role
from app.models.user import User


def test_admin_creates_user(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    customer_role: Role,
) -> None:
    response = client.post(
        "/api/v1/users",
        headers=admin_auth_headers,
        json={
            "role_id": customer_role.id,
            "name": "Customer User",
            "email": "new-customer@example.com",
            "password": "secret123",
            "is_active": True,
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new-customer@example.com"
    assert "hashed_password" not in body


def test_admin_lists_users(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    admin_user: User,
) -> None:
    response = client.get("/api/v1/users", headers=admin_auth_headers)

    assert response.status_code == 200
    assert response.json()


def test_admin_gets_user_by_id(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    admin_user: User,
) -> None:
    response = client.get(
        f"/api/v1/users/{admin_user.id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == admin_user.id


def test_admin_updates_user(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    admin_user: User,
) -> None:
    response = client.patch(
        f"/api/v1/users/{admin_user.id}",
        headers=admin_auth_headers,
        json={"name": "Updated Admin"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Admin"


def test_admin_removes_user(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    agent_user: User,
) -> None:
    response = client.delete(
        f"/api/v1/users/{agent_user.id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204


def test_user_without_token_receives_401(client: TestClient) -> None:
    response = client.get("/api/v1/users")

    assert response.status_code == 401


def test_user_without_admin_role_receives_403(
    client: TestClient,
    agent_auth_headers: dict[str, str],
) -> None:
    response = client.get("/api/v1/users", headers=agent_auth_headers)

    assert response.status_code == 403


def test_duplicate_user_creation_returns_409(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    admin_role: Role,
) -> None:
    payload = {
        "role_id": admin_role.id,
        "name": "Duplicate User",
        "email": "duplicate-api@example.com",
        "password": "secret123",
        "is_active": True,
    }
    assert (
        client.post(
            "/api/v1/users",
            headers=admin_auth_headers,
            json=payload,
        ).status_code
        == 201
    )

    response = client.post(
        "/api/v1/users",
        headers=admin_auth_headers,
        json=payload,
    )

    assert response.status_code == 409


def test_missing_user_returns_404(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    response = client.get("/api/v1/users/9999", headers=admin_auth_headers)

    assert response.status_code == 404
