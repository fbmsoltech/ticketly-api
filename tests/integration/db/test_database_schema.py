from collections.abc import Iterable
from os import getenv
from pathlib import Path

import pytest
from alembic.config import Config
from sqlalchemy import create_engine, select, text
from sqlalchemy.engine import Engine

from alembic import command
from app.core.config import normalize_database_url, settings
from app.db.session import SessionLocal, engine
from app.models.role import Role
from app.seed.initial_data import seed_initial_data

pytestmark = pytest.mark.integration

MAIN_TABLES = (
    "roles",
    "users",
    "customers",
    "ticket_categories",
    "ticket_statuses",
    "ticket_priorities",
    "tickets",
    "ticket_comments",
)


def _quote_schema(schema: str) -> str:
    return f'"{schema}"'


def _require_schema_database() -> None:
    test_database_url = getenv("TEST_DATABASE_URL")
    if test_database_url is None:
        pytest.skip("TEST_DATABASE_URL is required for schema integration tests.")

    if settings.database_url != normalize_database_url(test_database_url):
        pytest.skip(
            "Schema integration tests require DATABASE_URL and TEST_DATABASE_URL "
            "to point to the same isolated test database."
        )

    if settings.database_schema == "public":
        pytest.skip("Schema integration tests require DATABASE_SCHEMA != public.")

    if engine.url.get_backend_name() != "postgresql":
        pytest.skip("Schema integration tests require PostgreSQL.")


def _run_migrations_from_clean_schema() -> None:
    schema = settings.database_schema

    with engine.begin() as connection:
        connection.execute(
            text(f"DROP SCHEMA IF EXISTS {_quote_schema(schema)} CASCADE")
        )

    engine.dispose()

    alembic_config = Config(str(Path(__file__).resolve().parents[3] / "alembic.ini"))
    command.upgrade(alembic_config, "head")
    engine.dispose()


def _table_exists(db_engine: Engine, schema: str, table_name: str) -> bool:
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = :schema
              AND table_name = :table_name
        )
        """)

    with db_engine.connect() as connection:
        return bool(
            connection.scalar(
                query,
                {"schema": schema, "table_name": table_name},
            )
        )


def _missing_tables(
    db_engine: Engine, schema: str, table_names: Iterable[str]
) -> set[str]:
    return {
        table_name
        for table_name in table_names
        if not _table_exists(db_engine, schema, table_name)
    }


def test_migrations_create_tables_and_seed_uses_configured_schema() -> None:
    _require_schema_database()
    _run_migrations_from_clean_schema()

    schema = settings.database_schema
    inspection_engine = create_engine(settings.database_url, pool_pre_ping=True)
    try:
        assert _missing_tables(inspection_engine, schema, MAIN_TABLES) == set()
        assert _table_exists(inspection_engine, schema, "alembic_version")
        assert _missing_tables(inspection_engine, "public", MAIN_TABLES) == set(
            MAIN_TABLES
        )
    finally:
        inspection_engine.dispose()

    with SessionLocal() as db_session:
        seed_initial_data(db_session, settings)
        role_names = set(db_session.scalars(select(Role.name)).all())

    assert {"ADMIN", "AGENT", "CUSTOMER"}.issubset(role_names)
