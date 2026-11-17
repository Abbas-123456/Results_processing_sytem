# Results Processing System

A Django application for managing faculties, courses, course units, lecturer assignments, student results, and grading summaries. Access is controlled by user roles for registrars, faculty coordinators, lecturers, and system administrators.

## Requirements

- Python 3.13 or compatible
- Packages listed in `requirements.txt`

## Run locally

```powershell
.venv\Scripts\Activate.ps1
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`; the root page redirects to the login page.

## Deploying to Render

Create a Python web service from the `main` branch, leave Root Directory blank,
and set:

- Build Command: `pip install -r requirements.txt && python manage.py collectstatic --no-input`
- Start Command: `python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`

Attach a Render PostgreSQL database and make its internal connection URL
available to the web service as `DATABASE_URL`. Add `DJANGO_SECRET_KEY` using
Render's Generate Value option, and set `DJANGO_DEBUG` to `False`. Render's
service hostname is detected automatically. If using a custom domain, include
it in `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.

The hosted database starts empty; the local SQLite database is not uploaded.
After the first deploy, open the Render Shell and run
`python manage.py createsuperuser --username admin` to create the administrator.
Use a unique, strong password for the hosted administrator account.

## Local demo accounts

Local demo accounts are for development only. Create a separate superuser in
the hosted database after deployment.


## Group members

Group-member details are maintained separately from this deployment guide.