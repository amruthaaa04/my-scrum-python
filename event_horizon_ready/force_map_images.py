import sqlite3, os, requests

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, "static", "uploads")

# Ensure uploads folder exists
os.makedirs(UPLOADS, exist_ok=True)

# Ensure event_4.jpg exists
event4_path = os.path.join(UPLOADS, "event_4.jpg")
if not os.path.exists(event4_path):
    url = "https://images.unsplash.com/photo-1581091870627-3b4c7d3f6b77?auto=format&fit=crop&w=1200&q=80"
    print("Downloading event_4.jpg...")
    r = requests.get(url, timeout=20, allow_redirects=True)
    if r.status_code == 200 and r.content:
        with open(event4_path, "wb") as f:
            f.write(r.content)
        print("event_4.jpg downloaded.")
    else:
        print("Failed to download event_4.jpg:", r.status_code)

# Update DB
conn = sqlite3.connect(os.path.join(BASE, "app.db"))
cur = conn.cursor()

mapping = {
    "Coding Workshop": "event_1.jpg",
    "Music Day": "event_2.jpg",
    "Hackathon": "event_3.jpg",
    "Robotics Championship": "event_4.jpg"
}

for title, fname in mapping.items():
    cur.execute("SELECT COUNT(*) FROM event WHERE title=?", (title,))
    if cur.fetchone()[0]:
        cur.execute("UPDATE event SET image_filename=? WHERE title=?", (fname, title))
        print(f"Updated: {title} -> {fname}")
    else:
        print("Title not found:", title)

conn.commit()
conn.close()

print("DB mapping complete.")
