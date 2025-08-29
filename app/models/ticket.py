import uuid

from sqlmodel import SQLModel, Field
from typing import Optional
import datetime

from app.utils.enum import TicketStatus


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"
    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True, index=True)
    event_id: int = Field(foreign_key="events.id")
    user_id: Optional[int] = Field(default=None, index=True)
    status: str = Field(default=TicketStatus.AVAILABLE)
    expires_at: Optional[datetime.datetime] = None