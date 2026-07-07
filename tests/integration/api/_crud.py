from typing import Any, cast

from fastapi.testclient import TestClient


def assert_crud_contract(
    client: TestClient,
    *,
    path: str,
    create_payload: dict[str, Any],
    update_payload: dict[str, Any],
    updated_field: str,
    updated_value: Any,
    headers: dict[str, str] | None = None,
) -> int:
    create_response = client.post(path, json=create_payload, headers=headers)
    assert create_response.status_code == 201
    created = create_response.json()
    entity_id = created["id"]

    list_response = client.get(path, headers=headers)
    assert list_response.status_code == 200
    assert entity_id in [item["id"] for item in list_response.json()]

    get_response = client.get(f"{path}/{entity_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["id"] == entity_id

    update_response = client.patch(
        f"{path}/{entity_id}",
        json=update_payload,
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()[updated_field] == updated_value

    missing_response = client.get(f"{path}/9999", headers=headers)
    assert missing_response.status_code == 404

    delete_response = client.delete(f"{path}/{entity_id}", headers=headers)
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    deleted_response = client.get(f"{path}/{entity_id}", headers=headers)
    assert deleted_response.status_code == 404
    return cast(int, entity_id)
