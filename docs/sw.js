/* ═══════════════════════════════════════════
   AgentKush Icarus Mods — Service Worker
   Network-first for the site's own files and the GitHub API, so returning
   visitors always get the latest mod list; the cache is only a fallback for
   when the network or the server fails. Cache-first for the pinned
   third-party CDN files.
   ═══════════════════════════════════════════ */

// agentkush.github.io is shared by every project site on the account, and Cache
// Storage belongs to the whole origin. Everything here stays inside caches with
// this prefix, so other sites' caches are never read or deleted.
const CACHE_PREFIX = 'agentkush-mods-';
// v3: v2 served the site's own files cache-first, so returning visitors never
// saw a site update. The new name makes activate() delete the v2 cache.
const CACHE_NAME = CACHE_PREFIX + 'v3';

// The page itself. The install fails without these, so a half-installed worker
// never replaces a working one. The page is cached once, as './': every visit
// refreshes that copy, and it also answers for index.html when offline.
const SHELL = ['./', './style.css', './script.js'];
// Nice to have offline. A failure here must not block the install.
const EXTRAS = [
    './particle-worker.js',
    './manifest.json',
    './og-image.png',
    './icon-192x192.png',
    './icon-512x512.png',
    './404.html',
    'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap',
    'https://cdn.jsdelivr.net/npm/vanilla-tilt@1.8.1/dist/vanilla-tilt.min.js'
];
// Versioned or immutable URLs: safe to serve from the cache without asking the network.
const CDN_HOSTS = ['fonts.googleapis.com', 'fonts.gstatic.com', 'cdn.jsdelivr.net'];

const openCache = () => caches.open(CACHE_NAME);
const cached = (key, options) => openCache().then((cache) => cache.match(key, options));

function saveCopy(key, response) {
    if (!response || !response.ok) return;
    const copy = response.clone();
    openCache()
        .then((cache) => cache.put(key, copy))
        .catch(() => {});
}

// Install: pre-cache the page, then the extras one by one
self.addEventListener('install', (event) => {
    event.waitUntil(
        openCache().then((cache) =>
            cache.addAll(SHELL).then(() =>
                Promise.all(EXTRAS.map((url) => cache.add(url).catch(() => {})))
            )
        )
    );
    self.skipWaiting();
});

// Activate: delete this site's old caches and take over open pages
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(
                keys.filter((key) => key.startsWith(CACHE_PREFIX) && key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            ))
            .then(() => self.clients.claim())
    );
});

// Offline, for a page that was never visited: the home page for the site root,
// otherwise the 404 page, which is what GitHub Pages answers online.
function offlinePage(url) {
    const root = new URL('./', self.location).pathname;
    const home = url.pathname === root || url.pathname === root + 'index.html';
    return cached(home ? './' : './404.html');
}

self.addEventListener('fetch', (event) => {
    const request = event.request;
    if (request.method !== 'GET') return;   // nothing to cache: let the browser handle it
    const url = new URL(request.url);

    // Pinned CDN files (fonts, vanilla-tilt@1.8.1): cache-first
    if (CDN_HOSTS.includes(url.hostname)) {
        event.respondWith(
            cached(request, { ignoreVary: true }).then((hit) => hit ||
                // The page asks for these without CORS, and that answer is opaque: it can't be
                // checked, so it is never cached. Ask again with CORS (both CDNs allow it) and
                // keep that copy; if that fails, pass the page's own request through.
                fetch(request.url, { mode: 'cors', credentials: 'omit' })
                    .then((response) => {
                        saveCopy(request, response);
                        return response;
                    })
                    .catch(() => fetch(request))
            )
        );
        return;
    }

    // The site's own files and the GitHub API (download counts, changelog):
    // network-first, falling back to the cache
    const api = url.hostname === 'api.github.com';
    if (url.origin === self.location.origin || api) {
        const navigate = request.mode === 'navigate';
        // One cached copy per page, whatever its query string (?q=, ?category=, ...)
        const key = navigate ? url.origin + url.pathname : request;
        event.respondWith(
            fetch(request)
                .then((response) => {
                    // A server error, or the API's rate limit: a cached copy beats the error
                    const failing = response.status >= 500 ||
                        (api && (response.status === 403 || response.status === 429));
                    if (failing) return cached(key).then((hit) => hit || response);
                    saveCopy(key, response);
                    return response;
                })
                .catch(() =>
                    cached(key)
                        .then((hit) => hit || (navigate ? offlinePage(url) : undefined))
                        .then((hit) => hit || Response.error())
                )
        );
    }
    // Anything else (GitHub's banner copies the page falls back to, icons on github.com):
    // the browser's default handling. The banners themselves are site files (banners/*.webp).
});
