# Jaipur · marcador de Simi e Inés

App web para llevar las partidas de **Jaipur** desde el móvil. No es un marcador donde apuntar
totales: acompaña la partida entera. Se le registran las ventas, lleva la cuenta de las fichas que
quedan en cada montón, avisa cuando se agotan tres, calcula el recuento de la ronda con sus
desempates y guarda el cara a cara de las dos.

Sin dependencias, sin servidor y sin cuentas. Un HTML, un service worker y tres iconos.

## Cómo se usa

- **Toca el montón** de la mercancía que se vende → elige cuántas cartas → quién vende. Si son 3 o
  más, la app roba la ficha de bonus por su cuenta y la enseña un momento.
- **El botón del camello** de cada jugadora lleva su rebaño: se cogen y se gastan de una a cinco de
  golpe, y el diálogo se queda abierto para encadenar cambios. Cada ronda reparte 3 a cada una.
  Quien acabe con más se lleva las 5 rupias, y la app lo avisa con un `+5` antes de cerrar la ronda.
- **La ronda termina sola** al agotarse tres montones. Si se acaba antes el mazo, está el botón de
  abajo.
- **Deshacer** revierte la última acción, tantas veces como haga falta dentro de la partida.
- El menú `···` tiene las estadísticas, el historial de partidas, la copia de seguridad, la chuleta
  de puntuación y el botón de partida nueva.

## Copia de seguridad

El historial vive solo en el navegador del teléfono. Desde el menú se descarga un `.json` con todo
lo jugado y se vuelve a cargar en otro sitio. Importar **suma** en vez de reemplazar: descarta por
fecha las partidas que ya estén y añade el resto, para poder juntar lo jugado en dos teléfonos.

## Instalarla en el móvil

Abre la URL de Pages en el navegador del teléfono y añádela a la pantalla de inicio. En iPhone:
compartir → *Añadir a pantalla de inicio*. En Android: menú → *Instalar aplicación*. Se abre a
pantalla completa, con su icono, y funciona sin conexión.

## Dónde se guarda todo

En el `localStorage` del navegador del teléfono que lleva la cuenta. No hay servidor: si se borran
los datos del navegador o se cambia de móvil, el historial se va con ellos, y la única red de
seguridad es la copia que se descarga a mano.

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

El resto: mínimo de dos cartas para vender diamantes, oro o plata. La ronda acaba al agotarse tres
montones o el mazo. Los empates se resuelven por fichas de bonus y después por fichas de mercancía.
La partida es de quien logre dos sellos de excelencia.

Las **fichas de bonus las reparte la app**: monta los tres montones al empezar cada ronda, los
baraja y roba la de arriba en cada venta de 3 o más, así que las de cartón se quedan en la caja. No
se muestra cuántas quedan en cada montón.

| Montón | Fichas |
| --- | --- |
| Vender 3 | 1 · 1 · 2 · 2 · 2 · 3 · 3 |
| Vender 4 | 4 · 4 · 5 · 5 · 6 · 6 |
| Vender 5 o más | 8 · 8 · 9 · 10 · 10 |

Son 18, las del reglamento, pero ninguna fuente publica cuántas hay de cada valor: es el reparto
estándar asumido. Si la caja dice otra cosa, se corrige en la constante `BONUS`.

Cada ronda arranca además con **3 camellos por jugadora** (`CAMELLOS_INICIALES`), que es cosa de
la casa y no del reglamento.
