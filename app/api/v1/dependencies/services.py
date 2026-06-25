from hashlib import sha256
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.repositories.customer import CustomerRepository
from app.repositories.role import RoleRepository
from app.repositories.ticket import TicketRepository
from app.repositories.ticket_category import TicketCategoryRepository
from app.repositories.ticket_comment import TicketCommentRepository
from app.repositories.ticket_priority import TicketPriorityRepository
from app.repositories.ticket_status import TicketStatusRepository
from app.repositories.user import UserRepository
from app.services.customer import CustomerService
from app.services.role import RoleService
from app.services.ticket import TicketService
from app.services.ticket_category import TicketCategoryService
from app.services.ticket_comment import TicketCommentService
from app.services.ticket_priority import TicketPriorityService
from app.services.ticket_status import TicketStatusService
from app.services.user import UserService

DatabaseSession = Annotated[Session, Depends(get_db_session)]


def _hash_password(password: str) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


def get_role_service(db: DatabaseSession) -> RoleService:
    return RoleService(RoleRepository(db))


def get_user_service(
    db: DatabaseSession,
) -> UserService:
    return UserService(UserRepository(db), _hash_password)


def get_customer_service(db: DatabaseSession) -> CustomerService:
    return CustomerService(CustomerRepository(db))


def get_ticket_status_service(db: DatabaseSession) -> TicketStatusService:
    return TicketStatusService(TicketStatusRepository(db))


def get_ticket_priority_service(db: DatabaseSession) -> TicketPriorityService:
    return TicketPriorityService(TicketPriorityRepository(db))


def get_ticket_category_service(db: DatabaseSession) -> TicketCategoryService:
    return TicketCategoryService(TicketCategoryRepository(db))


def get_ticket_service(db: DatabaseSession) -> TicketService:
    return TicketService(TicketRepository(db))


def get_ticket_comment_service(db: DatabaseSession) -> TicketCommentService:
    return TicketCommentService(TicketCommentRepository(db))
