#!/usr/bin/env bash
# Render build script — runs during every deploy
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Checking DATABASE_URL ==="
if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL is not set! Check your Render environment variables."
  exit 1
else
  echo "DATABASE_URL is set."
fi

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

echo "=== Running migrations ==="
python manage.py migrate --run-syncdb

echo "=== Creating superuser ==="
python manage.py create_superuser

echo "=== Build complete ==="
