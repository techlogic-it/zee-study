"""
Comprehensive seed – inserts all questions from _all_questions.json.
Only called on first run (when the database is empty).
"""
import json
import os
import database as db

_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_all_questions.json')


def seed_all():
    with open(_JSON_PATH, 'r') as f:
        questions = json.load(f)

    rows = [
        (
            q.get('subject'), q.get('topic'), q.get('topic_code'),
            q.get('difficulty'), q.get('question_text'),
            q.get('option_a'), q.get('option_b'),
            q.get('option_c'), q.get('option_d'),
            q.get('correct_answer'), q.get('explanation'),
            q.get('correction_tip'),
        )
        for q in questions
    ]

    conn = db.get_db()
    c = conn.cursor()
    c.executemany(
        '''INSERT INTO questions
           (subject, topic, topic_code, difficulty,
            question_text, option_a, option_b, option_c, option_d,
            correct_answer, explanation, correction_tip)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
        rows
    )
    conn.commit()
    conn.close()
    print(f'[seed_all] Inserted {len(rows)} questions.')
