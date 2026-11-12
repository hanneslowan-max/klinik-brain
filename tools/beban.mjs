#!/usr/bin/env node
// beban.mjs — analisa padat/longgarnya beban kerja per orang dari kartu tugas (Anvil / ClickUp), BACA SAJA.
// Dipakai agent marketing-manager. Tanpa dependency (Node 18+).
//
//   node tools/beban.mjs                         # minggu ini + 3 minggu ke depan, semua orang
//   node tools/beban.mjs --dari 2026-10-12 --sampai 2026-10-30 [--orang Yosie] [--json]
//   node tools/beban.mjs --tanpa-sales           # sembunyikan sales (beban utamanya di pipeline, bukan kartu)
//
// Sumber kartu: folder kerja klinik (atur di tools/beban-config.json). Backend sama dengan
// tools/clickup.mjs: env TUGAS_BACKEND=tugas → Anvil (TUGAS_API_URL + TUGAS_API_TOKEN); tanpa env → ClickUp.
//
// Cara hitung (asumsi, bisa diubah di config):
// - Kapasitas = 4 poin bobot per hari kerja (pagar B5). 1 poin ≈ 2 jam kerja efektif.
// - Bobot kartu: angka "Bobot …: N" di deskripsi; kalau tak ada → bobot_default per awalan nama (config) → 1.
// - Jendela kerja kartu: start..due. Tanpa start → (bobot) hari kerja sebelum due s.d. due (min 1 hari).
//   Bobot dibagi rata ke hari kerja di jendelanya.
// - Kartu DITAHAN/BERSYARAT/tanpa due tidak dihitung sebagai beban (dilaporkan terpisah).
// - Tugas rutin di luar kartu (posting harian, pantau iklan) = config tugas_rutin (poin/hari, rentang tanggal).
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const loadEnv = (f) => { const o = {}; try { for (const l of fs.readFileSync(f, "utf8").split(/\r?\n/)) { const m = l.match(/^\s*([A-Za-z0-9_]+)\s*=\s*(.*)$/); if (m && !/^\s*#/.test(l)) o[m[1]] = m[2].trim(); } } catch {} return o; };
const env = loadEnv(path.join(HERE, ".env"));
const MODE = ((process.env.TUGAS_BACKEND || env.TUGAS_BACKEND || "clickup").trim().toLowerCase() === "tugas") ? "tugas" : "clickup";
const BASE = MODE === "tugas" ? (process.env.TUGAS_API_URL || env.TUGAS_API_URL || "").replace(/\/+$/, "") : "https://api.clickup.com/api/v2";
const TOKEN = (MODE === "tugas" ? process.env.TUGAS_API_TOKEN || env.TUGAS_API_TOKEN : process.env.CLICKUP_API_TOKEN || env.CLICKUP_API_TOKEN || "").trim();
if (!BASE || !TOKEN) { console.error(`beban: kredensial mode ${MODE} kosong`); process.exit(1); }

const args = process.argv.slice(2), opt = {};
for (let i = 0; i < args.length; i++) if (args[i].startsWith("--")) { const k = args[i].slice(2); opt[k] = args[i + 1] && !args[i + 1].startsWith("--") ? args[++i] : true; }
const CFG = JSON.parse(fs.readFileSync(path.join(HERE, "beban-config.json"), "utf8"));

async function api(url) {
  for (let t = 0; t < 5; t++) {
    const r = await fetch(BASE + url, { headers: { Authorization: TOKEN } });
    if (r.status === 429) { await new Promise((s) => setTimeout(s, (Number(r.headers.get("retry-after")) || 2) * 1000)); continue; }
    if (!r.ok) throw new Error(`${r.status} ${url}: ${(await r.text()).slice(0, 200)}`);
    if (MODE === "clickup") await new Promise((s) => setTimeout(s, 670));
    return r.json();
  }
  throw new Error("429 terus: " + url);
}
async function listTasks(id) {
  const out = [];
  for (let p = 0; ; p++) { const j = await api(`/list/${id}/task?page=${p}&subtasks=true&include_closed=true`); out.push(...(j.tasks || [])); if (j.last_page === true || (j.tasks || []).length < 100) break; }
  return out;
}

// --- tanggal WIB (hari kerja Sen–Jum) ---
const WIB = 7 * 3600e3, DAY = 864e5;
const wibDay = (ms) => new Date(Math.floor((Number(ms) + WIB) / DAY) * DAY).toISOString().slice(0, 10);
const addD = (s, n) => new Date(Date.parse(s) + n * DAY).toISOString().slice(0, 10);
const isWork = (s) => { const w = new Date(s).getUTCDay(); return w >= 1 && w <= 5 && !(CFG.libur || []).includes(s); };
const workBack = (s, n) => { let d = s, k = 1; while (k < n) { d = addD(d, -1); if (isWork(d)) k++; } return d; };
const today = wibDay(Date.now());
const monday = (s) => { const w = new Date(s).getUTCDay() || 7; return addD(s, 1 - w); };
const DARI = opt.dari || monday(today), SAMPAI = opt.sampai || addD(monday(today), 4 * 7 - 3);
const days = []; for (let d = DARI; d <= SAMPAI; d = addD(d, 1)) if (isWork(d)) days.push(d);

const bobotOf = (t) => {
  const ov = CFG.override?.[t.id];
  if (ov && ov.bobot != null) return { b: ov.bobot, src: "taksiran MM" };
  const m = (t.description || t.text_content || "").match(/bobot(?:\s*tenaga)?\s*[:=]?\s*(\d+(?:[.,]\d+)?)/i);
  if (m) return { b: Number(m[1].replace(",", ".")), src: "deskripsi" };
  for (const [pre, b] of Object.entries(CFG.bobot_default_awalan || {})) if (t.name.startsWith(pre)) return { b, src: "awalan " + pre };
  return { b: CFG.bobot_default || 1, src: "default" };
};
const tahan = (t) => /DITAHAN|\[BERSYARAT\]|\[CADANGAN|HOLD/i.test(t.name);
const nama = (a) => CFG.alias?.[a.username] || a.username;

const tasks = [];
for (const f of CFG.folder || []) { const { lists = [] } = await api(`/folder/${f}/list?archived=false`); for (const l of lists) tasks.push(...await listTasks(l.id)); }
for (const l of CFG.list_tambahan || []) tasks.push(...await listTasks(l));

const P = {}; // per orang
const get = (n) => (P[n] ??= { hari: Object.fromEntries(days.map((d) => [d, { poin: 0, due: 0, kartu: [] }])), selesai: 0, tertahan: [], tanpa_due: [], telat: [], kartu_aktif: 0, bobot_tebakan: 0 });
for (const t of tasks) {
  if (t.archived) continue;
  const closed = t.status?.type === "closed" || t.status?.type === "done";
  for (const a of t.assignees || []) {
    const n = nama(a), p = get(n);
    if (closed) { const c = wibDay(t.date_closed || t.date_done || 0); if (c >= DARI && c <= SAMPAI) p.selesai++; continue; }
    if (tahan(t)) { p.tertahan.push(t.name.slice(0, 70)); continue; }
    if (!t.due_date) { p.tanpa_due.push(t.name.slice(0, 70)); continue; }
    const due = wibDay(t.due_date);
    if (due < today) p.telat.push(`${due} ${t.name.slice(0, 60)}`);
    const { b, src } = bobotOf(t);
    if (due >= DARI && (t.start_date ? wibDay(t.start_date) : due) <= SAMPAI) { p.kartu_aktif++; if (src === "default" || src.startsWith("awalan")) p.bobot_tebakan++; }
    let start = CFG.override?.[t.id]?.mulai || (t.start_date ? wibDay(t.start_date) : workBack(due, Math.max(1, Math.ceil(b))));
    if (start > due) start = due;
    const win = []; for (let d = start; d <= due; d = addD(d, 1)) if (isWork(d)) win.push(d);
    if (!win.length) win.push(due);
    const per = b / win.length;
    for (const d of win) if (p.hari[d]) { p.hari[d].poin += per; p.hari[d].kartu.push(t.id); }
    if (p.hari[due]) p.hari[due].due++;
  }
}
for (const r of CFG.beban_tambahan || []) { const p = get(r.orang); if (p.hari[r.tanggal]) p.hari[r.tanggal].poin += r.poin; }
for (const r of CFG.tugas_rutin || []) { const p = get(r.orang); for (const d of days) if (d >= r.dari && d <= r.sampai && p.hari[d]) { p.hari[d].poin += r.poin_per_hari; } }

const KAP = (n) => CFG.kapasitas_poin_per_hari?.[n] ?? CFG.kapasitas_default ?? 4;
const zona = (u) => u < CFG.ambang.santai ? "SANTAI" : u < CFG.ambang.optimal ? "KURANG" : u <= 1 ? "OPTIMAL" : "LEBIH";
const hasil = [];
for (const [n, p] of Object.entries(P)) {
  if (opt.orang && !n.toLowerCase().includes(String(opt.orang).toLowerCase())) continue;
  const sales = (CFG.sales || []).some((s) => n.includes(s));
  if (opt["tanpa-sales"] && sales) continue;
  if ((CFG.abaikan || []).some((s) => n.includes(s))) continue;
  const minggu = {};
  for (const d of days) { const w = monday(d); (minggu[w] ??= []).push(d); }
  const rows = Object.entries(minggu).map(([w, ds]) => {
    const poin = ds.reduce((s, d) => s + p.hari[d].poin, 0), kap = KAP(n) * ds.length, u = poin / kap;
    const kosong = ds.filter((d) => p.hari[d].poin < 0.01), rendah = ds.filter((d) => p.hari[d].poin > 0 && p.hari[d].poin / KAP(n) < CFG.ambang.santai);
    const dueMax = Math.max(...ds.map((d) => p.hari[d].due)), lewatB5 = ds.filter((d) => p.hari[d].due > 7 || p.hari[d].poin > KAP(n) + 1e-9);
    return { minggu: w, utilisasi: Math.round(u * 100), zona: zona(u), poin: +poin.toFixed(1), kapasitas: kap, hari_kosong: kosong, hari_rendah: rendah, due_maks_per_hari: dueMax, hari_lewat_batas: lewatB5 };
  });
  hasil.push({ orang: n, sales, rows, kartu_aktif: p.kartu_aktif, bobot_tebakan: p.bobot_tebakan, selesai_dalam_rentang: p.selesai, telat: p.telat, tertahan: p.tertahan.length, tanpa_due: p.tanpa_due.length });
}
hasil.sort((a, b) => a.orang.localeCompare(b.orang));
if (opt.json) { console.log(JSON.stringify({ mode: MODE, dari: DARI, sampai: SAMPAI, hari_ini: today, hasil }, null, 2)); process.exit(0); }

const tgl = (a) => a.map((d) => d.slice(8, 10) + "/" + d.slice(5, 7)).join(", ") || "-";
console.log(`BEBAN KERJA ${DARI} s/d ${SAMPAI} (hari kerja) · sumber ${MODE} · dihitung ${today}`);
console.log(`Kapasitas ${CFG.kapasitas_default} poin/hari · zona: SANTAI <${CFG.ambang.santai * 100}% · KURANG <${CFG.ambang.optimal * 100}% · OPTIMAL ${CFG.ambang.optimal * 100}–100% · LEBIH >100%\n`);
for (const h of hasil) {
  console.log(`## ${h.orang}${h.sales ? " (sales: beban utama di pipeline, kartu hanya sebagian)" : ""}`);
  for (const r of h.rows) console.log(`- minggu ${r.minggu}: ${r.utilisasi}% ${r.zona} (${r.poin}/${r.kapasitas} poin) · kosong: ${tgl(r.hari_kosong)} · <${CFG.ambang.santai * 100}%: ${tgl(r.hari_rendah)} · due maks/hari ${r.due_maks_per_hari}${r.hari_lewat_batas.length ? " · LEWAT BATAS: " + tgl(r.hari_lewat_batas) : ""}`);
  console.log(`  kartu aktif di rentang: ${h.kartu_aktif} (bobot ditebak: ${h.bobot_tebakan}) · selesai dalam rentang: ${h.selesai_dalam_rentang} · telat: ${h.telat.length} · ditahan/bersyarat: ${h.tertahan} · tanpa due: ${h.tanpa_due}`);
  for (const t of h.telat.slice(0, 5)) console.log(`  · telat ${t}`);
  console.log("");
}
