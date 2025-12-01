import sqlite3, os
p = os.path.abspath('app.db')
print('inspecting ->', p, 'exists=', os.path.exists(p))
if not os.path.exists(p):
    print('app.db not found!')
else:
    conn = sqlite3.connect(p)
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM event")
        print('event count ->', cur.fetchone()[0])
        cur.execute("SELECT id, title, venue, start_time FROM event ORDER BY id LIMIT 10")
        rows = cur.fetchall()
        print('sample events:')
        for r in rows:
            print(' ', r)
    except Exception as e:
        print('error reading events:', e)
    finally:
        conn.close()
