import pytest
from sqlalchemy.orm import Session

from app.repositories.ticket_priority import TicketPriorityRepository
from app.schemas.ticket_priority import TicketPriorityCreate
from app.services.ticket_priority import TicketPriorityService

pytestmark = pytest.mark.integration


def test_ticket_priority_service_lists_ordered_priorities(db_session: Session) -> None:
    service = TicketPriorityService(TicketPriorityRepository(db_session))

    service.create(TicketPriorityCreate(name="Low", sort_order=2))
    high_priority = service.create(TicketPriorityCreate(name="High", sort_order=1))

    assert service.get_by_name("High") == high_priority
    assert [priority.name for priority in service.list_ordered()] == ["High", "Low"]
