from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def get_metadata_schema(database_schema: str) -> str | None:
    if database_schema == "public":
        return None

    return database_schema


class Base(DeclarativeBase):
    metadata = MetaData(schema=get_metadata_schema(settings.database_schema))
