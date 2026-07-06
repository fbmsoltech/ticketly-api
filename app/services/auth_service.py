from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService
from app.services.exceptions import AuthenticationError


class AuthService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, session: Session) -> None:
        self.user_repository = UserRepository(session)
        super().__init__(self.user_repository, User)

    def authenticate(self, email: str, password: str) -> User:
        user = self.user_repository.get_by_email(email)
        if user is None:
            raise AuthenticationError("Invalid credentials.")
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials.")
        if not user.is_active:
            raise AuthenticationError("Invalid credentials.")
        return user

    def login(self, email: str, password: str) -> str:
        user = self.authenticate(email, password)
        return create_access_token(subject=str(user.id))
