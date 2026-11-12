# Notif Telegram rapi (mobile-first)
Disalin dari rhj-brain 12 Nov 2026 (keluhan Bapak 17 Sep 2026: "berantakan banget, susah baca").

- 1 baris = 1 poin, baris pendek. Rapi tidak berarti memotong isi: semua angka tetap ada, boleh multi-pesan.
- JANGAN tabel/kolom yang diratakan dengan spasi/tab (Telegram tidak monospace). Angka perlu sejajar → bungkus ``` atau hindari.
- `tools/notify.mjs` mengirim PLAIN TEXT tanpa parse_mode → JANGAN markdown (`**`, `|`, `#` tampil apa adanya).
- Judul 1 baris (KAPITAL/emoji), bullet "• " atau "- ". Tanpa spasi ganda, tab, spasi di akhir baris.
- Isi Telegram TIDAK memuat nama, nomor, atau keluhan klien.
