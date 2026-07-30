import json, re, os

with open('/Users/dmitri/Downloads/zorgtech-new/data/products_detail.json') as f:
    data = json.load(f)

with open('/Users/dmitri/Downloads/zorgtech-new/data/categories.json') as f:
    cats = json.load(f)

# Build cat slug -> name mapping
cat_names = {}
for slug, cat in cats.items():
    cat_names[slug] = cat["name"]

def extract_features(desc_list, title):
    """Extract key features from description blocks."""
    text = ' '.join(desc_list)
    features = []
    
    # Screen/diagonal
    diag = re.search(r'(\d{2})[\s]*(?:дюйм|")', text)
    if diag:
        size = diag.group(1)
        features.append(("Диагональ", f"Сенсорный дисплей {size}″. Мультитач."))
    
    # Brightness
    bright = re.search(r'(\d+)\s*Кд', text)
    if bright:
        features.append(("Яркость", f"{bright.group(1)} Кд. Отлично виден при любом освещении."))
    
    # IP rating
    ip = re.search(r'IP\s*(\d+)', text)
    if ip:
        features.append(("Защита", f"IP{ip.group(1)}. Всепогодное исполнение."))
    
    # Glass
    if 'стекл' in text.lower():
        features.append(("Материал", "Закалённое тонированное стекло. Антивандальное исполнение."))
    
    # Capacitive/IR touch
    if 'емкост' in text.lower():
        features.append(("Технология", "Емкостной сенсорный экран. До 60 касаний."))
    elif 'инфракрасн' in text.lower() or 'ик' in text.lower():
        features.append(("Технология", "Инфракрасная сенсорная рамка. Высокая точность."))
    
    # Climate
    if 'климат' in text.lower():
        features.append(("Климат-контроль", "Встроенное климатическое оборудование."))
    
    # Printer
    if 'принтер' in text.lower() or 'печат' in text.lower():
        features.append(("Принтер", "Встроенный термопринтер. Печать чеков и талонов."))
    
    # Keyboard
    if 'клавиатур' in text.lower():
        features.append(("Клавиатура", "Встроенная металлическая клавиатура."))
    
    # Scanner
    if 'сканер' in text.lower():
        features.append(("Сканер", "Встроенный сканер документов."))
    
    # Payment
    if 'оплат' in text.lower() or 'платёж' in text.lower() or 'купюр' in text.lower():
        features.append(("Оплата", "Встроенный платёжный модуль. Приём карт и наличных."))
    
    # Anti-vandal
    if 'антивандал' in text.lower():
        if not any(f[0] == "Материал" for f in features):
            features.append(("Защита", "Антивандальное исполнение."))
    
    # Energy
    if 'энергопотреблен' in text.lower() or 'энерго' in text.lower():
        features.append(("Энергопотребление", "Низкое энергопотребление. Бесперебойная работа."))
    
    # Built-in PC
    if 'пк' in text.lower() or 'компьютер' in text.lower() or 'процессор' in text.lower():
        features.append(("Аппаратная часть", "Встроенный ПК. Надёжная комплектация."))
    
    # Kid/children
    if 'дет' in title.lower() or 'eco' in title.lower() or 'kid' in title.lower():
        features.append(("Для детей", "Безопасное исполнение. Яркий дизайн."))
    
    # Medical
    if 'medic' in title.lower() or 'медиц' in text.lower():
        features.append(("Медицина", "Специализированное медицинское исполнение."))
    
    # Disinfection
    if 'дезинфек' in text.lower() or 'agat' in title.lower():
        features.append(("Дезинфекция", "Бесконтактная обработка рук."))
    
    # Outdoor
    if 'улич' in text.lower() or 'outdoor' in title.lower():
        if not any(f[0] == "Защита" for f in features):
            features.append(("Уличное исполнение", "Всепогодный корпус. Работает под дождём и снегом."))
    
    # Fill to at least 3 features
    if len(features) < 3:
        if not any(f[0] == "Дизайн" for f in features):
            features.append(("Дизайн", "Запатентованный дизайн. Премиальное исполнение."))
        if not any(f[0] == "Аппаратная часть" for f in features):
            features.append(("Аппаратная часть", "Надёжная комплектация. Бесперебойная работа."))
    
    return features[:5]  # Max 5 features

APPLICATIONS = {
    "napolnye": [
        ("Торговые центры", "Навигация, поиск магазинов, акции"),
        ("Госучреждения", "Электронная очередь, приём документов"),
        ("Медицина", "Запись к врачу, оплата, навигация"),
        ("Транспорт", "Покупка билетов, расписание, информация"),
        ("Музеи", "Интерактивные экспозиции, аудиогид"),
        ("Отели", "Регистрация, информация, карта отеля"),
    ],
    "stoly": [
        ("Музеи", "Экспонаты из запасников, интерактивные карты"),
        ("Образование", "Расписание, документы, жизнь школы"),
        ("Переговорные", "Презентации, совместная работа"),
        ("Кафе и рестораны", "Заказ блюд, детские игровые зоны"),
    ],
    "nastennyy": [
        ("Ресепшн", "Регистрация, информация, навигация"),
        ("Медицина", "Электронная очередь, запись к врачу"),
        ("Офисы", "Пропускная система, бронирование комнат"),
        ("Ритейл", "Информация о товарах, акции"),
    ],
    "mono": [
        ("Торговые центры", "Навигация, поиск магазинов"),
        ("Госучреждения", "Электронная очередь, госуслуги"),
        ("Офисы", "Пропускная система, расписание"),
        ("Медицина", "Запись, навигация по клинике"),
    ],
    "apriori": [
        ("Ритейл", "Информация о товарах, программы лояльности"),
        ("Аптеки", "Поиск лекарств, консультация"),
        ("Банки", "Электронная очередь, курсы валют"),
        ("Госуслуги", "Приём документов, информация"),
    ],
    "ulichnye": [
        ("Транспорт", "Покупка билетов, расписание"),
        ("Парки", "Навигация, информация о мероприятиях"),
        ("АЗС", "Оплата топлива, программа лояльности"),
        ("Улицы города", "Городская навигация, афиша"),
    ],
    "avtokassy": [
        ("АЗС", "Оплата топлива, карты лояльности"),
        ("Парковки", "Оплата парковки, абонементы"),
        ("Кинотеатры", "Покупка билетов, выбор мест"),
        ("Транспорт", "Билетные кассы, регистрация"),
    ],
    "dezinfektory": [
        ("Медицина", "Поликлиники, больницы, процедурные"),
        ("Образование", "Школы, детские сады, университеты"),
        ("Торговые центры", "Входные группы, фуд-корты"),
        ("Офисы", "Ресепшн, переговорные, столовые"),
    ],
    "otraslevye": [
        ("Промышленность", "Доступ к порталу, контроль процессов"),
        ("Медицина", "Телемедицина, база знаний"),
        ("Нефтегаз", "Удалённый мониторинг, связь"),
        ("Склады", "Учёт, инвентаризация, логистика"),
    ],
    "detskie": [
        ("Детские сады", "Развивающие игры, обучение"),
        ("Школы", "Интерактивные уроки, расписание"),
        ("Игровые зоны", "Развлечения, конкурсы"),
        ("Кафе", "Детское меню, игры"),
    ],
    "samoobsluzhivanie": [
        ("Банки", "Платёжные терминалы, выписки"),
        ("Транспорт", "Билеты, регистрация, расписание"),
        ("Ритейл", "Самообслуживание, сканирование товаров"),
        ("Госуслуги", "Оплата пошлин, подача заявлений"),
    ],
}

def get_applications(cat_slug, title):
    """Get application areas for a product category."""
    apps = APPLICATIONS.get(cat_slug, [])
    if not apps:
        # Fallback: generic
        apps = [
            ("Торговые центры", "Навигация, поиск, акции"),
            ("Госучреждения", "Очередь, документы, информация"),
            ("Медицина", "Запись, оплата, навигация"),
            ("Офисы", "Пропуска, расписание, бронирование"),
        ]
    # For specific product types, filter
    title_lower = title.lower()
    if 'outdoor' in title_lower or 'улич' in title_lower:
        apps = APPLICATIONS.get("ulichnye", apps)
    if 'kid' in title_lower or 'eco' in title_lower or 'дет' in title_lower:
        apps = APPLICATIONS.get("detskie", apps)
    return apps[:4]

def make_lead(desc_list, title):
    """Create a compelling lead paragraph from scraped text."""
    text = ' '.join(desc_list)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    bad_words = ['продукция', 'diamant f', 'diamant n', 'diamant w', 'меню', 'каталог',
                 'купить за', 'заказать', 'звонок', 'бесплат', 'руб', 'р.', 'цена',
                 'о компании', 'блог', 'поддержка', 'контакты', 'области применения']
    for s in sentences:
        s = s.strip()
        s = re.sub(r'^\W+', '', s)
        # Remove price mentions
        s = re.sub(r'\d[\d\s]+\s*р\.?\s*', '', s)
        s = re.sub(r'купить\s+за\s*', '', s)
        s = re.sub(r'за\s+\d[\d\s]+\s*р\.?', '', s)
        s = re.sub(r'цена\s+по\s+запросу', '', s, flags=re.IGNORECASE)
        s = re.sub(r'\s+', ' ', s).strip()
        if len(s) > 40 and len(s) < 200:
            if not any(w in s.lower() for w in bad_words):
                # Remove leading garbage
                s = re.sub(r'^[^А-ЯЁA-Z]+', '', s)
                if len(s) > 30:
                    return s
    return ''

base_css = """:root,[data-theme="dark"]{--bg:#000;--bg-el:#1d1d1f;--bg-el-h:#333336;--tx:#f5f5f7;--tx2:#86868b;--tx3:#424245;--acc:#0071e3;--link:#2997ff;--nav-bg:rgba(0,0,0,.72);--nav-link:#ccc}
[data-theme="light"]{--bg:#fff;--bg-el:#f5f5f7;--bg-el-h:#e8e8ed;--tx:#1d1d1f;--tx2:#86868b;--tx3:#6e6e73;--acc:#0071e3;--link:#0066cc;--nav-bg:rgba(255,255,255,.8);--nav-link:#6e6e73}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}html{background:var(--bg);-webkit-font-smoothing:antialiased}
body{font-family:'SF Pro Text','Inter',ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-weight:300;font-size:17px;line-height:1.47;letter-spacing:-0.022em;color:var(--tx2);background:var(--bg);transition:background .4s,color .4s}
.nav{position:fixed;top:0;left:0;right:0;z-index:100;height:44px;display:flex;align-items:center;justify-content:center;background:var(--nav-bg);backdrop-filter:saturate(180%) blur(20px)}.nav-inner{width:100%;max-width:1440px;padding:0 40px;display:flex;align-items:center;justify-content:space-between}.nav-logo{font-size:17px;font-weight:600;color:var(--tx);text-decoration:none;letter-spacing:-0.01em}.nav-links{display:flex;gap:36px;list-style:none;align-items:center}.nav-links a{font-size:12px;font-weight:400;color:var(--nav-link);text-decoration:none;letter-spacing:-0.12px;transition:color .2s}.nav-links a:hover{color:var(--tx)}.toggle{width:44px;height:24px;border-radius:12px;border:none;background:var(--bg-el);cursor:pointer;position:relative}.toggle::after{content:'';position:absolute;top:2px;left:2px;width:20px;height:20px;border-radius:50%;background:var(--tx);transition:transform .3s}[data-theme="light"] .toggle::after{transform:translateX(20px)}
.page{padding:80px 40px 40px}.page-inner{max-width:1200px;margin:0 auto}
.back{font-size:12px;color:var(--tx3);text-decoration:none;letter-spacing:-0.12px;display:inline-block;margin-bottom:32px}.back:hover{color:var(--tx)}
.layout{display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start}
.thumbs{display:flex;gap:8px;margin-top:12px}.thumb{width:64px;height:64px;border-radius:10px;overflow:hidden;cursor:pointer;opacity:.5;transition:opacity .2s;background:var(--bg-el)}.thumb.active,.thumb:hover{opacity:1}.thumb img{width:100%;height:100%;object-fit:contain}
.gallery{background:var(--bg-el);border-radius:28px;overflow:hidden;display:flex;align-items:center;justify-content:center;aspect-ratio:3/4}
.gallery img{max-width:80%;max-height:80%;object-fit:contain}
.info{padding-top:40px}
.title-row{display:flex;justify-content:space-between;align-items:flex-start;gap:32px;margin-bottom:20px}.title-row .h1{margin-bottom:0;flex:1}
.tag{font-size:11px;font-weight:400;color:var(--acc);letter-spacing:.06em;text-transform:uppercase;margin-bottom:12px}
.h1{font-family:'SF Pro Display','Inter',ui-sans-serif;font-size:40px;font-weight:600;color:var(--tx);letter-spacing:-0.28px;line-height:1.1;margin-bottom:20px}
.price{font-size:21px;font-weight:300;color:var(--tx2);white-space:nowrap}
.lead{font-size:21px;font-weight:300;color:var(--tx2);line-height:1.38;letter-spacing:0.011em;max-width:440px;margin-bottom:32px}
.features{display:flex;flex-direction:column;gap:1px;background:var(--bg-el);border-radius:28px;overflow:hidden;margin-bottom:32px}
.feat{padding:20px 28px;background:var(--bg);transition:background .3s}.feat:hover{background:var(--bg-el-h)}
.feat h3{font-size:17px;font-weight:600;color:var(--tx);letter-spacing:-0.01em;margin-bottom:4px}
.feat p{font-size:14px;color:var(--tx2);line-height:1.43}
.apps{margin-bottom:32px}.apps h2{font-family:'SF Pro Display',Inter,ui-sans-serif;font-size:21px;font-weight:600;color:var(--tx);letter-spacing:0.011em;margin-bottom:16px}.app-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--bg-el);border-radius:28px;overflow:hidden}.app-item{padding:20px 24px;background:var(--bg);transition:background .3s}.app-item:hover{background:var(--bg-el-h)}.app-item h3{font-size:15px;font-weight:600;color:var(--tx);letter-spacing:-0.01em;margin-bottom:2px}.app-item p{font-size:12px;color:var(--tx2);line-height:1.4}
.btn-price{flex-direction:column;gap:2px;padding:16px 36px;flex-shrink:0}.btn-price-val{font-size:21px;font-weight:600;letter-spacing:-0.01em}.btn-price-sub{font-size:14px;font-weight:400;opacity:.8}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:14px 32px;font-family:'SF Pro Text','Inter',ui-sans-serif;font-size:17px;font-weight:400;border-radius:9999px;text-decoration:none;transition:background .2s;border:none;background:var(--acc);color:#fff;cursor:pointer}.btn:hover{background:#0077ed}
.footer{padding:40px;font-size:12px;color:var(--tx3);margin-top:80px}.footer-inner{max-width:1440px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}.footer-links{display:flex;gap:28px;list-style:none}.footer-links a{color:var(--tx2);text-decoration:none}.footer-links a:hover{color:var(--tx)}
@media(max-width:1024px){.layout{grid-template-columns:1fr;gap:40px}.info{padding-top:0}}
@media(max-width:640px){.nav-links{display:none}.page{padding:80px 20px 40px}.h1{font-size:32px}}"""

count = 0
for slug, pdata in data.items():
    title = pdata["title"]
    cat_slug = pdata["category"]
    cat_name = cat_names.get(cat_slug, pdata.get("cat_name", ""))
    images = pdata.get("images", [])
    desc = pdata.get("description", [])
    
    img_tag = ''
    thumbs_html = ''
    if images:
        img_tag = f'<img src="{images[0]}" alt="{title}" id="mainImg">'
        if len(images) > 1:
            thumbs_html = '<div class="thumbs">'
            for i, img in enumerate(images[:5]):
                active = ' active' if i == 0 else ''
                thumbs_html += f'<div class="thumb{active}" onclick="document.getElementById(\'mainImg\').src=\'{img}\';this.parentNode.querySelectorAll(\'.thumb\').forEach(t=>t.classList.remove(\'active\'));this.classList.add(\'active\')"><img src="{img}" alt=""></div>'
            thumbs_html += '</div>'
    lead = make_lead(desc, title)
    features = extract_features(desc, title)
    applications = get_applications(cat_slug, title)
    
    # Extract price
    text = ' '.join(desc)
    price_match = re.search(r'(\d[\d\s]+)\s*р\.', text)
    price_suffix = f" <span class='price'>{price_match.group(1).strip()} ₽</span>" if price_match else ''
    price = price_match.group(1).strip().replace(' ', '') if price_match else None
    btn_text = "Купить" if price else "Запросить цену"
    price_btn = f'<a href="tel:88005502645" class="btn btn-price"><span class="btn-price-val">{price_match.group(1).strip()} ₽</span><span class="btn-price-sub">Купить</span></a>' if price_match else '<a href="tel:88005502645" class="btn">Запросить цену</a>'
    
    features_html = ""
    apps_html = ""
    for name, desc in applications:
        apps_html += f'<div class="app-item"><h3>{name}</h3><p>{desc}</p></div>\n'
    for name, value in features:
        features_html += f'<div class="feat"><h3>{name}</h3><p>{value}</p></div>\n'
    
    html = f"""<!DOCTYPE html><html lang="ru" data-theme="dark"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{title} — Zorgtech</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,600&display=swap" rel="stylesheet">
<style>{base_css}</style></head><body>
<nav class="nav"><div class="nav-inner"><a href="index.html" class="nav-logo">Zorgtech</a><ul class="nav-links"><li><a href="catalog.html">Продукция</a></li><li><a href="solutions.html">Решения</a></li><li><a href="projects.html">Проекты</a></li><li><a href="about.html">О компании</a></li><li><a href="contacts.html">Контакты</a></li><li><button class="toggle" id="t" aria-label="Тема"></button></li></ul></div></nav>
<div class="page"><div class="page-inner">
<a href="cat-{cat_slug}.html" class="back">← {cat_name}</a>
<div class="layout">
<div><div class="gallery">{img_tag}</div>
{thumbs_html}</div>
<div class="info">
<p class="tag">{cat_name}</p>
<div class="title-row"><h1 class="h1">{title}</h1>{price_btn}</div>
<p class="lead">{lead}</p>
<div class="features">{features_html}</div>
<div class="apps"><h2>Сферы применения</h2><div class="app-grid">{apps_html}</div></div>
</div>
</div>
</div></div>
<footer class="footer"><div class="footer-inner"><span>© 2026 Zorgtech</span><ul class="footer-links"><li><a href="about.html">О компании</a></li><li><a href="#">Блог</a></li><li><a href="#">Поддержка</a></li><li><a href="contacts.html">Контакты</a></li></ul></div></footer>
<script>const h=document.documentElement,b=document.getElementById('t');b.addEventListener('click',()=>{{const n=h.dataset.theme==='dark'?'light':'dark';h.dataset.theme=n;try{{localStorage.setItem('zorgtech-theme',n)}}catch(e){{}}}});try{{const s=localStorage.getItem('zorgtech-theme');if(s)h.dataset.theme=s}}catch(e){{}}</script>
</body></html>"""
    
    fname = f"product-{slug}.html"
    path = os.path.join('/Users/dmitri/Downloads/zorgtech-new', fname)
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"Generated {count} product pages in Apple style")
