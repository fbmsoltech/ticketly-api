from threading import Lock
from time import monotonic
from typing import Any


class MetricsCollector:
    def __init__(self) -> None:
        self._started_at = monotonic()
        self._total_requests = 0
        self._requests_by_method: dict[str, int] = {}
        self._responses_by_status_code: dict[str, int] = {}
        self._total_5xx_errors = 0
        self._last_request_duration_ms: float | None = None
        self._lock = Lock()

    def record_request(
        self,
        method: str,
        status_code: int,
        duration_ms: float,
    ) -> None:
        normalized_method = method.upper()
        status_code_key = str(status_code)

        with self._lock:
            self._total_requests += 1
            self._requests_by_method[normalized_method] = (
                self._requests_by_method.get(normalized_method, 0) + 1
            )
            self._responses_by_status_code[status_code_key] = (
                self._responses_by_status_code.get(status_code_key, 0) + 1
            )
            if status_code >= 500:
                self._total_5xx_errors += 1
            self._last_request_duration_ms = duration_ms

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "uptime_seconds": monotonic() - self._started_at,
                "total_requests": self._total_requests,
                "requests_by_method": dict(self._requests_by_method),
                "responses_by_status_code": dict(self._responses_by_status_code),
                "total_5xx_errors": self._total_5xx_errors,
                "last_request_duration_ms": self._last_request_duration_ms,
            }

    def reset(self) -> None:
        with self._lock:
            self._started_at = monotonic()
            self._total_requests = 0
            self._requests_by_method.clear()
            self._responses_by_status_code.clear()
            self._total_5xx_errors = 0
            self._last_request_duration_ms = None


metrics_collector = MetricsCollector()
