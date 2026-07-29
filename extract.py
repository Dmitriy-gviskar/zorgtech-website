#!/usr/bin/env python3
"""Extract product names and URLs from Zorgtech catalog HTML files."""
import re, os, glob

data_dir = "/Users/dmitri/Downloads/zorgtech-new/data"
out_file = os.path.join(data_dir, "products.txt")

categories = {
    "catalog-napolnye": "Напольные сенсорные терминалы (Diamant F)",
    "catalog-stoly": "Сенсорные столы (Diamant N)",
    "catalog-nastennyy": "Настенные сенсорные терминалы (Diamant W)",
    "catalog-mono": "Сенсорные терминалы MONO",
    "catalog-apriori": "Сенсорные киоски Apriori",
    "catalog-ulichnye": "Уличные сенсорные терминалы",
    "catalog-avtokassy": "Автокассы",
    "catalog-dezinfektory": "Дезинфекторы рук",
    "catalog-otraslevye": "Отраслевые сенсорные киоски",
    "catalog-detskie": "Детские сенсорные столы",
    "catalog-samoobsluzhivanie": "Киоски самообслуживания",
    "catalog-unique": "Уникальные решения",
}

with open(out_file, "w") as out:
    for filename, cat_name in categories.items():
        fpath = os.path.join(data_dir, f"{filename}.html")
        if not os.path.exists(fpath):
            continue

        with open(fpath, "r") as f:
            html = f.read()

        # Find all product links
        product_urls = set(re.findall(r'"/catalog/product/([^/"]+)/"', html))
        # Remove empty matches from /catalog/product/
        product_urls.discard("")

        if not product_urls:
            continue

        out.write(f"## {cat_name}\n")
        for slug in sorted(product_urls):
            name = slug.replace("-", " ").title()
            out.write(f"  {name} | /catalog/product/{slug}/\n")
        out.write("\n")

    # Now solutions
    sol_path = os.path.join(data_dir, "solutions.html")
    if os.path.exists(sol_path):
        with open(sol_path, "r") as f:
            html = f.read()
        sol_urls = set(re.findall(r'"/gotovye-resheniya/([^/"]+)/"', html))
        sol_urls.discard("")
        out.write("## Готовые решения\n")
        for slug in sorted(sol_urls):
            name = slug.replace("-", " ").title()
            out.write(f"  {name} | /gotovye-resheniya/{slug}/\n")
        out.write("\n")

    # Projects
    proj_path = os.path.join(data_dir, "projects.html")
    if os.path.exists(proj_path):
        with open(proj_path, "r") as f:
            html = f.read()
        # Find project names - look for specific patterns
        # Try text content approach
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        out.write("## Реализованные проекты (текст страницы)\n")
        # Extract meaningful snippets
        snippets = re.findall(r'(?:аэропорт|музей|отель|школ|больниц|клиник|университет|вокзал|торгов|ТРЦ|ТЦ|гос|администраци|дума|медси|Медси)[^.]*\.', text, re.IGNORECASE)
        for s in snippets[:20]:
            out.write(f"  {s.strip()}\n")
        out.write("\n")

print(f"Done. Saved to {out_file}")
print(f"Size: {os.path.getsize(out_file)} bytes")
