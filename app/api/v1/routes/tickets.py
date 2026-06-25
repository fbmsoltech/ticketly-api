from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.services import get_ticket_service
from app.api.v1.routes.common import raise_not_found
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.services.ticket import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])

TicketServiceDependency = Annotated[TicketService, Depends(get_ticket_service)]


@router.get("", response_model=list[TicketRead], summary="Lista tickets")
def list_tickets(
    service: TicketServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[Ticket]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um ticket",
)
def create_ticket(data: TicketCreate, service: TicketServiceDependency) -> Ticket:
    return service.create(data)


@router.get("/{ticket_id}", response_model=TicketRead, summary="Busca um ticket")
def get_ticket(ticket_id: int, service: TicketServiceDependency) -> Ticket:
    ticket = service.get(ticket_id)
    if ticket is None:
        raise_not_found("Ticket")
    return ticket


@router.patch(
    "/{ticket_id}",
    response_model=TicketRead,
    summary="Atualiza um ticket",
)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    service: TicketServiceDependency,
) -> Ticket:
    ticket = service.update(ticket_id, data)
    if ticket is None:
        raise_not_found("Ticket")
    return ticket


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um ticket",
)
def delete_ticket(ticket_id: int, service: TicketServiceDependency) -> None:
    if not service.delete(ticket_id):
        raise_not_found("Ticket")
