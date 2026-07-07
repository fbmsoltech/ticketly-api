from functools import lru_cache
from typing import Self

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_DATABASE_URL = (
    "postgresql+psycopg://ticketly_user:ticketly_user@localhost:5432/ticketly_db"
)
DEFAULT_JWT_SECRET_KEY = "change-me-in-production-use-a-strong-secret-key"
DEFAULT_INITIAL_ADMIN_PASSWORD = "change-me"
PRODUCTION_PLACEHOLDER_JWT_SECRET_KEYS = {
    "change-me-in-production",
    DEFAULT_JWT_SECRET_KEY,
}


def normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)

    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    return database_url


class Settings(BaseSettings):
    app_name: str = "Ticketly API"
    app_version: str = "0.1.0"
    app_env: str = "local"
    database_url: str = DEFAULT_DATABASE_URL
    jwt_secret_key: str = DEFAULT_JWT_SECRET_KEY
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    log_level: str = "INFO"
    enable_request_logging: bool = True
    enable_metrics: bool = True
    create_initial_admin: bool = False
    initial_admin_name: str = "Admin"
    initial_admin_email: str | None = None
    initial_admin_password: str | None = None

    @field_validator("app_env")
    @classmethod
    def normalize_app_env(cls, app_env: str) -> str:
        return app_env.strip().lower()

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, database_url: str) -> str:
        if not database_url:
            raise ValueError("DATABASE_URL must be configured.")

        return normalize_database_url(database_url)

    @field_validator("jwt_secret_key")
    @classmethod
    def validate_jwt_secret_key(cls, jwt_secret_key: str) -> str:
        if not jwt_secret_key:
            raise ValueError("JWT_SECRET_KEY must be configured.")

        return jwt_secret_key

    @model_validator(mode="after")
    def validate_production_settings(self) -> Self:
        if self.create_initial_admin:
            if not self.initial_admin_email:
                raise ValueError(
                    "INITIAL_ADMIN_EMAIL must be configured when "
                    "CREATE_INITIAL_ADMIN is true."
                )

            if self.initial_admin_password is None:
                raise ValueError(
                    "INITIAL_ADMIN_PASSWORD must be configured when "
                    "CREATE_INITIAL_ADMIN is true."
                )

            if not self.initial_admin_password.strip():
                raise ValueError("INITIAL_ADMIN_PASSWORD must not be empty.")

            if self.initial_admin_password == DEFAULT_INITIAL_ADMIN_PASSWORD:
                raise ValueError(
                    "INITIAL_ADMIN_PASSWORD must not use the default example value."
                )

            if len(self.initial_admin_password) < 8:
                raise ValueError(
                    "INITIAL_ADMIN_PASSWORD must have at least 8 characters."
                )

        if self.app_env != "production":
            return self

        if self.database_url == DEFAULT_DATABASE_URL:
            raise ValueError("DATABASE_URL must be configured in production.")

        if self.jwt_secret_key in PRODUCTION_PLACEHOLDER_JWT_SECRET_KEYS:
            raise ValueError("JWT_SECRET_KEY must be configured in production.")

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
