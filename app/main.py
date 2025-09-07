from fastapi import FastAPI
from app.routes.api import router as api_router

app = FastAPI(
    title="Event Booking Service",
    description="Book seats for events and track user bookings with real-time seat updates.",
    version="1.0.0"
)
app.include_router(api_router, prefix="/api")
