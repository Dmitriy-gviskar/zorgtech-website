import json, os, subprocess

with open('/Users/dmitri/Downloads/zorgtech-new/data/categories.json') as f:
    cats = json.load(f)

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json') as f:
    data = json.load(f)

img_dir = "/Users/dmitri/Downloads/zorgtech-new/img"
BASE = "https://zorgtech.com"
count = 0

# For each product, use the category image (full product shot)
for cat_slug, cat in cats.items():
    for p in cat['products']:
        slug = p['slug']
        if slug not in data:
            continue
        
        if p.get('img'):
            fname = os.path.basename(p['img'])
            local = os.path.join(img_dir, fname)
            
            # Download the original-size image (not resize_cache)
            if not os.path.exists(local) or os.path.getsize(local) < 5000:
                try:
                    subprocess.run(['curl', '-sL', '-H', 'Referer: https://zorgtech.com/', '--max-time', '8', '-o', local, f'{BASE}{p["img"]}'], timeout=10)
                except:
                    pass
            
            if os.path.exists(local) and os.path.getsize(local) > 1000:
                data[slug]['images'] = [f'img/{fname}']
                count += 1

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Set category images for {count} products')

# Show a few
for slug in ['diamant-32-w', 'diamant-32-f', 'diamant-46-f-outdoor']:
    if slug in data:
        imgs = data[slug].get('images', [])
        if imgs:
            sz = os.path.getsize(os.path.join(img_dir, os.path.basename(imgs[0]))) if os.path.exists(os.path.join(img_dir, os.path.basename(imgs[0]))) else 0
            print(f'{slug}: {imgs[0]} ({sz} bytes)')
