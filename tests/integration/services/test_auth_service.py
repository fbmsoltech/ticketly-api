import pytest
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.services.auth_service import AuthService
from app.services.exceptions import AuthenticationError
from tests.factories import create_role, create_user

pytestmark = pytest.mark.integration


def test_authenticate_user_with_valid_credentials(db_session: Session) -> None:
    role = create_role(db_session)
    user = create_user(
        db_session,
        role=role,
        email="auth@example.com",
        password="secret123",
    )
    service = AuthService(db_session)

    assert service.authenticate("auth@example.com", "secret123") == user


def test_login_generates_token(db_session: Session) -> None:
    role = create_role(db_session)
    user = create_user(
        db_session,
        role=role,
        email="login@example.com",
        password="secret123",
    )
    service = AuthService(db_session)

    token = service.login("login@example.com", "secret123")
    payload = decode_access_token(token)

    assert payload["sub"] == str(user.id)
    assert "exp" in payload


def test_authenticate_with_missing_email_raises_error(db_session: Session) -> None:
    service = AuthService(db_session)

    with pytest.raises(AuthenticationError):
        service.authenticate("missing@example.com", "secret123")


def test_authenticate_with_wrong_password_raises_error(db_session: Session) -> None:
    role = create_role(db_session)
    create_user(
        db_session,
        role=role,
        email="wrong-password@example.com",
        password="secret123",
    )
    service = AuthService(db_session)

    with pytest.raises(AuthenticationError):
        service.authenticate("wrong-password@example.com", "wrongsecret")


def test_authenticate_inactive_user_raises_error(db_session: Session) -> None:
    role = create_role(db_session)
    create_user(
        db_session,
        role=role,
        email="inactive@example.com",
        password="secret123",
        is_active=False,
    )
    service = AuthService(db_session)

    with pytest.raises(AuthenticationError):
        service.authenticate("inactive@example.com", "secret123")
