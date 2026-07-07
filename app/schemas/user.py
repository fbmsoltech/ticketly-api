from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import TimestampedSchema


class UserBase(BaseModel):
    role_id: int
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)


class UserUpdate(BaseModel):
    role_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=120)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=255)
    is_active: bool | None = None


class UserRead(UserBase, TimestampedSchema):
    id: int
