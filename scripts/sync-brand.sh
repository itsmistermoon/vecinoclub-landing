#!/usr/bin/env bash
# Copia los archivos de marca desde ImaquinariaCL/loyalty-platform (ref fijado)
# hacia assets/brand/. No editar assets/brand/ a mano.
#
#   scripts/sync-brand.sh           descarga desde la fuente y actualiza assets/brand/
#   scripts/sync-brand.sh --check   falla si assets/brand/ difiere de la fuente (requiere gh)
#   scripts/sync-brand.sh --verify  falla si assets/brand/ difiere de SHA256SUMS (offline, usado en CI)
set -euo pipefail

REPO=ImaquinariaCL/loyalty-platform
REF=d7461f69a1e4edebaeb333b1481563a8e21b3132
# Rutas relativas a frontend/public/ según brand/platform/manifest.json
FILES=(
  brand/platform/vecinoclub_logo_color_light.svg
  brand/platform/vecinoclub_variant2_mono_dark.svg
  brand/platform/vecinoclub_favicon_color.svg
  brand/platform/favicon-16.png
  brand/platform/favicon-32.png
  vecinoclub/apple-touch-icon.png
  brand/platform/vecinoclub_social_og.png
)

cd "$(dirname "$0")/.."
DEST=assets/brand

fetch() {
  local dir=$1 f
  for f in "${FILES[@]}"; do
    gh api -H 'Accept: application/vnd.github.raw' \
      "repos/$REPO/contents/frontend/public/$f?ref=$REF" > "$dir/$(basename "$f")"
  done
}

case "${1:-}" in
  --verify)
    (cd "$DEST" && shasum -a 256 -c SHA256SUMS)
    ;;
  --check)
    tmp=$(mktemp -d)
    trap 'rm -rf "$tmp"' EXIT
    fetch "$tmp"
    for f in "${FILES[@]}"; do
      cmp "$tmp/$(basename "$f")" "$DEST/$(basename "$f")"
    done
    ;;
  "")
    rm -rf "$DEST"
    mkdir -p "$DEST"
    fetch "$DEST"
    sums=$(cd "$DEST" && shasum -a 256 -- *)
    echo "$sums" > "$DEST/SHA256SUMS"
    ;;
  *)
    echo "uso: $0 [--check|--verify]" >&2
    exit 2
    ;;
esac
