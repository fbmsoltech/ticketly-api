from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket_comment import TicketComment
from app.repositories.base import BaseRepository


class TicketCommentRepository(BaseRepository[TicketComment]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, TicketComment)

    def list_by_ticket(
        self,
        ticket_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[TicketComment]:
        statement = (
            select(TicketComment)
            .where(TicketComment.ticket_id == ticket_id)
            .offset(offset)
            .limit(limit)
        )
        return self.session.scalars(statement).all()

    def list_visible_by_ticket(
        self,
        ticket_id: int,
        *,
        include_internal: bool = True,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[TicketComment]:
        statement = select(TicketComment).where(TicketComment.ticket_id == ticket_id)
        if not include_internal:
            statement = statement.where(TicketComment.is_internal.is_(False))
        statement = statement.offset(offset).limit(limit)
        return self.session.scalars(statement).all()

    def list_public_by_ticket(
        self,
        ticket_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[TicketComment]:
        return self.list_visible_by_ticket(
            ticket_id,
            include_internal=False,
            offset=offset,
            limit=limit,
        )
