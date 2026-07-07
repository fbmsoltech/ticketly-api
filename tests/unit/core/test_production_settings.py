import pytest
from pydantic import ValidationError

from app.core.config import Settings, normalize_database_url

pytestmark = pytest.mark.unit


def test_normalize_database_url_keeps_psycopg_driver() -> None:
    database_url = "postgresql+psycopg://user:password@host:5432/database"

    assert normalize_database_url(database_url) == database_url


def test_normalize_database_url_converts_postgres_scheme() -> None:
    database_url = "postgres://user:password@host:5432/database"

    assert (
        normalize_database_url(database_url)
        == "postgresql+psycopg://user:password@host:5432/database"
    )


def test_normalize_database_url_converts_postgresql_scheme() -> None:
    database_url = "postgresql://user:password@host:5432/database"

    assert (
        normalize_database_url(database_url)
        == "postgresql+psycopg://user:password@host:5432/database"
    )


def test_production_settings_reject_placeholder_jwt_secret_key() -> None:
    with pytest.raises(ValidationError, match="JWT_SECRET_KEY"):
        Settings(
            app_env="production",
            database_url="postgresql+psycopg://user:password@host:5432/database",
            jwt_secret_key="change-me-in-production",
        )


def test_non_production_settings_accept_env_example_values() -> None:
    settings = Settings(
        app_env="local",
        database_url="postgresql+psycopg://ticketly_user:ticketly_user@db:5432/ticketly_db",
        jwt_secret_key="change-me-in-production",
    )

    assert settings.app_env == "local"
    assert (
        settings.database_url
        == "postgresql+psycopg://ticketly_user:ticketly_user@db:5432/ticketly_db"
    )
    assert settings.jwt_secret_key == "change-me-in-production"
