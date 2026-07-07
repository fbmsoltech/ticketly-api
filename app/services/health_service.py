from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.schemas.health import ComponentHealth, HealthResponse


class HealthService:
    def __init__(self, db: Session, settings: Settings) -> None:
        self.db = db
        self.settings = settings

    def check_database(self) -> ComponentHealth:
        try:
            self.db.execute(text("SELECT 1"))
        except Exception as exc:
            self.db.rollback()
            return ComponentHealth(status="error", details=exc.__class__.__name__)

        return ComponentHealth(status="ok")

    def get_health(self) -> HealthResponse:
        components = {
            "app": ComponentHealth(status="ok"),
            "database": self.check_database(),
        }
        overall_status = (
            "ok"
            if all(component.status == "ok" for component in components.values())
            else "degraded"
        )

        return HealthResponse(
            status=overall_status,
            app=self.settings.app_name,
            version=self.settings.app_version,
            environment=self.settings.app_env,
            components=components,
        )

    def get_liveness(self) -> HealthResponse:
        return HealthResponse(
            status="ok",
            app=self.settings.app_name,
            version=self.settings.app_version,
            environment=self.settings.app_env,
            components={"app": ComponentHealth(status="ok")},
        )
