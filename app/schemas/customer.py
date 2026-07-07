from pydantic import BaseModel, Field

from app.schemas.base import TimestampedSchema


class CustomerBase(BaseModel):
    user_id: int
    company_name: str | None = Field(default=None, max_length=150)
    phone: str | None = Field(default=None, max_length=30)


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    user_id: int | None = None
    company_name: str | None = Field(default=None, max_length=150)
    phone: str | None = Field(default=None, max_length=30)


class CustomerRead(CustomerBase, TimestampedSchema):
    id: int
