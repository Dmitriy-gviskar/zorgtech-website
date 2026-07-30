import re
with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py') as f:
    code = f.read()

# Add gallery CSS
old = '.gallery{background'
new = '.thumbs{display:flex;gap:8px;margin-top:12px}.thumb{width:64px;height:64px;border-radius:10px;overflow:hidden;cursor:pointer;opacity:.5;transition:opacity .2s;background:var(--bg-el)}.thumb.active,.thumb:hover{opacity:1}.thumb img{width:100%;height:100%;object-fit:contain}\n.gallery{background'
code = code.replace(old, new)

# Update gallery HTML in template: show first image as main, rest as thumbs
old_gallery = """    img_tag = f'<img src="{images[0]}" alt="{title}">' if images else ''"""
new_gallery = """    img_tag = ''
    thumbs_html = ''
    if images:
        img_tag = f'<img src="{images[0]}" alt="{title}" id="mainImg">'
        if len(images) > 1:
            thumbs_html = '<div class="thumbs">'
            for i, img in enumerate(images[:5]):
                active = ' active' if i == 0 else ''
                thumbs_html += f'<div class="thumb{active}" onclick="document.getElementById(\\'mainImg\\').src=\\'{img}\\';this.parentNode.querySelectorAll(\\'.thumb\\').forEach(t=>t.classList.remove(\\'active\\'));this.classList.add(\\'active\\')"><img src="{img}" alt=""></div>'
            thumbs_html += '</div>'"""
code = code.replace(old_gallery, new_gallery)

# Update gallery div in template to include thumbs
old_div = """<div class="gallery">{img_tag}</div>"""
new_div = """<div><div class="gallery">{img_tag}</div>\n{thumbs_html}</div>"""
code = code.replace(old_div, new_div)

with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py', 'w') as f:
    f.write(code)
print('gallery updated')
