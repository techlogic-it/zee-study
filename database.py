import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors as pg_errors
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta

DATABASE_URL = os.environ.get('DATABASE_URL', '')


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def _cur(conn):
    return conn.cursor(cursor_factory=RealDictCursor)


def init_db():
    conn = get_db()
    c = _cur(conn)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id              SERIAL PRIMARY KEY,
            username             TEXT    UNIQUE NOT NULL,
            password_hash        TEXT    NOT NULL,
            email                TEXT    UNIQUE,
            first_name           TEXT,
            last_name            TEXT,
            disabled             INTEGER DEFAULT 0,
            xp                   INTEGER DEFAULT 0,
            current_streak       INTEGER DEFAULT 0,
            highest_streak       INTEGER DEFAULT 0,
            last_active_date     TEXT,
            total_quizzes        INTEGER DEFAULT 0,
            subscription_plan    TEXT    DEFAULT 'free',
            subscription_expires TEXT,
            created_at           TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            question_id    SERIAL PRIMARY KEY,
            subject        TEXT    NOT NULL,
            topic          TEXT,
            topic_code     TEXT,
            difficulty     INTEGER NOT NULL,
            question_text  TEXT    NOT NULL,
            option_a       TEXT    NOT NULL,
            option_b       TEXT    NOT NULL,
            option_c       TEXT    NOT NULL,
            option_d       TEXT    NOT NULL,
            correct_answer TEXT    NOT NULL,
            explanation    TEXT    NOT NULL,
            correction_tip TEXT    NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            attempt_id      SERIAL PRIMARY KEY,
            user_id         INTEGER NOT NULL REFERENCES users(user_id),
            subject         TEXT    NOT NULL,
            topic_code      TEXT,
            difficulty      INTEGER NOT NULL,
            score           INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage      INTEGER NOT NULL,
            xp_earned       INTEGER NOT NULL,
            completed_at    TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_answers (
            answer_id   SERIAL PRIMARY KEY,
            attempt_id  INTEGER NOT NULL REFERENCES quiz_attempts(attempt_id),
            question_id INTEGER NOT NULL REFERENCES questions(question_id),
            user_answer TEXT,
            is_correct  INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# ── Users ─────────────────────────────────────────────────

def create_user(username, password, email=None, first_name=None, last_name=None):
    conn = get_db()
    try:
        c = _cur(conn)
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        c.execute(
            'INSERT INTO users (username, password_hash, email, first_name, last_name) VALUES (%s,%s,%s,%s,%s)',
            (username, password_hash, email, first_name, last_name)
        )
        conn.commit()
        return True, 'Account created.'
    except Exception:
        conn.rollback()
        # Check which field caused the conflict
        c2 = _cur(conn)
        c2.execute('SELECT 1 FROM users WHERE LOWER(username)=LOWER(%s)', (username,))
        if c2.fetchone():
            return False, 'That username is already taken. Please choose another.'
        c2.execute('SELECT 1 FROM users WHERE LOWER(email)=LOWER(%s)', (email or '',))
        if c2.fetchone():
            return False, 'An account with that email already exists. Try logging in instead.'
        return False, 'Account could not be created. Please try again.'
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_db()
    c = _cur(conn)
    c.execute(
        'SELECT * FROM users WHERE LOWER(username)=LOWER(%s) OR LOWER(email)=LOWER(%s)',
        (username, username)
    )
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        if user['disabled']:
            return 'disabled'
        return dict(user)
    return None


def get_user(user_id):
    conn = get_db()
    c = _cur(conn)
    c.execute('SELECT * FROM users WHERE user_id=%s', (user_id,))
    user = c.fetchone()
    conn.close()
    return dict(user) if user else None


def update_user_details(user_id, first_name, last_name, email, username):
    conn = get_db()
    try:
        c = _cur(conn)
        c.execute(
            'UPDATE users SET first_name=%s, last_name=%s, email=%s, username=%s WHERE user_id=%s',
            (first_name, last_name, email, username, user_id)
        )
        conn.commit()
        return True, ''
    except Exception:
        conn.rollback()
        return False, 'That username or email is already in use by another account.'
    finally:
        conn.close()


def update_user_password(user_id, new_password):
    conn = get_db()
    c = _cur(conn)
    password_hash = generate_password_hash(new_password, method='pbkdf2:sha256')
    c.execute('UPDATE users SET password_hash=%s WHERE user_id=%s', (password_hash, user_id))
    conn.commit()
    conn.close()


def set_user_disabled(user_id, disabled):
    conn = get_db()
    c = _cur(conn)
    c.execute('UPDATE users SET disabled=%s WHERE user_id=%s', (1 if disabled else 0, user_id))
    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_db()
    c = _cur(conn)
    c.execute('DELETE FROM user_answers WHERE attempt_id IN (SELECT attempt_id FROM quiz_attempts WHERE user_id=%s)', (user_id,))
    c.execute('DELETE FROM quiz_attempts WHERE user_id=%s', (user_id,))
    c.execute('DELETE FROM users WHERE user_id=%s', (user_id,))
    conn.commit()
    conn.close()


def admin_update_user(user_id, first_name, last_name, email, username):
    conn = get_db()
    try:
        c = _cur(conn)
        c.execute(
            'UPDATE users SET first_name=%s, last_name=%s, email=%s, username=%s WHERE user_id=%s',
            (first_name, last_name, email, username, user_id)
        )
        conn.commit()
        return True, ''
    except Exception:
        conn.rollback()
        c2 = _cur(conn)
        c2.execute('SELECT user_id FROM users WHERE LOWER(username)=LOWER(%s) AND user_id!=%s', (username, user_id))
        if c2.fetchone():
            return False, 'That username is already taken.'
        return False, 'That email is already in use.'
    finally:
        conn.close()


def update_streak(user_id):
    conn = get_db()
    c = _cur(conn)
    c.execute('SELECT * FROM users WHERE user_id=%s', (user_id,))
    user = c.fetchone()
    today     = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    last    = user['last_active_date']
    current = user['current_streak']
    highest = user['highest_streak']
    bonus   = False

    if last == today:
        conn.close()
        return False, current

    current = current + 1 if last == yesterday else 1
    if current > highest:
        highest = current
    if current % 10 == 0:
        bonus = True

    c.execute(
        'UPDATE users SET current_streak=%s, highest_streak=%s, last_active_date=%s WHERE user_id=%s',
        (current, highest, today, user_id)
    )
    conn.commit()
    conn.close()
    return bonus, current


def add_xp(user_id, amount):
    conn = get_db()
    c = _cur(conn)
    c.execute('UPDATE users SET xp=xp+%s WHERE user_id=%s', (amount, user_id))
    conn.commit()
    conn.close()


# ── Questions ─────────────────────────────────────────────

def questions_exist():
    conn = get_db()
    c = _cur(conn)
    c.execute('SELECT COUNT(*) AS cnt FROM questions')
    count = c.fetchone()['cnt']
    conn.close()
    return count > 0


def get_questions(subject, difficulty, topic_code=None):
    conn = get_db()
    c = _cur(conn)
    if topic_code:
        c.execute(
            'SELECT * FROM questions WHERE subject=%s AND difficulty=%s AND topic_code=%s',
            (subject, difficulty, topic_code)
        )
    else:
        c.execute(
            'SELECT * FROM questions WHERE subject=%s AND difficulty=%s',
            (subject, difficulty)
        )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_topic_counts(subject):
    conn = get_db()
    c = _cur(conn)
    c.execute(
        'SELECT topic_code, difficulty, COUNT(*) AS cnt FROM questions '
        'WHERE subject=%s AND topic_code IS NOT NULL GROUP BY topic_code, difficulty',
        (subject,)
    )
    rows = c.fetchall()
    conn.close()
    counts = {}
    for r in rows:
        code = r['topic_code']
        if code not in counts:
            counts[code] = {}
        counts[code][r['difficulty']] = r['cnt']
    return counts


def get_questions_by_ids(ids):
    if not ids:
        return []
    placeholders = ','.join(['%s'] * len(ids))
    conn = get_db()
    c = _cur(conn)
    c.execute(f'SELECT * FROM questions WHERE question_id IN ({placeholders})', ids)
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Attempts ──────────────────────────────────────────────

def save_attempt(user_id, subject, difficulty, score, total, xp_earned, answers, questions, topic_code=None):
    percentage = round((score / total) * 100) if total else 0
    conn = get_db()
    c = _cur(conn)
    c.execute(
        '''INSERT INTO quiz_attempts
           (user_id, subject, difficulty, score, total_questions, percentage, xp_earned, topic_code)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING attempt_id''',
        (user_id, subject, difficulty, score, total, percentage, xp_earned, topic_code)
    )
    attempt_id = c.fetchone()['attempt_id']

    q_map = {str(q['question_id']): q for q in questions}
    for qid_str, user_answer in answers.items():
        q = q_map.get(qid_str)
        if q:
            is_correct = 1 if (user_answer or '').upper() == q['correct_answer'].upper() else 0
            c.execute(
                'INSERT INTO user_answers (attempt_id, question_id, user_answer, is_correct) VALUES (%s,%s,%s,%s)',
                (attempt_id, q['question_id'], user_answer, is_correct)
            )

    c.execute('UPDATE users SET total_quizzes=total_quizzes+1 WHERE user_id=%s', (user_id,))
    conn.commit()
    conn.close()
    return attempt_id


def get_attempt(attempt_id, user_id):
    conn = get_db()
    c = _cur(conn)
    c.execute(
        'SELECT * FROM quiz_attempts WHERE attempt_id=%s AND user_id=%s',
        (attempt_id, user_id)
    )
    attempt = c.fetchone()
    if not attempt:
        conn.close()
        return None
    attempt = dict(attempt)

    c.execute(
        '''SELECT ua.user_answer, q.question_text, q.correct_answer,
                  q.option_a, q.option_b, q.option_c, q.option_d,
                  q.explanation, q.correction_tip
           FROM user_answers ua
           JOIN questions q ON ua.question_id=q.question_id
           WHERE ua.attempt_id=%s AND ua.is_correct=0''',
        (attempt_id,)
    )
    attempt['wrong_answers'] = [dict(r) for r in c.fetchall()]
    conn.close()
    return attempt


def get_recent_attempts(user_id, limit=10):
    conn = get_db()
    c = _cur(conn)
    c.execute(
        'SELECT * FROM quiz_attempts WHERE user_id=%s ORDER BY completed_at DESC LIMIT %s',
        (user_id, limit)
    )
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Admin ─────────────────────────────────────────────────

def get_all_users():
    conn = get_db()
    c = _cur(conn)
    c.execute('''
        SELECT u.user_id, u.username, u.first_name, u.last_name, u.email,
               u.xp, u.current_streak, u.highest_streak,
               u.total_quizzes, u.subscription_plan, u.subscription_expires,
               u.created_at, u.last_active_date, u.disabled,
               COUNT(qa.attempt_id) AS quiz_count
        FROM users u
        LEFT JOIN quiz_attempts qa ON u.user_id=qa.user_id
        GROUP BY u.user_id
        ORDER BY u.created_at DESC
    ''')
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_admin_stats():
    conn = get_db()
    c = _cur(conn)
    stats = {}
    c.execute('SELECT COUNT(*) AS cnt FROM users')
    stats['total_users'] = c.fetchone()['cnt']
    c.execute("SELECT COUNT(*) AS cnt FROM users WHERE subscription_plan='premium'")
    stats['premium_users'] = c.fetchone()['cnt']
    c.execute('SELECT COUNT(*) AS cnt FROM quiz_attempts')
    stats['total_quizzes'] = c.fetchone()['cnt']
    c.execute("SELECT COUNT(DISTINCT user_id) AS cnt FROM quiz_attempts WHERE DATE(completed_at)=CURRENT_DATE")
    stats['active_today'] = c.fetchone()['cnt']
    conn.close()
    return stats


def update_user_subscription(user_id, plan, expires=None):
    conn = get_db()
    c = _cur(conn)
    c.execute(
        'UPDATE users SET subscription_plan=%s, subscription_expires=%s WHERE user_id=%s',
        (plan, expires, user_id)
    )
    conn.commit()
    conn.close()


def get_users_for_reminder(days_inactive=7):
    conn = get_db()
    c = _cur(conn)
    c.execute('''
        SELECT user_id, username, email, last_active_date
        FROM users
        WHERE email IS NOT NULL AND email != ''
          AND (last_active_date IS NULL
               OR last_active_date::date <= CURRENT_DATE - INTERVAL '%s days')
    ''', (days_inactive,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]
