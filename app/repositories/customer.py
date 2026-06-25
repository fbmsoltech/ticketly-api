from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Customer)

    def get_by_user_id(self, user_id: int) -> Customer | None:
        statement = select(Customer).where(Customer.user_id == user_id)
        return self.session.scalar(statement)
