from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.schemas.base import TimestampedSchema


class TicketCommentCreate(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    content: str = Field(
        min_length=1,
        validation_alias=AliasChoices("content", "body"),
    )
    is_internal: bool = False


class TicketCommentUpdate(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    content: str | None = Field(
        default=None,
        min_length=1,
        validation_alias=AliasChoices("content", "body"),
    )
    is_internal: bool | None = None


class TicketCommentRead(TimestampedSchema):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )

    id: int
    ticket_id: int
    author_user_id: int = Field(
        validation_alias=AliasChoices("author_user_id", "author_id"),
    )
    author_customer_id: int | None = None
    content: str = Field(validation_alias=AliasChoices("content", "body"))
    is_internal: bool
