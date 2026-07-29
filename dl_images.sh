#!/bin/bash
IMG_DIR="/Users/dmitri/Downloads/zorgtech-new/img"
BASE="https://zorgtech.com"
mkdir -p "$IMG_DIR"

# Collect all unique product images from catalog pages
grep -ohE 'src="/upload/[^"]+\.(png|jpg|webp)"' /Users/dmitri/Downloads/zorgtech-new/data/catalog-*.html | sort -u | while read -r src; do
  # Strip src=" and "
  path=$(echo "$src" | sed 's/^src="//' | sed 's/"$//')
  fname=$(basename "$path")
  if [ ! -f "$IMG_DIR/$fname" ]; then
    curl -sL -o "$IMG_DIR/$fname" --max-time 10 "${BASE}${path}"
    echo "DL: $fname ($(wc -c < "$IMG_DIR/$fname") bytes)"
  fi
done

echo "Done. Images: $(ls "$IMG_DIR" | wc -l)"
