from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.v1.dependencies.auth import get_current_user
from app.api.v1.dependencies.services import get_auth_service
from app.models.user import User
from app.schemas.auth import CurrentUserRead, LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserDependency = Annotated[User, Depends(get_current_user)]


@router.post("/login", response_model=TokenResponse, summary="Autentica usuario")
def login(data: LoginRequest, service: AuthServiceDependency) -> TokenResponse:
    return TokenResponse(access_token=service.login(data.email, data.password))


@router.get("/me", response_model=CurrentUserRead, summary="Busca usuario atual")
def get_me(current_user: CurrentUserDependency) -> CurrentUserRead:
    return CurrentUserRead(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role_id=current_user.role_id,
        role_name=current_user.role.name,
        is_active=current_user.is_active,
    )
