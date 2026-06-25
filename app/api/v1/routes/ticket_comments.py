from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.services import get_ticket_comment_service
from app.api.v1.routes.common import raise_not_found
from app.models.ticket_comment import TicketComment
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentRead,
    TicketCommentUpdate,
)
from app.services.ticket_comment import TicketCommentService

router = APIRouter(prefix="/ticket-comments", tags=["ticket-comments"])

TicketCommentServiceDependency = Annotated[
    TicketCommentService,
    Depends(get_ticket_comment_service),
]


@router.get("", response_model=list[TicketCommentRead], summary="Lista comentários")
def list_ticket_comments(
    service: TicketCommentServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[TicketComment]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=TicketCommentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um comentário",
)
def create_ticket_comment(
    data: TicketCommentCreate,
    service: TicketCommentServiceDependency,
) -> TicketComment:
    return service.create(data)


@router.get(
    "/{ticket_comment_id}",
    response_model=TicketCommentRead,
    summary="Busca um comentário",
)
def get_ticket_comment(
    ticket_comment_id: int,
    service: TicketCommentServiceDependency,
) -> TicketComment:
    ticket_comment = service.get(ticket_comment_id)
    if ticket_comment is None:
        raise_not_found("Ticket comment")
    return ticket_comment


@router.patch(
    "/{ticket_comment_id}",
    response_model=TicketCommentRead,
    summary="Atualiza um comentário",
)
def update_ticket_comment(
    ticket_comment_id: int,
    data: TicketCommentUpdate,
    service: TicketCommentServiceDependency,
) -> TicketComment:
    ticket_comment = service.update(ticket_comment_id, data)
    if ticket_comment is None:
        raise_not_found("Ticket comment")
    return ticket_comment


@router.delete(
    "/{ticket_comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um comentário",
)
def delete_ticket_comment(
    ticket_comment_id: int,
    service: TicketCommentServiceDependency,
) -> None:
    if not service.delete(ticket_comment_id):
        raise_not_found("Ticket comment")
