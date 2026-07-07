import pytest

from app.observability.metrics import MetricsCollector

pytestmark = pytest.mark.unit


def test_collector_starts_with_zero_requests() -> None:
    collector = MetricsCollector()

    snapshot = collector.snapshot()

    assert snapshot["total_requests"] == 0
    assert snapshot["requests_by_method"] == {}
    assert snapshot["responses_by_status_code"] == {}
    assert snapshot["total_5xx_errors"] == 0
    assert snapshot["last_request_duration_ms"] is None


def test_record_request_increments_total_method_and_status_code() -> None:
    collector = MetricsCollector()

    collector.record_request("get", 200, 12.5)

    snapshot = collector.snapshot()
    assert snapshot["total_requests"] == 1
    assert snapshot["requests_by_method"] == {"GET": 1}
    assert snapshot["responses_by_status_code"] == {"200": 1}
    assert snapshot["last_request_duration_ms"] == 12.5


def test_record_request_increments_total_5xx_errors() -> None:
    collector = MetricsCollector()

    collector.record_request("POST", 503, 3.2)

    snapshot = collector.snapshot()
    assert snapshot["total_5xx_errors"] == 1
    assert snapshot["responses_by_status_code"] == {"503": 1}


def test_snapshot_returns_expected_structure() -> None:
    collector = MetricsCollector()

    snapshot = collector.snapshot()

    assert set(snapshot) == {
        "uptime_seconds",
        "total_requests",
        "requests_by_method",
        "responses_by_status_code",
        "total_5xx_errors",
        "last_request_duration_ms",
    }
    assert isinstance(snapshot["uptime_seconds"], float)
