import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder

from app.validation_schemas.ticket_schema import ReserveTicket
from app.services.ticket_service import retrieve_tickets, reserve_ticket, expire_ticket
from app.utils.format import format_response

async def check_tickets_expiry():
    while True:
        print("Check for ticket expiration.")  # <- should now print
        await expire_ticket()
        await asyncio.sleep(15)  # check every 1 minute

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(check_tickets_expiry())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

app = FastAPI(lifespan=lifespan)

@app.get("/tickets")
async def get_tickets():
    data = await retrieve_tickets()
    return format_response(status_code=status.HTTP_200_OK, response={"data": jsonable_encoder(data)})

@app.patch("/tickets/reserve")
async def update_ticket(params: ReserveTicket):
    result, message = await reserve_ticket(user_id=params.user_id, ticket_id=params.ticket_id)
    status_code = status.HTTP_200_OK if result else status.HTTP_409_CONFLICT
    return format_response(status_code=status_code, response={"message": message})
