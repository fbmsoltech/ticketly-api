from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.auth import require_admin
from app.api.v1.dependencies.services import get_ticket_category_service
from app.api.v1.routes.common import raise_not_found
from app.models.ticket_category import TicketCategory
from app.schemas.ticket_category import (
    TicketCategoryCreate,
    TicketCategoryRead,
    TicketCategoryUpdate,
)
from app.services.ticket_category import TicketCategoryService

router = APIRouter(
    prefix="/ticket-categories",
    tags=["ticket-categories"],
    dependencies=[Depends(require_admin)],
)

TicketCategoryServiceDependency = Annotated[
    TicketCategoryService,
    Depends(get_ticket_category_service),
]


@router.get("", response_model=list[TicketCategoryRead], summary="Lista categorias")
def list_ticket_categories(
    service: TicketCategoryServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[TicketCategory]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=TicketCategoryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma categoria",
)
def create_ticket_category(
    data: TicketCategoryCreate,
    service: TicketCategoryServiceDependency,
) -> TicketCategory:
    return service.create(data)


@router.get(
    "/{ticket_category_id}",
    response_model=TicketCategoryRead,
    summary="Busca uma categoria",
)
def get_ticket_category(
    ticket_category_id: int,
    service: TicketCategoryServiceDependency,
) -> TicketCategory:
    ticket_category = service.get(ticket_category_id)
    if ticket_category is None:
        raise_not_found("Ticket category")
    return ticket_category


@router.patch(
    "/{ticket_category_id}",
    response_model=TicketCategoryRead,
    summary="Atualiza uma categoria",
)
def update_ticket_category(
    ticket_category_id: int,
    data: TicketCategoryUpdate,
    service: TicketCategoryServiceDependency,
) -> TicketCategory:
    ticket_category = service.update(ticket_category_id, data)
    if ticket_category is None:
        raise_not_found("Ticket category")
    return ticket_category


@router.delete(
    "/{ticket_category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove uma categoria",
)
def delete_ticket_category(
    ticket_category_id: int,
    service: TicketCategoryServiceDependency,
) -> None:
    if not service.delete(ticket_category_id):
        raise_not_found("Ticket category")
