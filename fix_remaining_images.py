import os, sqlite3, requests, sys

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, 'static', 'uploads')
os.makedirs(UPLOADS, exist_ok=True)

# stable Picsum seeds (deterministic)
stable = [
    (2, "Music Day", "https://picsum.photos/seed/musicday/1200/600"),
    (3, "Hackathon", "https://picsum.photos/seed/hackathon/1200/600"),
    (4, "Robotics Championship", "https://picsum.photos/seed/robotics2/1200/600"),
]

for idx, title, url in stable:
    fname = f'event_{idx}.jpg'
    path = os.path.join(UPLOADS, fname)
    try:
        print('Downloading', title, '->', fname)
        r = requests.get(url, timeout=30, allow_redirects=True)
        r.raise_for_status()
        with open(path, 'wb') as fh:
            fh.write(r.content)
        print('Saved', fname, 'size', os.path.getsize(path))
    except Exception as e:
        print('ERROR downloading', title, '->', e, file=sys.stderr)

# update DB by title
db = os.path.join(BASE, 'app.db')
conn = sqlite3.connect(db)
cur = conn.cursor()
for idx, title, url in stable:
    fname = f'event_{idx}.jpg'
    cur.execute('SELECT COUNT(*) FROM event WHERE title=?', (title,))
    if cur.fetchone()[0]:
        cur.execute('UPDATE event SET image_filename=? WHERE title=?', (fname, title))
        print('DB updated:', title, '->', fname)
    else:
        print('Title not found in DB:', title)
conn.commit()
conn.close()
print('Done.')
