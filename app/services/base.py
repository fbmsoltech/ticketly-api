from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel

from app.db.base import Base
from app.repositories.base import BaseRepository


class BaseService[
    ModelType: Base,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
]:
    def __init__(
        self,
        repository: BaseRepository[ModelType],
        model: type[ModelType],
    ) -> None:
        self.repository = repository
        self.model = model

    def get(self, entity_id: int) -> ModelType | None:
        return self.repository.get(entity_id)

    def list(self, *, offset: int = 0, limit: int = 100) -> Sequence[ModelType]:
        return self.repository.list(offset=offset, limit=limit)

    def create(self, data: CreateSchemaType) -> ModelType:
        entity = self._build_entity(data.model_dump())
        return self.repository.add(entity)

    def update(self, entity_id: int, data: UpdateSchemaType) -> ModelType | None:
        entity = self.repository.get(entity_id)
        if entity is None:
            return None

        for field_name, value in self._get_update_data(data).items():
            setattr(entity, field_name, value)

        return self.repository.update(entity)

    def delete(self, entity_id: int) -> bool:
        entity = self.repository.get(entity_id)
        if entity is None:
            return False

        self.repository.delete(entity)
        return True

    def _build_entity(self, data: dict[str, Any]) -> ModelType:
        return self.model(**data)

    def _get_update_data(self, data: UpdateSchemaType) -> dict[str, Any]:
        return data.model_dump(exclude_unset=True)
