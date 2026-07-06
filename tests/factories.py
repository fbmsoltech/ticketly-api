from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.customer import Customer
from app.models.role import Role
from app.models.ticket import Ticket
from app.models.ticket_category import TicketCategory
from app.models.ticket_priority import TicketPriority
from app.models.ticket_status import TicketStatus
from app.models.user import User


def create_role(session: Session, *, name: str = "AGENT") -> Role:
    role = Role(name=name, description=f"{name} role")
    session.add(role)
    session.flush()
    session.refresh(role)
    return role


def create_user(
    session: Session,
    *,
    role: Role | None = None,
    email: str = "agent@example.com",
    name: str = "Agent User",
    password: str = "secret123",
    is_active: bool = True,
) -> User:
    user_role = role or create_role(session)
    user = User(
        role_id=user_role.id,
        name=name,
        email=email,
        hashed_password=get_password_hash(password),
        is_active=is_active,
    )
    session.add(user)
    session.flush()
    session.refresh(user)
    return user


def create_customer(session: Session, *, user: User | None = None) -> Customer:
    customer_user = user or create_user(session, email="customer@example.com")
    customer = Customer(
        user_id=customer_user.id,
        company_name="Acme Inc.",
        phone="+55 11 99999-0000",
    )
    session.add(customer)
    session.flush()
    session.refresh(customer)
    return customer


def create_ticket_status(
    session: Session,
    *,
    name: str = "Open",
    sort_order: int = 1,
) -> TicketStatus:
    status = TicketStatus(
        name=name, description=f"{name} status", sort_order=sort_order
    )
    session.add(status)
    session.flush()
    session.refresh(status)
    return status


def create_ticket_priority(
    session: Session,
    *,
    name: str = "High",
    sort_order: int = 1,
) -> TicketPriority:
    priority = TicketPriority(
        name=name,
        description=f"{name} priority",
        sort_order=sort_order,
    )
    session.add(priority)
    session.flush()
    session.refresh(priority)
    return priority


def create_ticket_category(
    session: Session,
    *,
    name: str = "Support",
    is_active: bool = True,
) -> TicketCategory:
    category = TicketCategory(
        name=name,
        description=f"{name} category",
        is_active=is_active,
    )
    session.add(category)
    session.flush()
    session.refresh(category)
    return category


def create_ticket(
    session: Session,
    *,
    customer: Customer | None = None,
    assignee: User | None = None,
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    category: TicketCategory | None = None,
) -> Ticket:
    ticket_customer = customer or create_customer(session)
    ticket_status = status or create_ticket_status(session)
    ticket_priority = priority or create_ticket_priority(session)
    ticket = Ticket(
        customer_id=ticket_customer.id,
        assignee_id=assignee.id if assignee else None,
        category_id=category.id if category else None,
        status_id=ticket_status.id,
        priority_id=ticket_priority.id,
        title="Cannot access dashboard",
        description="The dashboard returns an error.",
    )
    session.add(ticket)
    session.flush()
    session.refresh(ticket)
    return ticket
