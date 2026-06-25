from app.models.ticket_priority import TicketPriority
from app.repositories.ticket_priority import TicketPriorityRepository
from app.schemas.ticket_priority import TicketPriorityCreate, TicketPriorityUpdate
from app.services.base import BaseService


class TicketPriorityService(
    BaseService[TicketPriority, TicketPriorityCreate, TicketPriorityUpdate]
):
    def __init__(self, repository: TicketPriorityRepository) -> None:
        super().__init__(repository, TicketPriority)
        self.ticket_priority_repository = repository

    def get_by_name(self, name: str) -> TicketPriority | None:
        return self.ticket_priority_repository.get_by_name(name)

    def list_ordered(self) -> list[TicketPriority]:
        return self.ticket_priority_repository.list_ordered()
