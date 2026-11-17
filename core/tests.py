import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

from django.contrib.auth.hashers import check_password
from django.test import SimpleTestCase

BASE_DIR = Path(__file__).resolve().parent.parent
PROBE = (
    "import json;from django.conf import settings;"
    "d=settings.DATABASES['default'];"
    "print(json.dumps([settings.DEBUG,d['ENGINE'],str(d['NAME'])]))"
)


def probe(**env):
    base = {k: v for k, v in os.environ.items() if not k.startswith(('DJANGO_', 'DATABASE_URL', 'RENDER'))}
    base['DJANGO_SETTINGS_MODULE'] = 'core.settings'
    base.update(env)
    return subprocess.run([sys.executable, '-c', PROBE], cwd=BASE_DIR, env=base, capture_output=True, text=True)


class SettingsTests(SimpleTestCase):
    prod = {'DJANGO_SECRET_KEY': 'x', 'RENDER_EXTERNAL_HOSTNAME': 'app.onrender.com'}

    def test_database_is_sqlite_even_with_database_url(self):
        r = probe(DATABASE_URL='postgres://u:p@h/db', DJANGO_DEBUG='false', **self.prod)
        self.assertEqual(r.returncode, 0, r.stderr)
        _, engine, name = json.loads(r.stdout)
        self.assertEqual(engine, 'django.db.backends.sqlite3')
        self.assertTrue(name.endswith('db.sqlite3'))

    def test_production_start_without_database_url(self):
        self.assertEqual(probe(**self.prod).returncode, 0)

    def test_debug_defaults_to_false(self):
        self.assertIs(json.loads(probe(**self.prod).stdout)[0], False)

    def test_secret_key_required_when_not_debug(self):
        self.assertNotEqual(probe(RENDER_EXTERNAL_HOSTNAME='app.onrender.com').returncode, 0)


class CommittedDatabaseTests(SimpleTestCase):
    def rows(self):
        con = sqlite3.connect(f"file:{BASE_DIR / 'db.sqlite3'}?mode=ro", uri=True)
        try:
            return con.execute(
                'select username,password,is_superuser,is_staff,is_active from auth_user'
            ).fetchall()
        finally:
            con.close()

    def test_admin_password_is_admin123(self):
        admin = [r for r in self.rows() if r[0] == 'admin'][0]
        self.assertTrue(check_password('admin123', admin[1]))

    def test_admin_is_active_superuser_and_staff(self):
        admin = [r for r in self.rows() if r[0] == 'admin'][0]
        self.assertEqual(admin[2:], (1, 1, 1))

    def test_other_users_unchanged(self):
        rows = self.rows()
        self.assertEqual({r[0] for r in rows}, {
            'academicregistrar', 'eng.kasagga.usama', 'eng.walusimbi.hakim',
            'facultycoordinator', 'admin', 'sudaice'})
        for r in rows:
            if r[0] != 'admin':
                self.assertFalse(check_password('admin123', r[1]))
