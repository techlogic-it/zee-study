"""
WSGI entry point for production (gunicorn / Railway).
Initialises the database; seeds questions in a background thread
so the app responds to healthchecks immediately on first boot.
"""
import threading
import database as db

db.init_db()

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
