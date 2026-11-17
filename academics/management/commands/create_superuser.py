import os
import sys

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import OperationalError, ProgrammingError


class Command(BaseCommand):
    help = "Create a superuser non-interactively if one does not already exist."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

        try:
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Superuser "{username}" already exists — skipping creation.'
                    )
                )
            else:
                User.objects.create_superuser(
                    username=username,
                    password=password,
                    email=email,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Superuser "{username}" created successfully.'
                    )
                )
        except (OperationalError, ProgrammingError) as e:
            self.stderr.write(
                self.style.ERROR(
                    f"Database error while creating superuser: {e}\n"
                    "Make sure DATABASE_URL is set and migrations have run."
                )
            )
            sys.exit(1)
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Unexpected error creating superuser: {e}")
            )
            sys.exit(1)
