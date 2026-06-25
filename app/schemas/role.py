from pydantic import BaseModel, Field

from app.schemas.base import TimestampedSchema


class RoleBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class RoleRead(RoleBase, TimestampedSchema):
    id: int
