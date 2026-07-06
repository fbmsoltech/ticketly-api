from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.ticket_comment import TicketComment
from app.repositories.ticket import TicketRepository
from app.repositories.ticket_comment import TicketCommentRepository
from app.repositories.user import UserRepository
from app.schemas.ticket_comment import TicketCommentCreate, TicketCommentUpdate
from app.services.base import BaseService
from app.services.exceptions import ResourceNotFoundError


class TicketCommentService(
    BaseService[TicketComment, TicketCommentCreate, TicketCommentUpdate]
):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.ticket_comment_repository = TicketCommentRepository(session)
        self.ticket_repository = TicketRepository(session)
        self.user_repository = UserRepository(session)
        super().__init__(self.ticket_comment_repository, TicketComment)

    def get_by_id(self, comment_id: int) -> TicketComment:
        comment = self.ticket_comment_repository.get(comment_id)
        if comment is None:
            raise ResourceNotFoundError("Ticket comment not found.")
        return comment

    def get_by_ticket_and_id(self, ticket_id: int, comment_id: int) -> TicketComment:
        self._ensure_ticket_exists(ticket_id)
        comment = self.get_by_id(comment_id)
        if comment.ticket_id != ticket_id:
            raise ResourceNotFoundError("Ticket comment not found.")
        return comment

    def list_by_ticket(
        self,
        ticket_id: int,
        *,
        include_internal: bool = True,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[TicketComment]:
        self._ensure_ticket_exists(ticket_id)
        return self.ticket_comment_repository.list_visible_by_ticket(
            ticket_id,
            include_internal=include_internal,
            offset=offset,
            limit=limit,
        )

    def list_public_by_ticket(
        self,
        ticket_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[TicketComment]:
        return self.list_by_ticket(
            ticket_id,
            include_internal=False,
            offset=offset,
            limit=limit,
        )

    def create_for_user(
        self,
        ticket_id: int,
        author_user_id: int,
        data: TicketCommentCreate,
    ) -> TicketComment:
        try:
            self._ensure_ticket_exists(ticket_id)
            self._ensure_author_user_exists(author_user_id)

            comment = TicketComment(
                ticket_id=ticket_id,
                author_id=author_user_id,
                body=data.content,
                is_internal=data.is_internal,
            )
            created = self.ticket_comment_repository.add(comment)
            self.session.commit()
            self.session.refresh(created)
            return created
        except Exception:
            self.session.rollback()
            raise

    def update(self, comment_id: int, data: TicketCommentUpdate) -> TicketComment:
        try:
            comment = self.get_by_id(comment_id)
            update_data = data.model_dump(exclude_unset=True)

            if "content" in update_data:
                comment.body = update_data["content"]
            if "is_internal" in update_data:
                comment.is_internal = update_data["is_internal"]

            updated = self.ticket_comment_repository.update(comment)
            self.session.commit()
            self.session.refresh(updated)
            return updated
        except Exception:
            self.session.rollback()
            raise

    def delete(self, comment_id: int) -> None:  # type: ignore[override]
        try:
            comment = self.get_by_id(comment_id)
            self.ticket_comment_repository.delete(comment)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def _ensure_ticket_exists(self, ticket_id: int) -> None:
        if self.ticket_repository.get(ticket_id) is None:
            raise ResourceNotFoundError("Ticket not found.")

    def _ensure_author_user_exists(self, author_user_id: int) -> None:
        if self.user_repository.get(author_user_id) is None:
            raise ResourceNotFoundError("Author user not found.")
