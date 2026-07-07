from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base import Base


class BaseRepository[ModelType: Base]:
    def __init__(self, session: Session, model: type[ModelType]) -> None:
        self.session = session
        self.model = model

    def get(self, entity_id: int) -> ModelType | None:
        return self.session.get(self.model, entity_id)

    def list(self, *, offset: int = 0, limit: int = 100) -> Sequence[ModelType]:
        statement = select(self.model).offset(offset).limit(limit)
        return self.session.scalars(statement).all()

    def add(self, entity: ModelType) -> ModelType:
        self.session.add(entity)
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def update(self, entity: ModelType) -> ModelType:
        self.session.flush()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: ModelType) -> None:
        self.session.delete(entity)
        self.session.flush()
