import re
with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py') as f:
    code = f.read()

# Remove price_suffix from title — price goes in button
code = code.replace('<h1 class="h1">{title}{price_suffix}</h1>', '<h1 class="h1">{title}</h1>')

# Update button logic: when price exists, button has price + "Купить" subtext
old_btn = '<a href="tel:88005502645" class="btn">{btn_text}</a>'
new_btn = '{price_btn}'
code = code.replace(old_btn, new_btn)

# Add price_btn generation after btn_text
old_btntext = 'btn_text = "Купить" if price else "Запросить цену"'
new_btntext = '''btn_text = "Купить" if price else "Запросить цену"
    price_btn = f\'<a href="tel:88005502645" class="btn btn-price"><span class="btn-price-val">{price_match.group(1).strip()} ₽</span><span class="btn-price-sub">Купить</span></a>\' if price_match else \'<a href="tel:88005502645" class="btn">Запросить цену</a>\''''
code = code.replace(old_btntext, new_btntext)

# Add CSS for price button
old_css = '.btn{display:inline-flex'
new_css = '.btn-price{flex-direction:column;gap:2px;padding:16px 36px}.btn-price-val{font-size:21px;font-weight:600;letter-spacing:-0.01em}.btn-price-sub{font-size:14px;font-weight:400;opacity:.8}\n.btn{display:inline-flex'
code = code.replace(old_css, new_css)

with open('/Users/dmitri/Downloads/zorgtech-new/gen_apple_products.py', 'w') as f:
    f.write(code)
print('done')
