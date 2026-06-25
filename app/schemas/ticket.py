from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.base import TimestampedSchema


class TicketBase(BaseModel):
    customer_id: int
    assignee_id: int | None = None
    category_id: int | None = None
    status_id: int
    priority_id: int
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    customer_id: int | None = None
    assignee_id: int | None = None
    category_id: int | None = None
    status_id: int | None = None
    priority_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    closed_at: datetime | None = None


class TicketRead(TicketBase, TimestampedSchema):
    id: int
    closed_at: datetime | None = None
