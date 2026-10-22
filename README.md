# VecinoClub landing

Landing estática de VecinoClub. Se construye con Python estándar, sin dependencias externas. El build copia el sitio a `dist/` y genera `/llms.txt` como Markdown a partir del texto público y los enlaces de `index.html`, incluidos los ejemplos de beneficios definidos en ese mismo archivo.

En Vercel, usa este repositorio con **Root Directory** en `.` y producción desde `main`. Las páginas son `index.html` y `contacto.html` (servida en `/contacto` gracias a `cleanUrls` en `vercel.json`), con estilos en `styles.css`; los fondos están en `assets/`, las fuentes aprobadas autoalojadas en `fonts/`. `/llms.txt` es una convención reconocible para publicar contexto de un sitio en texto plano a herramientas de IA; se genera en cada build desde la landing para mantenerlo sincronizado.

## Marca

Los logos, iconos, fuentes y tokens de marca son copias de [`itsmistermoon/vecinoclub-brand`](https://github.com/itsmistermoon/vecinoclub-brand), fijadas al commit indicado en `scripts/sync-brand.sh`. No se editan a mano. Para actualizar, cambia `REF` y ejecuta `scripts/sync-brand.sh`; `--check` compara contra la fuente y `--verify` valida `assets/brand/SHA256SUMS` sin red. Los estilos propios de esta landing permanecen en `styles.css`.

La galería de ejemplos y las transiciones están implementadas en la página y respetan `prefers-reduced-motion`.
