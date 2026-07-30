import re
with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py') as f:
    code = f.read()

# Add price_suffix after price extraction
old = "price = price_match.group(1).strip().replace(' ', '') if price_match else None"
new = """price_suffix = f" <span class='price'>{price_match.group(1).strip()} ₽</span>" if price_match else ''
    price = price_match.group(1).strip().replace(' ', '') if price_match else None"""
code = code.replace(old, new)

# Update title template
code = code.replace('<h1 class="h1">{title}</h1>', '<h1 class="h1">{title}{price_suffix}</h1>')

# Add price CSS
code = code.replace('.lead{font-size:21px', '.price{font-size:21px;font-weight:300;color:var(--tx2);white-space:nowrap}\n.lead{font-size:21px')

with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py', 'w') as f:
    f.write(code)
print('done')
