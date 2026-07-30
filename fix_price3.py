import re
with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py') as f:
    code = f.read()

# Move price button next to title in a flex row
old = '<h1 class="h1">{title}</h1>\n<p class="lead">{lead}</p>'
new = '<div class="title-row"><h1 class="h1">{title}</h1>{price_btn}</div>\n<p class="lead">{lead}</p>'
code = code.replace(old, new)

# Remove old price_btn from bottom
code = code.replace('\n{price_btn}\n</div>\n</div>', '\n</div>\n</div>')

# Add CSS for title-row
old_css = '.tag{font-size:11px'
new_css = '.title-row{display:flex;justify-content:space-between;align-items:flex-start;gap:32px;margin-bottom:20px}.title-row .h1{margin-bottom:0;flex:1}\n.tag{font-size:11px'
code = code.replace(old_css, new_css)

# Make price button compact when in title row
code = code.replace('.btn-price{flex-direction:column;gap:2px;padding:16px 36px}', '.btn-price{flex-direction:column;gap:2px;padding:16px 36px;flex-shrink:0}')

with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py', 'w') as f:
    f.write(code)
print('done')
