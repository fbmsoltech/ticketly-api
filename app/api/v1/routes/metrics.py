from fastapi import APIRouter

from app.observability.metrics import metrics_collector
from app.schemas.metrics import MetricsResponse

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=MetricsResponse, summary="Exibe metricas basicas")
def get_metrics() -> dict[str, object]:
    return metrics_collector.snapshot()
