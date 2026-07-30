import json, os

with open('/Users/dmitri/Downloads/zorgtech-new/data/categories.json') as f:
    cats = json.load(f)

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json') as f:
    old = json.load(f)

out = {}
for cat_slug, cat in cats.items():
    for p in cat['products']:
        slug = p['slug']
        # Primary image from category page — this is the correct product image
        primary = None
        if p.get('img'):
            fname = os.path.basename(p['img'])
            primary = f'img/{fname}'
        
        # Keep scraped data (title, description) but replace images
        scraped = old.get(slug, {})
        title = scraped.get('title', p['name'])
        desc = scraped.get('description', [])
        
        # Use primary image as the main one
        images = [primary] if primary else []
        
        out[slug] = {
            "title": title,
            "images": images,
            "description": desc,
            "category": cat_slug,
            "cat_name": cat.get("name", "")
        }

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json', 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# Show stats
for slug in ['diamant-32-w', 'diamant-32-f', 'diamant-32-n', 'diamant-46-f-outdoor']:
    if slug in out:
        print(f'{slug}: {len(out[slug]["images"])} images - {out[slug]["images"]}')
print(f'Total: {len(out)} products')
