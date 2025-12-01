from app import app, db, Event

def pick_image(title):
    t = (title or "").lower()
    if "code" in t or "workshop" in t:
        return "coding_workshop.svg"
    if "music" in t or "concert" in t:
        return "music_day.svg"
    # accept both spellings
    if "hack" in t or "hackothon" in t or "hackathon" in t:
        return "hackathon.svg"
    if "robot" in t or "robotics" in t or "champion" in t:
        return "robotics_champion.svg"
    return "coding_workshop.svg"

with app.app_context():
    events = Event.query.all()
    changed = 0
    for e in events:
        desired = pick_image(e.title)
        if e.image_filename != desired:
            print(f"Updating: {e.title!r} {e.image_filename!r} -> {desired!r}")
            e.image_filename = desired
            changed += 1
    db.session.commit()
    print(f"Done. Updated {changed} events out of {len(events)}.")
