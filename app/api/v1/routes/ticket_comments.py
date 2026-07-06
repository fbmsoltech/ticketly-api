from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.auth import require_admin, require_roles
from app.api.v1.dependencies.services import get_ticket_comment_service
from app.models.ticket_comment import TicketComment
from app.models.user import User
from app.schemas.ticket_comment import (
    TicketCommentCreate,
    TicketCommentRead,
    TicketCommentUpdate,
)
from app.services.ticket_comment_service import TicketCommentService

router = APIRouter(
    prefix="/tickets/{ticket_id}/comments",
    tags=["Ticket Comments"],
)

TicketCommentServiceDependency = Annotated[
    TicketCommentService,
    Depends(get_ticket_comment_service),
]
AdminOrAgentDependency = Annotated[
    User,
    Depends(require_roles({"ADMIN", "AGENT"})),
]
AdminDependency = Annotated[User, Depends(require_admin)]


@router.post(
    "",
    response_model=TicketCommentRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria comentario de ticket",
)
def create_ticket_comment(
    ticket_id: int,
    data: TicketCommentCreate,
    service: TicketCommentServiceDependency,
    current_user: AdminOrAgentDependency,
) -> TicketComment:
    return service.create_for_user(
        ticket_id=ticket_id,
        author_user_id=current_user.id,
        data=data,
    )


@router.get(
    "",
    response_model=list[TicketCommentRead],
    summary="Lista comentarios do ticket",
)
def list_ticket_comments(
    ticket_id: int,
    service: TicketCommentServiceDependency,
    _current_user: AdminOrAgentDependency,
    include_internal: bool = True,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[TicketComment]:
    return service.list_by_ticket(
        ticket_id,
        include_internal=include_internal,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{comment_id}",
    response_model=TicketCommentRead,
    summary="Busca comentario do ticket",
)
def get_ticket_comment(
    ticket_id: int,
    comment_id: int,
    service: TicketCommentServiceDependency,
    _current_user: AdminOrAgentDependency,
) -> TicketComment:
    return service.get_by_ticket_and_id(ticket_id, comment_id)


@router.patch(
    "/{comment_id}",
    response_model=TicketCommentRead,
    summary="Atualiza comentario do ticket",
)
def update_ticket_comment(
    ticket_id: int,
    comment_id: int,
    data: TicketCommentUpdate,
    service: TicketCommentServiceDependency,
    _current_user: AdminOrAgentDependency,
) -> TicketComment:
    service.get_by_ticket_and_id(ticket_id, comment_id)
    return service.update(comment_id, data)


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove comentario do ticket",
)
def delete_ticket_comment(
    ticket_id: int,
    comment_id: int,
    service: TicketCommentServiceDependency,
    _current_user: AdminDependency,
) -> None:
    service.get_by_ticket_and_id(ticket_id, comment_id)
    service.delete(comment_id)
