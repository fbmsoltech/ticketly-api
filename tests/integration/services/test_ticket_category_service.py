import pytest
from sqlalchemy.orm import Session

from app.repositories.ticket_category import TicketCategoryRepository
from app.schemas.ticket_category import TicketCategoryCreate
from app.services.ticket_category import TicketCategoryService

pytestmark = pytest.mark.integration


def test_ticket_category_service_lists_active_categories(db_session: Session) -> None:
    service = TicketCategoryService(TicketCategoryRepository(db_session))

    active_category = service.create(
        TicketCategoryCreate(name="Billing", is_active=True),
    )
    service.create(TicketCategoryCreate(name="Legacy", is_active=False))

    assert service.list_active() == [active_category]
