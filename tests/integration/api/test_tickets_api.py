from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.models.customer import Customer
from app.models.ticket import Ticket
from app.models.ticket_category import TicketCategory
from app.models.ticket_priority import TicketPriority
from app.models.ticket_status import TicketStatus
from app.models.user import User

pytestmark = pytest.mark.integration


def _ticket_payload(
    *,
    customer: Customer,
    category: TicketCategory,
    status: TicketStatus,
    priority: TicketPriority,
    assigned_agent: User | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": "Cannot access dashboard",
        "description": "The dashboard returns an error.",
        "customer_id": customer.id,
        "category_id": category.id,
        "status_id": status.id,
        "priority_id": priority.id,
    }
    if assigned_agent is not None:
        payload["assigned_agent_id"] = assigned_agent.id
    return payload


def test_admin_creates_ticket_successfully(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
) -> None:
    response = client.post(
        "/api/v1/tickets",
        headers=admin_auth_headers,
        json=_ticket_payload(
            customer=customer,
            category=ticket_category,
            status=ticket_status,
            priority=ticket_priority,
        ),
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Cannot access dashboard"


def test_agent_creates_ticket_successfully(
    client: TestClient,
    agent_auth_headers: dict[str, str],
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
) -> None:
    response = client.post(
        "/api/v1/tickets",
        headers=agent_auth_headers,
        json=_ticket_payload(
            customer=customer,
            category=ticket_category,
            status=ticket_status,
            priority=ticket_priority,
        ),
    )

    assert response.status_code == 201


def test_ticket_without_token_receives_401(client: TestClient) -> None:
    response = client.get("/api/v1/tickets")

    assert response.status_code == 401


def test_customer_cannot_create_ticket(
    client: TestClient,
    customer_auth_headers: dict[str, str],
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
) -> None:
    response = client.post(
        "/api/v1/tickets",
        headers=customer_auth_headers,
        json=_ticket_payload(
            customer=customer,
            category=ticket_category,
            status=ticket_status,
            priority=ticket_priority,
        ),
    )

    assert response.status_code == 403


def test_admin_lists_tickets(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    response = client.get("/api/v1/tickets", headers=admin_auth_headers)

    assert response.status_code == 200
    assert ticket.id in [item["id"] for item in response.json()]


def test_admin_filters_tickets(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    response = client.get(
        f"/api/v1/tickets?customer_id={ticket.customer_id}&status_id={ticket.status_id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [ticket.id]


def test_gets_ticket_by_id(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    response = client.get(f"/api/v1/tickets/{ticket.id}", headers=admin_auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == ticket.id


def test_updates_ticket(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    response = client.patch(
        f"/api/v1/tickets/{ticket.id}",
        headers=admin_auth_headers,
        json={"title": "Cannot access reports"},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Cannot access reports"


def test_assigns_ticket_to_agent(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
    agent_user: User,
) -> None:
    response = client.patch(
        f"/api/v1/tickets/{ticket.id}",
        headers=admin_auth_headers,
        json={"assigned_agent_id": agent_user.id},
    )

    assert response.status_code == 200
    assert response.json()["assigned_agent_id"] == agent_user.id


def test_admin_deletes_ticket(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    response = client.delete(
        f"/api/v1/tickets/{ticket.id}",
        headers=admin_auth_headers,
    )

    assert response.status_code == 204


def test_agent_cannot_delete_ticket(
    client: TestClient,
    agent_auth_headers: dict[str, str],
    ticket: Ticket,
) -> None:
    response = client.delete(
        f"/api/v1/tickets/{ticket.id}",
        headers=agent_auth_headers,
    )

    assert response.status_code == 403


def test_create_ticket_with_missing_relation_returns_404(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_priority: TicketPriority,
) -> None:
    response = client.post(
        "/api/v1/tickets",
        headers=admin_auth_headers,
        json={
            "title": "Missing status",
            "description": "Status does not exist.",
            "customer_id": customer.id,
            "category_id": ticket_category.id,
            "status_id": 9999,
            "priority_id": ticket_priority.id,
        },
    )

    assert response.status_code == 404


def test_assign_ticket_to_user_without_role_returns_400(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    ticket: Ticket,
    customer_user: User,
) -> None:
    response = client.patch(
        f"/api/v1/tickets/{ticket.id}",
        headers=admin_auth_headers,
        json={"assigned_agent_id": customer_user.id},
    )

    assert response.status_code == 400
