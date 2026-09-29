# VecinoClub landing

Landing estática independiente de `frontend/`: no usa JavaScript, build ni
dependencias del frontend. En Vercel, configurar `landing/` como **Root
Directory** y publicar como sitio estático.

Las etiquetas monoespaciadas usan `ui-monospace, Menlo, monospace` porque
JetBrains Mono no está aprobada para esta superficie. Las fuentes aprobadas
(Rubik y Barlow Condensed) están autoalojadas en `fonts/`.

Las metaetiquetas `og:url`, `og:image` y `twitter:image` de `index.html` usan
`https://vecinoclub.cl/` como URL base provisoria. Ajustarla al dominio de
Vercel cuando se asigne, y luego al apex definitivo.
