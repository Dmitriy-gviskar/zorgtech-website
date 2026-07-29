#!/bin/bash
# Fetch all Zorgtech catalog subcategories and pages
BASE="https://zorgtech.com"
OUT="/Users/dmitri/Downloads/zorgtech-new/data"

declare -A PAGES=(
  ["catalog-napolnye"]="/catalog/napolnye/"
  ["catalog-stoly"]="/catalog/stoly/"
  ["catalog-nastennyy"]="/catalog/nastennyy/"
  ["catalog-mono"]="/catalog/mono-napolnye/"
  ["catalog-apriori"]="/catalog/apriori/"
  ["catalog-ulichnye"]="/catalog/ulichnye/"
  ["catalog-avtokassy"]="/catalog/avtokassy/"
  ["catalog-dezinfektory"]="/catalog/dezinfektora-ruk/"
  ["catalog-otraslevye"]="/catalog/otraslevye/"
  ["catalog-detskie"]="/catalog/detskie-stoliki/"
  ["catalog-samoobsluzhivanie"]="/catalog/kioski-samoobsluzhivaniya/"
  ["catalog-unique"]="/catalog/unique/"
  ["solutions"]="/gotovye-resheniya/"
  ["projects"]="/realizovanye-proekty/"
  ["about"]="/about/"
  ["contacts"]="/contacts/"
)

for name in "${!PAGES[@]}"; do
  url="${BASE}${PAGES[$name]}"
  file="${OUT}/${name}.html"
  echo "Fetching $name: $url"
  curl -sL -o "$file" --max-time 15 "$url"
  echo "  -> $(wc -c < "$file") bytes"
done

echo "Done."
