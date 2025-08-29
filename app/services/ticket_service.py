import uuid
from datetime import datetime, timedelta
from typing import List

from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Event
from app.models.ticket import Ticket
from app.utils.db_engine import create_db_engine
from app.utils.enum import TicketStatus


async def retrieve_tickets() -> List[dict]:
    engine = create_db_engine()
    async with AsyncSession(engine) as session:
        statement = select(Ticket.id, Ticket.status, Event.event_name).join(Event, Event.id == Ticket.event_id) # type: ignore
        result = await session.exec(statement)
        rows = result.all()
    return [
        {"id": id_, "status": status, "event_name": event_name}
        for id_, status, event_name in rows
    ]

async def reserve_ticket(user_id: int, ticket_id: uuid.UUID) -> (bool, str):
    try:
        engine = create_db_engine()
        async with AsyncSession(engine) as session:
            statement = select(Ticket).where(
                and_(
                    Ticket.id == ticket_id,
                    Ticket.status == TicketStatus.AVAILABLE
                )
            ).with_for_update()
            result = await session.exec(statement) # type: ignore
            ticket = result.first()

            if not ticket:
                return False, "Ticket not available."

            ticket.status = TicketStatus.RESERVED
            ticket.user_id = user_id
            ticket.expires_at = datetime.utcnow() + timedelta(minutes=5)
            session.add(ticket)
            await session.commit()
            await session.refresh(ticket)
            return True, "Ticket has been reserved. Continue with payment to secure your ticket."
    except Exception as e:
        return str(e)


async def expire_ticket():
    try:
        engine = create_db_engine()
        async with AsyncSession(engine) as session:
            statement = select(Ticket).where(
                (Ticket.status == TicketStatus.RESERVED) &
                (Ticket.expires_at < datetime.utcnow())
            )
            result = await session.exec(statement) # type: ignore
            expired_tickets = result.all()
            print(f"Found expired tickets: {expired_tickets}")

            for ticket in expired_tickets:
                ticket.status = TicketStatus.AVAILABLE
                ticket.expires_at = None
                ticket.user_id = None
                session.add(ticket)
                await session.flush()  # ensure all changes are applied
                await session.commit()

    except Exception as e:
        return str(e)