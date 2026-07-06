import pytest
from fastapi.testclient import TestClient

from tests.integration.api._crud import assert_crud_contract

pytestmark = pytest.mark.integration


def test_ticket_statuses_crud_endpoints(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    assert_crud_contract(
        client,
        path="/api/v1/ticket-statuses",
        create_payload={"name": "Open", "description": "Open tickets", "sort_order": 1},
        update_payload={"sort_order": 2},
        updated_field="sort_order",
        updated_value=2,
        headers=admin_auth_headers,
    )
