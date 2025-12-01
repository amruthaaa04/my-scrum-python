from app import db, Event

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

events = Event.query.all()
for e in events:
    e.image_filename = pick_image(e.title)

db.session.commit()
print("Assigned images to", len(events), "events.")
