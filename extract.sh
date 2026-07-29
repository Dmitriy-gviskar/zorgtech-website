#!/bin/bash
OUT="/Users/dmitri/Downloads/zorgtech-new/data/products.txt"
> "$OUT"

for f in /Users/dmitri/Downloads/zorgtech-new/data/catalog-*.html; do
  catname=$(basename "$f" .html)
  echo "## ${catname}" >> "$OUT"

  # Extract all product links with their visible text
  grep -oE '<a[^>]*href="/catalog/product/[^"]*"[^>]*>[^<]*</a>' "$f" | while read -r line; do
    url=$(echo "$line" | grep -oE '/catalog/product/[^"]*')
    label=$(echo "$line" | sed 's/<[^>]*>//g' | tr -d '\n\r\t' | xargs)
    if [ -n "$label" ]; then
      echo "  $label | $url" >> "$OUT"
    fi
  done
  echo "" >> "$OUT"
done

echo "Done. Lines: $(wc -l < "$OUT")"
