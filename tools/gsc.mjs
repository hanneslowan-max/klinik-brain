// gsc.mjs — Google Search Console API resmi, BACA SAJA (scope webmasters.readonly), lewat service account.
// Kenapa: sheet export Agus bisa berhenti/terpotong (10.000 baris, tab harian hilang 5 Okt) dan status indeks
// selama ini BUTA. API ini gratis; kuota URL Inspection 2.000/hari & 600/menit per properti.
// Setup sekali (Bapak): deliverables/PANDUAN-GSC-API-SETUP.md. Kunci TIDAK pernah masuk repo.
//
// Kredensial (salah satu, dicek berurutan):
//   GSC_SA_JSON      isi file kunci JSON service account (boleh multi-baris)
//   GSC_SA_JSON_B64  isi file kunci JSON yang di-base64 (aman untuk kolom env satu baris)
//   GSC_SA_FILE      path ke file kunci JSON (desktop/lokal)
//
// Pemakaian (output JSON ke stdout; --csv untuk CSV):
//   node tools/gsc.mjs sites                                  properti yang bisa dibaca service account
//   node tools/gsc.mjs query <site> [--days 28 | --start YYYY-MM-DD --end YYYY-MM-DD] [--dims date,page,query]
//        [--type web|image|video|news|discover] [--page-contains x] [--query-contains x] [--country idn]
//        [--device desktop|mobile|tablet] [--limit N] [--fresh] [--csv] [--dry-run]
//        semua halaman hasil (25.000 baris per panggilan). --fresh = ikut data terbaru yang belum final.
//   node tools/gsc.mjs ringkas <site> [--days 28]             total periode, 7 hari vs 7 hari sebelumnya,
//        tanggal data terakhir, 10 halaman teratas (klik), peluang CTR (impr>=100, pos<=10, CTR<1%)
//   node tools/gsc.mjs inspect <site> <url...> | --file urls.txt | --sitemap <url> [--contains /panduan/] [--max 100] [--dry-run]
//        status indeks per URL (verdict, coverageState, lastCrawlTime, canonical Google vs kita). Jeda 1,1 dtk/URL.
//   node tools/gsc.mjs selftest                               uji tanda tangan JWT dengan kunci uji lokal (tanpa jaringan)
//
// <site>: alias `klinik` (= env KLINIK_DOMAIN, mis. namaklinik.com) atau string properti GSC persis
// (mis. "sc-domain:namaklinik.com" atau "https://namaklinik.com/"). Alias dicocokkan ke daftar `sites`.
// Tanggal = zona waktu Pacific (aturan GSC). Default akhir periode = 2 hari lalu (data GSC telat ±2–3 hari).

import crypto from "node:crypto";
import fs from "node:fs";

const SCOPE = "https://www.googleapis.com/auth/webmasters.readonly";
const API = "https://www.googleapis.com/webmasters/v3";
const INSPECT = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect";
const ALIAS = { klinik: (process.env.KLINIK_DOMAIN || "").trim() };

function die(msg, code = 1) { console.error("gsc: " + msg); process.exit(code); }

function parseArgs(argv) {
  const pos = [], opt = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const k = a.slice(2), v = argv[i + 1];
      if (v === undefined || v.startsWith("--")) opt[k] = true; else { opt[k] = v; i++; }
    } else pos.push(a);
  }
  return { pos, opt };
}

// ---------- kredensial & token ----------
function loadKey() {
  let raw = process.env.GSC_SA_JSON;
  if (!raw && process.env.GSC_SA_JSON_B64) raw = Buffer.from(process.env.GSC_SA_JSON_B64.trim(), "base64").toString("utf8");
  if (!raw && process.env.GSC_SA_FILE) raw = fs.readFileSync(process.env.GSC_SA_FILE, "utf8");
  if (!raw) die("kredensial belum ada. Isi env GSC_SA_JSON / GSC_SA_JSON_B64 / GSC_SA_FILE (lihat deliverables/PANDUAN-GSC-API-SETUP.md).");
  let k;
  try { k = JSON.parse(raw); } catch { die("isi kredensial bukan JSON yang valid (kalau pakai GSC_SA_JSON_B64, pastikan base64 dari file JSON utuh)."); }
  if (!k.client_email || !k.private_key) die("JSON kredensial tidak memuat client_email/private_key (pakai kunci SERVICE ACCOUNT, bukan OAuth client).");
  return k;
}

const b64u = (b) => Buffer.from(b).toString("base64url");
export function makeJwt(key, now = Math.floor(Date.now() / 1000)) {
  const head = b64u(JSON.stringify({ alg: "RS256", typ: "JWT" }));
  const claim = b64u(JSON.stringify({ iss: key.client_email, scope: SCOPE, aud: key.token_uri || "https://oauth2.googleapis.com/token", iat: now, exp: now + 3600 }));
  const sig = crypto.createSign("RSA-SHA256").update(`${head}.${claim}`).sign(key.private_key, "base64url");
  return `${head}.${claim}.${sig}`;
}

let TOKEN = null, KEY = null;
async function token() {
  if (TOKEN && TOKEN.exp > Date.now() + 60_000) return TOKEN.v;
  KEY = KEY || loadKey();
  const r = await fetch(KEY.token_uri || "https://oauth2.googleapis.com/token", {
    method: "POST", headers: { "content-type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer", assertion: makeJwt(KEY) }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) die(`gagal ambil token (${r.status}): ${j.error_description || j.error || "tanpa pesan"}. Cek kunci masih aktif & jam sistem benar.`);
  TOKEN = { v: j.access_token, exp: Date.now() + (j.expires_in || 3600) * 1000 };
  return TOKEN.v;
}

async function call(url, body, tries = 3) {
  for (let i = 0; i < tries; i++) {
    const r = await fetch(url, {
      method: body ? "POST" : "GET",
      headers: { authorization: "Bearer " + await token(), ...(body ? { "content-type": "application/json" } : {}) },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (r.status === 429 || r.status >= 500) { await sleep(2000 * (i + 1)); continue; }
    const j = await r.json().catch(() => ({}));
    if (r.status === 403) die(`403 dari Google: ${j.error?.message || ""}\n  Biasanya: email service account (${KEY?.client_email}) belum ditambahkan sebagai pengguna di properti GSC ini, atau "Google Search Console API" belum diaktifkan di project Google Cloud.`);
    if (!r.ok) die(`${r.status} dari Google: ${j.error?.message || JSON.stringify(j).slice(0, 300)}`);
    return j;
  }
  die("Google terus membalas 429/5xx; coba lagi nanti.");
}
const sleep = (ms) => new Promise((s) => setTimeout(s, ms));

// ---------- tanggal (zona Pacific, sesuai GSC) ----------
function pacificToday() {
  const s = new Intl.DateTimeFormat("en-CA", { timeZone: "America/Los_Angeles", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
  return new Date(s + "T00:00:00Z");
}
const iso = (d) => d.toISOString().slice(0, 10);
const addDays = (d, n) => new Date(d.getTime() + n * 86400000);
function period(opt, defDays = 28) {
  const end = opt.end ? new Date(opt.end + "T00:00:00Z") : addDays(pacificToday(), -2);
  const start = opt.start ? new Date(opt.start + "T00:00:00Z") : addDays(end, -(Number(opt.days || defDays) - 1));
  if (isNaN(start) || isNaN(end) || start > end) die("periode tidak valid (pakai YYYY-MM-DD, start <= end).");
  return { start: iso(start), end: iso(end) };
}

// ---------- site ----------
async function resolveSite(s, dry) {
  if (!s) die("site wajib: rh | pm | string properti GSC.");
  if (!ALIAS[s]) return s;
  const dom = ALIAS[s];
  if (dry) return `sc-domain:${dom} (alias; properti persis dipilih dari daftar sites saat jalan)`;
  const list = (await call(`${API}/sites`)).siteEntry || [];
  const urls = list.map((x) => x.siteUrl);
  const pick = [`sc-domain:${dom}`, `https://${dom}/`, `https://www.${dom}/`, `http://${dom}/`, `http://www.${dom}/`].find((c) => urls.includes(c));
  if (!pick) die(`properti untuk ${dom} tidak terlihat oleh service account. Yang terlihat: ${urls.join(", ") || "(kosong)"}. Tambahkan email service account di GSC > Setelan > Pengguna & izin.`);
  return pick;
}

// ---------- perintah ----------
async function cmdSites() {
  const j = await call(`${API}/sites`);
  out((j.siteEntry || []).map((x) => ({ site: x.siteUrl, izin: x.permissionLevel })));
}

async function fetchRows(site, body, limit) {
  const rows = [];
  for (let start = 0; ; start += 25000) {
    const j = await call(`${API}/sites/${encodeURIComponent(site)}/searchAnalytics/query`, { ...body, rowLimit: 25000, startRow: start });
    const got = j.rows || [];
    rows.push(...got);
    if (got.length < 25000 || (limit && rows.length >= limit)) break;
  }
  return limit ? rows.slice(0, limit) : rows;
}

function buildBody(opt, p, dims) {
  const filters = [];
  if (opt["page-contains"]) filters.push({ dimension: "page", operator: "contains", expression: String(opt["page-contains"]) });
  if (opt["query-contains"]) filters.push({ dimension: "query", operator: "contains", expression: String(opt["query-contains"]) });
  if (opt.country) filters.push({ dimension: "country", operator: "equals", expression: String(opt.country).toLowerCase() });
  if (opt.device) filters.push({ dimension: "device", operator: "equals", expression: String(opt.device).toUpperCase() });
  return {
    startDate: p.start, endDate: p.end, dimensions: dims, type: opt.type || "web",
    ...(filters.length ? { dimensionFilterGroups: [{ groupType: "and", filters }] } : {}),
    ...(opt.fresh ? { dataState: "all" } : {}),
  };
}

const flat = (dims) => (r) => {
  const o = {}; dims.forEach((d, i) => (o[d] = r.keys?.[i]));
  return { ...o, clicks: r.clicks, impressions: r.impressions, ctr: +(r.ctr * 100).toFixed(2), position: +r.position.toFixed(1) };
};

async function cmdQuery(pos, opt) {
  const dry = !!opt["dry-run"];
  const site = await resolveSite(pos[0], dry);
  const p = period(opt);
  const dims = String(opt.dims || "date").split(",").map((s) => s.trim()).filter(Boolean);
  const body = buildBody(opt, p, dims);
  if (dry) return out({ dry_run: true, site, request: { ...body, rowLimit: 25000, startRow: 0 } });
  const rows = (await fetchRows(site, body, opt.limit ? Number(opt.limit) : 0)).map(flat(dims));
  if (opt.csv) return csv(rows);
  out({ site, periode: p, dims, baris: rows.length, catatan: "ctr dalam %. Kueri anonim tidak muncul bila dimensi memuat query.", rows });
}

async function cmdRingkas(pos, opt) {
  const site = await resolveSite(pos[0]);
  const days = Number(opt.days || 28);
  const p = period({ ...opt, days }, days);
  const daily = (await fetchRows(site, buildBody(opt, p, ["date"]))).map(flat(["date"]));
  const sum = (a) => a.reduce((t, r) => ({ clicks: t.clicks + r.clicks, impressions: t.impressions + r.impressions }), { clicks: 0, impressions: 0 });
  const last = daily.map((r) => r.date).sort().pop() || null;
  const d7 = daily.filter((r) => last && r.date > iso(addDays(new Date(last + "T00:00:00Z"), -7)));
  const p7 = daily.filter((r) => last && r.date <= iso(addDays(new Date(last + "T00:00:00Z"), -7)) && r.date > iso(addDays(new Date(last + "T00:00:00Z"), -14)));
  const pages = (await fetchRows(site, buildBody(opt, p, ["page"]))).map(flat(["page"]));
  const pct = (a, b) => (b ? +(((a - b) / b) * 100).toFixed(1) : null);
  const s7 = sum(d7), sp = sum(p7);
  out({
    site, periode: p, data_terakhir: last,
    total: sum(daily),
    tujuh_hari: { periode: d7.length ? `${d7[0].date}..${last}` : null, ...s7, vs_7_sebelumnya: { ...sp, klik_pct: pct(s7.clicks, sp.clicks), impresi_pct: pct(s7.impressions, sp.impressions) } },
    halaman_teratas: pages.sort((a, b) => b.clicks - a.clicks || b.impressions - a.impressions).slice(0, 10),
    peluang_ctr: pages.filter((r) => r.impressions >= 100 && r.position <= 10 && r.ctr < 1).sort((a, b) => b.impressions - a.impressions).slice(0, 5),
    catatan: "Angka halaman = total per URL (termasuk kueri anonim). Posisi = rata-rata tertimbang Google.",
  });
}

async function urlsFromSitemap(url, depth = 0) {
  const r = await fetch(url);
  if (!r.ok) die(`sitemap ${url} → ${r.status}`);
  const x = await r.text();
  const locs = [...x.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map((m) => m[1].replace(/&amp;/g, "&"));
  if (/<sitemapindex/i.test(x) && depth < 1) {
    const all = [];
    for (const l of locs) all.push(...(await urlsFromSitemap(l, depth + 1)));
    return all;
  }
  return locs;
}

async function cmdInspect(pos, opt) {
  const dry = !!opt["dry-run"];
  const site = await resolveSite(pos[0], dry);
  let urls = pos.slice(1);
  if (opt.file) urls.push(...fs.readFileSync(opt.file, "utf8").split(/\r?\n/).map((s) => s.trim()).filter(Boolean));
  if (opt.sitemap) urls.push(...(await urlsFromSitemap(opt.sitemap)));
  if (opt.contains) urls = urls.filter((u) => u.includes(String(opt.contains)));
  urls = [...new Set(urls)];
  const max = Number(opt.max || 100);
  if (!urls.length) die("tidak ada URL. Beri URL, --file, atau --sitemap.");
  const dipotong = urls.length > max;
  urls = urls.slice(0, max);
  if (dry) return out({ dry_run: true, site, jumlah: urls.length, dipotong, contoh_request: { inspectionUrl: urls[0], siteUrl: site, languageCode: "id-ID" } });
  const res = [];
  for (const [i, u] of urls.entries()) {
    if (i) await sleep(1100);
    const j = await call(INSPECT, { inspectionUrl: u, siteUrl: site, languageCode: "id-ID" });
    const s = j.inspectionResult?.indexStatusResult || {};
    res.push({
      url: u, verdict: s.verdict, coverage: s.coverageState, indexing: s.indexingState, fetch: s.pageFetchState,
      robots: s.robotsTxtState, last_crawl: s.lastCrawlTime || null, crawled_as: s.crawledAs || null,
      canonical_google: s.googleCanonical || null, canonical_kita: s.userCanonical || null,
      canonical_beda: !!(s.googleCanonical && s.userCanonical && s.googleCanonical !== s.userCanonical),
      sitemap: s.sitemap || [], referring: (s.referringUrls || []).length,
    });
  }
  const hit = (v) => res.filter((r) => r.verdict === v).length;
  out({ site, diperiksa: res.length, dipotong, ringkas: { PASS: hit("PASS"), NEUTRAL: hit("NEUTRAL"), FAIL: hit("FAIL"), lainnya: res.length - hit("PASS") - hit("NEUTRAL") - hit("FAIL") }, catatan: "PASS = terindeks. Kuota 2.000/hari per properti.", hasil: res });
}

function cmdSelftest() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync("rsa", { modulusLength: 2048 });
  const key = { client_email: "uji@contoh.iam.gserviceaccount.com", private_key: privateKey.export({ type: "pkcs8", format: "pem" }) };
  const jwt = makeJwt(key, 1700000000);
  const [h, c, s] = jwt.split(".");
  const ok = crypto.createVerify("RSA-SHA256").update(`${h}.${c}`).verify(publicKey, Buffer.from(s, "base64url"));
  const claim = JSON.parse(Buffer.from(c, "base64url").toString());
  out({ jwt_valid: ok, scope_baca_saja: claim.scope === SCOPE, exp_detik: claim.exp - claim.iat, iss: claim.iss });
  if (!ok) process.exit(1);
}

// ---------- keluaran ----------
const out = (o) => console.log(JSON.stringify(o, null, 2));
function csv(rows) {
  if (!rows.length) return;
  const cols = Object.keys(rows[0]);
  const esc = (v) => (v == null ? "" : /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v));
  console.log([cols.join(","), ...rows.map((r) => cols.map((c) => esc(r[c])).join(","))].join("\n"));
}

// ---------- main ----------
const { pos, opt } = parseArgs(process.argv.slice(2));
const cmd = pos.shift();
const run = { sites: cmdSites, query: () => cmdQuery(pos, opt), ringkas: () => cmdRingkas(pos, opt), inspect: () => cmdInspect(pos, opt), selftest: cmdSelftest }[cmd];
if (!run) die("perintah: sites | query | ringkas | inspect | selftest (lihat komentar di atas file).", 2);
await run();
