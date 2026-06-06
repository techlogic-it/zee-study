"""
WSGI entry point for production (gunicorn / Railway).
Initialises the database; seeds questions in a background thread
so the app responds to healthchecks immediately on first boot.
"""
import threading
import os
import database as db

print(f'[wsgi] DATABASE_URL set = {"YES" if os.environ.get("DATABASE_URL") else "NO — app will crash"}', flush=True)

db.init_db()
print('[wsgi] Database initialised.', flush=True)

_conn = db.get_db()
_c    = db._cur(_conn)
_c.execute('SELECT COUNT(*) AS cnt FROM users')
_user_count = _c.fetchone()['cnt']
_conn.close()
print(f'[wsgi] Users in database = {_user_count}', flush=True)


def _seed_if_needed():
    if not db.questions_exist():
        try:
            from seed_all import seed_all
            seed_all()
            print('[wsgi] Database seeded.', flush=True)
        except Exception as e:
            print(f'[wsgi] Seeding error: {e}', flush=True)
    else:
        print('[wsgi] Questions already present — skipping seed.', flush=True)


threading.Thread(target=_seed_if_needed, daemon=True).start()

from app import app  # noqa: E402
