import os, sqlite3, requests

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, "static", "uploads")
os.makedirs(UPLOADS, exist_ok=True)

# Curated topic-matching images (Unsplash direct urls with format params)
urls = [
    "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?auto=format&fit=crop&w=1200&q=80",  # Coding Workshop
    "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=1200&q=80",  # Music Day
    "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80",  # Hackathon
    "https://images.unsplash.com/photo-1581091870627-3b4c7d3f6b77?auto=format&fit=crop&w=1200&q=80",  # Robotics
]

conn = sqlite3.connect(os.path.join(BASE, "app.db"))
cur = conn.cursor()

cur.execute("SELECT id, title FROM event ORDER BY id")
events = cur.fetchall()

# Map in order: event_1 -> first row, etc. If event count < 4, will only update existing
for i, ev in enumerate(events, start=1):
    idx = i-1
    if idx >= len(urls):
        break
    url = urls[idx]
    filename = f"event_{i}.jpg"
    path = os.path.join(UPLOADS, filename)
    try:
        print(f"Downloading image for: {ev[1]} -> {filename}")
        r = requests.get(url, timeout=20, allow_redirects=True)
        if r.status_code == 200 and r.content:
            with open(path, "wb") as f:
                f.write(r.content)
            # update DB to point to this filename
            cur.execute("UPDATE event SET image_filename = ? WHERE id = ?", (filename, ev[0]))
            conn.commit()
            print("Saved and DB updated.")
        else:
            print("Failed to download (status):", r.status_code)
    except Exception as e:
        print("Download error:", e)

conn.close()
print("Done.")
