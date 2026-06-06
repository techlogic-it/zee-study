import sqlite3
import os
import random
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.environ.get(
    'DB_PATH',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quiz.db')
)


def get_db():
    # Ensure the directory exists (needed for Railway volume path e.g. /data)
    db_dir = os.path.dirname(DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            email         TEXT    UNIQUE,
            first_name    TEXT,
            last_name     TEXT,
            xp            INTEGER DEFAULT 0,
            current_streak  INTEGER DEFAULT 0,
            highest_streak  INTEGER DEFAULT 0,
            last_active_date TEXT,
            total_quizzes   INTEGER DEFAULT 0,
            subscription_plan    TEXT    DEFAULT 'free',
            subscription_expires TEXT,
            created_at    TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS questions (
            question_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            subject       TEXT    NOT NULL,
            topic         TEXT,
            topic_code    TEXT,
            difficulty    INTEGER NOT NULL,
            question_text TEXT    NOT NULL,
            option_a      TEXT    NOT NULL,
            option_b      TEXT    NOT NULL,
            option_c      TEXT    NOT NULL,
            option_d      TEXT    NOT NULL,
            correct_answer TEXT   NOT NULL,
            explanation   TEXT    NOT NULL,
            correction_tip TEXT   NOT NULL
        );

        CREATE TABLE IF NOT EXISTS quiz_attempts (
            attempt_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            subject         TEXT    NOT NULL,
            topic_code      TEXT,
            difficulty      INTEGER NOT NULL,
            score           INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage      INTEGER NOT NULL,
            xp_earned       INTEGER NOT NULL,
            completed_at    TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS user_answers (
            answer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id  INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            user_answer TEXT,
            is_correct  INTEGER NOT NULL,
            FOREIGN KEY (attempt_id)  REFERENCES quiz_attempts(attempt_id),
            FOREIGN KEY (question_id) REFERENCES questions(question_id)
        );
    ''')
    conn.commit()

    # Migrations: add columns that may be missing from older DB schemas
    for sql in [
        'ALTER TABLE questions ADD COLUMN topic_code TEXT',
        'ALTER TABLE quiz_attempts ADD COLUMN topic_code TEXT',
    ]:
        try:
            c.execute(sql)
            conn.commit()
        except Exception:
            pass  # Column already exists — safe to ignore

    for sql in [
        "ALTER TABLE users ADD COLUMN subscription_plan TEXT DEFAULT 'free'",
        "ALTER TABLE users ADD COLUMN subscription_expires TEXT",
    ]:
        try:
            c.execute(sql)
            conn.commit()
        except Exception:
            pass

    for sql in [
        'ALTER TABLE users ADD COLUMN email TEXT',
        'ALTER TABLE users ADD COLUMN first_name TEXT',
        'ALTER TABLE users ADD COLUMN last_name TEXT',
    ]:
        try:
            c.execute(sql)
            conn.commit()
        except Exception:
            pass

    conn.close()


def create_user(username, password, email=None, first_name=None, last_name=None):
    conn = get_db()
    try:
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        conn.execute(
            'INSERT INTO users (username, password_hash, email, first_name, last_name) VALUES (?, ?, ?, ?, ?)',
            (username, password_hash, email, first_name, last_name)
        )
        conn.commit()
        return True, 'Account created.'
    except sqlite3.IntegrityError:
        return False, 'That username is already taken.'
    finally:
        conn.close()


def authenticate_user(username, password):
    """Accept login via username OR email address."""
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)',
        (username, username)
    ).fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None


def get_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_questions(subject, difficulty, topic_code=None):
    conn = get_db()
    c = conn.cursor()
    if topic_code:
        c.execute(
            'SELECT * FROM questions WHERE subject=? AND difficulty=? AND topic_code=?',
            (subject, difficulty, topic_code)
        )
    else:
        c.execute(
            'SELECT * FROM questions WHERE subject=? AND difficulty=?',
            (subject, difficulty)
        )
    rows = c.fetchall()
    conn.close()
    return rows


def get_topic_counts(subject):
    """Returns {topic_code: {difficulty: count}} for a subject."""
    conn = get_db()
    c = conn.cursor()
    c.execute(
        'SELECT topic_code, difficulty, COUNT(*) FROM questions '
        'WHERE subject=? AND topic_code IS NOT NULL '
        'GROUP BY topic_code, difficulty',
        (subject,)
    )
    rows = c.fetchall()
    conn.close()
    counts = {}
    for code, diff, cnt in rows:
        if code not in counts:
            counts[code] = {}
        counts[code][diff] = cnt
    return counts


def get_questions_by_ids(ids):
    if not ids:
        return []
    placeholders = ','.join('?' * len(ids))
    conn = get_db()
    rows = conn.execute(
        f'SELECT * FROM questions WHERE question_id IN ({placeholders})', ids
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def save_attempt(user_id, subject, difficulty, score, total, xp_earned, answers, questions, topic_code=None):
    percentage = round((score / total) * 100) if total else 0
    conn = get_db()
    c = conn.cursor()
    c.execute(
        '''INSERT INTO quiz_attempts
           (user_id, subject, difficulty, score, total_questions, percentage, xp_earned, topic_code)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, subject, difficulty, score, total, percentage, xp_earned, topic_code)
    )
    attempt_id = c.lastrowid

    q_map = {str(q['question_id']): q for q in questions}
    for qid_str, user_answer in answers.items():
        q = q_map.get(qid_str)
        if q:
            is_correct = 1 if (user_answer or '').upper() == q['correct_answer'].upper() else 0
            c.execute(
                '''INSERT INTO user_answers (attempt_id, question_id, user_answer, is_correct)
                   VALUES (?, ?, ?, ?)''',
                (attempt_id, q['question_id'], user_answer, is_correct)
            )

    c.execute(
        'UPDATE users SET total_quizzes = total_quizzes + 1 WHERE user_id = ?',
        (user_id,)
    )
    conn.commit()
    conn.close()
    return attempt_id


def get_attempt(attempt_id, user_id):
    conn = get_db()
    attempt = conn.execute(
        'SELECT * FROM quiz_attempts WHERE attempt_id = ? AND user_id = ?',
        (attempt_id, user_id)
    ).fetchone()
    if not attempt:
        conn.close()
        return None
    attempt = dict(attempt)

    wrong = conn.execute(
        '''SELECT ua.user_answer, q.question_text, q.correct_answer,
                  q.option_a, q.option_b, q.option_c, q.option_d,
                  q.explanation, q.correction_tip
           FROM user_answers ua
           JOIN questions q ON ua.question_id = q.question_id
           WHERE ua.attempt_id = ? AND ua.is_correct = 0''',
        (attempt_id,)
    ).fetchall()
    attempt['wrong_answers'] = [dict(r) for r in wrong]

    conn.close()
    return attempt


def get_recent_attempts(user_id, limit=10):
    conn = get_db()
    rows = conn.execute(
        '''SELECT * FROM quiz_attempts WHERE user_id = ?
           ORDER BY completed_at DESC LIMIT ?''',
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_streak(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    today = date.today().isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    last = user['last_active_date']
    current = user['current_streak']
    highest = user['highest_streak']
    bonus = False

    if last == today:
        conn.close()
        return False, current

    if last == yesterday:
        current += 1
    else:
        current = 1

    if current > highest:
        highest = current

    if current % 10 == 0:
        bonus = True

    conn.execute(
        '''UPDATE users
           SET current_streak = ?, highest_streak = ?, last_active_date = ?
           WHERE user_id = ?''',
        (current, highest, today, user_id)
    )
    conn.commit()
    conn.close()
    return bonus, current


def add_xp(user_id, amount):
    conn = get_db()
    conn.execute('UPDATE users SET xp = xp + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()


def questions_exist():
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    conn.close()
    return count > 0


def get_all_users():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT u.user_id, u.username, u.first_name, u.last_name, u.email,
               u.xp, u.current_streak, u.highest_streak,
               u.total_quizzes, u.subscription_plan, u.subscription_expires,
               u.created_at, u.last_active_date,
               COUNT(qa.attempt_id) as quiz_count
        FROM users u
        LEFT JOIN quiz_attempts qa ON u.user_id = qa.user_id
        GROUP BY u.user_id
        ORDER BY u.created_at DESC
    ''')
    rows = c.fetchall()
    conn.close()
    return rows

def get_admin_stats():
    conn = get_db()
    c = conn.cursor()
    stats = {}
    c.execute('SELECT COUNT(*) FROM users')
    stats['total_users'] = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE subscription_plan = 'premium'")
    stats['premium_users'] = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM quiz_attempts')
    stats['total_quizzes'] = c.fetchone()[0]
    c.execute('SELECT COUNT(DISTINCT user_id) FROM quiz_attempts WHERE DATE(completed_at) = DATE("now")')
    stats['active_today'] = c.fetchone()[0]
    conn.close()
    return stats

def update_user_subscription(user_id, plan, expires=None):
    conn = get_db()
    conn.execute(
        'UPDATE users SET subscription_plan=?, subscription_expires=? WHERE user_id=?',
        (plan, expires, user_id)
    )
    conn.commit()
    conn.close()


def get_users_for_reminder(days_inactive=7):
    """Return users with email who haven't been active for N days."""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT user_id, username, email, last_active_date
        FROM users
        WHERE email IS NOT NULL
          AND email != ''
          AND (
            last_active_date IS NULL
            OR DATE(last_active_date) <= DATE('now', ?)
          )
    ''', (f'-{days_inactive} days',))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]
