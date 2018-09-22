#!/bin/bash

echo "Waiting for database to start"
./wait-for-it.sh db:5432 --timeout=60 -- echo "Postgres is up"

echo "Making database migrations"
./manage.py makemigrations districts noauth
echo "Applying database migrations"
./manage.py migrate

echo "Load sample data"
./manage.py loaddata local.yaml

echo "Starting server"
./manage.py runserver 0.0.0.0:8001