import pytest
from pydantic import ValidationError

from app.core.config import Settings, normalize_database_url, validate_database_schema

pytestmark = pytest.mark.unit


def test_database_schema_empty_is_rejected() -> None:
    with pytest.raises(ValueError, match="DATABASE_SCHEMA cannot be empty"):
        validate_database_schema(" ")


def test_database_schema_with_space_is_rejected() -> None:
    with pytest.raises(ValueError, match="DATABASE_SCHEMA"):
        validate_database_schema("ticketly api")


def test_database_schema_with_semicolon_is_rejected() -> None:
    with pytest.raises(ValueError, match="DATABASE_SCHEMA"):
        validate_database_schema("ticketly;drop")


def test_database_schema_with_dot_is_rejected() -> None:
    with pytest.raises(ValueError, match="DATABASE_SCHEMA"):
        validate_database_schema("ticketly.api")


def test_database_schema_with_quotes_is_rejected() -> None:
    with pytest.raises(ValueError, match="DATABASE_SCHEMA"):
        validate_database_schema('"ticketly"')


def test_database_schema_ticketly_is_accepted() -> None:
    assert validate_database_schema("ticketly") == "ticketly"


def test_database_schema_with_underscore_is_accepted() -> None:
    assert validate_database_schema("ticketly_test") == "ticketly_test"


def test_settings_reject_invalid_database_schema() -> None:
    with pytest.raises(ValidationError, match="DATABASE_SCHEMA"):
        Settings(database_schema="ticketly.api")


def test_normalize_database_url_keeps_existing_psycopg_driver() -> None:
    database_url = "postgresql+psycopg://user:password@host:5432/database"

    assert normalize_database_url(database_url) == database_url


def test_normalize_database_url_converts_render_postgres_scheme() -> None:
    database_url = "postgres://user:password@host:5432/database"

    assert (
        normalize_database_url(database_url)
        == "postgresql+psycopg://user:password@host:5432/database"
    )
