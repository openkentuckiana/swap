#!/bin/bash

# Wait for DB
echo "Waiting for database to start"
./wait-for-it.sh db:5432 --timeout=60 -- echo "Postgres is up"

# Apply database migrations
echo "Making database migrations"
./manage.py makemigrations districts noauth
echo "Applying database migrations"
./manage.py migrate

# Load sample data
echo "Load sample data"
./manage.py loaddata local.yaml

# Start server
echo "Starting server"
./manage.py runserver 0.0.0.0:8001