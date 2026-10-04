const ALLOWED_HOSTS = ['data.europa.eu', 'data.gov.ua', 'arma.gov.ua'];

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname !== '/proxy') {
      return new Response('ARMA proxy — utilisez /proxy?url=...', { status: 200 });
    }
    const target = url.searchParams.get('url');
    if (!target) return new Response('url requis', { status: 400 });
    let u;
    try { u = new URL(target); } catch { return new Response('url invalide', { status: 400 }); }
    if (!ALLOWED_HOSTS.some(h => u.hostname === h || u.hostname.endsWith('.' + h))) {
      return new Response('hôte non autorisé', { status: 403 });
    }
    const upstream = await fetch(target, {
      headers: { 'User-Agent': 'ARMA-Dashboard/1.0' },
    });
    const headers = new Headers(upstream.headers);
    headers.set('Access-Control-Allow-Origin', '*');
    headers.set('X-Upstream-Status', upstream.status);
    return new Response(upstream.body, { status: upstream.status, headers });
  },
};