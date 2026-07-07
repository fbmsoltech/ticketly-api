import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.security import verify_password
from app.models.role import Role
from app.models.ticket_category import TicketCategory
from app.models.ticket_priority import TicketPriority
from app.models.ticket_status import TicketStatus
from app.models.user import User
from app.seed.initial_data import seed_initial_data

pytestmark = pytest.mark.integration


def _settings(*, create_initial_admin: bool = False) -> Settings:
    return Settings(
        create_initial_admin=create_initial_admin,
        initial_admin_name="Admin",
        initial_admin_email=("admin@example.com" if create_initial_admin else None),
        initial_admin_password=(
            "strong-admin-password" if create_initial_admin else None
        ),
    )


def _count(db_session: Session, model: type[object]) -> int:
    return len(db_session.scalars(select(model)).all())


def test_seed_creates_initial_roles(db_session: Session) -> None:
    seed_initial_data(db_session, _settings())

    names = set(db_session.scalars(select(Role.name)).all())

    assert {"ADMIN", "AGENT", "CUSTOMER"}.issubset(names)


def test_seed_creates_initial_statuses(db_session: Session) -> None:
    seed_initial_data(db_session, _settings())

    names = set(db_session.scalars(select(TicketStatus.name)).all())

    assert {"OPEN", "IN_PROGRESS", "WAITING_CUSTOMER", "RESOLVED", "CLOSED"} == names


def test_seed_creates_initial_priorities(db_session: Session) -> None:
    seed_initial_data(db_session, _settings())

    priorities = db_session.scalars(select(TicketPriority)).all()

    assert {priority.name for priority in priorities} == {
        "LOW",
        "MEDIUM",
        "HIGH",
        "URGENT",
    }
    assert {priority.sort_order for priority in priorities} == {1, 2, 3, 4}


def test_seed_creates_initial_categories(db_session: Session) -> None:
    seed_initial_data(db_session, _settings())

    names = set(db_session.scalars(select(TicketCategory.name)).all())

    assert {"GENERAL", "TECHNICAL", "BILLING", "ACCESS"} == names


def test_seed_is_idempotent_for_base_data(db_session: Session) -> None:
    seed_initial_data(db_session, _settings())
    seed_initial_data(db_session, _settings())

    assert _count(db_session, Role) == 3
    assert _count(db_session, TicketStatus) == 5
    assert _count(db_session, TicketPriority) == 4
    assert _count(db_session, TicketCategory) == 4


def test_seed_creates_initial_admin_with_hashed_password(
    db_session: Session,
) -> None:
    seed_initial_data(db_session, _settings(create_initial_admin=True))

    user = db_session.scalar(select(User).where(User.email == "admin@example.com"))

    assert user is not None
    assert user.role.name == "ADMIN"
    assert user.hashed_password != "strong-admin-password"
    assert verify_password("strong-admin-password", user.hashed_password)


def test_seed_does_not_duplicate_initial_admin(db_session: Session) -> None:
    settings = _settings(create_initial_admin=True)

    seed_initial_data(db_session, settings)
    seed_initial_data(db_session, settings)

    users = db_session.scalars(
        select(User).where(User.email == "admin@example.com")
    ).all()

    assert len(users) == 1


def test_seed_does_not_create_admin_when_disabled(db_session: Session) -> None:
    seed_initial_data(db_session, _settings(create_initial_admin=False))

    assert db_session.scalar(select(User)) is None
