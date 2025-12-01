import os, requests

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, 'static', 'uploads')
os.makedirs(UPLOADS, exist_ok=True)

pics = [
  ('event_1.jpg', 'https://picsum.photos/seed/codingworkshop/1200/600'),
  ('event_2.jpg', 'https://picsum.photos/seed/musicdayphoto/1200/600'),
  ('event_3.jpg', 'https://picsum.photos/seed/hackathonphoto/1200/600'),
  ('event_4.jpg', 'https://picsum.photos/seed/roboticsphoto/1200/600'),
]

for fname, url in pics:
    path = os.path.join(UPLOADS, fname)
    try:
        print('Downloading', fname, 'from', url)
        r = requests.get(url, timeout=30, allow_redirects=True)
        r.raise_for_status()
        ct = r.headers.get('Content-Type','')
        if not ct.startswith('image'):
            print('ERROR: not an image, content-type=', ct)
        with open(path, 'wb') as f:
            f.write(r.content)
        print('Saved', fname, 'size', os.path.getsize(path))
    except Exception as e:
        print('DOWNLOAD ERROR for', fname, e)

print('Done.')
