import re, os, json

cats = {
    "ulichnye": "Уличные терминалы",
    "napolnye": "Напольные терминалы",
    "stoly": "Сенсорные столы",
    "nastennyy": "Настенные терминалы",
    "mono": "MONO Multitouch",
    "apriori": "Apriori",
    "avtokassy": "Автокассы",
    "dezinfektory": "Дезинфекторы рук",
    "otraslevye": "Отраслевые киоски",
    "detskie": "Детские столы",
    "samoobsluzhivanie": "Киоски самообслуживания",
}

out = {}
data_dir = "/Users/dmitri/Downloads/zorgtech-new/data"
img_dir = "/Users/dmitri/Downloads/zorgtech-new/img"

for slug, name in cats.items():
    fpath = os.path.join(data_dir, f"catalog-{slug}.html")
    if not os.path.exists(fpath):
        continue
    with open(fpath) as f:
        html = f.read()
    
    products = []
    # Find product URLs
    urls = set(re.findall(r'/catalog/product/([^/"]+)/', html))
    urls.discard('')
    
    for pslug in sorted(urls):
        # Find product name near the URL
        pattern = re.compile(r'href="[^"]*' + re.escape(pslug) + r'[^"]*"[^>]*>([^<]{3,80})</a>')
        m = pattern.search(html)
        name = m.group(1).strip() if m else pslug.replace('-', ' ').title()
        
        # Find product image near the URL
        # Look for img src near this product block
        idx = html.find(f'/catalog/product/{pslug}/')
        chunk = html[max(0,idx-2000):idx+500]
        imgs = re.findall(r'src="(/upload/[^"]+)"', chunk)
        img = imgs[-1] if imgs else None
        
        products.append({"slug": pslug, "name": name, "img": img})
    
    out[slug] = {"name": name, "products": products}

print(json.dumps(out, ensure_ascii=False, indent=2))
