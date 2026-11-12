---
name: rhj-analisa-beban
description: Analisa padat/longgarnya beban kerja tiap pegawai RHJ dari kartu tugas (Anvil/ClickUp) — cari yang terlalu santai (utilisasi rendah, hari kosong) maupun yang kelebihan (lewat B5), lalu usulkan pengisian/pemindahan kerja. Dipakai MM (rhj-manajer-marketing) saat Hannes tanya "load si X", "siapa yang santai", "padatkan tugas", atau tiap Senin sebelum menyusun kartu minggu itu. Bahasa Indonesia.
---

# Analisa Beban Pegawai (MM)

Tujuan (Hannes 6 Okt): **tidak ada pegawai yang terlalu santai**, tanpa melanggar batas beban. Targetnya tiap orang berada di zona **OPTIMAL (80–100% kapasitas)** setiap minggu.

## 1. Tarik angka (WAJIB alat, jangan menghitung kira-kira)
```
node tools/beban.mjs                              # minggu ini + 3 minggu ke depan, semua orang
node tools/beban.mjs --dari 2026-10-12 --sampai 2026-11-06 [--orang Yosie] [--tanpa-sales] [--json]
```
Backend ikut `TUGAS_BACKEND` (Anvil sejak 6 Okt; tanpa env = ClickUp). Baca saja, tidak mengubah kartu.
Config di `tools/beban-config.json`: kapasitas, ambang zona, bobot default per awalan nama, tugas rutin di luar kartu, daftar sales, libur.

**Cara alat menghitung (sebut di laporan bila ditanya):**
- Kapasitas 4 poin/hari kerja (B5); 1 poin ≈ 2 jam kerja efektif.
- Bobot kartu = "Bobot: N" di deskripsi; kalau tidak ada → default per awalan (mis. R-Eps- 1,5) → 1. Baris "bobot ditebak: X" menunjukkan berapa yang tebakan.
- Bobot dibagi rata ke hari kerja antara start dan due (tanpa start: mundur sejumlah bobot hari dari due).
- Kartu DITAHAN/BERSYARAT/CADANGAN dan kartu tanpa due tidak dihitung sebagai beban (dilaporkan terpisah).
- Tugas rutin tanpa kartu (posting harian, cek iklan harian) masuk lewat `tugas_rutin`.

Zona per minggu: **SANTAI** <50% · **KURANG** 50–79% · **OPTIMAL** 80–100% · **LEBIH** >100% atau >7 due/hari (B5).

## 2. Jangan langsung menuduh santai — cek 4 hal dulu
Utilisasi rendah bisa berarti salah satu dari ini. Tulis mana yang terjadi:
1. **Bobot meremehkan** — kartu besar (bangun campaign, artikel, video) tercatat bobot 1. Kalau "bobot ditebak" banyak, perkirakan ulang bobot kartu orang itu dulu (skala di bagian 5) sebelum menyimpulkan.
2. **Kerja di luar kartu** — sales (Riksa, Michael): beban utama di pipeline/WA, kartu hanya sebagian → nilai dari pipeline (skill rhj-sales-manager Bagian A), bukan dari angka ini. Hannes diabaikan.
3. **Sengaja kosong** — masa transisi (Peter → Felix, B17), masa ukur iklan (B6: akun tak boleh disentuh), menunggu pihak lain. Kosong karena aturan BUKAN santai, tapi tetap bisa diisi kerja offline.
4. **Benar-benar kurang tugas** — kosongnya karena memang belum dikasih kerja. Ini yang diisi.

Bukti tambahan (pakai bila meragukan): kartu selesai per minggu (velocity), kartu telat, komentar progres terakhir (`node tools/clickup.mjs comments <id>` / `activity <id>` di Anvil), false-complete (skill verifikator-task).

## 3. Isi yang santai/kurang — urutan sumber kerja
Isi sampai ±80–100%, prioritas:
1. **Majukan kartu yang sudah ada** dari minggu-minggu berikutnya, terutama kerja **offline** (draf, analisa, laporan, persiapan) yang tidak terikat slot/gerbang.
2. **Kartu tanpa due / backlog** milik orang itu → beri jadwal.
3. **Pecah persiapan** dari kartu besar yang jatuh nanti (mis. prasyarat, screenshot baseline, draf copy) ke hari kosong.
4. **Tugas pendukung PIC lain** sesuai keahliannya (mis. Yosie: usulan negative keyword dari search terms; Felix: QA halaman; Darwis: rapikan data pipeline).
5. Kalau tetap kosong → usulkan ke Hannes ide kerja baru (dari arah CMO), jangan mengarang kartu tanpa ACC.

Untuk yang LEBIH: geser kartu tanpa tanggal tayang/tenggat keras ke minggu berikut, pecah, atau pindah ke orang yang SANTAI dengan keahlian sama.

## 4. Pagar yang tetap berlaku saat mengisi
- **RAHASIA beban (Hannes 7/10):** angka beban hanya untuk Hannes; tidak muncul di kartu/komentar/email tim.
- **ACC Hannes WAJIB** sebelum membuat/mengubah kartu yang menugaskan orang. Analisa + usulan dulu, eksekusi sesudah ACC.
- **B5:** ≤7 due/orang/hari, ≤4 poin/hari (pengecualian tes beban yang Hannes minta, catat di LOG-PAGAR).
- **B18 (Rengga):** 1 kartu = 1 video, mulai Senin due Jumat, tanpa kartu harian; persiapan non-video = 1 kartu.
- **B17:** kartu baru web hanya ke Felix, mulai sesudah 15/10; Peter tidak diberi kartu baru.
- **B6 (Yosie/akun iklan):** 1 perubahan per campaign per slot, jeda ≥7 hari per campaign (beberapa campaign boleh di hari yang sama, Hannes 14 Okt) — hari kosong di masa ukur diisi kerja **offline**, bukan perubahan akun.
- **HOLD dari Hannes** (mis. 7 konten lepas lama) tidak dipakai sebagai pengisi dan tidak diusulkan lagi.
- Jangan mengisi dengan pekerjaan sibuk tanpa hasil: tiap kartu pengisi punya hasil yang bisa dicek ("SELESAI = ...").

## 5. Skala bobot — RAHASIA, hanya di `tools/beban-config.json` (bagian override)
- **0,5** = <1 jam (screenshot, cek status, satu komentar balasan)
- **1** = ±2 jam (laporan pendek, satu perubahan kecil, analisa satu laporan)
- **2** = setengah hari (draf copy/RSA, setting campaign, satu artikel poles, satu video pendek ≤20 dtk)
- **3** = sehari kurang sedikit (episode/video dengan lip-sync, halaman web baru)
- **4** = sehari penuh (bangun campaign dari nol, riset besar)
**Keputusan Hannes 7/10: pegawai TIDAK boleh melihat beban/bobot/utilisasinya.** Bobot hanya dicatat di config repo (private). JANGAN tulis bobot, persen utilisasi, zona, atau kata "beban/santai/pengisian" di kartu, komentar, email tim pagi, atau pesan ke pegawai. Kartu pengisi ditulis netral seperti kartu kerja biasa. Laporan beban HANYA ke Hannes (sesi ini / Digest MM ke Hannes).

## 6. Format laporan ke Hannes (ringkas, verdict di depan)
```
VERDICT: <siapa santai / optimal / lebih, minggu mana>
Per orang (minggu ini → 3 minggu ke depan): utilisasi % + zona, hari kosong, catatan (bobot tebakan / di luar kartu / sengaja kosong)
Usulan pengisian: tabel tanggal | orang | kerja | asal (dimajukan dari / baru) | bobot
Butuh ACC: <daftar kartu yang akan diubah/dibuat>
```
Angka harus dari alat (ATURAN NOL). Bila bobot sebagian besar tebakan, tulis jelas "angka ini kemungkinan meremehkan beban X".

## 7. Ritme
- **Senin pagi** (sebelum menyusun kartu minggu itu) dan saat Hannes bertanya.
- Sesudah perubahan besar jadwal (mis. pemadatan), jalankan ulang untuk cek tidak ada yang LEBIH.
- Catat temuan penting di `memori/LOG-PAGAR.md` (keputusan) dan pelajaran di `memori/PELAJARAN-PIC.md`.
