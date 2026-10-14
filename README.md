# VecinoClub landing

Landing estática de VecinoClub. El proyecto se sirve desde la raíz del repositorio, sin build ni dependencias externas.

En Vercel, usa este repositorio con **Root Directory** en `.` y producción desde `main`. Las páginas son `index.html` y `contacto.html` (servida en `/contacto` gracias a `cleanUrls` en `vercel.json`), con estilos en `styles.css`; los fondos están en `assets/`, las fuentes aprobadas autoalojadas en `fonts/`.

## Marca

Los logos, iconos, fuentes y tokens de marca son copias de [`itsmistermoon/vecinoclub-brand`](https://github.com/itsmistermoon/vecinoclub-brand), fijadas al commit indicado en `scripts/sync-brand.sh`. No se editan a mano. Para actualizar, cambia `REF` y ejecuta `scripts/sync-brand.sh`; `--check` compara contra la fuente y `--verify` valida `assets/brand/SHA256SUMS` sin red. Los estilos propios de esta landing permanecen en `styles.css`.

La galería de ejemplos y las transiciones están implementadas en la página y respetan `prefers-reduced-motion`.
