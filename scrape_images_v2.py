import re, json, os, subprocess

with open('/Users/dmitri/Downloads/zorgtech-new/data/categories.json') as f:
    cats = json.load(f)

all_products = []
for slug, cat in cats.items():
    for p in cat['products']:
        all_products.append({"slug": p["slug"], "cat": slug})

print(f"Fetching main images for {len(all_products)} products...")

BASE = "https://zorgtech.com"
img_dir = "/Users/dmitri/Downloads/zorgtech-new/img"
updates = {}

for i, prod in enumerate(all_products):
    slug = prod["slug"]
    url = f"{BASE}/catalog/product/{slug}/"
    
    try:
        result = subprocess.run(['curl', '-sL', '-H', 'Referer: https://zorgtech.com/', '--max-time', '8', url], capture_output=True, text=True, timeout=12)
        html = result.stdout
    except:
        continue
    
    # Find main product image: first image after h1 pattern (large gallery images)
    imgs = re.findall(r"<h1[^>]*>.*?<img[^>]*src=\"([^\"]+)\"", html, re.DOTALL)
    if not imgs:
        # Try any large image not in resize_cache
        imgs = re.findall(r'"(/upload/iblock/[^"]+\.(?:png|jpg))"', html)
        # Filter to only large files
        imgs = [i for i in imgs if 'resize_cache' not in i]
    
    if not imgs:
        # Fallback: use the one from categories.json
        for cat_slug, cat in cats.items():
            for p in cat['products']:
                if p['slug'] == slug and p.get('img'):
                    imgs = [p['img']]
                    break
    
    if imgs:
        # Download the image
        img_path = imgs[0]
        fname = os.path.basename(img_path)
        local = os.path.join(img_dir, fname)
        if not os.path.exists(local):
            try:
                subprocess.run(['curl', '-sL', '-H', 'Referer: https://zorgtech.com/', '--max-time', '8', '-o', local, f'{BASE}{img_path}'], timeout=10)
            except:
                pass
        if os.path.exists(local):
            size = os.path.getsize(local)
            updates[slug] = f"img/{fname}"
            print(f"[{i+1}/{len(all_products)}] {slug}: {fname} ({size} bytes)")
        else:
            print(f"[{i+1}/{len(all_products)}] {slug}: DOWNLOAD FAILED")
    else:
        print(f"[{i+1}/{len(all_products)}] {slug}: NO IMAGE FOUND")

# Update products_detail.json with new images
with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json') as f:
    data = json.load(f)

count = 0
for slug, img in updates.items():
    if slug in data:
        data[slug]['images'] = [img]
        count += 1

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nUpdated {count} products with correct large images")
