import pytest
from fastapi.testclient import TestClient

from app.observability.metrics import metrics_collector

pytestmark = pytest.mark.integration


def test_metrics_returns_snapshot(client: TestClient) -> None:
    metrics_collector.reset()

    response = client.get("/api/v1/metrics")

    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "uptime_seconds" in data


def test_metrics_reflect_requests_after_endpoint_call(client: TestClient) -> None:
    metrics_collector.reset()

    client.get("/api/v1/health/live")
    response = client.get("/api/v1/metrics")

    assert response.status_code == 200
    data = response.json()
    assert data["total_requests"] >= 1
    assert data["requests_by_method"]["GET"] >= 1
