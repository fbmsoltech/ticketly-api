from app.models.ticket_status import TicketStatus
from app.repositories.ticket_status import TicketStatusRepository
from app.schemas.ticket_status import TicketStatusCreate, TicketStatusUpdate
from app.services.base import BaseService


class TicketStatusService(
    BaseService[TicketStatus, TicketStatusCreate, TicketStatusUpdate]
):
    def __init__(self, repository: TicketStatusRepository) -> None:
        super().__init__(repository, TicketStatus)
        self.ticket_status_repository = repository

    def get_by_name(self, name: str) -> TicketStatus | None:
        return self.ticket_status_repository.get_by_name(name)

    def list_ordered(self) -> list[TicketStatus]:
        return self.ticket_status_repository.list_ordered()
