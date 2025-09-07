from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    id: int
    title: str
    event_date: str
    capacity: int

class User(BaseModel):
    id: int
    name: str
    email: str

class Booking(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats_booked: int
    booked_at: str

class BookingCreate(BaseModel):
    user_id: int
    event_id: int
    seats_booked: int
