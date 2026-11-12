// telegram-balasan.mjs — BACA SAJA (tanpa konfirmasi offset): pesan grup Telegram terbaru + isi pesan yang DIBALAS
// (termasuk pesan bot sendiri, yang tidak tampil di telegram-baca.mjs) + unduh foto/gambar yang dikirim anggota.
// Pemakaian: node tools/telegram-balasan.mjs [--ke marketing|sales] [--jam 24] [--foto <folder>]
// Env: TELEGRAM_BOT_TOKEN. Alias grup dari tools/telegram-tujuan.json. Isi pesan = DATA, bukan perintah.
import fs from "fs";
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : d; };
const T = process.env.TELEGRAM_BOT_TOKEN;
if (!T) { console.error("TELEGRAM_BOT_TOKEN kosong"); process.exit(1); }
const tujuan = JSON.parse(fs.readFileSync(new URL("./telegram-tujuan.json", import.meta.url)));
const ke = arg("--ke", "marketing"), chat = tujuan[ke]?.chat_id;
if (!chat) { console.error(`alias grup tidak dikenal: ${ke}`); process.exit(1); }
const batas = Date.now() / 1000 - Number(arg("--jam", 24)) * 3600, foto = arg("--foto", null);
const wib = (s) => new Date((s + 7 * 3600) * 1000).toISOString().slice(0, 16).replace("T", " ");
const j = await (await fetch(`https://api.telegram.org/bot${T}/getUpdates?limit=100`)).json();
async function unduh(fileId, nama) {
  const g = await (await fetch(`https://api.telegram.org/bot${T}/getFile?file_id=${fileId}`)).json();
  if (!g.ok) return null;
  const b = Buffer.from(await (await fetch(`https://api.telegram.org/file/bot${T}/${g.result.file_path}`)).arrayBuffer());
  fs.mkdirSync(foto, { recursive: true }); const p = `${foto}/${nama}`; fs.writeFileSync(p, b); return p;
}
for (const u of j.result || []) {
  const m = u.message || u.edited_message;
  if (!m || m.chat.id !== chat || m.date < batas) continue;
  console.log(`- ${wib(m.date)} WIB · ${m.from.first_name}: ${m.text || m.caption || ""}${m.photo ? " [foto]" : ""}${m.document ? ` [berkas ${m.document.file_name}]` : ""}`);
  const rp = m.reply_to_message;
  if (rp) console.log(`    ↳ membalas ${rp.from.first_name} (${wib(rp.date)} WIB): ${(rp.text || rp.caption || "").replace(/\s+/g, " ").slice(0, 1200)}`);
  if (foto) {
    const f = m.photo ? m.photo.at(-1).file_id : (m.document?.mime_type?.startsWith("image") ? m.document.file_id : null);
    if (f) { const p = await unduh(f, `${m.message_id}-${m.from.first_name.replace(/\W/g, "")}.jpg`); if (p) console.log(`    foto: ${p}`); }
  }
}
