from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.services import get_ticket_status_service
from app.api.v1.routes.common import raise_not_found
from app.models.ticket_status import TicketStatus
from app.schemas.ticket_status import (
    TicketStatusCreate,
    TicketStatusRead,
    TicketStatusUpdate,
)
from app.services.ticket_status import TicketStatusService

router = APIRouter(prefix="/ticket-statuses", tags=["ticket-statuses"])

TicketStatusServiceDependency = Annotated[
    TicketStatusService,
    Depends(get_ticket_status_service),
]


@router.get("", response_model=list[TicketStatusRead], summary="Lista status")
def list_ticket_statuses(
    service: TicketStatusServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[TicketStatus]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=TicketStatusRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um status",
)
def create_ticket_status(
    data: TicketStatusCreate,
    service: TicketStatusServiceDependency,
) -> TicketStatus:
    return service.create(data)


@router.get(
    "/{ticket_status_id}",
    response_model=TicketStatusRead,
    summary="Busca um status",
)
def get_ticket_status(
    ticket_status_id: int,
    service: TicketStatusServiceDependency,
) -> TicketStatus:
    ticket_status = service.get(ticket_status_id)
    if ticket_status is None:
        raise_not_found("Ticket status")
    return ticket_status


@router.patch(
    "/{ticket_status_id}",
    response_model=TicketStatusRead,
    summary="Atualiza um status",
)
def update_ticket_status(
    ticket_status_id: int,
    data: TicketStatusUpdate,
    service: TicketStatusServiceDependency,
) -> TicketStatus:
    ticket_status = service.update(ticket_status_id, data)
    if ticket_status is None:
        raise_not_found("Ticket status")
    return ticket_status


@router.delete(
    "/{ticket_status_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um status",
)
def delete_ticket_status(
    ticket_status_id: int,
    service: TicketStatusServiceDependency,
) -> None:
    if not service.delete(ticket_status_id):
        raise_not_found("Ticket status")
