#!/bin/bash
set -e

echo "Starting PostgreSQL..."
while ! nc -z $PG_HOST 5432; do
  sleep 1
done
echo "Done"

echo "Making migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Done"

if [ ! -d "media" ]; then
  echo "First run! Preparing media..."
  mkdir -p media
  cp static/images/* media/ -r
  echo "Creating admin user..."
  python manage.py create_administrator --email $ADMIN_USER --password $ADMIN_PASSWORD --first_name Super --last_name User
  echo "Filling database..."
  python manage.py add_users
  python manage.py add_courses
  echo "Done"
fi

echo "Starting backend app..."
python manage.py runserver 0.0.0.0:8000
