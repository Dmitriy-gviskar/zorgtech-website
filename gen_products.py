import json, os

try:
    with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json') as f:
        data = json.load(f)
except:
    print("Waiting for scrape to complete... run scrape_all.py first")
    exit(1)

base_css = """:root,[data-theme="dark"]{--bg:#000;--bg-el:#1d1d1f;--bg-el-h:#333336;--tx:#f5f5f7;--tx2:#86868b;--tx3:#424245;--acc:#0071e3;--link:#2997ff;--nav-bg:rgba(0,0,0,.72);--nav-link:#ccc}
[data-theme="light"]{--bg:#fff;--bg-el:#f5f5f7;--bg-el-h:#e8e8ed;--tx:#1d1d1f;--tx2:#86868b;--tx3:#6e6e73;--acc:#0071e3;--link:#0066cc;--nav-bg:rgba(255,255,255,.8);--nav-link:#6e6e73}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}html{background:var(--bg);-webkit-font-smoothing:antialiased}
body{font-family:'SF Pro Text','Inter',ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-weight:300;font-size:17px;line-height:1.47;letter-spacing:-0.022em;color:var(--tx2);background:var(--bg);transition:background .4s,color .4s}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;height:44px;display:flex;align-items:center;justify-content:center;background:var(--nav-bg);backdrop-filter:saturate(180%) blur(20px)}.nav-inner{width:100%;max-width:1440px;padding:0 40px;display:flex;align-items:center;justify-content:space-between}.nav-logo{font-size:17px;font-weight:600;color:var(--tx);text-decoration:none;letter-spacing:-0.01em}.nav-links{display:flex;gap:36px;list-style:none;align-items:center}.nav-links a{font-size:12px;font-weight:400;color:var(--nav-link);text-decoration:none;letter-spacing:-0.12px;transition:color .2s}.nav-links a:hover{color:var(--tx)}.toggle{width:44px;height:24px;border-radius:12px;border:none;background:var(--bg-el);cursor:pointer;position:relative}.toggle::after{content:'';position:absolute;top:2px;left:2px;width:20px;height:20px;border-radius:50%;background:var(--tx);transition:transform .3s}[data-theme="light"] .toggle::after{transform:translateX(20px)}.page{padding:80px 40px 40px}.page-inner{max-width:1000px;margin:0 auto}.back{font-size:12px;color:var(--tx3);text-decoration:none;letter-spacing:-0.12px;display:inline-block;margin-bottom:40px}.back:hover{color:var(--tx)}.h1{font-family:'SF Pro Display','Inter',ui-sans-serif;font-size:40px;font-weight:600;color:var(--tx);letter-spacing:-0.28px;line-height:1.1;margin-bottom:24px}.gallery{display:flex;gap:1px;background:var(--bg-el);border-radius:28px;overflow:hidden;margin-bottom:40px;max-height:500px}.gallery img{width:100%;height:100%;object-fit:contain;background:var(--bg);padding:20px}.desc{margin-bottom:32px}.desc p{font-size:17px;color:var(--tx2);line-height:1.47;margin-bottom:12px;max-width:600px}.specs{margin-bottom:40px}.specs h2{font-family:'SF Pro Display','Inter',ui-sans-serif;font-size:21px;font-weight:600;color:var(--tx);letter-spacing:0.011em;margin-bottom:12px}.btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 32px;font-family:'SF Pro Text','Inter',ui-sans-serif;font-size:17px;font-weight:400;border-radius:9999px;text-decoration:none;transition:background .2s;border:none;background:var(--acc);color:#fff;cursor:pointer}.btn:hover{background:#0077ed}.footer{padding:40px;font-size:12px;color:var(--tx3)}.footer-inner{max-width:1440px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}.footer-links{display:flex;gap:28px;list-style:none}.footer-links a{color:var(--tx2);text-decoration:none}.footer-links a:hover{color:var(--tx)}@media(max-width:640px){.nav-links{display:none}.page{padding:80px 20px 40px}.gallery{max-height:300px}}"""

count = 0
for slug, pdata in data.items():
    title = pdata["title"]
    cat_slug = pdata["category"]
    
    # Gallery: use first image as hero, rest as thumbnails
    images = pdata.get("images", [])
    gallery_html = ""
    if images:
        # Single large image
        gallery_html = f'<div class="gallery"><img src="{images[0]}" alt="{title}"></div>'
    
    # Description
    desc_html = ""
    for d in pdata.get("description", []):
        desc_html += f'<p>{d}</p>'
    
    html = f"""<!DOCTYPE html><html lang="ru" data-theme="dark"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title} — Zorgtech</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,600&display=swap" rel="stylesheet">
<style>{base_css}</style></head><body>
<nav class="nav"><div class="nav-inner"><a href="index.html" class="nav-logo">Zorgtech</a><ul class="nav-links"><li><a href="catalog.html">Продукция</a></li><li><a href="solutions.html">Решения</a></li><li><a href="projects.html">Проекты</a></li><li><a href="about.html">О компании</a></li><li><a href="contacts.html">Контакты</a></li><li><button class="toggle" id="t" aria-label="Тема"></button></li></ul></div></nav>
<div class="page"><div class="page-inner">
<a href="cat-{cat_slug}.html" class="back">← {pdata.get("cat_name", "В каталог")}</a>
<h1 class="h1">{title}</h1>
{gallery_html}
<div class="desc">{desc_html}</div>
<a href="tel:88005502645" class="btn">Запросить цену</a>
</div></div>
<footer class="footer"><div class="footer-inner"><span>© 2026 Zorgtech</span><ul class="footer-links"><li><a href="about.html">О компании</a></li><li><a href="#">Блог</a></li><li><a href="#">Поддержка</a></li><li><a href="contacts.html">Контакты</a></li></ul></div></footer>
<script>const h=document.documentElement,b=document.getElementById('t');b.addEventListener('click',()=>{{const n=h.dataset.theme==='dark'?'light':'dark';h.dataset.theme=n;try{{localStorage.setItem('zorgtech-theme',n)}}catch(e){{}}}});try{{const s=localStorage.getItem('zorgtech-theme');if(s)h.dataset.theme=s}}catch(e){{}}</script>
</body></html>"""
    
    fname = f"product-{slug}.html"
    path = os.path.join('/Users/dmitri/Downloads/zorgtech-new', fname)
    with open(path, 'w') as f:
        f.write(html)
    count += 1

# Now update all cat-*.html files to link to local product pages
for slug, cat_data in data.items():
    cat_slug = cat_data["category"]
    cat_file = f"/Users/dmitri/Downloads/zorgtech-new/cat-{cat_slug}.html"
    if os.path.exists(cat_file):
        with open(cat_file) as f:
            content = f.read()
        # Replace old site links with local product links
        content = content.replace(
            f'href="https://zorgtech.com/catalog/product/{slug}/"',
            f'href="product-{slug}.html"'
        )
        with open(cat_file, 'w') as f:
            f.write(content)

print(f"Generated {count} product pages")
