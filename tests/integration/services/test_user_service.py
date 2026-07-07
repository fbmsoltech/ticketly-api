import pytest
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.services.exceptions import ResourceAlreadyExistsError, ResourceNotFoundError
from app.services.user import UserService
from tests.factories import create_role, create_user

pytestmark = pytest.mark.integration


def test_create_user_hashes_password(db_session: Session) -> None:
    role = create_role(db_session)
    service = UserService(db_session)

    user = service.create(
        UserCreate(
            role_id=role.id,
            name="Jane Agent",
            email="jane.agent@example.com",
            password="secret123",
            is_active=True,
        ),
    )

    assert user.hashed_password != "secret123"
    assert verify_password("secret123", user.hashed_password)


def test_get_user_by_id_and_email(db_session: Session) -> None:
    role = create_role(db_session)
    user = create_user(db_session, role=role, email="lookup@example.com")
    service = UserService(db_session)

    assert service.get_by_id(user.id) == user
    assert service.get_by_email("lookup@example.com") == user


def test_list_users(db_session: Session) -> None:
    role = create_role(db_session)
    user = create_user(db_session, role=role, email="listed@example.com")
    service = UserService(db_session)

    assert user in service.list()


def test_update_user(db_session: Session) -> None:
    role = create_role(db_session)
    user = create_user(db_session, role=role, email="update@example.com")
    service = UserService(db_session)

    updated = service.update(user.id, UserUpdate(name="Updated User"))

    assert updated.name == "Updated User"


def test_update_user_password_replaces_hash(db_session: Session) -> None:
    role = create_role(db_session)
    user = create_user(db_session, role=role, email="password@example.com")
    original_hash = user.hashed_password
    service = UserService(db_session)

    updated = service.update(user.id, UserUpdate(password="newsecret123"))

    assert updated.hashed_password != original_hash
    assert updated.hashed_password != "newsecret123"
    assert verify_password("newsecret123", updated.hashed_password)


def test_delete_user(db_session: Session) -> None:
    role = create_role(db_session)
    user = create_user(db_session, role=role, email="delete@example.com")
    service = UserService(db_session)

    service.delete(user.id)

    with pytest.raises(ResourceNotFoundError):
        service.get_by_id(user.id)


def test_create_user_with_duplicate_email_raises_error(db_session: Session) -> None:
    role = create_role(db_session)
    create_user(db_session, role=role, email="duplicate@example.com")
    service = UserService(db_session)

    with pytest.raises(ResourceAlreadyExistsError):
        service.create(
            UserCreate(
                role_id=role.id,
                name="Duplicate User",
                email="duplicate@example.com",
                password="secret123",
                is_active=True,
            ),
        )


def test_create_user_with_missing_role_raises_error(db_session: Session) -> None:
    service = UserService(db_session)

    with pytest.raises(ResourceNotFoundError):
        service.create(
            UserCreate(
                role_id=9999,
                name="No Role",
                email="missing-role@example.com",
                password="secret123",
                is_active=True,
            ),
        )


def test_get_missing_user_raises_error(db_session: Session) -> None:
    service = UserService(db_session)

    with pytest.raises(ResourceNotFoundError):
        service.get_by_id(9999)
