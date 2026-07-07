from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.repositories.base import BaseRepository


class TicketRepository(BaseRepository[Ticket]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Ticket)

    def list_by_assignee(
        self,
        assignee_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        return self.list_by_assigned_agent(assignee_id, offset=offset, limit=limit)

    def list_by_customer(
        self,
        customer_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        statement = (
            select(Ticket)
            .where(Ticket.customer_id == customer_id)
            .offset(offset)
            .limit(limit)
        )
        return self.session.scalars(statement).all()

    def list_by_status(
        self,
        status_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        statement = (
            select(Ticket)
            .where(Ticket.status_id == status_id)
            .offset(offset)
            .limit(limit)
        )
        return self.session.scalars(statement).all()

    def list_by_assigned_agent(
        self,
        agent_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        statement = (
            select(Ticket)
            .where(Ticket.assignee_id == agent_id)
            .offset(offset)
            .limit(limit)
        )
        return self.session.scalars(statement).all()

    def list_filtered(
        self,
        *,
        customer_id: int | None = None,
        status_id: int | None = None,
        priority_id: int | None = None,
        assigned_agent_id: int | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        statement = select(Ticket)
        if customer_id is not None:
            statement = statement.where(Ticket.customer_id == customer_id)
        if status_id is not None:
            statement = statement.where(Ticket.status_id == status_id)
        if priority_id is not None:
            statement = statement.where(Ticket.priority_id == priority_id)
        if assigned_agent_id is not None:
            statement = statement.where(Ticket.assignee_id == assigned_agent_id)
        statement = statement.offset(offset).limit(limit)
        return self.session.scalars(statement).all()
