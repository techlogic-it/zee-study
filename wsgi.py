"""
WSGI entry point for production (gunicorn / Railway).
Initialises the database and seeds it on first run.
"""
import database as db

db.init_db()

if not db.questions_exist():
    from seed_all import seed_all
    seed_all()
    print('[wsgi] Database seeded.')

from app import app  # noqa: E402  (must come after init)
