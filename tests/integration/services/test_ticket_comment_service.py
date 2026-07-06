import pytest
from sqlalchemy.orm import Session

from app.repositories.ticket_comment import TicketCommentRepository
from app.schemas.ticket_comment import TicketCommentCreate
from app.services.ticket_comment import TicketCommentService
from tests.factories import (
    create_customer,
    create_role,
    create_ticket,
    create_ticket_category,
    create_ticket_priority,
    create_ticket_status,
    create_user,
)

pytestmark = pytest.mark.integration


def test_ticket_comment_service_filters_comments(db_session: Session) -> None:
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
    service = TicketCommentService(TicketCommentRepository(db_session))

    public_comment = service.create(
        TicketCommentCreate(
            ticket_id=ticket.id,
            author_id=assignee.id,
            body="We are checking this.",
            is_internal=False,
        ),
    )
    service.create(
        TicketCommentCreate(
            ticket_id=ticket.id,
            author_id=assignee.id,
            body="Escalated internally.",
            is_internal=True,
        ),
    )

    assert service.list_by_ticket(ticket.id) == ticket.comments
    assert service.list_public_by_ticket(ticket.id) == [public_comment]
