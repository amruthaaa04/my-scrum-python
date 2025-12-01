import requests, os
BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, 'static', 'uploads', 'event_4.jpg')
url = 'https://picsum.photos/seed/robotics/1200/600'
print('Downloading to', path)
r = requests.get(url, timeout=30, allow_redirects=True)
r.raise_for_status()
with open(path, 'wb') as f:
    f.write(r.content)
print('Saved', path, 'size=', os.path.getsize(path))
