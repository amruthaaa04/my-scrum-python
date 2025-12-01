import os, sqlite3, requests

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, 'static', 'uploads')
os.makedirs(UPLOADS, exist_ok=True)

# Curated fixed images (specific photos) - these are stable file URLs
# If a download fails, tell me the error and I'll swap the URL immediately.
curated = [
    ("Coding Workshop", "https://images.unsplash.com/photo-1517433456452-f9633a875f6f?auto=format&fit=crop&w=1200&q=80"),
    ("Music Day",        "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=1200&q=80"),
    ("Hackathon",        "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80"),
    ("Robotics Championship", "https://images.unsplash.com/photo-1581091870627-3b4c7d3f6b77?auto=format&fit=crop&w=1200&q=80"),
]

print('Downloading curated images and updating DB...')

for idx, (title, url) in enumerate(curated, start=1):
    fname = f'event_{idx}.jpg'
    fpath = os.path.join(UPLOADS, fname)
    try:
        print('Downloading', title, '->', fname)
        r = requests.get(url, timeout=30, allow_redirects=True)
        # If Unsplash returns HTML or non-image, check status/content-type
        if r.status_code == 200 and r.headers.get('Content-Type','').startswith('image'):
            with open(fpath, 'wb') as fh:
                fh.write(r.content)
            print('Saved', fname)
        else:
            print('FAILED download for', title, 'status', r.status_code, 'type', r.headers.get('Content-Type'))
    except Exception as e:
        print('ERROR downloading', title, ':', e)

# Update DB mapping by title (only if title exists)
db = os.path.join(BASE, 'app.db')
conn = sqlite3.connect(db)
cur = conn.cursor()
for idx, (title, url) in enumerate(curated, start=1):
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
