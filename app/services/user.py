from collections.abc import Sequence as SequenceABC
from typing import Any

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService
from app.services.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.user_repository = UserRepository(session)
        self.role_repository = RoleRepository(session)
        super().__init__(self.user_repository, User)

    def get_by_id(self, user_id: int) -> User:
        user = self.user_repository.get(user_id)
        if user is None:
            raise ResourceNotFoundError("User not found.")
        return user

    def get_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email)

    def list(self, *, offset: int = 0, limit: int = 100) -> SequenceABC[User]:
        return self.user_repository.list(offset=offset, limit=limit)

    def list_by_role(self, role_id: int) -> SequenceABC[User]:
        return self.user_repository.list_by_role(role_id)

    def create(self, data: UserCreate) -> User:
        try:
            self._ensure_email_is_available(data.email)
            self._ensure_role_exists(data.role_id)
            user = self.user_repository.add(self._build_entity(data.model_dump()))
            self.session.commit()
            self.session.refresh(user)
            return user
        except Exception:
            self.session.rollback()
            raise

    def update(self, entity_id: int, data: UserUpdate) -> User:
        try:
            user = self.get_by_id(entity_id)
            update_data = self._get_update_data(data)

            email = update_data.get("email")
            if isinstance(email, str):
                self._ensure_email_is_available(email, current_user_id=user.id)

            role_id = update_data.get("role_id")
            if isinstance(role_id, int):
                self._ensure_role_exists(role_id)

            for field_name, value in update_data.items():
                setattr(user, field_name, value)

            updated = self.user_repository.update(user)
            self.session.commit()
            self.session.refresh(updated)
            return updated
        except Exception:
            self.session.rollback()
            raise

    def delete(self, entity_id: int) -> bool:
        try:
            user = self.get_by_id(entity_id)
            self.user_repository.delete(user)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise

    def _build_entity(self, data: dict[str, Any]) -> User:
        password = data.pop("password")
        data["hashed_password"] = get_password_hash(password)
        return User(**data)

    def _get_update_data(self, data: UserUpdate) -> dict[str, Any]:
        update_data = data.model_dump(exclude_unset=True)
        password = update_data.pop("password", None)
        if password is not None:
            update_data["hashed_password"] = get_password_hash(password)
        return update_data

    def _ensure_email_is_available(
        self,
        email: str,
        *,
        current_user_id: int | None = None,
    ) -> None:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None and existing_user.id != current_user_id:
            raise ResourceAlreadyExistsError("User email already exists.")

    def _ensure_role_exists(self, role_id: int) -> None:
        if self.role_repository.get(role_id) is None:
            raise ResourceNotFoundError("Role not found.")
