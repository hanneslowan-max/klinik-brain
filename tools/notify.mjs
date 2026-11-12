// notify.mjs — Pengirim Telegram SATU ARAH (tanpa Anthropic API key, tanpa long-polling).
// Kirim update ke chat Telegram Hannes atau grup terdaftar. Dipakai routine harian.
//
// Pemakaian:
//   node notify.mjs "pesan singkat"
//   node notify.mjs --file C:\path\ke\digest.txt      (untuk pesan multi-baris; paling aman)
//   echo "pesan" | node notify.mjs                     (dari stdin)
//   node notify.mjs --ke sales --file <path>           (ke grup; alias di tools/telegram-tujuan.json)
//   node notify.mjs --ke marketing --file <ringkas.txt> --dokumen <artikel.html>
//                                                      (pesan teks lalu berkas lampiran)
//   node notify.mjs --ke sales --kunci arahan-pipeline --file <path>
//                                                      (anti-dobel: sekali per kunci per tanggal WIB)
//
// Tanpa --ke -> chat Hannes (NOTIFY_CHAT_ID). --ke hanya menerima alias yang terdaftar di
// tools/telegram-tujuan.json (grup yang dibuat Hannes; bot klinik anggota grup).
// --kunci <nama>: cek memori/KIRIM-TELEGRAM.md; baris "<YYYY-MM-DD> <nama> <tujuan>" sudah ada
// -> tidak kirim ("sudah terkirim", exit 0). Sesudah terkirim baris itu ditambahkan; routine
// wajib ikut meng-commit memori/KIRIM-TELEGRAM.md lewat routine-git.sh finish.
//
// Sumber kredensial: file .env di folder ini.
//   TELEGRAM_BOT_TOKEN  (wajib)
//   NOTIFY_CHAT_ID      (opsional; fallback: entri pertama ALLOWED_TELEGRAM_IDS)

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const LOG = path.join(HERE, "..", "memori", "KIRIM-TELEGRAM.md");

function loadEnv(file) {
  const out = {};
  try {
    for (const line of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
      if (/^\s*#/.test(line)) continue;
      const m = line.match(/^\s*([A-Za-z0-9_]+)\s*=\s*(.*)$/);
      if (m) out[m[1]] = m[2].trim();
    }
  } catch { /* .env tak ada -> pakai process.env */ }
  return out;
}

function ambilOpsi(args, nama) {
  const i = args.indexOf(nama);
  if (i === -1) return null;
  const v = args[i + 1] || "";
  args.splice(i, 2);
  return v;
}

const env = loadEnv(path.join(HERE, ".env"));
const TOKEN = (process.env.TELEGRAM_BOT_TOKEN || env.TELEGRAM_BOT_TOKEN || "").trim();
let CHAT = (
  process.env.NOTIFY_CHAT_ID ||
  env.NOTIFY_CHAT_ID ||
  (env.ALLOWED_TELEGRAM_IDS || "").split(",")[0] ||
  ""
).trim();

const args = process.argv.slice(2);
const alias = ambilOpsi(args, "--ke");
const dokumen = ambilOpsi(args, "--dokumen");
const kunci = ambilOpsi(args, "--kunci");
const fileTeks = ambilOpsi(args, "--file");

if (alias !== null) {
  let tujuan = {};
  try { tujuan = JSON.parse(fs.readFileSync(path.join(HERE, "telegram-tujuan.json"), "utf8")); } catch { /* kosong */ }
  if (!tujuan[alias] || !tujuan[alias].chat_id) {
    console.error(`notify: tujuan "${alias}" tidak terdaftar di tools/telegram-tujuan.json`);
    process.exit(1);
  }
  CHAT = String(tujuan[alias].chat_id);
}

// Ambil teks: --file <path> | argumen | stdin (stdin dilewati bila hanya kirim dokumen)
let text = "";
if (fileTeks) {
  text = fs.readFileSync(fileTeks, "utf8");
} else if (args.length) {
  text = args.join(" ");
} else if (!dokumen) {
  try { text = fs.readFileSync(0, "utf8"); } catch { text = ""; }
}
text = text.replace(/\s+$/,"").trim();

if (!TOKEN) { console.error("notify: TELEGRAM_BOT_TOKEN kosong di .env"); process.exit(1); }
if (!CHAT)  { console.error("notify: chat id kosong (set NOTIFY_CHAT_ID atau ALLOWED_TELEGRAM_IDS di .env)"); process.exit(1); }
if (!text && !dokumen) { console.error('notify: pesan kosong (usage: node notify.mjs "pesan"  atau  --file <path>)'); process.exit(1); }
if (dokumen && !fs.existsSync(dokumen)) { console.error(`notify: dokumen tidak ada: ${dokumen}`); process.exit(1); }

const tanggal = new Date(Date.now() + 7 * 3600 * 1000).toISOString().slice(0, 10); // WIB
const barisKunci = kunci ? `${tanggal} ${kunci} ${alias || "hannes"}` : null;
if (barisKunci) {
  let log = "";
  try { log = fs.readFileSync(LOG, "utf8"); } catch { /* belum ada */ }
  if (log.split(/\r?\n/).some((l) => l.startsWith(barisKunci))) {
    console.log(`notify: sudah terkirim hari ini (${barisKunci}), tidak dikirim ulang.`);
    process.exit(0);
  }
}

const CHUNK = 3800; // batas Telegram 4096, sisakan ruang
// Potong di batas baris supaya satu poin tidak terbelah ke dua pesan.
const chunks = [];
let rest = text;
while (rest.length > CHUNK) {
  let cut = rest.lastIndexOf("\n", CHUNK);
  if (cut < CHUNK / 2) cut = CHUNK;
  chunks.push(rest.slice(0, cut).trimEnd());
  rest = rest.slice(cut).replace(/^\n+/, "");
}
if (rest) chunks.push(rest);

for (const c of chunks) {
  const res = await fetch(`https://api.telegram.org/bot${TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ chat_id: CHAT, text: c, disable_web_page_preview: true }),
  });
  const j = await res.json().catch(() => ({}));
  if (!j.ok) { console.error("notify: GAGAL ->", j.description || ("HTTP " + res.status)); process.exit(1); }
}

if (dokumen) {
  const form = new FormData();
  form.append("chat_id", CHAT);
  form.append("document", new Blob([fs.readFileSync(dokumen)]), path.basename(dokumen));
  const res = await fetch(`https://api.telegram.org/bot${TOKEN}/sendDocument`, { method: "POST", body: form });
  const j = await res.json().catch(() => ({}));
  if (!j.ok) { console.error("notify: GAGAL kirim dokumen ->", j.description || ("HTTP " + res.status)); process.exit(1); }
}

if (barisKunci) fs.appendFileSync(LOG, `${barisKunci} ${new Date().toISOString()}\n`);
console.log(`notify: terkirim ke ${CHAT} (${text.length} char, ${chunks.length} pesan${dokumen ? " + dokumen " + path.basename(dokumen) : ""}).`);
