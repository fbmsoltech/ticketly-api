from app.models.ticket_comment import TicketComment
from app.repositories.ticket_comment import TicketCommentRepository
from app.schemas.ticket_comment import TicketCommentCreate, TicketCommentUpdate
from app.services.base import BaseService


class TicketCommentService(
    BaseService[TicketComment, TicketCommentCreate, TicketCommentUpdate]
):
    def __init__(self, repository: TicketCommentRepository) -> None:
        super().__init__(repository, TicketComment)
        self.ticket_comment_repository = repository

    def list_by_ticket(self, ticket_id: int) -> list[TicketComment]:
        return self.ticket_comment_repository.list_by_ticket(ticket_id)

    def list_public_by_ticket(self, ticket_id: int) -> list[TicketComment]:
        return self.ticket_comment_repository.list_public_by_ticket(ticket_id)
