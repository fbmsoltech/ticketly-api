import pytest
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.ticket import Ticket
from app.models.ticket_category import TicketCategory
from app.models.ticket_priority import TicketPriority
from app.models.ticket_status import TicketStatus
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.services.exceptions import InvalidOperationError, ResourceNotFoundError
from app.services.ticket_service import TicketService

pytestmark = pytest.mark.integration


def _create_payload(
    *,
    customer: Customer,
    category: TicketCategory,
    status: TicketStatus,
    priority: TicketPriority,
    assigned_agent: User | None = None,
) -> TicketCreate:
    return TicketCreate(
        title="Cannot access dashboard",
        description="The dashboard returns an error.",
        customer_id=customer.id,
        category_id=category.id,
        status_id=status.id,
        priority_id=priority.id,
        assigned_agent_id=assigned_agent.id if assigned_agent else None,
    )


def test_creates_ticket_successfully(
    db_session: Session,
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
) -> None:
    service = TicketService(db_session)

    ticket = service.create(
        _create_payload(
            customer=customer,
            category=ticket_category,
            status=ticket_status,
            priority=ticket_priority,
        )
    )

    assert ticket.id is not None
    assert ticket.title == "Cannot access dashboard"


def test_gets_ticket_by_id(db_session: Session, ticket: Ticket) -> None:
    service = TicketService(db_session)

    found = service.get_by_id(ticket.id)

    assert found.id == ticket.id


def test_lists_tickets(db_session: Session, ticket: Ticket) -> None:
    service = TicketService(db_session)

    tickets = service.list()

    assert ticket.id in [item.id for item in tickets]


def test_lists_tickets_by_customer_status_and_assigned_agent(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketService(db_session)
    service.update(ticket.id, TicketUpdate(assigned_agent_id=agent_user.id))

    assert service.list_by_customer(ticket.customer_id) == [ticket]
    assert service.list_by_status(ticket.status_id) == [ticket]
    assert service.list_by_assigned_agent(agent_user.id) == [ticket]


def test_updates_title_and_description(db_session: Session, ticket: Ticket) -> None:
    service = TicketService(db_session)

    updated = service.update(
        ticket.id,
        TicketUpdate(title="Cannot access reports", description="Reports fail."),
    )

    assert updated.title == "Cannot access reports"
    assert updated.description == "Reports fail."


def test_updates_status(
    db_session: Session,
    ticket: Ticket,
    second_ticket_status: TicketStatus,
) -> None:
    service = TicketService(db_session)

    updated = service.update(ticket.id, TicketUpdate(status_id=second_ticket_status.id))

    assert updated.status_id == second_ticket_status.id


def test_assigns_ticket_to_agent(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketService(db_session)

    updated = service.update(ticket.id, TicketUpdate(assigned_agent_id=agent_user.id))

    assert updated.assignee_id == agent_user.id


def test_assigns_ticket_to_admin(
    db_session: Session,
    ticket: Ticket,
    admin_user: User,
) -> None:
    service = TicketService(db_session)

    updated = service.update(ticket.id, TicketUpdate(assigned_agent_id=admin_user.id))

    assert updated.assignee_id == admin_user.id


def test_rejects_assignment_to_customer(
    db_session: Session,
    ticket: Ticket,
    customer_user: User,
) -> None:
    service = TicketService(db_session)

    with pytest.raises(InvalidOperationError, match="agent or admin"):
        service.update(ticket.id, TicketUpdate(assigned_agent_id=customer_user.id))


def test_create_fails_with_missing_customer(
    db_session: Session,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
) -> None:
    service = TicketService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Customer not found"):
        service.create(
            TicketCreate(
                title="Missing customer",
                description="Customer does not exist.",
                customer_id=9999,
                category_id=ticket_category.id,
                status_id=ticket_status.id,
                priority_id=ticket_priority.id,
            )
        )


def test_create_fails_with_missing_category(
    db_session: Session,
    customer: Customer,
    ticket_status: TicketStatus,
    ticket_priority: TicketPriority,
) -> None:
    service = TicketService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Ticket category not found"):
        service.create(
            TicketCreate(
                title="Missing category",
                description="Category does not exist.",
                customer_id=customer.id,
                category_id=9999,
                status_id=ticket_status.id,
                priority_id=ticket_priority.id,
            )
        )


def test_create_fails_with_missing_status(
    db_session: Session,
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_priority: TicketPriority,
) -> None:
    service = TicketService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Ticket status not found"):
        service.create(
            TicketCreate(
                title="Missing status",
                description="Status does not exist.",
                customer_id=customer.id,
                category_id=ticket_category.id,
                status_id=9999,
                priority_id=ticket_priority.id,
            )
        )


def test_create_fails_with_missing_priority(
    db_session: Session,
    customer: Customer,
    ticket_category: TicketCategory,
    ticket_status: TicketStatus,
) -> None:
    service = TicketService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Ticket priority not found"):
        service.create(
            TicketCreate(
                title="Missing priority",
                description="Priority does not exist.",
                customer_id=customer.id,
                category_id=ticket_category.id,
                status_id=ticket_status.id,
                priority_id=9999,
            )
        )


def test_get_missing_ticket_raises_not_found(db_session: Session) -> None:
    service = TicketService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Ticket not found"):
        service.get_by_id(9999)


def test_deletes_ticket(db_session: Session, ticket: Ticket) -> None:
    service = TicketService(db_session)

    service.delete(ticket.id)

    with pytest.raises(ResourceNotFoundError, match="Ticket not found"):
        service.get_by_id(ticket.id)
