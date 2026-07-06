from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.auth import require_roles
from app.api.v1.dependencies.services import get_customer_service
from app.api.v1.routes.common import raise_not_found
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.services.customer import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[Depends(require_roles({"ADMIN", "AGENT"}))],
)

CustomerServiceDependency = Annotated[CustomerService, Depends(get_customer_service)]


@router.get("", response_model=list[CustomerRead], summary="Lista clientes")
def list_customers(
    service: CustomerServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[Customer]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um cliente",
)
def create_customer(
    data: CustomerCreate,
    service: CustomerServiceDependency,
) -> Customer:
    return service.create(data)


@router.get("/{customer_id}", response_model=CustomerRead, summary="Busca um cliente")
def get_customer(
    customer_id: int,
    service: CustomerServiceDependency,
) -> Customer:
    customer = service.get(customer_id)
    if customer is None:
        raise_not_found("Customer")
    return customer


@router.patch(
    "/{customer_id}",
    response_model=CustomerRead,
    summary="Atualiza um cliente",
)
def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    service: CustomerServiceDependency,
) -> Customer:
    customer = service.update(customer_id, data)
    if customer is None:
        raise_not_found("Customer")
    return customer


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um cliente",
)
def delete_customer(customer_id: int, service: CustomerServiceDependency) -> None:
    if not service.delete(customer_id):
        raise_not_found("Customer")
