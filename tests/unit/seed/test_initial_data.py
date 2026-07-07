import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.seed.initial_data import (
    INITIAL_ROLES,
    INITIAL_TICKET_PRIORITIES,
    validate_initial_admin_password,
)

pytestmark = pytest.mark.unit


def test_initial_admin_password_rejects_default_value() -> None:
    with pytest.raises(ValueError, match="default"):
        validate_initial_admin_password("change-me")


def test_initial_admin_password_rejects_empty_value() -> None:
    with pytest.raises(ValueError, match="empty"):
        validate_initial_admin_password(" ")


def test_initial_admin_password_rejects_short_value() -> None:
    with pytest.raises(ValueError, match="at least 8"):
        validate_initial_admin_password("short")


def test_create_initial_admin_false_does_not_require_email_or_password() -> None:
    settings = Settings(create_initial_admin=False)

    assert settings.create_initial_admin is False
    assert settings.initial_admin_email is None
    assert settings.initial_admin_password is None


def test_create_initial_admin_true_requires_email_and_password() -> None:
    with pytest.raises(ValidationError, match="INITIAL_ADMIN_EMAIL"):
        Settings(create_initial_admin=True)


def test_production_settings_reject_default_initial_admin_password() -> None:
    with pytest.raises(ValidationError, match="INITIAL_ADMIN_PASSWORD"):
        Settings(
            app_env="production",
            database_url="postgresql+psycopg://user:password@host:5432/database",
            jwt_secret_key="strong-production-secret",
            create_initial_admin=True,
            initial_admin_email="admin@example.com",
            initial_admin_password="change-me",
        )


def test_initial_roles_contain_required_names() -> None:
    role_names = {role.name for role in INITIAL_ROLES}

    assert {"ADMIN", "AGENT", "CUSTOMER"}.issubset(role_names)


def test_initial_priorities_have_unique_levels() -> None:
    levels = [priority.sort_order for priority in INITIAL_TICKET_PRIORITIES]

    assert len(levels) == len(set(levels))
