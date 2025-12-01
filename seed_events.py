# seed_events.py — idempotent seeding using your app models
from app import app, db, Event
from datetime import datetime, timedelta, timezone

with app.app_context():
    count = Event.query.count()
    print('existing events ->', count)
    if count > 0:
        print('No action: events already present.')
    else:
        now = datetime.now(timezone.utc).isoformat()
        events = [
            ("Coding Workshop","Hands-on coding workshop","Lab A",
             (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
             (datetime.now(timezone.utc) + timedelta(days=2, hours=4)).isoformat(),
             "event_1.jpg"),
            ("Music Day","Live musical performances","Auditorium",
             (datetime.now(timezone.utc) + timedelta(days=4)).isoformat(),
             (datetime.now(timezone.utc) + timedelta(days=4, hours=4)).isoformat(),
             "event_2.jpg"),
            ("Hackathon","24-hour coding challenge","Main Hall",
             (datetime.now(timezone.utc) + timedelta(days=6)).isoformat(),
             (datetime.now(timezone.utc) + timedelta(days=6, hours=4)).isoformat(),
             "event_3.jpg"),
            ("Robotics Championship","Robot battles & competitions","Sports Complex",
             (datetime.now(timezone.utc) + timedelta(days=8)).isoformat(),
             (datetime.now(timezone.utc) + timedelta(days=8, hours=4)).isoformat(),
             "event_4.jpg"),
        ]

        for t,d,v,start,end,img in events:
            e = Event(
                title=t,
                description=d,
                venue=v,
                start_time=start,
                end_time=end,
                capacity=60,
                image_filename=img,
                created_at=now
            )
            db.session.add(e)
        db.session.commit()
        print('Seeded', len(events), 'events.')
