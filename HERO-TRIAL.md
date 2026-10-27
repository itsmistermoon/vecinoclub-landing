# Prueba del hero isométrico

Comparar sin publicar: abrir `index.html` para la escena lateral y `index.html?hero=fondo` para la escena de fondo. También funciona con `python3 -m http.server 8765 --bind 127.0.0.1`, desde la raíz del repositorio: `http://127.0.0.1:8765/` y `http://127.0.0.1:8765/?hero=fondo`. Sin JavaScript se muestra la composición lateral.

Se conserva el título, el texto, Rubik/Barlow Condensed, los tokens y el fondo cálido oscuro de la landing, según DESIGN.md de vecinoclub-brand. El CTA principal queda como **Ver recorrido** hacia `#como-funciona`, conforme al encargo; el checkout traía “Lo quiero en mi negocio” hacia WhatsApp. Contacto permanece en `/contacto`; el WhatsApp sigue en cabecera y cierre. La tarjeta anterior y sus estilos/símbolos exclusivos se retiraron.

## SVG y movimiento

Fuente: exportación aprobada `vecinoclub-escena.svg` y JSON homónimo del editor v6. No se redibujó ni rasterizó. `assets/hero-escena.svg` usa `<img>` con texto alternativo, dimensiones explícitas y prioridad alta; no requiere librerías ni peticiones externas.

- Original: **145.902 bytes**. Versión web: **61.194 bytes** (−58,1 %); gzip local: **15.297 bytes**. La transferencia real depende del servidor.
- ViewBox original `0 0 1000 760` → `150 130 700 500`, con margen para la flotación y las líneas. Fondo transparente; se quitaron el fondo del editor, metadatos, objeto oculto y atributos de edición. Se conservaron colores y `data-shade`, necesarios para las caras de Punto.
- Optimizado con **SVGO 4.1.0**, preset-default con `inlineStyles: false` y `minifyStyles: false`, para mantener la media query de movimiento reducido y las variables de color. No hay dependencia de SVGO en producción.
- Punto flota durante **un ciclo de 3,2 s** y después queda quieto; evita movimiento perpetuo sin añadir controles. Con `prefers-reduced-motion: reduce` la animación computada es `none` (verificado en Chrome).
- En móvil la composición lateral coloca la escena debajo del texto; la de fondo reserva espacio bajo el panel y reencuadra la escena. El panel mantiene el texto y los enlaces legibles.

## Verificación local (2026-10-26)

Chrome headless vía Puppeteer local, una página a la vez; 1440×1000 y 390×844, DPR 1. Red simulada de 1,6 Mbps, latencia 150 ms, CPU ×4 y caché desactivada. LCP mediante PerformanceObserver, tres navegaciones por caso; no son datos de campo ni equivalen a Lighthouse/CrUX. La línea base es el HTML/CSS del commit anterior, servido con los mismos assets. Chrome estable y Chrome for Testing 154 se usaron tras desconectarse el navegador estable; una muestra móvil lateral se tomó con Testing.

| Composición | LCP escritorio, mediana | LCP móvil, mediana |
| --- | ---: | ---: |
| Anterior | 288 ms | 284 ms |
| Escena lateral | 972 ms | 980 ms |
| Escena de fondo | 956 ms | 960 ms |

La imagen pasa a ser el mayor elemento pintado: añade aproximadamente 0,7 s en esta simulación sin compresión, manteniéndose por debajo de 2,5 s. No se afirma igualdad con la línea base. No se observó desbordamiento horizontal, errores JavaScript ni fallos de carga en los casos medidos. Las capturas se guardan fuera del repositorio, junto a las mediciones JSON y una comparación HTML abrible.

La landing fija `data-theme="dark"` y `color-scheme: dark`; no tiene selector de tema claro. Se capturaron ambas composiciones en móvil/escritorio con preferencia de sistema clara y oscura; el sitio conserva su tema oscuro en ambos casos. No se inventó un tema nuevo para esta prueba.

Validación: diez casos funcionales (320, 390, 768, 1024 y 1440 px en ambas composiciones) sin desbordamiento, con un único h1, imagen cargada, alt y CTA Ver recorrido funcional; composición lateral sin JavaScript. CLS medido: 0 en móvil y aproximadamente 0,03 en escritorio (antes: 0,045). Siete pruebas existentes de build, verificación de checksums de marca y `git diff --check`. El build conserva el SVG en `dist/assets/`. La landing no se publica y la elección de composición queda pendiente de revisión del PR.
