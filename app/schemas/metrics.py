from pydantic import BaseModel


class MetricsResponse(BaseModel):
    uptime_seconds: float
    total_requests: int
    requests_by_method: dict[str, int]
    responses_by_status_code: dict[str, int]
    total_5xx_errors: int
    last_request_duration_ms: float | None = None
