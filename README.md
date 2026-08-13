# Jaipur · marcador de Simi e Inés

App web para llevar las partidas de **Jaipur** desde el móvil. No es un marcador donde apuntar
totales: acompaña la partida entera. Se le registran las ventas, lleva la cuenta de las fichas que
quedan en cada montón, avisa cuando se agotan tres, calcula el recuento de la ronda con sus
desempates y guarda el cara a cara de las dos.

Sin dependencias, sin servidor y sin cuentas. Un HTML, un service worker y tres iconos.

## Cómo se usa

- **Toca el montón** de la mercancía que se vende → elige cuántas cartas → quién vende. Si son 3 o
  más, pide el valor de la ficha de bonus que salga.
- **El botón del camello** de cada jugadora lleva su rebaño. Quien acabe con más se lleva las 5
  rupias, y la app lo avisa con un `+5` antes de cerrar la ronda.
- **La ronda termina sola** al agotarse tres montones. Si se acaba antes el mazo, está el botón de
  abajo.
- **Deshacer** revierte la última acción, tantas veces como haga falta dentro de la partida.
- El menú `⋯` tiene las estadísticas, la chuleta de puntuación y el botón de partida nueva.

## Instalarla en el móvil

Abre la URL de Pages en el navegador del teléfono y añádela a la pantalla de inicio. En iPhone:
compartir → *Añadir a pantalla de inicio*. En Android: menú → *Instalar aplicación*. Se abre a
pantalla completa, con su icono, y funciona sin conexión.

## Dónde se guarda todo

En el `localStorage` del navegador del teléfono que lleva la cuenta. No hay servidor ni copia: si
se borran los datos del navegador o se cambia de móvil, el historial se pierde.

## Archivos

| Archivo | Qué es |
| --- | --- |
| `index.html` | La app entera: marcado, estilos y lógica |
| `sw.js` | Service worker; red primero y caché de respaldo, para jugar sin cobertura |
| `manifest.webmanifest` | Metadatos de la PWA (nombre, colores, iconos) |
| `icono-*.png` | Iconos de la pantalla de inicio |
| `generar-iconos.py` | Regenera los PNG si cambia la paleta; no hace falta para usar la app |

## Las reglas que implementa

Valores de las fichas de mercancía, de la primera a la última:

| Mercancía | Fichas |
| --- | --- |
| Diamantes | 7 · 7 · 5 · 5 · 5 |
| Oro | 6 · 6 · 5 · 5 · 5 |
| Plata | 5 · 5 · 5 · 5 · 5 |
| Tela | 5 · 3 · 3 · 2 · 2 · 1 · 1 |
| Especias | 5 · 3 · 3 · 2 · 2 · 1 · 1 |
| Cuero | 4 · 3 · 2 · 1 · 1 · 1 · 1 · 1 · 1 |

Suman las 38 fichas de mercancía del reglamento, y los montones de bonus (7 de tres, 6 de cuatro y
5 de cinco) suman las 18 que declara. Si algún valor no coincide con la caja, se corrige en la
constante `MERCANCIAS` de `index.html`.

El resto: bonus de 1/2/3 al vender 3 cartas, 4/5/6 al vender 4 y 8/9/10 al vender 5 o más. Ficha de
camellos de 5 rupias para quien acabe con más. Mínimo de dos cartas para vender diamantes, oro o
plata. La ronda acaba al agotarse tres montones o el mazo. Los empates se resuelven por fichas de
bonus y después por fichas de mercancía. La partida es de quien logre dos sellos de excelencia.
