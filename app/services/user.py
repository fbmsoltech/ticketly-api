from collections.abc import Callable
from typing import Any

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: Callable[[str], str],
    ) -> None:
        super().__init__(repository, User)
        self.user_repository = repository
        self.password_hasher = password_hasher

    def get_by_email(self, email: str) -> User | None:
        return self.user_repository.get_by_email(email)

    def list_by_role(self, role_id: int) -> list[User]:
        return self.user_repository.list_by_role(role_id)

    def _build_entity(self, data: dict[str, Any]) -> User:
        password = data.pop("password")
        data["hashed_password"] = self.password_hasher(password)
        return User(**data)

    def _get_update_data(self, data: UserUpdate) -> dict[str, Any]:
        update_data = data.model_dump(exclude_unset=True)
        password = update_data.pop("password", None)
        if password is not None:
            update_data["hashed_password"] = self.password_hasher(password)
        return update_data
