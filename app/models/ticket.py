from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.ticket_category import TicketCategory
    from app.models.ticket_comment import TicketComment
    from app.models.ticket_priority import TicketPriority
    from app.models.ticket_status import TicketStatus
    from app.models.user import User


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("ticket_categories.id", ondelete="SET NULL"),
    )
    status_id: Mapped[int] = mapped_column(
        ForeignKey("ticket_statuses.id", ondelete="RESTRICT"),
        nullable=False,
    )
    priority_id: Mapped[int] = mapped_column(
        ForeignKey("ticket_priorities.id", ondelete="RESTRICT"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    customer: Mapped["Customer"] = relationship(back_populates="tickets")
    assignee: Mapped["User | None"] = relationship(back_populates="assigned_tickets")
    category: Mapped["TicketCategory | None"] = relationship(back_populates="tickets")
    status: Mapped["TicketStatus"] = relationship(back_populates="tickets")
    priority: Mapped["TicketPriority"] = relationship(back_populates="tickets")
    comments: Mapped[list["TicketComment"]] = relationship(back_populates="ticket")
