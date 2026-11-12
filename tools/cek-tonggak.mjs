// cek-tonggak.mjs — bandingkan due kartu tugas dengan tanggal tonggak di Google Calendar Bapak.
// Sumber peta: tools/tonggak-kalender.json. READ-ONLY (tidak mengubah kartu maupun kalender).
// Pakai: node tools/cek-tonggak.mjs            -> ringkasan teks
//        node tools/cek-tonggak.mjs --json     -> JSON {backend, berubah:[...], kartu_lain:[...], tutup:[...], gagal:[...]}
// Kartu dibaca lewat tools/clickup.mjs (dua-mode): ikut env TUGAS_BACKEND -> Anvil sejak cutover 6 Okt,
// ClickUp kalau rollback. Dulu memanggil api.clickup.com langsung = data basi sesudah sinkron dimatikan.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const peta = JSON.parse(fs.readFileSync(path.join(HERE, "tonggak-kalender.json"), "utf8"));
const CLI = path.join(HERE, "clickup.mjs");
const run = (...args) => JSON.parse(execFileSync("node", [CLI, ...args], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], maxBuffer: 32 << 20 }));
let backend = "?";
try { backend = run("backend").backend; } catch { /* dilaporkan per kartu */ }

function kartu(id) {
  try {
    const d = run("task", id);
    const due = d.due_date ? new Date(+d.due_date + 7 * 3600e3).toISOString().slice(0, 10) : null; // tanggal WIB
    const tutup = d.status?.status === "complete" || d.status?.type === "closed" || d.status?.type === "done";
    return { id, nama: d.name, due, tutup, url: d.url };
  } catch (e) {
    return { id, gagal: String(e.stderr || e.message).trim().split("\n").pop().slice(0, 200) };
  }
}

const hasil = { backend, berubah: [], kartu_lain: [], tutup: [], gagal: [] };
for (const t of peta.tonggak) {
  for (const [peran, id] of [["kunci", t.kunci], ...t.lain.map((x) => ["lain", x])]) {
    if (!id) continue;
    const k = kartu(id);
    if (k.gagal) { hasil.gagal.push({ event: t.judul, id, alasan: k.gagal }); continue; }
    if (k.tutup) hasil.tutup.push({ event: t.judul, kartu: k.nama, url: k.url });
    if (k.due !== t.tanggal) {
      const row = { event_id: t.event_id, event: t.judul, tanggal_kalender: t.tanggal, kartu: k.nama, due_baru: k.due, url: k.url };
      (peran === "kunci" ? hasil.berubah : hasil.kartu_lain).push(row);
    }
  }
}

if (process.argv.includes("--json")) { console.log(JSON.stringify(hasil, null, 1)); process.exit(0); }
const n = hasil.berubah.length + hasil.kartu_lain.length;
console.log(`(backend kartu: ${backend})`);
console.log(n ? `TANGGAL BERUBAH: ${n}` : "Nihil: semua tanggal kartu sama dengan kalender.");
for (const b of hasil.berubah) console.log(`- GESER EVENT "${b.event}" ${b.tanggal_kalender} -> ${b.due_baru ?? "tanpa due"} (kartu kunci: ${b.kartu})`);
for (const b of hasil.kartu_lain) console.log(`- "${b.kartu}" kini due ${b.due_baru ?? "-"}, tidak lagi ${b.tanggal_kalender} (event "${b.event}") -> perbarui deskripsi event`);
for (const g of hasil.gagal) console.log(`- GAGAL baca ${g.id} (${g.event}): ${g.alasan}`);
