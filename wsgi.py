"""
WSGI entry point for production (gunicorn / Railway).
Initialises the database; seeds questions in a background thread
so the app responds to healthchecks immediately on first boot.
"""
import threading
import os
import database as db

print(f'[wsgi] DB_PATH = {db.DB_PATH}', flush=True)
print(f'[wsgi] DB file exists = {os.path.exists(db.DB_PATH)}', flush=True)
print(f'[wsgi] DB directory = {os.path.dirname(db.DB_PATH)}', flush=True)

db.init_db()

import sqlite3
_conn = db.get_db()
_user_count = _conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
_conn.close()
print(f'[wsgi] Users in database = {_user_count}', flush=True)

def _seed_if_needed():
    if not db.questions_exist():
        try:
            from seed_all import seed_all
            seed_all()
            print('[wsgi] Database seeded.')
        except Exception as e:
            print(f'[wsgi] Seeding error: {e}')

threading.Thread(target=_seed_if_needed, daemon=True).start()

from app import app  # noqa: E402
