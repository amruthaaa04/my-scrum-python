# create_tables.py — create DB tables using your app's SQLAlchemy models
from app import app, db    # assumes app.py defines pp and db (Flask & SQLAlchemy)
with app.app_context():
    db.create_all()
    print('db.create_all() completed — tables created if they did not exist')
