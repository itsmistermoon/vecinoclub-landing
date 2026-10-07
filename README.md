# VecinoClub landing

Landing estática de VecinoClub. El proyecto se sirve desde la raíz del repositorio, sin build ni dependencias externas.

En Vercel, usa este repositorio con **Root Directory** en `.` y producción desde `main`. Las páginas son `index.html` y `contacto.html` (servida en `/contacto` gracias a `cleanUrls` en `vercel.json`), con estilos en `styles.css`; los fondos están en `assets/`, las fuentes aprobadas autoalojadas en `fonts/`.

## Marca

Los archivos de `assets/brand/` (logos, favicons, apple-touch-icon e imagen social) son copias de `ImaquinariaCL/loyalty-platform`, carpeta `frontend/public/brand/platform/`, fijadas a un commit en `scripts/sync-brand.sh`. No se editan a mano: para actualizar, cambia `REF` y ejecuta `scripts/sync-brand.sh` (requiere `gh` con acceso al repo). `scripts/sync-brand.sh --check` compara contra la fuente; `--verify` compara contra `assets/brand/SHA256SUMS` y corre en CI.

La galería de ejemplos y las transiciones están implementadas en la página y respetan `prefers-reduced-motion`.
