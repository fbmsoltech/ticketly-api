import pytest
from sqlalchemy.orm import Session

from app.repositories.ticket_status import TicketStatusRepository
from app.schemas.ticket_status import TicketStatusCreate
from app.services.ticket_status import TicketStatusService

pytestmark = pytest.mark.integration


def test_ticket_status_service_lists_ordered_statuses(db_session: Session) -> None:
    service = TicketStatusService(TicketStatusRepository(db_session))

    service.create(TicketStatusCreate(name="Closed", sort_order=2))
    open_status = service.create(TicketStatusCreate(name="Open", sort_order=1))

    assert service.get_by_name("Open") == open_status
    assert [status.name for status in service.list_ordered()] == ["Open", "Closed"]
