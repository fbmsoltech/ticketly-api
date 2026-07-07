from typing import Any

from app.services.exceptions import (
    AuthenticationError,
    AuthorizationError,
    InvalidOperationError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
)

__all__ = [
    "AuthService",
    "AuthenticationError",
    "AuthorizationError",
    "CustomerService",
    "InvalidOperationError",
    "ResourceAlreadyExistsError",
    "ResourceNotFoundError",
    "RoleService",
    "TicketCategoryService",
    "TicketCommentService",
    "TicketPriorityService",
    "TicketService",
    "TicketStatusService",
    "UserService",
]


def __getattr__(name: str) -> Any:
    if name == "AuthService":
        from app.services.auth_service import AuthService

        return AuthService
    if name == "CustomerService":
        from app.services.customer import CustomerService

        return CustomerService
    if name == "RoleService":
        from app.services.role import RoleService

        return RoleService
    if name == "TicketCategoryService":
        from app.services.ticket_category import TicketCategoryService

        return TicketCategoryService
    if name == "TicketCommentService":
        from app.services.ticket_comment_service import TicketCommentService

        return TicketCommentService
    if name == "TicketPriorityService":
        from app.services.ticket_priority import TicketPriorityService

        return TicketPriorityService
    if name == "TicketService":
        from app.services.ticket_service import TicketService

        return TicketService
    if name == "TicketStatusService":
        from app.services.ticket_status import TicketStatusService

        return TicketStatusService
    if name == "UserService":
        from app.services.user import UserService

        return UserService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
