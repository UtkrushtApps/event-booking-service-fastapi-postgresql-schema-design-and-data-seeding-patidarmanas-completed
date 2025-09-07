# Event Booking Service – FastAPI & PostgreSQL Schema Setup

## Task Overview
Utkrusht is preparing an online event booking service to let users browse upcoming events and reserve multiple seats. While the FastAPI interface is fully functional and already handles event listing, booking logic, and basic seat management, the platform cannot serve real data until the core PostgreSQL schema and some initial data are provided. Your work will enable end-to-end booking, let users see which events are open or full, and support business reporting.

## Guidance
- The FastAPI application is already implemented and connected to the PostgreSQL database—do not modify Python code.
- Focus exclusively on creating:
  - `schema.sql`: All required tables, keys, and relationships, defining the booking domain.
  - `data/sample_data.sql`: Populate users, events, and booking rows with realistic and diverse examples.
- Review:
  - `app/database.py` (understand DB connection model: all queries are async-compatible, but schema/data creation is your task).
  - `app/routes/api.py` (API endpoints for booking and event querying).
- No performance tuning or index optimization is needed; correctness and data integrity come first.
- All API endpoints depend on your schema—test them using the API docs or tools like curl/Postman.

## Database Access
- **Host**: <DROPLET_IP>
- **Port**: 5432
- **Database name**: eventdb
- **Username**: event_user
- **Password**: event_pass
- You may use any SQL database client (pgAdmin, DBeaver, psql, etc.) to connect and validate data directly if desired.

## Objectives
- Design a normalized PostgreSQL schema supporting:
  - Events (with title, event date, and seat capacity)
  - Users (with name and email)
  - Bookings (linking users to events, with seat counts and booked timestamps)
- Implement all relevant constraints:
  - Proper primary/foreign keys between users/bookings and bookings/events
  - Ensure that bookings reference existing users/events (FK integrity)
- Insert sample data:
  - At least 6 events (past and future, various capacities)
  - 10 users
  - 18+ booking rows with multiple seat bookings; ensure some events are fully booked and some remain open

## How to Verify
- Confirm schema and sample data are successfully created by executing the provided SQL files with no errors.
- Use the API endpoints to:
  - List upcoming events and verify capacity vs. total seats booked per event is accurate
  - Create bookings for events with available seats and verify seat counts are correct
  - Attempt to overbook a fully-booked event and confirm proper error handling
  - Query individual user bookings to see linked data (user, event, seats, booked_at)
- Optionally, verify via direct SQL queries that table contents match sample requirements and that all required relationships are enforced.