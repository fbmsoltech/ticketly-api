from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.api.v1.dependencies.services import get_health_service
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter(prefix="/health", tags=["health"])

HealthServiceDependency = Annotated[HealthService, Depends(get_health_service)]


@router.get("", response_model=HealthResponse, summary="Verifica o estado da API")
def health_check(service: HealthServiceDependency) -> HealthResponse:
    return service.get_health()


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Verifica se o processo da API esta vivo",
)
def liveness_check(service: HealthServiceDependency) -> HealthResponse:
    return service.get_liveness()


@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Verifica se a API esta pronta para receber trafego",
)
def readiness_check(
    service: HealthServiceDependency,
    response: Response,
) -> HealthResponse:
    health = service.get_health()
    if health.status != "ok":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return health
