import pytest
from fastapi.testclient import TestClient

from app.models.ticket import Ticket
from app.models.user import User

pytestmark = pytest.mark.integration


def _create_comment(
    client: TestClient,
    ticket_id: int,
    headers: dict[str, str],
    *,
    content: str = "We are checking this.",
    is_internal: bool = False,
) -> dict[str, object]:
    response = client.post(
        f"/api/v1/tickets/{ticket_id}/comments",
        json={"content": content, "is_internal": is_internal},
        headers=headers,
    )
    assert response.status_code == 201
    body: dict[str, object] = response.json()
    return body


def test_admin_creates_ticket_comment(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    admin_user: User,
    ticket: Ticket,
) -> None:
    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments",
        json={"content": "Admin comment.", "is_internal": True},
        headers=admin_auth_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["ticket_id"] == ticket.id
    assert body["author_user_id"] == admin_user.id
    assert body["author_customer_id"] is None
    assert body["content"] == "Admin comment."
    assert body["is_internal"] is True


def test_agent_creates_ticket_comment(
    client: TestClient,
    agent_auth_headers: dict[str, str],
    agent_user: User,
    ticket: Ticket,
) -> None:
    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments",
        json={"content": "Agent comment."},
        headers=agent_auth_headers,
    )

    assert response.status_code == 201
    body = response.json()
    assert body["author_user_id"] == agent_user.id
    assert body["content"] == "Agent comment."


def test_create_ticket_comment_without_token_returns_401(
    client: TestClient,
    ticket: Ticket,
) -> None:
    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments",
        json={"content": "Unauthorized comment."},
    )

    assert response.status_code == 401


def test_customer_cannot_create_ticket_comment(
    client: TestClient,
    customer_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments",
        json={"content": "Customer comment."},
        headers=customer_auth_headers,
    )

    assert response.status_code == 403


def test_list_ticket_comments(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    created = _create_comment(client, ticket.id, admin_auth_headers)

    response = client.get(
        f"/api/v1/tickets/{ticket.id}/comments",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == [created]


def test_list_ticket_comments_excludes_internal_when_requested(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    public = _create_comment(
        client,
        ticket.id,
        admin_auth_headers,
        content="Public note.",
        is_internal=False,
    )
    _create_comment(
        client,
        ticket.id,
        admin_auth_headers,
        content="Internal note.",
        is_internal=True,
    )

    response = client.get(
        f"/api/v1/tickets/{ticket.id}/comments?include_internal=false",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == [public]


def test_get_ticket_comment_by_id(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    created = _create_comment(client, ticket.id, admin_auth_headers)

    response = client.get(
        f"/api/v1/tickets/{ticket.id}/comments/{created['id']}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == created


def test_update_ticket_comment(
    client: TestClient,
    agent_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    created = _create_comment(client, ticket.id, agent_auth_headers)

    response = client.patch(
        f"/api/v1/tickets/{ticket.id}/comments/{created['id']}",
        json={"content": "Updated comment.", "is_internal": True},
        headers=agent_auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["content"] == "Updated comment."
    assert body["is_internal"] is True


def test_admin_deletes_ticket_comment(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    created = _create_comment(client, ticket.id, admin_auth_headers)

    response = client.delete(
        f"/api/v1/tickets/{ticket.id}/comments/{created['id']}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204


def test_agent_cannot_delete_ticket_comment(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    agent_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    created = _create_comment(client, ticket.id, admin_auth_headers)

    response = client.delete(
        f"/api/v1/tickets/{ticket.id}/comments/{created['id']}",
        headers=agent_auth_headers,
    )

    assert response.status_code == 403


def test_create_ticket_comment_for_missing_ticket_returns_404(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/tickets/999/comments",
        json={"content": "Missing ticket."},
        headers=admin_auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found."


def test_created_comment_uses_authenticated_user_as_author(
    client: TestClient,
    agent_auth_headers: dict[str, str],
    agent_user: User,
    ticket: Ticket,
) -> None:
    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments",
        json={"content": "Authenticated author."},
        headers=agent_auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["author_user_id"] == agent_user.id


def test_body_cannot_override_comment_author(
    client: TestClient,
    agent_auth_headers: dict[str, str],
    admin_user: User,
    agent_user: User,
    ticket: Ticket,
) -> None:
    response = client.post(
        f"/api/v1/tickets/{ticket.id}/comments",
        json={
            "content": "Attempted author override.",
            "author_user_id": admin_user.id,
            "author_id": admin_user.id,
        },
        headers=agent_auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["author_user_id"] == agent_user.id
