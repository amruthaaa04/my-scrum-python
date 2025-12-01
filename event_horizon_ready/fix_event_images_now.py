import sqlite3, os
db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')
conn = sqlite3.connect(db)
cur = conn.cursor()
mapping = {
    'Coding Workshop': 'event_1.jpg',
    'Music Day': 'event_2.jpg',
    'Hackathon': 'event_3.jpg',
    'Robotics Championship': 'event_4.jpg'
}
for title, fname in mapping.items():
    cur.execute('UPDATE event SET image_filename=? WHERE title=?', (fname, title))
    print('Updated', title, '->', fname)
conn.commit()
conn.close()
print('DB update complete')
