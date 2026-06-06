import database as db
from seed_questions import seed

db.init_db()
if not db.questions_exist():
    seed()
    print('Database seeded with sample questions.')

from app import app
app.run(debug=True, port=5001)
