from app import app, db, User, Event

with app.app_context():
    print("\n===== USERS =====")
    users = User.query.all()
    print("Total users:", len(users))
    for u in users:
        print(f"[{u.id}] {u.full_name} | {u.email} | admin={getattr(u,'is_admin','N/A')}")

    print("\n===== EVENTS =====")
    events = Event.query.all()
    print("Total events:", len(events))
    for e in events:
        print("-" * 50)
        print("ID:", e.id)
        print("TITLE:", e.title)
        print("START:", e.start_time)
        print("END:", e.end_time)
        print("CAPACITY:", getattr(e, 'capacity', 'NO CAPACITY COLUMN'))
        print("IMAGE FILE:", e.image_filename)
        print("-" * 50)

print("\n===== DONE =====")
