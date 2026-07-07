import pytest
from fastapi.testclient import TestClient

from app.models.role import Role
from tests.integration.api._crud import assert_crud_contract

pytestmark = pytest.mark.integration


def test_customers_crud_endpoints(
    client: TestClient,
    admin_auth_headers: dict[str, str],
    agent_role: Role,
) -> None:
    customer_user = client.post(
        "/api/v1/users",
        json={
            "role_id": agent_role.id,
            "name": "Customer User",
            "email": "customer-crud@example.com",
            "password": "secret123",
            "is_active": True,
        },
        headers=admin_auth_headers,
    ).json()

    assert_crud_contract(
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
        headers=admin_auth_headers,
    )
