from pydantic import BaseModel, Field

from app.schemas.base import TimestampedSchema


class TicketCommentBase(BaseModel):
    ticket_id: int
    author_id: int
    body: str = Field(min_length=1)
    is_internal: bool = False


class TicketCommentCreate(TicketCommentBase):
    pass


class TicketCommentUpdate(BaseModel):
    body: str | None = Field(default=None, min_length=1)
    is_internal: bool | None = None


class TicketCommentRead(TicketCommentBase, TimestampedSchema):
    id: int
