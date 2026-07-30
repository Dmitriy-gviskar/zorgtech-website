import re, json, os, subprocess, time

with open('/Users/dmitri/Downloads/zorgtech-new/data/categories.json') as f:
    cats = json.load(f)

all_products = []
for slug, cat in cats.items():
    for p in cat['products']:
        all_products.append({"slug": p["slug"], "cat": slug, "cat_name": cat["name"]})

print(f"Total products to scrape: {len(all_products)}")

BASE = "https://zorgtech.com"
products_data = {}

for i, prod in enumerate(all_products):
    slug = prod["slug"]
    url = f"{BASE}/catalog/product/{slug}/"
    print(f"[{i+1}/{len(all_products)}] {slug}...", end=" ", flush=True)
    
    try:
        result = subprocess.run(['curl', '-sL', '--max-time', '10', url], capture_output=True, text=True, timeout=15)
        html = result.stdout
        if not html or len(html) < 1000:
            print("EMPTY")
            continue
    except:
        print("FAIL")
        continue
    
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL)
    
    title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()
    
    imgs = list(set(re.findall(r'"(/upload/[^"]+\.(?:png|jpg|webp))"', html)))
    imgs = [i for i in imgs if 'preview' not in i.lower() and 'resize_cache' not in i][:6]
    
    clean = re.sub(r'<[^>]+>', ' ', html)
    clean = re.sub(r'\s+', ' ', clean).strip()
    blocks = re.findall(r'[А-ЯЁA-Z][^.]{40,}\.', clean)
    desc = []
    for b in blocks:
        t = b.strip()
        if len(t) > 60 and not any(w in t.lower() for w in ['zorgtech', 'куки', 'телефон', 'звонок', 'бесплатный', 'заказать звонок', 'продукция ', 'diamant f multitouch', 'diamant n multitouch', 'diamant w multitouch']):
            desc.append(t[:300])
    
    # Download images
    img_dir = "/Users/dmitri/Downloads/zorgtech-new/img"
    downloaded = []
    for img_path in imgs:
        fname = os.path.basename(img_path)
        local = os.path.join(img_dir, fname)
        if not os.path.exists(local):
            try:
                subprocess.run(['curl', '-sL', '--max-time', '8', '-o', local, f'{BASE}{img_path}'], timeout=10)
            except:
                pass
        if os.path.exists(local):
            downloaded.append(f"img/{fname}")
    
    products_data[slug] = {
        "title": title,
        "images": downloaded,
        "description": desc[:4],
        "category": prod["cat"],
        "cat_name": prod["cat_name"]
    }
    print(f"OK ({len(downloaded)} img, {len(desc)} desc)")
    time.sleep(0.3)

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json', 'w') as f:
    json.dump(products_data, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(products_data)} products to products_detail.json")
