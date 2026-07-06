import pytest
from fastapi.testclient import TestClient

from tests.integration.api._crud import assert_crud_contract

pytestmark = pytest.mark.integration


def test_ticket_categories_crud_endpoints(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    assert_crud_contract(
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
        headers=admin_auth_headers,
    )
