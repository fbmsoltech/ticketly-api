from app.models.ticket import Ticket
from app.repositories.ticket import TicketRepository
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.services.base import BaseService


class TicketService(BaseService[Ticket, TicketCreate, TicketUpdate]):
    def __init__(self, repository: TicketRepository) -> None:
        super().__init__(repository, Ticket)
        self.ticket_repository = repository

    def list_by_assignee(self, assignee_id: int) -> list[Ticket]:
        return self.ticket_repository.list_by_assignee(assignee_id)

    def list_by_customer(self, customer_id: int) -> list[Ticket]:
        return self.ticket_repository.list_by_customer(customer_id)

    def list_by_status(self, status_id: int) -> list[Ticket]:
        return self.ticket_repository.list_by_status(status_id)
