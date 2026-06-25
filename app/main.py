from fastapi import FastAPI

from app.api.v1.routes.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    app.include_router(health_router, prefix="/api/v1", tags=["health"])
    return app


app: FastAPI = create_app()
