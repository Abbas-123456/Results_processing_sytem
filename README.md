# Results Processing System

A Django application for managing faculties, courses, course units, lecturer assignments, student results, and grading summaries. Access is controlled by user roles for registrars, faculty coordinators, lecturers, and system administrators.

## Requirements

- Python 3.13 or compatible
- Packages listed in `requirements.txt`

## Run locally

```powershell
.venv\Scripts\Activate.ps1
$env:DJANGO_DEBUG='true'
python manage.py runserver
```

Open `http://127.0.0.1:8000/`; the root page redirects to the login page.

## Deploying to Render

Create a Python web service from the `main` branch (or use `render.yaml`) and set:

- Build Command: `bash build.sh`
- Start Command: `gunicorn core.wsgi:application`
- Environment: `DJANGO_SECRET_KEY` (Generate Value), `PYTHON_VERSION=3.13.0`, `DJANGO_DEBUG=false`

The committed `db.sqlite3` is the live database; no external database is used.
Render's free disk resets on every restart, so changes made on the live site are
lost and the committed data returns. Demo login: `admin` / `admin123`.

## Group members

Group-member details are maintained separately from this deployment guide.