from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.services import get_role_service
from app.api.v1.routes.common import raise_not_found
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.services.role import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])

RoleServiceDependency = Annotated[RoleService, Depends(get_role_service)]


@router.get("", response_model=list[RoleRead], summary="Lista papéis")
def list_roles(
    service: RoleServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[Role]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um papel",
)
def create_role(data: RoleCreate, service: RoleServiceDependency) -> Role:
    return service.create(data)


@router.get("/{role_id}", response_model=RoleRead, summary="Busca um papel")
def get_role(role_id: int, service: RoleServiceDependency) -> Role:
    role = service.get(role_id)
    if role is None:
        raise_not_found("Role")
    return role


@router.patch("/{role_id}", response_model=RoleRead, summary="Atualiza um papel")
def update_role(
    role_id: int,
    data: RoleUpdate,
    service: RoleServiceDependency,
) -> Role:
    role = service.update(role_id, data)
    if role is None:
        raise_not_found("Role")
    return role


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um papel",
)
def delete_role(role_id: int, service: RoleServiceDependency) -> None:
    if not service.delete(role_id):
        raise_not_found("Role")
