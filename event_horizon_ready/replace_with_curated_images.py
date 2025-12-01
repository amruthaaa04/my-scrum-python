import os, sqlite3, requests

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, "static", "uploads")
os.makedirs(UPLOADS, exist_ok=True)

# Curated fixed image URLs (will not change)
urls = [
    ("Coding Workshop", "https://images.unsplash.com/photo-1537432376769-00a2f2ee5582?auto=format&fit=crop&w=1200&q=80"),
    ("Music Day", "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=1200&q=80"),
    ("Hackathon", "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1200&q=80"),
    ("Robotics Championship", "https://images.unsplash.com/photo-1581091870627-3b4c7d3f6b77?auto=format&fit=crop&w=1200&q=80"),
]

print("Downloading curated images and updating DB...")

# Download each URL to event_1.jpg..event_4.jpg
for idx, (title, url) in enumerate(urls, start=1):
    fname = f"event_{idx}.jpg"
    fpath = os.path.join(UPLOADS, fname)
    try:
        print(f"Downloading for '{title}' -> {fname}")
        r = requests.get(url, timeout=30, allow_redirects=True)
        if r.status_code == 200 and r.content:
            with open(fpath, "wb") as f:
                f.write(r.content)
            print("Saved:", fname)
        else:
            print("Download failed (status):", r.status_code)
    except Exception as e:
        print("Download error:", e)

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

print("Done. Please restart your Flask app and hard-refresh browser (Ctrl+F5).")
