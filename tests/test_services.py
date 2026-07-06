from sqlalchemy.orm import Session

from app.repositories.customer import CustomerRepository
from app.repositories.role import RoleRepository
from app.repositories.ticket import TicketRepository
from app.repositories.ticket_category import TicketCategoryRepository
from app.repositories.ticket_comment import TicketCommentRepository
from app.repositories.ticket_priority import TicketPriorityRepository
from app.repositories.ticket_status import TicketStatusRepository
from app.schemas.role import RoleCreate, RoleUpdate
from app.schemas.ticket_category import TicketCategoryCreate
from app.schemas.ticket_comment import TicketCommentCreate
from app.schemas.ticket_priority import TicketPriorityCreate
from app.schemas.ticket_status import TicketStatusCreate
from app.schemas.user import UserCreate, UserUpdate
from app.services.customer import CustomerService
from app.services.role import RoleService
from app.services.ticket import TicketService
from app.services.ticket_category import TicketCategoryService
from app.services.ticket_comment import TicketCommentService
from app.services.ticket_priority import TicketPriorityService
from app.services.ticket_status import TicketStatusService
from app.services.user import UserService
from tests.factories import (
    create_customer,
    create_role,
    create_ticket,
    create_ticket_category,
    create_ticket_priority,
    create_ticket_status,
    create_user,
)


def test_base_service_crud_flow(db_session: Session) -> None:
    service = RoleService(RoleRepository(db_session))

    created = service.create(
        RoleCreate(name="ADMIN", description="Administrators"),
    )
    assert created.id is not None

    updated = service.update(
        created.id,
        RoleUpdate(description="Platform administrators"),
    )
    assert updated is not None
    assert updated.name == "ADMIN"
    assert updated.description == "Platform administrators"
    assert service.get_by_name("ADMIN") == updated
    assert service.delete(created.id) is True
    assert service.get(created.id) is None
    assert service.delete(created.id) is False


def test_user_service_hashes_password_on_create_and_update(
    db_session: Session,
) -> None:
    role = create_role(db_session)
    service = UserService(db_session)

    user = service.create(
        UserCreate(
            role_id=role.id,
            name="Jane Agent",
            email="jane@example.com",
            password="secret123",
            is_active=True,
        ),
    )
    assert user.hashed_password != "secret123"
    assert service.get_by_email("jane@example.com") == user
    assert service.list_by_role(role.id) == [user]

    old_hash = user.hashed_password
    updated = service.update(user.id, UserUpdate(password="newsecret123"))
    assert updated.hashed_password != old_hash
    assert updated.hashed_password != "newsecret123"


def test_lookup_services_delegate_special_queries(db_session: Session) -> None:
    status_service = TicketStatusService(TicketStatusRepository(db_session))
    priority_service = TicketPriorityService(TicketPriorityRepository(db_session))
    category_service = TicketCategoryService(TicketCategoryRepository(db_session))

    status_service.create(TicketStatusCreate(name="Closed", sort_order=2))
    open_status = status_service.create(TicketStatusCreate(name="Open", sort_order=1))
    priority_service.create(TicketPriorityCreate(name="Low", sort_order=2))
    high_priority = priority_service.create(
        TicketPriorityCreate(name="High", sort_order=1),
    )
    active_category = category_service.create(
        TicketCategoryCreate(name="Billing", is_active=True),
    )
    category_service.create(TicketCategoryCreate(name="Legacy", is_active=False))

    assert status_service.get_by_name("Open") == open_status
    assert [status.name for status in status_service.list_ordered()] == [
        "Open",
        "Closed",
    ]
    assert priority_service.get_by_name("High") == high_priority
    assert [priority.name for priority in priority_service.list_ordered()] == [
        "High",
        "Low",
    ]
    assert category_service.list_active() == [active_category]


def test_customer_ticket_and_comment_services_filter_entities(
    db_session: Session,
) -> None:
    role = create_role(db_session)
    customer_user = create_user(db_session, role=role, email="customer@example.com")
    assignee = create_user(db_session, role=role, email="agent@example.com")
    customer = create_customer(db_session, user=customer_user)
    status = create_ticket_status(db_session)
    priority = create_ticket_priority(db_session)
    category = create_ticket_category(db_session)
    ticket = create_ticket(
        db_session,
        customer=customer,
        assignee=assignee,
        status=status,
        priority=priority,
        category=category,
    )

    customer_service = CustomerService(CustomerRepository(db_session))
    ticket_service = TicketService(TicketRepository(db_session))
    comment_service = TicketCommentService(TicketCommentRepository(db_session))

    public_comment = comment_service.create(
        TicketCommentCreate(
            ticket_id=ticket.id,
            author_id=assignee.id,
            body="We are checking this.",
            is_internal=False,
        ),
    )
    comment_service.create(
        TicketCommentCreate(
            ticket_id=ticket.id,
            author_id=assignee.id,
            body="Escalated internally.",
            is_internal=True,
        ),
    )

    assert customer_service.get_by_user_id(customer_user.id) == customer
    assert ticket_service.list_by_assignee(assignee.id) == [ticket]
    assert ticket_service.list_by_customer(customer.id) == [ticket]
    assert ticket_service.list_by_status(status.id) == [ticket]
    assert comment_service.list_by_ticket(ticket.id) == ticket.comments
    assert comment_service.list_public_by_ticket(ticket.id) == [public_comment]
