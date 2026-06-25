from app.models.role import Role
from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.base import BaseService


class RoleService(BaseService[Role, RoleCreate, RoleUpdate]):
    def __init__(self, repository: RoleRepository) -> None:
        super().__init__(repository, Role)
        self.role_repository = repository

    def get_by_name(self, name: str) -> Role | None:
        return self.role_repository.get_by_name(name)
