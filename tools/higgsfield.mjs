#!/usr/bin/env node
// higgsfield.mjs — klien CLI API Higgsfield (https://docs.higgsfield.ai). Tanpa dependency (Node 18+).
//
// Kredensial: env HF_KEY = "<key_id>:<key_secret>" (JANGAN commit, JANGAN cetak).
// Header: Authorization: Key <key_id>:<key_secret>. Base: https://api.higgsfield.ai
//
// Perintah:
//   upload <berkas> [...]                 unggah acuan (jpg/png/webp/gif, wav, mp4) -> public_url
//   estimate <endpoint> <body.json>       biaya resmi (credits + usd) TANPA generate
//   submit <endpoint> <body.json> --ya    kirim generate (memakai kredit!) -> request_id
//   status <request_id>                   cek status + url hasil
//   wait <request_id> [--out berkas]      tunggu sampai selesai, unduh hasil
//   run <endpoint> <body.json> --ya --out berkas   submit + wait + unduh
//   cancel <request_id>                   batalkan (hanya saat masih queued; dana kembali)
//
// Opsi:
//   --ya          WAJIB untuk submit/run (generate = biaya; ACC Andrew/Bapak dulu)
//   --take N      bagian dari Idempotency-Key; take baru dengan body sama = generate baru (default 1)
//   --log FILE    log JSONL tiap estimate/submit/hasil (default ./hf-log.jsonl)
//   --label TEKS  label bebas di log (mis. "PM-06 S1 still")
//
// body.json boleh memuat "@upload:<path>" sebagai nilai string -> diunggah otomatis dan diganti public_url
// (path relatif ke folder body.json). Peta unggahan disimpan di <folder body>/.hf-uploads.json supaya
// berkas yang sama tidak diunggah ulang (url publik berlaku >= 7 hari).

import { readFileSync, writeFileSync, existsSync, appendFileSync, createWriteStream } from 'node:fs';
import { dirname, resolve, extname, basename } from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';

const BASE = 'https://api.higgsfield.ai';
const KEY = process.env.HF_KEY || (process.env.HF_API_KEY && process.env.HF_API_SECRET
  ? `${process.env.HF_API_KEY}:${process.env.HF_API_SECRET}` : '');
const TERMINAL = new Set(['completed', 'failed', 'nsfw', 'canceled']);
const MIME = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp',
  '.gif': 'image/gif', '.wav': 'audio/wav', '.mp4': 'video/mp4' };

const argv = process.argv.slice(2);
const opt = (name, def) => { const i = argv.indexOf(name); return i >= 0 ? argv[i + 1] : def; };
const flag = (name) => argv.includes(name);
const pos = argv.filter((a, i) => !a.startsWith('--') && !['--take', '--log', '--label', '--out'].includes(argv[i - 1]));
const LOG = resolve(opt('--log', 'hf-log.jsonl'));
const LABEL = opt('--label', '');

function die(msg) { console.error(msg); process.exit(1); }
function log(obj) { appendFileSync(LOG, JSON.stringify({ ts: new Date().toISOString(), label: LABEL || undefined, ...obj }) + '\n'); }

async function api(method, path, body, extraHeaders = {}) {
  if (!KEY) die('HF_KEY tidak ada di env.');
  const url = path.startsWith('http') ? path : BASE + path;
  const res = await fetch(url, {
    method,
    headers: { Authorization: `Key ${KEY}`, 'Content-Type': 'application/json', ...extraHeaders },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await res.text();
  let data; try { data = text ? JSON.parse(text) : {}; } catch { data = { raw: text }; }
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status} ${method} ${path}: ${JSON.stringify(data.detail ?? data).slice(0, 500)}`);
    err.status = res.status; err.data = data; err.cid = res.headers.get('x-correlation-id');
    throw err;
  }
  return data;
}

// ---------- upload ----------
async function uploadFile(file) {
  const ct = MIME[extname(file).toLowerCase()];
  if (!ct) die(`Tipe berkas tidak didukung API: ${file} (video harus .mp4)`);
  const buf = readFileSync(file);
  const u = await api('POST', '/files/generate-upload-url', { content_type: ct });
  const put = await fetch(u.upload_url, { method: 'PUT', headers: { ...(u.upload_headers || {}), 'Content-Type': u.content_type || ct }, body: buf });
  if (!put.ok) die(`Upload gagal ${put.status}: ${(await put.text()).slice(0, 300)}`);
  return { public_url: u.public_url, sha256: createHash('sha256').update(buf).digest('hex'), bytes: buf.length };
}

async function resolveUploads(body, baseDir) {
  const mapFile = resolve(baseDir, '.hf-uploads.json');
  const map = existsSync(mapFile) ? JSON.parse(readFileSync(mapFile, 'utf8')) : {};
  let changed = false;
  async function walk(v) {
    if (typeof v === 'string' && v.startsWith('@upload:')) {
      const p = resolve(baseDir, v.slice(8));
      const sha = createHash('sha256').update(readFileSync(p)).digest('hex');
      if (map[sha]) return map[sha].public_url;
      const r = await uploadFile(p);
      map[sha] = { public_url: r.public_url, file: basename(p), at: new Date().toISOString() };
      changed = true;
      log({ op: 'upload', file: basename(p), public_url: r.public_url, bytes: r.bytes });
      return r.public_url;
    }
    if (Array.isArray(v)) return Promise.all(v.map(walk));
    if (v && typeof v === 'object') {
      const o = {};
      for (const [k, x] of Object.entries(v)) if (!k.startsWith('_')) o[k] = await walk(x);   // kunci "_..." = catatan, tidak dikirim
      return o;
    }
    return v;
  }
  const out = await walk(body);
  if (changed) writeFileSync(mapFile, JSON.stringify(map, null, 1));
  return out;
}

async function loadBody(file) {
  const p = resolve(file);
  return resolveUploads(JSON.parse(readFileSync(p, 'utf8')), dirname(p));
}

// ---------- estimate / submit / status ----------
async function estimate(endpoint, body) {
  const e = await api('POST', `/estimate/${endpoint}`, body);
  log({ op: 'estimate', endpoint, credits: e.credits, usd: e.usd, harga: e.usd ? undefined : e.pricing_description });
  return e;
}

async function submit(endpoint, body) {
  if (!flag('--ya')) die('Generate memakai kredit. Tambahkan --ya hanya sesudah ACC Andrew/Bapak (pakai "estimate" dulu).');
  const take = opt('--take', '1');
  const key = createHash('sha256').update(`${endpoint}|${JSON.stringify(body)}|take${take}`).digest('hex').slice(0, 64);
  const est = await estimate(endpoint, body).catch((e) => ({ error: e.message }));
  const r = await api('POST', `/${endpoint}`, body, { 'Idempotency-Key': key }).catch((e) => {
    log({ op: 'submit_gagal', endpoint, take: Number(take), http: e.status, error: e.data?.detail ?? e.message, correlation: e.cid || undefined });
    throw e;
  });
  log({ op: 'submit', endpoint, take: Number(take), request_id: r.request_id, usd_est: est.usd, credits_est: est.credits });
  return { ...r, estimate: est };
}

async function status(id) { return api('GET', `/requests/${id}/status`); }

function outputs(s) {
  const urls = [];
  if (s.video?.url) urls.push(s.video.url);
  for (const im of s.images || []) if (im?.url) urls.push(im.url);
  if (s.audio?.url) urls.push(s.audio.url);
  for (const a of s.audios || []) if (a?.url) urls.push(a.url);
  return urls;
}

async function download(url, out) {
  const res = await fetch(url);
  if (!res.ok) die(`Unduh gagal ${res.status}: ${url}`);
  await pipeline(Readable.fromWeb(res.body), createWriteStream(out));
}

async function wait(id, out) {
  let delay = 2000; const t0 = Date.now();
  for (;;) {
    const s = await status(id);
    if (TERMINAL.has(s.status)) {
      const urls = outputs(s);
      const files = [];
      if (s.status === 'completed' && out) {
        for (let i = 0; i < urls.length; i++) {
          const f = urls.length === 1 ? out : out.replace(/(\.[^.]+)?$/, `-${i + 1}$1`);
          await download(urls[i], f); files.push(f);
        }
      }
      log({ op: 'hasil', request_id: id, status: s.status, error: s.error || undefined, urls, files, detik: Math.round((Date.now() - t0) / 1000) });
      return { status: s.status, error: s.error, urls, files };
    }
    if (Date.now() - t0 > 45 * 60 * 1000) die(`Timeout 45 mnt, request ${id} masih ${s.status}. Cek lagi: status ${id}`);
    await new Promise((r) => setTimeout(r, delay + Math.random() * 500));
    delay = Math.min(10000, delay * 1.5);
  }
}

// ---------- main ----------
const [cmd, a1, a2] = pos;
const print = (o) => console.log(JSON.stringify(o, null, 2));
try {
  switch (cmd) {
    case 'upload':
      for (const f of pos.slice(1)) { const r = await uploadFile(resolve(f)); log({ op: 'upload', file: basename(f), public_url: r.public_url, bytes: r.bytes }); print({ file: f, ...r }); }
      break;
    case 'estimate': print(await estimate(a1, await loadBody(a2))); break;
    case 'submit': print(await submit(a1, await loadBody(a2))); break;
    case 'status': { const s = await status(a1); print({ status: s.status, error: s.error, urls: outputs(s) }); break; }
    case 'wait': print(await wait(a1, opt('--out'))); break;
    case 'run': {
      const out = opt('--out'); if (!out) die('run butuh --out <berkas>');
      const r = await submit(a1, await loadBody(a2));
      console.error(`request ${r.request_id} (estimasi US$${r.estimate?.usd ?? '?'}) ... menunggu`);
      print({ request_id: r.request_id, estimate: r.estimate, ...(await wait(r.request_id, out)) });
      break;
    }
    case 'cancel': { const res = await fetch(`${BASE}/requests/${a1}/cancel`, { method: 'POST', headers: { Authorization: `Key ${KEY}` } }); print({ http: res.status }); break; }
    default:
      console.log(readFileSync(new URL(import.meta.url), 'utf8').split('\n').filter((l) => l.startsWith('//')).map((l) => l.slice(3)).join('\n'));
  }
} catch (e) {
  die(`${e.message}${e.cid ? ` (correlation ${e.cid})` : ''}`);
}
