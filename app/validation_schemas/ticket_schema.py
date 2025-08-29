import uuid

from sqlmodel import SQLModel

class ReserveTicket(SQLModel):
    user_id: int
    ticket_id: uuid.UUID

