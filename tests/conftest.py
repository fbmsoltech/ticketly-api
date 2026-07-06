from collections.abc import Generator
from os import getenv

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.core.security import create_access_token
from app.db.base import Base
from app.db.session import get_db_session
from app.main import create_app
from app.models.customer import Customer
from app.models.role import Role
from app.models.ticket import Ticket
from app.models.ticket_category import TicketCategory
from app.models.ticket_priority import TicketPriority
from app.models.ticket_status import TicketStatus
from app.models.user import User
from tests.factories import (
    create_customer,
    create_role,
    create_ticket,
    create_ticket_category,
    create_ticket_priority,
    create_ticket_status,
    create_user,
)


@pytest.fixture
def engine() -> Generator[Engine]:
    test_database_url = getenv("TEST_DATABASE_URL")
    if test_database_url is None:
        test_engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        test_engine = create_engine(test_database_url, pool_pre_ping=True)

    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    try:
        yield test_engine
    finally:
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


@pytest.fixture
def db_session(engine: Engine) -> Generator[Session]:
    testing_session_local = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient]:
    app = create_app()

    def override_get_db_session() -> Generator[Session]:
        try:
            yield db_session
            db_session.commit()
        except Exception:
            db_session.rollback()
            raise

    app.dependency_overrides[get_db_session] = override_get_db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def admin_role(db_session: Session) -> Role:
    return create_role(db_session, name="ADMIN")


@pytest.fixture
def agent_role(db_session: Session) -> Role:
    return create_role(db_session, name="AGENT")


@pytest.fixture
def customer_role(db_session: Session) -> Role:
    return create_role(db_session, name="CUSTOMER")


@pytest.fixture
def admin_user(db_session: Session, admin_role: Role) -> User:
    return create_user(
        db_session,
        role=admin_role,
        name="Admin User",
        email="admin@example.com",
        password="admin123",
    )


@pytest.fixture
def agent_user(db_session: Session, agent_role: Role) -> User:
    return create_user(
        db_session,
        role=agent_role,
        name="Agent User",
        email="agent-auth@example.com",
        password="agent123",
    )


@pytest.fixture
def customer_user(db_session: Session, customer_role: Role) -> User:
    return create_user(
        db_session,
        role=customer_role,
        name="Customer User",
        email="customer-auth@example.com",
        password="customer123",
    )


@pytest.fixture
def customer(db_session: Session, customer_user: User) -> Customer:
    return create_customer(db_session, user=customer_user)


@pytest.fixture
def ticket_category(db_session: Session) -> TicketCategory:
    return create_ticket_category(db_session, name="Technical Support")


@pytest.fixture
def ticket_status(db_session: Session) -> TicketStatus:
    return create_ticket_status(db_session, name="Open", sort_order=1)


@pytest.fixture
def second_ticket_status(db_session: Session) -> TicketStatus:
    return create_ticket_status(db_session, name="In Progress", sort_order=2)


@pytest.fixture
def ticket_priority(db_session: Session) -> TicketPriority:
    return create_ticket_priority(db_session, name="High", sort_order=1)


@pytest.fixture
def ticket(
    db_session: Session,
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
) -> Ticket:
    return create_ticket(
        db_session,
        customer=customer,
        category=ticket_category,
        status=ticket_status,
        priority=ticket_priority,
    )


@pytest.fixture
def admin_token(admin_user: User) -> str:
    return create_access_token(subject=str(admin_user.id))


@pytest.fixture
def agent_token(agent_user: User) -> str:
    return create_access_token(subject=str(agent_user.id))


@pytest.fixture
def customer_token(customer_user: User) -> str:
    return create_access_token(subject=str(customer_user.id))


@pytest.fixture
def admin_auth_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def agent_auth_headers(agent_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {agent_token}"}


@pytest.fixture
def customer_auth_headers(customer_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {customer_token}"}
