// Offline support: serve the app from cache, refresh the cache in the background.
// Bump CACHE when files are added or renamed.
const CACHE = 'vb-trainer-v1';
const ASSETS = [
  './',
  'index.html',
  'workout.html',
  'library.html',
  'log.html',
  'css/style.css',
  'js/app.js',
  'js/index.js',
  'js/workout.js',
  'js/library.js',
  'js/log.js',
  'data/program.json',
  'data/exercises.json',
  'manifest.webmanifest',
  'icons/icon-192.png',
  'icons/icon-512.png',
  'icons/apple-touch-icon.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  // One cache entry per file, whatever the query string (workout.html?week=3&day=A).
  const cacheKey = url.origin + url.pathname;
  event.respondWith(caches.open(CACHE).then(async (cache) => {
    const cached = await cache.match(cacheKey);
    const network = fetch(request)
      .then((res) => {
        if (res.ok) cache.put(cacheKey, res.clone());
        return res;
      })
      .catch(() => null);
    if (cached) {
      event.waitUntil(network);
      return cached;
    }
    return (await network) || Response.error();
  }));
});
