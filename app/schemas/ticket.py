from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.schemas.base import ORMModel, TimestampedSchema


class TicketBase(ORMModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    customer_id: int
    category_id: int
    status_id: int
    priority_id: int
    assigned_agent_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("assigned_agent_id", "assignee_id"),
    )


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    customer_id: int | None = None
    category_id: int | None = None
    status_id: int | None = None
    priority_id: int | None = None
    assigned_agent_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("assigned_agent_id", "assignee_id"),
    )


class TicketRead(TicketBase, TimestampedSchema):
    id: int
