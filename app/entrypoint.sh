#!/bin/bash
set -e

echo "Let the DB start..."
while ! nc -z $PG_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

if [ ! -d "media" ]; then
  echo "Preparing media"
  mkdir -p media
  cp static/images/* media/ -r
fi

echo "Making migrations"
python manage.py makemigrations
python manage.py migrate

echo "Starting backend app"
python manage.py runserver 0.0.0.0:8000

# Deploy:
# Create superuser
