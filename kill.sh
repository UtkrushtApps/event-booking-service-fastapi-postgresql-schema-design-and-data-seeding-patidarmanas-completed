#!/bin/bash
set -e

echo "Stopping containers..."
docker-compose -f /root/task/docker-compose.yml down --volumes --remove-orphans || true

echo "Removing Docker images..."
docker rmi -f $(docker images -q | grep -E 'event_api|postgres:15-alpine' || true) || true

echo "Pruning Docker system..."
docker system prune -a --volumes -f

echo "Deleting /root/task directory..."
rm -rf /root/task || true

echo "Cleanup completed successfully! Droplet is now clean."
