import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_liveness_returns_200(client: TestClient) -> None:
    response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["components"]["app"]["status"] == "ok"
    assert "database" not in data["components"]


def test_health_returns_application_status(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Ticketly API"
    assert data["status"] == "ok"
    assert data["components"]["app"]["status"] == "ok"


def test_readiness_checks_database(client: TestClient) -> None:
    response = client.get("/api/v1/health/ready")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["components"]["database"]["status"] == "ok"
