#!/bin/bash
set -e

echo "Starting Docker containers with docker-compose..."
docker-compose -f /root/task/docker-compose.yml up -d

for i in {1..30}; do
  if docker exec event_postgres pg_isready -U event_user -d eventdb; then
    echo "PostgreSQL is up."
    break
  fi
  echo "Waiting for PostgreSQL... ($i/30)"
  sleep 2
done

echo "Running schema.sql to create tables..."
docker exec -i event_postgres psql -U event_user -d eventdb < /root/task/schema.sql

echo "Running sample_data.sql to seed data..."
docker exec -i event_postgres psql -U event_user -d eventdb < /root/task/data/sample_data.sql

echo "Validating FastAPI is up..."
for i in {1..20}; do
  if curl -s http://localhost:8000/docs | grep -q 'Event Booking Service'; then
    echo "FastAPI is running and connected."
    exit 0
  fi
  echo "Waiting for FastAPI... ($i/20)"
  sleep 2
done

>&2 echo "ERROR: FastAPI did not start as expected."
exit 1
