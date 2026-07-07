import logging
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.config import DEFAULT_INITIAL_ADMIN_PASSWORD, Settings
from app.core.security import get_password_hash
from app.models.role import Role
from app.models.ticket_category import TicketCategory
from app.models.ticket_priority import TicketPriority
from app.models.ticket_status import TicketStatus
from app.models.user import User
from app.repositories.role import RoleRepository
from app.repositories.ticket_category import TicketCategoryRepository
from app.repositories.ticket_priority import TicketPriorityRepository
from app.repositories.ticket_status import TicketStatusRepository
from app.repositories.user import UserRepository

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NamedSeedData:
    name: str
    description: str


@dataclass(frozen=True)
class OrderedSeedData(NamedSeedData):
    sort_order: int


INITIAL_ROLES: tuple[NamedSeedData, ...] = (
    NamedSeedData("ADMIN", "Full access to manage the system."),
    NamedSeedData("AGENT", "Support agent responsible for handling tickets."),
    NamedSeedData("CUSTOMER", "Customer user with limited access."),
)

INITIAL_TICKET_STATUSES: tuple[OrderedSeedData, ...] = (
    OrderedSeedData("OPEN", "Ticket has been created and is awaiting triage.", 1),
    OrderedSeedData("IN_PROGRESS", "Ticket is being handled by a support agent.", 2),
    OrderedSeedData(
        "WAITING_CUSTOMER",
        "Ticket is waiting for customer response.",
        3,
    ),
    OrderedSeedData("RESOLVED", "Ticket was resolved but not closed yet.", 4),
    OrderedSeedData("CLOSED", "Ticket was closed.", 5),
)

INITIAL_TICKET_PRIORITIES: tuple[OrderedSeedData, ...] = (
    OrderedSeedData("LOW", "Low impact issue.", 1),
    OrderedSeedData("MEDIUM", "Normal priority issue.", 2),
    OrderedSeedData("HIGH", "High impact issue.", 3),
    OrderedSeedData("URGENT", "Critical issue requiring immediate attention.", 4),
)

INITIAL_TICKET_CATEGORIES: tuple[NamedSeedData, ...] = (
    NamedSeedData("GENERAL", "General support requests."),
    NamedSeedData("TECHNICAL", "Technical support issues."),
    NamedSeedData("BILLING", "Billing and payment related requests."),
    NamedSeedData("ACCESS", "Login, password and access related issues."),
)


def validate_initial_admin_password(password: str | None) -> str:
    if password is None or not password.strip():
        raise ValueError("INITIAL_ADMIN_PASSWORD must not be empty.")

    if password == DEFAULT_INITIAL_ADMIN_PASSWORD:
        raise ValueError("INITIAL_ADMIN_PASSWORD must not use the default value.")

    if len(password) < 8:
        raise ValueError("INITIAL_ADMIN_PASSWORD must have at least 8 characters.")

    return password


def seed_roles(db: Session) -> None:
    repository = RoleRepository(db)

    for item in INITIAL_ROLES:
        if repository.get_by_name(item.name) is not None:
            logger.info("Role %s already exists; skipping.", item.name)
            continue

        repository.add(Role(name=item.name, description=item.description))
        logger.info("Created role %s.", item.name)


def seed_ticket_statuses(db: Session) -> None:
    repository = TicketStatusRepository(db)

    for item in INITIAL_TICKET_STATUSES:
        if repository.get_by_name(item.name) is not None:
            logger.info("Ticket status %s already exists; skipping.", item.name)
            continue

        repository.add(
            TicketStatus(
                name=item.name,
                description=item.description,
                sort_order=item.sort_order,
            )
        )
        logger.info("Created ticket status %s.", item.name)


def seed_ticket_priorities(db: Session) -> None:
    repository = TicketPriorityRepository(db)

    for item in INITIAL_TICKET_PRIORITIES:
        if repository.get_by_name(item.name) is not None:
            logger.info("Ticket priority %s already exists; skipping.", item.name)
            continue

        repository.add(
            TicketPriority(
                name=item.name,
                description=item.description,
                sort_order=item.sort_order,
            )
        )
        logger.info("Created ticket priority %s.", item.name)


def seed_ticket_categories(db: Session) -> None:
    repository = TicketCategoryRepository(db)

    for item in INITIAL_TICKET_CATEGORIES:
        if repository.get_by_name(item.name) is not None:
            logger.info("Ticket category %s already exists; skipping.", item.name)
            continue

        repository.add(
            TicketCategory(
                name=item.name,
                description=item.description,
                is_active=True,
            )
        )
        logger.info("Created ticket category %s.", item.name)


def seed_initial_admin(db: Session, settings: Settings) -> None:
    if not settings.create_initial_admin:
        logger.info("Initial admin creation is disabled; skipping.")
        return

    if settings.initial_admin_email is None:
        raise ValueError(
            "INITIAL_ADMIN_EMAIL must be configured when CREATE_INITIAL_ADMIN is true."
        )

    password = validate_initial_admin_password(settings.initial_admin_password)
    user_repository = UserRepository(db)

    if user_repository.get_by_email(settings.initial_admin_email) is not None:
        logger.info("Initial admin user already exists; skipping.")
        return

    role_repository = RoleRepository(db)
    admin_role = role_repository.get_by_name("ADMIN")
    if admin_role is None:
        admin_role = role_repository.add(
            Role(
                name="ADMIN",
                description="Full access to manage the system.",
            )
        )
        logger.info("Created role ADMIN for initial admin.")

    user_repository.add(
        User(
            role_id=admin_role.id,
            name=settings.initial_admin_name,
            email=settings.initial_admin_email,
            hashed_password=get_password_hash(password),
            is_active=True,
        )
    )
    logger.info("Created initial admin user %s.", settings.initial_admin_email)


def seed_initial_data(db: Session, settings: Settings) -> None:
    try:
        seed_roles(db)
        seed_ticket_statuses(db)
        seed_ticket_priorities(db)
        seed_ticket_categories(db)
        seed_initial_admin(db, settings)
        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Initial seed failed.")
        raise
