import re
with open('/Users/dmitri/Downloads/zorgtech-new/data/projects.html') as f:
    html = f.read()
html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<[^>]+>', ' ', html)
html = re.sub(r'\s+', ' ', html).strip()
blocks = re.findall(r'[А-ЯЁA-Z][^.]{40,}\.', html)
for b in blocks[:30]:
    t = b.strip()
    if len(t) > 60:
        print(t[:250])
        print('---')
