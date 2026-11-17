#!/usr/bin/env bash
# Render build script. The committed db.sqlite3 is already migrated, so no migrate here.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
