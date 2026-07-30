import json
from collections import Counter

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json') as f:
    data = json.load(f)

cnt = Counter()
for slug, p in data.items():
    for img in p.get('images', []):
        cnt[img] += 1

shared = {img for img, c in cnt.items() if c > 5}
print(f'Removing {len(shared)} shared images')

for slug, p in data.items():
    p['images'] = [img for img in p.get('images', []) if img not in shared]

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

for slug in ['diamant-32-w', 'diamant-32-f', 'diamant-32-n']:
    if slug in data:
        imgs = data[slug].get('images', [])
        print(f'{slug}: {len(imgs)} remaining')
print('Done')
