from app.repositories.customer import CustomerRepository
from app.repositories.role import RoleRepository
from app.repositories.ticket import TicketRepository
from app.repositories.ticket_category import TicketCategoryRepository
from app.repositories.ticket_comment import TicketCommentRepository
from app.repositories.ticket_priority import TicketPriorityRepository
from app.repositories.ticket_status import TicketStatusRepository
from app.repositories.user import UserRepository

__all__ = [
    "CustomerRepository",
    "RoleRepository",
    "TicketCategoryRepository",
    "TicketCommentRepository",
    "TicketPriorityRepository",
    "TicketRepository",
    "TicketStatusRepository",
    "UserRepository",
]
