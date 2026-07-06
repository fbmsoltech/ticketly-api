from datetime import UTC, datetime

import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)

pytestmark = pytest.mark.unit


def test_get_password_hash_returns_value_different_from_plain_password() -> None:
    hashed_password = get_password_hash("secret123")

    assert hashed_password != "secret123"


def test_verify_password_returns_true_for_correct_password() -> None:
    hashed_password = get_password_hash("secret123")

    assert verify_password("secret123", hashed_password) is True


def test_verify_password_returns_false_for_incorrect_password() -> None:
    hashed_password = get_password_hash("secret123")

    assert verify_password("wrongsecret", hashed_password) is False


def test_create_access_token_generates_token() -> None:
    token = create_access_token(subject="123")

    assert token


def test_decode_access_token_returns_payload_with_sub() -> None:
    token = create_access_token(subject="123")

    payload = decode_access_token(token)

    assert payload["sub"] == "123"


def test_access_token_has_expiration() -> None:
    token = create_access_token(subject="123")

    payload = decode_access_token(token)

    assert "exp" in payload
    assert datetime.fromtimestamp(payload["exp"], tz=UTC) > datetime.now(UTC)
