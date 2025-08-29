from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Event(SQLModel, table=True):
    __tablename__ = "events"
    id: int = Field(primary_key=True, index=True)
    event_name: str
    event_date: str
    date_added: Optional[datetime] = Field(default=datetime.now())