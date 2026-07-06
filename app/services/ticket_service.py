from collections.abc import Sequence
from typing import Any

from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.user import User
from app.repositories.customer import CustomerRepository
from app.repositories.ticket import TicketRepository
from app.repositories.ticket_category import TicketCategoryRepository
from app.repositories.ticket_priority import TicketPriorityRepository
from app.repositories.ticket_status import TicketStatusRepository
from app.repositories.user import UserRepository
from app.schemas.ticket import TicketCreate, TicketUpdate
from app.services.base import BaseService
from app.services.exceptions import InvalidOperationError, ResourceNotFoundError

_MISSING = object()


class TicketService(BaseService[Ticket, TicketCreate, TicketUpdate]):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.ticket_repository = TicketRepository(session)
        self.customer_repository = CustomerRepository(session)
        self.category_repository = TicketCategoryRepository(session)
        self.status_repository = TicketStatusRepository(session)
        self.priority_repository = TicketPriorityRepository(session)
        self.user_repository = UserRepository(session)
        super().__init__(self.ticket_repository, Ticket)

    def get_by_id(self, ticket_id: int) -> Ticket:
        ticket = self.ticket_repository.get(ticket_id)
        if ticket is None:
            raise ResourceNotFoundError("Ticket not found.")
        return ticket

    def list(self, *, offset: int = 0, limit: int = 100) -> Sequence[Ticket]:
        return self.ticket_repository.list(offset=offset, limit=limit)

    def list_filtered(
        self,
        *,
        customer_id: int | None = None,
        status_id: int | None = None,
        priority_id: int | None = None,
        assigned_agent_id: int | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        return self.ticket_repository.list_filtered(
            customer_id=customer_id,
            status_id=status_id,
            priority_id=priority_id,
            assigned_agent_id=assigned_agent_id,
            offset=offset,
            limit=limit,
        )

    def list_by_customer(
        self,
        customer_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        return self.ticket_repository.list_by_customer(
            customer_id,
            offset=offset,
            limit=limit,
        )

    def list_by_status(
        self,
        status_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        return self.ticket_repository.list_by_status(
            status_id,
            offset=offset,
            limit=limit,
        )

    def list_by_assigned_agent(
        self,
        agent_id: int,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[Ticket]:
        return self.ticket_repository.list_by_assigned_agent(
            agent_id,
            offset=offset,
            limit=limit,
        )

    def create(self, data: TicketCreate) -> Ticket:
        try:
            ticket_data = self._get_create_data(data)
            self._validate_required_relations(ticket_data)
            assigned_agent_id = ticket_data.get("assignee_id")
            if isinstance(assigned_agent_id, int):
                self._ensure_assignable_agent(assigned_agent_id)

            ticket = self.ticket_repository.add(Ticket(**ticket_data))
            self.session.commit()
            self.session.refresh(ticket)
            return ticket
        except Exception:
            self.session.rollback()
            raise

    def update(self, ticket_id: int, data: TicketUpdate) -> Ticket:
        try:
            ticket = self.get_by_id(ticket_id)
            update_data = self._get_update_data(data)
            self._validate_update_relations(update_data)

            for field_name, value in update_data.items():
                setattr(ticket, field_name, value)

            updated = self.ticket_repository.update(ticket)
            self.session.commit()
            self.session.refresh(updated)
            return updated
        except Exception:
            self.session.rollback()
            raise

    def delete(self, ticket_id: int) -> None:  # type: ignore[override]
        try:
            ticket = self.get_by_id(ticket_id)
            self.ticket_repository.delete(ticket)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def _get_create_data(self, data: TicketCreate) -> dict[str, Any]:
        return self._map_schema_data(data.model_dump())

    def _get_update_data(self, data: TicketUpdate) -> dict[str, Any]:
        return self._map_schema_data(data.model_dump(exclude_unset=True))

    def _map_schema_data(self, data: dict[str, Any]) -> dict[str, Any]:
        assigned_agent_id = data.pop("assigned_agent_id", _MISSING)
        if assigned_agent_id is not _MISSING:
            data["assignee_id"] = assigned_agent_id
        return data

    def _validate_required_relations(self, data: dict[str, Any]) -> None:
        self._ensure_customer_exists(data["customer_id"])
        self._ensure_category_exists(data["category_id"])
        self._ensure_status_exists(data["status_id"])
        self._ensure_priority_exists(data["priority_id"])

    def _validate_update_relations(self, data: dict[str, Any]) -> None:
        customer_id = data.get("customer_id")
        if isinstance(customer_id, int):
            self._ensure_customer_exists(customer_id)

        category_id = data.get("category_id")
        if isinstance(category_id, int):
            self._ensure_category_exists(category_id)

        status_id = data.get("status_id")
        if isinstance(status_id, int):
            self._ensure_status_exists(status_id)

        priority_id = data.get("priority_id")
        if isinstance(priority_id, int):
            self._ensure_priority_exists(priority_id)

        if "assignee_id" in data and data["assignee_id"] is not None:
            self._ensure_assignable_agent(data["assignee_id"])

    def _ensure_customer_exists(self, customer_id: int) -> None:
        if self.customer_repository.get(customer_id) is None:
            raise ResourceNotFoundError("Customer not found.")

    def _ensure_category_exists(self, category_id: int) -> None:
        if self.category_repository.get(category_id) is None:
            raise ResourceNotFoundError("Ticket category not found.")

    def _ensure_status_exists(self, status_id: int) -> None:
        if self.status_repository.get(status_id) is None:
            raise ResourceNotFoundError("Ticket status not found.")

    def _ensure_priority_exists(self, priority_id: int) -> None:
        if self.priority_repository.get(priority_id) is None:
            raise ResourceNotFoundError("Ticket priority not found.")

    def _ensure_assignable_agent(self, agent_id: int) -> User:
        user = self.user_repository.get(agent_id)
        if user is None:
            raise ResourceNotFoundError("Assigned agent not found.")
        if user.role.name not in {"ADMIN", "AGENT"}:
            raise InvalidOperationError("Assigned user must be an agent or admin.")
        return user
