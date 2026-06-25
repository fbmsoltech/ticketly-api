from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ticketly API"
    app_version: str = "0.1.0"
    app_env: str = "local"
    database_url: str = (
        "postgresql+psycopg://supportflow_user:supportflow_password"
        "@localhost:5432/supportflow_db"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
