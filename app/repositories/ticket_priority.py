from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket_priority import TicketPriority
from app.repositories.base import BaseRepository


class TicketPriorityRepository(BaseRepository[TicketPriority]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, TicketPriority)

    def get_by_name(self, name: str) -> TicketPriority | None:
        statement = select(TicketPriority).where(TicketPriority.name == name)
        return self.session.scalar(statement)

    def list_ordered(self) -> list[TicketPriority]:
        statement = select(TicketPriority).order_by(TicketPriority.sort_order)
        return list(self.session.scalars(statement).all())
