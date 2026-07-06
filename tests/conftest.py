from collections.abc import Generator
from os import getenv

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db_session
from app.main import create_app


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
