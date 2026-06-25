from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.repositories.base import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Ticket)

    def list_by_assignee(self, assignee_id: int) -> list[Ticket]:
        statement = select(Ticket).where(Ticket.assignee_id == assignee_id)
        return list(self.session.scalars(statement).all())

    def list_by_customer(self, customer_id: int) -> list[Ticket]:
        statement = select(Ticket).where(Ticket.customer_id == customer_id)
        return list(self.session.scalars(statement).all())

    def list_by_status(self, status_id: int) -> list[Ticket]:
        statement = select(Ticket).where(Ticket.status_id == status_id)
        return list(self.session.scalars(statement).all())
