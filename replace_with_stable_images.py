import os, sqlite3, requests

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, "static", "uploads")
os.makedirs(UPLOADS, exist_ok=True)

# Stable, deterministic Picsum seeds (won't change)
urls = [
    ("Coding Workshop", "https://picsum.photos/seed/coding/1200/600"),
    ("Music Day", "https://picsum.photos/seed/musicday/1200/600"),
    ("Hackathon", "https://picsum.photos/seed/hackathon/1200/600"),
    ("Robotics Championship", "https://picsum.photos/seed/robotics/1200/600"),
]

print("Downloading stable images and updating DB...")

# download and save as event_1..event_4
for idx, (title, url) in enumerate(urls, start=1):
    fname = f"event_{idx}.jpg"
    fpath = os.path.join(UPLOADS, fname)
    try:
        print(f"Downloading for: {title} -> {fname}")
        r = requests.get(url, timeout=30, allow_redirects=True)
        r.raise_for_status()
        with open(fpath, "wb") as fh:
            fh.write(r.content)
        print("Saved:", fname)
    except Exception as e:
        print("Download failed for", title, ":", e)

# Update DB mapping by title
db = os.path.join(BASE, "app.db")
conn = sqlite3.connect(db)
cur = conn.cursor()
for idx, (title, url) in enumerate(urls, start=1):
    fname = f"event_{idx}.jpg"
    cur.execute("SELECT COUNT(*) FROM event WHERE title=?", (title,))
    if cur.fetchone()[0]:
        cur.execute("UPDATE event SET image_filename=? WHERE title=?", (fname, title))
        print("DB updated:", title, "->", fname)
    else:
        print("Title not found in DB:", title)

conn.commit()
conn.close()
print("Done.")
