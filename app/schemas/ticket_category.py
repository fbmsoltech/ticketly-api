from pydantic import BaseModel, Field

from app.schemas.base import TimestampedSchema


class TicketCategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class TicketCategoryCreate(TicketCategoryBase):
    pass


class TicketCategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class TicketCategoryRead(TicketCategoryBase, TimestampedSchema):
    id: int
