#!/bin/sh

# Wait for postgres
echo "Waiting for postgres..."

while ! nc -z db 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

# Run migrations and server
python manage.py migrate
python manage.py runserver 0.0.0.0:8000