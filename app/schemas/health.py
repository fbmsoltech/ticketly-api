from pydantic import BaseModel


class ComponentHealth(BaseModel):
    status: str
    details: str | None = None


class HealthResponse(BaseModel):
    status: str
    app: str
    version: str
    environment: str
    components: dict[str, ComponentHealth]
