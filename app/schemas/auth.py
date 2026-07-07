from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role_id: int
    role_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
