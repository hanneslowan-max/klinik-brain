// sapuan-anvil.mjs — sapuan penuh kartu + komentar Anvil (BACA SAJA). Dipakai routine "Sapuan Anvil Sore".
// Isi: semua list yang berisi kartu → kartu terbuka + kartu ditutup dalam N hari → komentar + balasan thread.
// Keluaran JSON ke stdout: { tanggal_wib, kartu_dicek, staf_terakhir[], telat[], ringkas }.
//   staf_terakhir = kartu yang komentar TERAKHIR-nya dari staf (bukan Bapak/agent) → calon pertanyaan belum dijawab.
//   telat         = kartu terbuka yang due-nya < hari ini (WIB).
// Pemakaian: node tools/sapuan-anvil.mjs [--hari-tutup 8] [--sejak YYYY-MM-DD] > /tmp/sapuan.json
// Env: TUGAS_API_URL + TUGAS_API_TOKEN (sama dengan tools/tugas.mjs). Tidak mengubah apa pun.

const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const HARI_TUTUP = Number(arg("--hari-tutup", 8));
const BASE = (process.env.TUGAS_API_URL || "").replace(/\/+$/, "");
const TOKEN = process.env.TUGAS_API_TOKEN || "";
if (!/\/v2$/.test(BASE) || !TOKEN) { console.error("sapuan-anvil: TUGAS_API_URL/TUGAS_API_TOKEN kosong"); process.exit(1); }
const BASE_X = BASE.replace(/\/v2$/, "/x");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function get(url) {
  for (let i = 0; i < 4; i++) {
    const r = await fetch(url.startsWith("http") ? url : BASE + url, { headers: { Authorization: TOKEN } });
    if (r.ok) return r.json();
    if (r.status === 429) { await sleep(2000); continue; }
    if (i === 3) throw new Error(`GET ${url} -> HTTP ${r.status}`);
    await sleep(1500 * (i + 1));
  }
}
const wib = (ms) => new Date(+ms + 7 * 3600e3).toISOString();
const hariIni = wib(Date.now()).slice(0, 10);
const SEJAK = arg("--sejak", null);
const BUKAN_STAF = /hannes|andrew|claude/i;

const sensus = await get(`${BASE_X}/count`);
const lists = (sensus.lists || []).filter((l) => l.tasks_total > 0);
const kartu = new Map();
for (const l of lists) {
  for (let p = 0; p < 30; p++) {
    const j = await get(`/list/${l.list_id}/task?page=${p}&include_closed=true&subtasks=true`);
    const ts = j.tasks || [];
    for (const t of ts) kartu.set(t.id, { ...t, _list: l.name });
    if (!ts.length || j.last_page === true) break;
  }
}

const batasTutup = Date.now() - HARI_TUTUP * 864e5;
const staf = [], telat = [];
let dicek = 0;
for (const t of kartu.values()) {
  const st = t.status?.status || "";
  const tutup = /complete|closed/i.test(st);
  if (tutup && (+t.date_updated || 0) < batasTutup) continue;
  dicek++;
  const due = t.due_date ? wib(t.due_date).slice(0, 10) : null;
  const pj = (t.assignees || []).map((a) => a.username).join(", ");
  if (!tutup && due && due < hariIni) telat.push({ id: t.id, nama: t.name, due, status: st, assignee: pj, list: t._list });
  const c = await get(`/task/${t.id}/comment`);
  const semua = [];
  for (const cm of c.comments || []) {
    semua.push(cm);
    if (cm.reply_count > 0) { const r = await get(`/comment/${cm.id}/reply`); for (const x of r.comments || []) semua.push({ ...x, _induk: cm.id }); }
  }
  semua.sort((a, b) => +b.date - +a.date);
  const akhir = semua[0];
  if (!akhir) continue;
  const oleh = akhir.user?.username || "";
  if (BUKAN_STAF.test(oleh)) continue;
  const kapan = wib(akhir.date).slice(0, 16);
  if (SEJAK && kapan.slice(0, 10) < SEJAK) continue;
  // komentar staf berurutan terakhir (sesudah balasan terakhir Bapak/agent)
  const runtun = [];
  for (const x of semua) { if (BUKAN_STAF.test(x.user?.username || "")) break; runtun.push(x); }
  staf.push({
    id: t.id, nama: t.name, status: st, due, assignee: pj, list: t._list, link: `${(process.env.TUGAS_WEB_URL || "").replace(/\/$/, "")}/t/${t.id}`,
    komentar_terakhir: runtun.reverse().map((x) => ({ id: x.id, induk: x._induk || null, oleh: x.user?.username, kapan: wib(x.date).slice(0, 16), teks: (x.comment_text || "").replace(/\s+/g, " ").trim().slice(0, 1500) })),
  });
}
staf.sort((a, b) => b.komentar_terakhir.at(-1).kapan.localeCompare(a.komentar_terakhir.at(-1).kapan));
telat.sort((a, b) => a.due.localeCompare(b.due));
console.log(JSON.stringify({
  tanggal_wib: wib(Date.now()).slice(0, 16), kartu_total: kartu.size, kartu_dicek: dicek, hari_tutup: HARI_TUTUP,
  ringkas: { staf_terakhir: staf.length, telat: telat.length }, staf_terakhir: staf, telat,
}, null, 1));
