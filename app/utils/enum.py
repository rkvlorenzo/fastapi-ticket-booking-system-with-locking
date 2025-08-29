from enum import Enum

class TicketStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    BOOKED = "booked"