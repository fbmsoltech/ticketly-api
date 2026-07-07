from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.auth import require_admin
from app.api.v1.dependencies.services import get_ticket_priority_service
from app.api.v1.routes.common import raise_not_found
from app.models.ticket_priority import TicketPriority
from app.schemas.ticket_priority import (
    TicketPriorityCreate,
    TicketPriorityRead,
    TicketPriorityUpdate,
)
from app.services.ticket_priority import TicketPriorityService

router = APIRouter(
    prefix="/ticket-priorities",
    tags=["ticket-priorities"],
    dependencies=[Depends(require_admin)],
)

TicketPriorityServiceDependency = Annotated[
    TicketPriorityService,
    Depends(get_ticket_priority_service),
]


@router.get("", response_model=list[TicketPriorityRead], summary="Lista prioridades")
def list_ticket_priorities(
    service: TicketPriorityServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[TicketPriority]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=TicketPriorityRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma prioridade",
)
def create_ticket_priority(
    data: TicketPriorityCreate,
    service: TicketPriorityServiceDependency,
) -> TicketPriority:
    return service.create(data)


@router.get(
    "/{ticket_priority_id}",
    response_model=TicketPriorityRead,
    summary="Busca uma prioridade",
)
def get_ticket_priority(
    ticket_priority_id: int,
    service: TicketPriorityServiceDependency,
) -> TicketPriority:
    ticket_priority = service.get(ticket_priority_id)
    if ticket_priority is None:
        raise_not_found("Ticket priority")
    return ticket_priority


@router.patch(
    "/{ticket_priority_id}",
    response_model=TicketPriorityRead,
    summary="Atualiza uma prioridade",
)
def update_ticket_priority(
    ticket_priority_id: int,
    data: TicketPriorityUpdate,
    service: TicketPriorityServiceDependency,
) -> TicketPriority:
    ticket_priority = service.update(ticket_priority_id, data)
    if ticket_priority is None:
        raise_not_found("Ticket priority")
    return ticket_priority


@router.delete(
    "/{ticket_priority_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove uma prioridade",
)
def delete_ticket_priority(
    ticket_priority_id: int,
    service: TicketPriorityServiceDependency,
) -> None:
    if not service.delete(ticket_priority_id):
        raise_not_found("Ticket priority")
