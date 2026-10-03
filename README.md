# VecinoClub landing

Landing estática de VecinoClub. El proyecto se sirve desde la raíz del repositorio, sin build ni dependencias externas.

En Vercel, usa este repositorio con **Root Directory** en `.` y producción desde `main`. Las páginas son `index.html` y `contacto.html` (servida en `/contacto` gracias a `cleanUrls` en `vercel.json`), con estilos en `styles.css`; los recursos de marca y el favicon están en `assets/`, las fuentes aprobadas autoalojadas en `fonts/`, y la imagen social en `og-image.png`.

La galería de ejemplos y las transiciones están implementadas en la página y respetan `prefers-reduced-motion`.
