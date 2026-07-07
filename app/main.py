from fastapi import FastAPI

from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.customers import router as customers_router
from app.api.v1.routes.error_handlers import register_exception_handlers
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.metrics import router as metrics_router
from app.api.v1.routes.roles import router as roles_router
from app.api.v1.routes.ticket_categories import router as ticket_categories_router
from app.api.v1.routes.ticket_comments import router as ticket_comments_router
from app.api.v1.routes.ticket_priorities import router as ticket_priorities_router
from app.api.v1.routes.ticket_statuses import router as ticket_statuses_router
from app.api.v1.routes.tickets import router as tickets_router
from app.api.v1.routes.users import router as users_router
from app.core.config import settings
from app.observability.logging import configure_logging
from app.observability.middleware import register_observability_middleware

configure_logging(settings.log_level)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json",
    )
    register_exception_handlers(app)
    if settings.enable_request_logging:
        register_observability_middleware(app)

    app.include_router(health_router, prefix="/api/v1")
    app.include_router(metrics_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(roles_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(customers_router, prefix="/api/v1")
    app.include_router(ticket_statuses_router, prefix="/api/v1")
    app.include_router(ticket_priorities_router, prefix="/api/v1")
    app.include_router(ticket_categories_router, prefix="/api/v1")
    app.include_router(tickets_router, prefix="/api/v1")
    app.include_router(ticket_comments_router, prefix="/api/v1")
    return app


app: FastAPI = create_app()
