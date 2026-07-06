from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.core.security import get_password_hash
from app.services.auth_service import AuthService
from app.services.exceptions import AuthenticationError

pytestmark = pytest.mark.unit


def _auth_service_with_user(user: object | None) -> AuthService:
    service = AuthService.__new__(AuthService)
    service.user_repository = Mock()
    service.user_repository.get_by_email.return_value = user
    return service


def test_authentication_fails_when_repository_does_not_find_user() -> None:
    service = _auth_service_with_user(None)

    with pytest.raises(AuthenticationError):
        service.authenticate("missing@example.com", "secret123")


def test_authentication_fails_when_password_is_incorrect() -> None:
    user = SimpleNamespace(
        hashed_password=get_password_hash("secret123"),
        is_active=True,
    )
    service = _auth_service_with_user(user)

    with pytest.raises(AuthenticationError):
        service.authenticate("user@example.com", "wrongsecret")


def test_authentication_fails_when_user_is_inactive() -> None:
    user = SimpleNamespace(
        hashed_password=get_password_hash("secret123"),
        is_active=False,
    )
    service = _auth_service_with_user(user)

    with pytest.raises(AuthenticationError):
        service.authenticate("user@example.com", "secret123")
