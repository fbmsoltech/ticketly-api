from pydantic import BaseModel, Field

from app.schemas.base import TimestampedSchema


class TicketPriorityBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    sort_order: int


class TicketPriorityCreate(TicketPriorityBase):
    pass


class TicketPriorityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    sort_order: int | None = None


class TicketPriorityRead(TicketPriorityBase, TimestampedSchema):
    id: int
