from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket_category import TicketCategory
from app.repositories.base import BaseRepository


class TicketCategoryRepository(BaseRepository[TicketCategory]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, TicketCategory)

    def get_by_name(self, name: str) -> TicketCategory | None:
        statement = select(TicketCategory).where(TicketCategory.name == name)
        return self.session.scalar(statement)

    def list_active(self) -> list[TicketCategory]:
        statement = select(TicketCategory).where(TicketCategory.is_active.is_(True))
        return list(self.session.scalars(statement).all())
