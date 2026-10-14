#!/usr/bin/env bash
# Copias fijadas de itsmistermoon/vecinoclub-brand. No editar los archivos a mano.
set -euo pipefail
REPO=https://github.com/itsmistermoon/vecinoclub-brand.git
REF=527a85763cbfb3c4a72090ab69378b9ff6d4b065
FILES=(
  assets/identity/vecinoclub_logo_color_light.svg
  assets/identity/vecinoclub_variant2_mono_dark.svg
  assets/identity/vecinoclub_favicon_color.svg
  assets/identity/favicon-16.png
  assets/identity/favicon-32.png
  assets/app-icons/apple-touch-icon.png
  assets/identity/vecinoclub_social_og.png
)
FONTS=(
  rubik-latin-wght-normal.woff2
  barlow-condensed-latin-400-normal.woff2
  barlow-condensed-latin-700-normal.woff2
)
cd "$(dirname "$0")/.."
DEST=assets/brand
MODE=${1:-}
if [[ "$MODE" == --verify ]]; then
  (cd "$DEST" && shasum -a 256 -c SHA256SUMS)
  exit
fi
if [[ "$MODE" != '' && "$MODE" != --check ]]; then
  echo "uso: $0 [--check|--verify]" >&2
  exit 2
fi
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
git clone -q "$REPO" "$TMP/brand"
git -C "$TMP/brand" checkout -q "$REF"
copy_or_check() {
  if [[ "$MODE" == --check ]]; then cmp "$1" "$2"; else cp "$1" "$2"; fi
}
if [[ "$MODE" != --check ]]; then mkdir -p "$DEST" fonts; fi
for file in "${FILES[@]}"; do
  copy_or_check "$TMP/brand/$file" "$DEST/$(basename "$file")"
done
for file in "${FONTS[@]}"; do
  copy_or_check "$TMP/brand/fonts/$file" "fonts/$file"
done
copy_or_check "$TMP/brand/tokens/vecinoclub.css" "$DEST/vecinoclub.css"
if [[ "$MODE" != --check ]]; then
  (cd "$DEST" && shasum -a 256 -- $(find . -maxdepth 1 -type f ! -name SHA256SUMS -print | sed 's|^./||' | sort)) > "$DEST/SHA256SUMS"
fi
