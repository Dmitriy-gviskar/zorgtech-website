import re, json, os, sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://zorgtech.com/catalog/product/diamant-46-f-outdoor/"
slug = url.rstrip('/').split('/')[-1]

import subprocess
result = subprocess.run(['curl', '-sL', '--max-time', '15', url], capture_output=True, text=True)
html = result.stdout

# Remove scripts and styles
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html, flags=re.DOTALL)

# Extract title
title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
title = title_match.group(1).strip() if title_match else slug.replace('-', ' ').title()

# Extract all images
imgs = list(set(re.findall(r'"(/upload/[^"]+\.(?:png|jpg|webp))"', html)))
imgs = [i for i in imgs if 'preview' not in i.lower()][:8]

# Extract text blocks
clean = re.sub(r'<[^>]+>', ' ', html)
clean = re.sub(r'\s+', ' ', clean).strip()
blocks = re.findall(r'[А-ЯЁA-Z][^.]{60,}\.', clean)
desc_blocks = []
for b in blocks:
    t = b.strip()
    if len(t) > 60 and 'zorgtech' not in t.lower() and 'куки' not in t.lower() and 'телефон' not in t.lower():
        desc_blocks.append(t)

# Extract specs table if exists
specs = {}
spec_rows = re.findall(r'<tr[^>]*>.*?<td[^>]*>([^<]+)</td>.*?<td[^>]*>([^<]+)</td>', html, re.DOTALL)
for key, val in spec_rows:
    specs[key.strip()] = val.strip()

print(json.dumps({
    "title": title,
    "images": imgs,
    "description": desc_blocks[:5],
    "specs": specs
}, ensure_ascii=False, indent=2))
