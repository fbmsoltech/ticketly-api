from typing import Any, cast

from fastapi.testclient import TestClient


def _assert_crud_contract(
    client: TestClient,
    *,
    path: str,
    create_payload: dict[str, Any],
    update_payload: dict[str, Any],
    updated_field: str,
    updated_value: Any,
) -> int:
    create_response = client.post(path, json=create_payload)
    assert create_response.status_code == 201
    created = create_response.json()
    entity_id = created["id"]

    list_response = client.get(path)
    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [entity_id]

    get_response = client.get(f"{path}/{entity_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == entity_id

    update_response = client.patch(f"{path}/{entity_id}", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()[updated_field] == updated_value

    missing_response = client.get(f"{path}/9999")
    assert missing_response.status_code == 404

    delete_response = client.delete(f"{path}/{entity_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    deleted_response = client.get(f"{path}/{entity_id}")
    assert deleted_response.status_code == 404
    return cast(int, entity_id)


def test_lookup_entity_crud_endpoints(client: TestClient) -> None:
    _assert_crud_contract(
        client,
        path="/api/v1/roles",
        create_payload={"name": "ADMIN", "description": "Administrators"},
        update_payload={"description": "Platform administrators"},
        updated_field="description",
        updated_value="Platform administrators",
    )
    _assert_crud_contract(
        client,
        path="/api/v1/ticket-statuses",
        create_payload={"name": "Open", "description": "Open tickets", "sort_order": 1},
        update_payload={"sort_order": 2},
        updated_field="sort_order",
        updated_value=2,
    )
    _assert_crud_contract(
        client,
        path="/api/v1/ticket-priorities",
        create_payload={"name": "High", "description": "High impact", "sort_order": 1},
        update_payload={"name": "Urgent"},
        updated_field="name",
        updated_value="Urgent",
    )
    _assert_crud_contract(
        client,
        path="/api/v1/ticket-categories",
        create_payload={
            "name": "Billing",
            "description": "Billing issues",
            "is_active": True,
        },
        update_payload={"is_active": False},
        updated_field="is_active",
        updated_value=False,
    )


def test_user_customer_ticket_and_comment_crud_endpoints(
    client: TestClient,
) -> None:
    role = client.post(
        "/api/v1/roles",
        json={"name": "AGENT", "description": "Support agents"},
    ).json()

    _assert_crud_contract(
        client,
        path="/api/v1/users",
        create_payload={
            "role_id": role["id"],
            "name": "Jane Agent",
            "email": "jane@example.com",
            "password": "secret123",
            "is_active": True,
        },
        update_payload={"name": "Jane Support"},
        updated_field="name",
        updated_value="Jane Support",
    )

    assignee = client.post(
        "/api/v1/users",
        json={
            "role_id": role["id"],
            "name": "Ticket Assignee",
            "email": "ticket-assignee@example.com",
            "password": "secret123",
            "is_active": True,
        },
    ).json()

    customer_user = client.post(
        "/api/v1/users",
        json={
            "role_id": role["id"],
            "name": "Customer User",
            "email": "customer@example.com",
            "password": "secret123",
            "is_active": True,
        },
    ).json()
    _assert_crud_contract(
        client,
        path="/api/v1/customers",
        create_payload={
            "user_id": customer_user["id"],
            "company_name": "Acme Inc.",
            "phone": "+55 11 99999-0000",
        },
        update_payload={"phone": "+55 11 98888-0000"},
        updated_field="phone",
        updated_value="+55 11 98888-0000",
    )

    ticket_user = client.post(
        "/api/v1/users",
        json={
            "role_id": role["id"],
            "name": "Ticket Customer",
            "email": "ticket-customer@example.com",
            "password": "secret123",
            "is_active": True,
        },
    ).json()
    ticket_customer = client.post(
        "/api/v1/customers",
        json={"user_id": ticket_user["id"], "company_name": "Ticket Co."},
    ).json()
    status = client.post(
        "/api/v1/ticket-statuses",
        json={"name": "Open", "description": "Open tickets", "sort_order": 1},
    ).json()
    priority = client.post(
        "/api/v1/ticket-priorities",
        json={"name": "High", "description": "High impact", "sort_order": 1},
    ).json()
    category = client.post(
        "/api/v1/ticket-categories",
        json={"name": "Support", "description": "Support issues", "is_active": True},
    ).json()

    _assert_crud_contract(
        client,
        path="/api/v1/tickets",
        create_payload={
            "customer_id": ticket_customer["id"],
            "assignee_id": assignee["id"],
            "category_id": category["id"],
            "status_id": status["id"],
            "priority_id": priority["id"],
            "title": "Cannot access dashboard",
            "description": "The dashboard returns an error.",
        },
        update_payload={"title": "Cannot access reports"},
        updated_field="title",
        updated_value="Cannot access reports",
    )

    comment_ticket = client.post(
        "/api/v1/tickets",
        json={
            "customer_id": ticket_customer["id"],
            "assignee_id": assignee["id"],
            "category_id": category["id"],
            "status_id": status["id"],
            "priority_id": priority["id"],
            "title": "Email issue",
            "description": "Emails are delayed.",
        },
    ).json()
    _assert_crud_contract(
        client,
        path="/api/v1/ticket-comments",
        create_payload={
            "ticket_id": comment_ticket["id"],
            "author_id": assignee["id"],
            "body": "We are checking this.",
            "is_internal": False,
        },
        update_payload={"body": "We fixed this."},
        updated_field="body",
        updated_value="We fixed this.",
    )
