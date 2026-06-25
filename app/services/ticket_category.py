from app.models.ticket_category import TicketCategory
from app.repositories.ticket_category import TicketCategoryRepository
from app.schemas.ticket_category import TicketCategoryCreate, TicketCategoryUpdate
from app.services.base import BaseService


class TicketCategoryService(
    BaseService[TicketCategory, TicketCategoryCreate, TicketCategoryUpdate]
):
    def __init__(self, repository: TicketCategoryRepository) -> None:
        super().__init__(repository, TicketCategory)
        self.ticket_category_repository = repository

    def get_by_name(self, name: str) -> TicketCategory | None:
        return self.ticket_category_repository.get_by_name(name)

    def list_active(self) -> list[TicketCategory]:
        return self.ticket_category_repository.list_active()
