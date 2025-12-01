import os

count = 0

for root, _, files in os.walk('.'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'rb') as fh:
                data = fh.read()
            if b'\x00' in data:
                new = data.replace(b'\x00', b'')
                with open(p, 'wb') as fh:
                    fh.write(new)
                print("Cleaned:", p)
                count += 1

print("Total cleaned files:", count)
