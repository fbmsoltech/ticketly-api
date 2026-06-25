from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket_comment import TicketComment
from app.repositories.base import BaseRepository


class TicketCommentRepository(BaseRepository[TicketComment]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, TicketComment)

    def list_by_ticket(self, ticket_id: int) -> list[TicketComment]:
        statement = select(TicketComment).where(TicketComment.ticket_id == ticket_id)
        return list(self.session.scalars(statement).all())

    def list_public_by_ticket(self, ticket_id: int) -> list[TicketComment]:
        statement = select(TicketComment).where(
            TicketComment.ticket_id == ticket_id,
            TicketComment.is_internal.is_(False),
        )
        return list(self.session.scalars(statement).all())
