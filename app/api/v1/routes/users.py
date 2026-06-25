from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.dependencies.services import get_user_service
from app.api.v1.routes.common import raise_not_found
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]


@router.get("", response_model=list[UserRead], summary="Lista usuários")
def list_users(
    service: UserServiceDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> Sequence[User]:
    return list(service.list(offset=offset, limit=limit))


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um usuário",
)
def create_user(data: UserCreate, service: UserServiceDependency) -> User:
    return service.create(data)


@router.get("/{user_id}", response_model=UserRead, summary="Busca um usuário")
def get_user(user_id: int, service: UserServiceDependency) -> User:
    user = service.get(user_id)
    if user is None:
        raise_not_found("User")
    return user


@router.patch("/{user_id}", response_model=UserRead, summary="Atualiza um usuário")
def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserServiceDependency,
) -> User:
    user = service.update(user_id, data)
    if user is None:
        raise_not_found("User")
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove um usuário",
)
def delete_user(user_id: int, service: UserServiceDependency) -> None:
    if not service.delete(user_id):
        raise_not_found("User")
