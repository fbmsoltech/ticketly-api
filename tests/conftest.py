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
from app.models.role import Role
from app.models.user import User
from tests.factories import create_role, create_user


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
def admin_token(admin_user: User) -> str:
    return create_access_token(subject=str(admin_user.id))


@pytest.fixture
def agent_token(agent_user: User) -> str:
    return create_access_token(subject=str(agent_user.id))


@pytest.fixture
def admin_auth_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def agent_auth_headers(agent_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {agent_token}"}
