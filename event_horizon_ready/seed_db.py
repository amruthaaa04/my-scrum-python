# seed_db.py — creates app.db (backups old), creates admin with password Admin@123 and seeds 4 events
import sqlite3, os
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE, 'app.db')

# backup existing DB
if os.path.exists(db_path):
    os.rename(db_path, db_path + '.old')

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# create tables (minimal based on your app)
cur.executescript('''
CREATE TABLE IF NOT EXISTS user (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 full_name TEXT,
 email TEXT UNIQUE NOT NULL,
 password_hash TEXT NOT NULL,
 role TEXT DEFAULT 'registrant',
 created_at TEXT
);
CREATE TABLE IF NOT EXISTS event (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 title TEXT,
 description TEXT,
 venue TEXT,
 start_time TEXT,
 end_time TEXT,
 capacity INTEGER DEFAULT 60,
 image_filename TEXT,
 created_at TEXT
);
CREATE TABLE IF NOT EXISTS seat (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 event_id INTEGER,
 row TEXT,
 number INTEGER,
 is_booked INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS booking (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER,
 event_id INTEGER,
 seat_id INTEGER,
 booked_at TEXT
);
''')

now = datetime.now(timezone.utc).isoformat()

# create admin with known password
pwd_hash = generate_password_hash("Admin@123")
cur.execute("INSERT INTO user (full_name, email, password_hash, role, created_at) VALUES (?,?,?,?,?)",
            ("Administrator","admin@eventhorizon.com", pwd_hash, "admin", now))

# seed events (use event_1..event_4.jpg from static/uploads)
events = [
 ("Coding Workshop","Hands-on coding workshop","Lab A", (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(), (datetime.now(timezone.utc) + timedelta(days=2, hours=4)).isoformat(), "event_1.jpg"),
 ("Music Day","Live musical performances","Auditorium", (datetime.now(timezone.utc) + timedelta(days=4)).isoformat(), (datetime.now(timezone.utc) + timedelta(days=4, hours=4)).isoformat(), "event_2.jpg"),
 ("Hackathon","24-hour coding challenge","Main Hall", (datetime.now(timezone.utc) + timedelta(days=6)).isoformat(), (datetime.now(timezone.utc) + timedelta(days=6, hours=4)).isoformat(), "event_3.jpg"),
 ("Robotics Championship","Robot battles & competitions","Sports Complex", (datetime.now(timezone.utc) + timedelta(days=8)).isoformat(), (datetime.now(timezone.utc) + timedelta(days=8, hours=4)).isoformat(), "event_4.jpg"),
]

for t,d,v,start,end,img in events:
    cur.execute("INSERT INTO event (title, description, venue, start_time, end_time, capacity, image_filename, created_at) VALUES (?,?,?,?,?,?,?,?)",
                (t,d,v,start,end,60,img,now))

conn.commit()
conn.close()
print('SEEDER: created app.db, admin=admin@eventhorizon.com / Admin@123 and seeded 4 events.')
