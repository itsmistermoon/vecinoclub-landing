# VecinoClub landing

Landing estática de VecinoClub. Python estándar construye `dist/` y genera `llms.txt` desde el contenido de `index.html`; no hay dependencias externas. CI comprueba el contenido generado.

En Vercel, usa este repositorio con **Root Directory** en `.` y producción desde `main`. Las páginas son `index.html` y `contacto.html` (servida en `/contacto` gracias a `cleanUrls` en `vercel.json`), con estilos en `styles.css`; los fondos están en `assets/`, las fuentes aprobadas autoalojadas en `fonts/`.

`/llms.txt` se genera durante el build. `robots.txt` permite el rastreo normal y no menciona un sitemap porque el sitio no publica uno; tampoco restringe bots por proveedor.

## Marca

Los logos, iconos, fuentes y tokens de marca son copias de [`itsmistermoon/vecinoclub-brand`](https://github.com/itsmistermoon/vecinoclub-brand), fijadas al commit indicado en `scripts/sync-brand.sh`. No se editan a mano. Para actualizar, cambia `REF` y ejecuta `scripts/sync-brand.sh`; `--check` compara contra la fuente y `--verify` valida `assets/brand/SHA256SUMS` sin red. Los estilos propios de esta landing permanecen en `styles.css`.

La galería de ejemplos y las transiciones están implementadas en la página y respetan `prefers-reduced-motion`.
