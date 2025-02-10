#!/bin/sh

# Wait for postgres
while ! nc -z $POSTGRES_HOST 5432; do
    echo "Waiting for postgres..."
    sleep 0.1
done

echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Execute passed command
exec "$@"