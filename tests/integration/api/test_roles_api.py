import pytest
from fastapi.testclient import TestClient

from tests.integration.api._crud import assert_crud_contract

pytestmark = pytest.mark.integration


def test_roles_crud_endpoints(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    assert_crud_contract(
        client,
        path="/api/v1/roles",
        create_payload={"name": "MANAGER", "description": "Managers"},
        update_payload={"description": "Platform administrators"},
        updated_field="description",
        updated_value="Platform administrators",
        headers=admin_auth_headers,
    )
