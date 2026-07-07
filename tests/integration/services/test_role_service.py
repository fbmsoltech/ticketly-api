import pytest
from sqlalchemy.orm import Session

from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.role import RoleService

pytestmark = pytest.mark.integration


def test_role_service_crud_flow(db_session: Session) -> None:
    service = RoleService(RoleRepository(db_session))

    created = service.create(
        RoleCreate(name="ADMIN", description="Administrators"),
    )
    assert created.id is not None

    updated = service.update(
        created.id,
        RoleUpdate(description="Platform administrators"),
    )
    assert updated is not None
    assert updated.name == "ADMIN"
    assert updated.description == "Platform administrators"
    assert service.get_by_name("ADMIN") == updated
    assert service.delete(created.id) is True
    assert service.get(created.id) is None
    assert service.delete(created.id) is False
