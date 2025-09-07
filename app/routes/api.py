from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.schemas import Event, User, Booking, BookingCreate
from app.database import fetch_all, fetch_one, execute

router = APIRouter()

@router.get("/events", response_model=List[Event])
async def list_events():
    rows = await fetch_all("SELECT id, title, event_date, capacity FROM events ORDER BY event_date ASC")
    return [Event(id=r["id"], title=r["title"], event_date=str(r["event_date"]), capacity=r["capacity"]) for r in rows]

@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: int):
    row = await fetch_one("SELECT id, title, event_date, capacity FROM events WHERE id=$1", event_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return Event(id=row["id"], title=row["title"], event_date=str(row["event_date"]), capacity=row["capacity"])

@router.get("/events/{event_id}/remaining_seats")
async def event_remaining_seats(event_id: int):
    event_row = await fetch_one("SELECT capacity FROM events WHERE id=$1", event_id)
    if event_row is None:
        raise HTTPException(status_code=404, detail="Event not found")
    booked_row = await fetch_one("SELECT COALESCE(SUM(seats_booked), 0) as total_booked FROM bookings WHERE event_id=$1", event_id)
    remaining = event_row["capacity"] - (booked_row["total_booked"] or 0)
    return {"event_id": event_id, "remaining_seats": remaining}

@router.get("/users", response_model=List[User])
async def list_users():
    rows = await fetch_all("SELECT id, name, email FROM users")
    return [User(id=r["id"], name=r["name"], email=r["email"]) for r in rows]

@router.post("/bookings", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking(b: BookingCreate):
    event = await fetch_one("SELECT id, capacity FROM events WHERE id=$1", b.event_id)
    if not event:
        raise HTTPException(status_code=400, detail="Event does not exist")
    total_booked = (await fetch_one("SELECT COALESCE(SUM(seats_booked),0) as s FROM bookings WHERE event_id=$1", b.event_id))["s"]
    if total_booked + b.seats_booked > event["capacity"]:
        raise HTTPException(status_code=400, detail="Not enough seats available")
    user = await fetch_one("SELECT id FROM users WHERE id=$1", b.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    row = await fetch_one(
        """
        INSERT INTO bookings (user_id, event_id, seats_booked, booked_at) VALUES ($1, $2, $3, NOW())
        RETURNING id, user_id, event_id, seats_booked, booked_at
        """, b.user_id, b.event_id, b.seats_booked)
    return Booking(
        id=row["id"], user_id=row["user_id"], event_id=row["event_id"],
        seats_booked=row["seats_booked"], booked_at=str(row["booked_at"])
    )

@router.get("/users/{user_id}/bookings", response_model=List[Booking])
async def get_user_bookings(user_id: int):
    rows = await fetch_all("SELECT id, user_id, event_id, seats_booked, booked_at FROM bookings WHERE user_id=$1 ORDER BY booked_at DESC", user_id)
    return [Booking(
        id=r["id"], user_id=r["user_id"], event_id=r["event_id"],
        seats_booked=r["seats_booked"], booked_at=str(r["booked_at"])
    ) for r in rows]
