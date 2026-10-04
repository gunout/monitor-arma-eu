// package.json : { "type": "module", "dependencies": { "express": "^4.19.2" } }
import express from 'express';
import { fileURLToPath } from 'url';
import path from 'path';

const app = express();
const PORT = process.env.PORT || 3000;

// Whitelist de domaines autorisés à être proxifiés
const ALLOWED_HOSTS = [
  'data.europa.eu',
  'data.gov.ua',
  'arma.gov.ua',
];

// Sert le dashboard statique
const __dirname = path.dirname(fileURLToPath(import.meta.url));
app.use(express.static(__dirname));

// Proxy avec whitelist
app.get('/proxy', async (req, res) => {
  const target = req.query.url;
  if (!target) return res.status(400).send('url requis');
  let u;
  try { u = new URL(target); }
  catch { return res.status(400).send('url invalide'); }
  if (!ALLOWED_HOSTS.some(h => u.hostname === h || u.hostname.endsWith('.' + h))) {
    return res.status(403).send('hôte non autorisé');
  }
  try {
    const upstream = await fetch(target, {
      headers: { 'User-Agent': 'ARMA-Dashboard/1.0' },
    });
    res.set('Access-Control-Allow-Origin', '*');
    res.set('Content-Type', upstream.headers.get('content-type') || 'application/octet-stream');
    res.set('X-Upstream-Status', upstream.status);
    const buf = Buffer.from(await upstream.arrayBuffer());
    res.send(buf);
  } catch (e) {
    res.status(502).send('Erreur upstream: ' + e.message);
  }
});

app.listen(PORT, () => console.log(`▶ http://localhost:${PORT}`));