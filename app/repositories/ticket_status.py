from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket_status import TicketStatus
from app.repositories.base import BaseRepository


class TicketStatusRepository(BaseRepository[TicketStatus]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, TicketStatus)

    def get_by_name(self, name: str) -> TicketStatus | None:
        statement = select(TicketStatus).where(TicketStatus.name == name)
        return self.session.scalar(statement)

    def list_ordered(self) -> list[TicketStatus]:
        statement = select(TicketStatus).order_by(TicketStatus.sort_order)
        return list(self.session.scalars(statement).all())
