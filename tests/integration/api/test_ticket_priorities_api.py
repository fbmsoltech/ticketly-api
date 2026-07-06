import pytest
from fastapi.testclient import TestClient

from tests.integration.api._crud import assert_crud_contract

pytestmark = pytest.mark.integration


def test_ticket_priorities_crud_endpoints(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    assert_crud_contract(
        client,
        path="/api/v1/ticket-priorities",
        create_payload={"name": "High", "description": "High impact", "sort_order": 1},
        update_payload={"name": "Urgent"},
        updated_field="name",
        updated_value="Urgent",
        headers=admin_auth_headers,
    )
