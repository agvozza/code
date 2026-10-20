// Offline copy of the camera guide.
// Opens instantly from the saved copy, then quietly fetches any update for next time.
const CACHE = 'camera-guide-v1';
const FILES = ['./', 'manifest.webmanifest', 'apple-touch-icon.png', 'icon-192.png', 'icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  // every page request (/, /index.html, with or without #section) uses the one saved page
  const key = req.mode === 'navigate' ? './' : req;
  const cache = caches.open(CACHE);
  const fresh = cache.then(c => fetch(req).then(res => {
    if (res.ok) {
      // Safari refuses saved pages that came through a redirect, so store a clean copy
      const copy = res.redirected ? res.blob().then(b => new Response(b, { headers: res.headers })) : Promise.resolve(res.clone());
      return copy.then(r => c.put(key, r)).then(() => res.redirected ? c.match(key) : res);
    }
    return res;
  }));
  e.waitUntil(fresh.catch(() => {}));
  e.respondWith(cache.then(c => c.match(key, { ignoreSearch: true })).then(saved => saved || fresh));
});
