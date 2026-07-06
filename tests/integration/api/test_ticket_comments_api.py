import pytest
from fastapi.testclient import TestClient

from app.models.customer import Customer
from app.models.ticket_category import TicketCategory
from app.models.ticket_priority import TicketPriority
from app.models.ticket_status import TicketStatus
from app.models.user import User
from tests.integration.api._crud import assert_crud_contract

pytestmark = pytest.mark.integration


def test_ticket_comments_crud_endpoints(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
    agent_user: User,
) -> None:
    ticket = client.post(
        "/api/v1/tickets",
        json={
            "customer_id": customer.id,
            "assignee_id": agent_user.id,
            "category_id": ticket_category.id,
            "status_id": ticket_status.id,
            "priority_id": ticket_priority.id,
            "title": "Email issue",
            "description": "Emails are delayed.",
        },
        headers=admin_auth_headers,
    ).json()

    assert_crud_contract(
        client,
        path="/api/v1/ticket-comments",
        create_payload={
            "ticket_id": ticket["id"],
            "author_id": agent_user.id,
            "body": "We are checking this.",
            "is_internal": False,
        },
        update_payload={"body": "We fixed this."},
        updated_field="body",
        updated_value="We fixed this.",
    )
