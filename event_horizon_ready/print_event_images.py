from app import app, Event

with app.app_context():
    for e in Event.query.all():
        print(repr(e.title), "=>", repr(e.image_filename))
