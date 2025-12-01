from app import app, db, Event

def pick_image(title):
    t = (title or "").lower()
    if "code" in t or "workshop" in t:
        return "coding_workshop.svg"
    if "music" in t or "concert" in t:
        return "music_day.svg"
    if "hack" in t or "hackothon" in t or "hackathon" in t:
        return "hackathon.svg"
    if "robot" in t or "robotics" in t or "champion" in t:
        return "robotics_champion.svg"
    return "coding_workshop.svg"

try:
    with app.app_context():
        events = Event.query.all()
        count = 0
        for e in events:
            new_img = pick_image(e.title)
            if e.image_filename != new_img:
                e.image_filename = new_img
            count += 1
        db.session.commit()
        print(f"Assigned images to {count} events.")
except Exception as exc:
    print("ERROR:", exc)
