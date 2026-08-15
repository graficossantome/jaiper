/* Service worker de la app de Jaipur.
 *
 * Estrategia: red primero y caché de respaldo. La partida se juega en el sofá,
 * a veces sin cobertura, así que todo tiene que seguir abriendo sin conexión;
 * pero cuando hay red interesa servir la versión recién desplegada, no una
 * copia vieja pegada para siempre (que es lo que pasa con caché primero).
 */

const CACHE = 'jaipur-v5';

const ARCHIVOS = [
  '.',
  'index.html',
  'manifest.webmanifest',
  'inter.woff2',
  'icono-192.png',
  'icono-512.png',
  'icono-180.png'
];

self.addEventListener('install', ev => {
  ev.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(ARCHIVOS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', ev => {
  ev.waitUntil(
    caches.keys()
      .then(nombres => Promise.all(nombres.filter(n => n !== CACHE).map(n => caches.delete(n))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', ev => {
  if (ev.request.method !== 'GET') return;

  // El marcador compartido no se cachea nunca: una copia vieja del espejo sería
  // peor que no tener ninguna, porque parecería estar al día.
  if (ev.request.url.includes('.supabase.co')) return;

  ev.respondWith(
    fetch(ev.request)
      .then(respuesta => {
        // Solo se guardan las respuestas buenas: cachear un 404 deja la app rota offline.
        if (respuesta.ok) {
          const copia = respuesta.clone();
          caches.open(CACHE).then(c => c.put(ev.request, copia));
        }
        return respuesta;
      })
      .catch(() => caches.match(ev.request).then(r => r || caches.match('index.html')))
  );
});
