import pytest
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket_comment import TicketCommentCreate, TicketCommentUpdate
from app.services.exceptions import ResourceNotFoundError
from app.services.ticket_comment_service import TicketCommentService

pytestmark = pytest.mark.integration


def test_create_comment_with_user_author(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)

    comment = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="We are checking this.", is_internal=False),
    )

    assert comment.ticket_id == ticket.id
    assert comment.author_id == agent_user.id
    assert comment.body == "We are checking this."
    assert comment.is_internal is False


def test_get_comment_by_id(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)
    comment = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Initial analysis."),
    )

    found = service.get_by_id(comment.id)

    assert found.id == comment.id


def test_list_comments_by_ticket(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)
    first = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="First comment."),
    )
    second = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Second comment."),
    )

    comments = service.list_by_ticket(ticket.id)

    assert list(comments) == [first, second]


def test_list_comments_including_internal(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)
    public = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Public note.", is_internal=False),
    )
    internal = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Internal note.", is_internal=True),
    )

    comments = service.list_by_ticket(ticket.id, include_internal=True)

    assert list(comments) == [public, internal]


def test_list_comments_excluding_internal(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)
    public = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Public note.", is_internal=False),
    )
    service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Internal note.", is_internal=True),
    )

    comments = service.list_by_ticket(ticket.id, include_internal=False)

    assert list(comments) == [public]


def test_update_comment_content(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)
    comment = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Before."),
    )

    updated = service.update(comment.id, TicketCommentUpdate(content="After."))

    assert updated.body == "After."
    assert updated.ticket_id == ticket.id
    assert updated.author_id == agent_user.id


def test_update_comment_is_internal(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)
    comment = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Visibility update.", is_internal=False),
    )

    updated = service.update(comment.id, TicketCommentUpdate(is_internal=True))

    assert updated.is_internal is True


def test_delete_comment(
    db_session: Session,
    ticket: Ticket,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)
    comment = service.create_for_user(
        ticket.id,
        agent_user.id,
        TicketCommentCreate(content="Temporary comment."),
    )

    service.delete(comment.id)

    with pytest.raises(ResourceNotFoundError, match="Ticket comment not found."):
        service.get_by_id(comment.id)


def test_create_comment_for_missing_ticket_raises_error(
    db_session: Session,
    agent_user: User,
) -> None:
    service = TicketCommentService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Ticket not found."):
        service.create_for_user(
            999,
            agent_user.id,
            TicketCommentCreate(content="Cannot create this."),
        )


def test_create_comment_with_missing_author_raises_error(
    db_session: Session,
    ticket: Ticket,
) -> None:
    service = TicketCommentService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Author user not found."):
        service.create_for_user(
            ticket.id,
            999,
            TicketCommentCreate(content="Cannot create this."),
        )


def test_get_missing_comment_raises_error(db_session: Session) -> None:
    service = TicketCommentService(db_session)

    with pytest.raises(ResourceNotFoundError, match="Ticket comment not found."):
        service.get_by_id(999)
