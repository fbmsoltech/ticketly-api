from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.auth import require_admin, require_roles
from app.api.v1.dependencies.services import get_ticket_service
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Tickets"])

TicketServiceDependency = Annotated[TicketService, Depends(get_ticket_service)]
AdminOrAgentDependency = Annotated[
    object,
    Depends(require_roles({"ADMIN", "AGENT"})),
]
AdminDependency = Annotated[object, Depends(require_admin)]


@router.get("", response_model=list[TicketRead], summary="Lista tickets")
def list_tickets(
    service: TicketServiceDependency,
    _current_user: AdminOrAgentDependency,
    customer_id: int | None = None,
    status_id: int | None = None,
    priority_id: int | None = None,
    assigned_agent_id: int | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[Ticket]:
    return service.list_filtered(
        customer_id=customer_id,
        status_id=status_id,
        priority_id=priority_id,
        assigned_agent_id=assigned_agent_id,
        offset=offset,
        limit=limit,
    )


@router.post(
    "",
    response_model=TicketRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um ticket",
)
def create_ticket(
    data: TicketCreate,
    service: TicketServiceDependency,
    _current_user: AdminOrAgentDependency,
) -> Ticket:
    return service.create(data)


@router.get("/{ticket_id}", response_model=TicketRead, summary="Busca um ticket")
def get_ticket(
    ticket_id: int,
    service: TicketServiceDependency,
    _current_user: AdminOrAgentDependency,
) -> Ticket:
    return service.get_by_id(ticket_id)


@router.patch(
    "/{ticket_id}",
    response_model=TicketRead,
    summary="Atualiza um ticket",
)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    service: TicketServiceDependency,
    _current_user: AdminOrAgentDependency,
) -> Ticket:
    return service.update(ticket_id, data)


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um ticket",
)
def delete_ticket(
    ticket_id: int,
    service: TicketServiceDependency,
    _current_user: AdminDependency,
) -> None:
    service.delete(ticket_id)
