import sqlite3, os

paths = ["app.db", "instance/app.db"]

for path in paths:
    abspath = os.path.abspath(path)
    print("\nChecking:", abspath)
    if not os.path.exists(path):
        print("  -> does NOT exist")
        continue
    print("  -> exists")
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cur.fetchall()
    print("  Tables:", tables)
    if ('event',) in tables:
        cur.execute("PRAGMA table_info(event);")
        print("  event columns:", cur.fetchall())
        cur.execute("SELECT COUNT(*) FROM event;")
        print("  event rowcount:", cur.fetchone()[0])
    conn.close()
