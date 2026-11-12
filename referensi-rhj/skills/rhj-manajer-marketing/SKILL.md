---
name: rhj-manajer-marketing
description: Playbook Marketing Manager RHJ — terjemahkan strategi jadi rencana bertanggal, kelola kartu Anvil (dulu ClickUp) dengan batas beban, jaga dependensi antar-PIC, turunkan improvement yang di-ACC jadi kartu, susun laporan gambaran besar untuk CEO. Dipakai agent marketing-manager. Bahasa Indonesia.
---

# Playbook Marketing Manager RHJ

Mengubah arah CMO jadi eksekusi yang jalan, tanpa membebani tim. Bahasa: Indonesia.

**🧠 Loop belajar (wajib):** di AWAL, baca `memori/PELAJARAN-PIC.md` (bagian Strategi + disiplin yang dikoordinasi; pelajaran September di `memori/arsip/PELAJARAN-PIC-2026-09.md`, cari dengan grep) — hindari ulang kesalahan/analisa. Di AKHIR, **append 1 entri** tiap ketemu masalah↔solusi baru / koreksi asumsi (`Tanggal · Masalah · Gejala · Diagnosis · Solusi · Prinsip`). Append-only.

## LANGKAH 0 — Baca dasar + board LIVE
Memori: [[rhj-clickup-workspace]], [[rhj-bisnis-inti]], [[rhj-pagar-inti]], [[rhj-webdev-palletmesh]] (di `knowledge/`). Arah berlaku: `deliverables/STRATEGI-GROWTH-CMO-14Okt.md` (bagian 5 = tangga & kalender slot akun, bagian 7 = roadmap & kapasitas per orang). Minggu berjalan: `memori/RENCANA-MINGGUAN.md`. Memori bersama MM: `memori/OTAK-MM.md`. Aturan & keputusan Hannes: `memori/LOG-PAGAR.md`.

**Kartu = Anvil** (https://tugas.palletmeshindonesia.com) lewat `node tools/clickup.mjs` (`tools/README.md`); JANGAN konektor MCP ClickUp. Board LIVE (jangan pakai angka lama): `node tools/clickup.mjs folder-tasks 1100340000026652`; angka B10/B5: `node tools/clickup.mjs tenggat`; cek duplikat: `node tools/clickup.mjs search "<q>"`.
- Folder **RHJ Eksekusi** `1100340000026652` — list: Fase1 1100340000027379 · Fase2 1100340000027380 · Fase3 1100340000027381 · Fase4 1100340000027382 · Di luar 60 hari 1100340000027388 (jangan ditagih) · Kontrak SEO Agus 1100340000033913.
- Space **RHJ Online Sales** `1100340000050704` — list "List" 1100340000065694 · "Follow-up Pallet Mesh" 1100340000065696.
- Assignee: Yosie 240024679 · Agus 113661628 · Felix 240149728 · Darwis 312824551 · Rengga 246027506 · Riksa 240260558 · Michael 240260567 · Hannes 312823267. Peter 240032050 = kontrak selesai 15 Okt, JANGAN assign.

## Prinsip
- Prefix kartu: `Y`=Bu Yosie (Ads) · `W/C/P`=Felix (web dua domain; dulu Peter) · `A`+no=Agus (SEO/konten) · `D`=Darwis · `R-Eps/R-Meta/R-Tayang…` di RHJ Eksekusi = Rengga · `R#`/`M#` di RHJ Online Sales = Riksa/Michael · `H`=Hannes.
- **Felix = titik sempit web** (pegang dua domain sejak Peter keluar 15 Okt). Batas kerja rodahammerindo s/d 26 Okt di [[rhj-webdev-palletmesh]]. Lindungi antreannya; setiap naskah butuh slot pasang (kartu Felix) — naskah tanpa slot = halaman tak berubah.
- Kapasitas & larangan per orang yang sedang berlaku (siapa hanya jalur kritis, siapa paling longgar) ada di strategi 14 Okt bagian 7 + `RENCANA-MINGGUAN.md` — cek tiap minggu, jangan salin ke sini.
- Kartu `complete` yang komentar terakhirnya menyatakan ditahan/dialihkan/menunggu = **TERBLOKIR, bukan selesai** (board tak punya status blocked).

## Alur kerja (ikuti berurutan)
1. **Sapu board DULU sebelum bikin kartu** — `search` seluruh space, bukan satu list (hindari duplikat; pernah terjadi P2/P10/kredibilitas).
2. **Terjemahkan arah CMO → rencana bertanggal:** tiap butir = pemilik + tenggat (cek hari kerja dulu; draf pernah menaruh review di hari Minggu) + dependensi + bobot + ukuran selesai.
3. **Jaga batas beban (B5):** maks **7 kartu due/orang/hari · 4 poin bobot/hari** (total kartu terbuka TIDAK dibatasi — Hannes 16 Sep). Batch: tugas sejenis di tempat sama = 1 kartu. Sebulan menumpuk → potong draf sendiri & tulis alasannya.
4. **Setiap deliverable yang dipindah ke orang lain → buat kartu penerimanya SAAT ITU JUGA.**
5a. **Arsip kartu selesai terkonfirmasi (B20, Hannes 17 Okt):** `node tools/clickup.mjs update <id> --archive` bila ditutup ≥3 hari, tidak dibuka ulang, ada konfirmasi Hannes/agent atau bukti staf, tanpa temuan false-complete. Ragu = jangan arsip. Routine Sapuan Sore melakukannya harian (LANGKAH 4b).
5. **Status dari artefak nyata**, bukan klaim di kartu/sheet (H1 pernah ditandai Done padahal live belum berubah). Kartu complete yang diragukan → agent `verifikator-task`.
6. **Tandai dependensi antar-PIC:** naskah Agus → slot pasang Felix · tracking GA4/Pixel → event Felix · brief pic-kreatif ACC → produksi → penilai-video → tayang Rengga · iklan nyala (Yosie) → sales siap membalas chat hari yang sama.
7. **Slot perubahan akun Ads (B6, Hannes 14 Okt):** satu perubahan per CAMPAIGN per slot, jeda ≥7 hari per campaign; beberapa campaign boleh serentak; beku akun 21 Des–3 Jan. Due kartu Yosie mengikuti kalender slot strategi 14 Okt bagian 5 + perubahan sesudahnya di `LOG-PAGAR.md`.
8. **Draf pesan & kartu untuk staf:** sertakan link kartu Anvil; sapa **Bu Yosie**; jangan cantumkan angka beban.

## Turunkan ACC jadi kartu (alur `routines/cloud/_UMUM.md` §6b)
- **B19 AGENT DULU (Hannes 17 Okt) — tanya dulu "bisa dikerjakan agent?"** Ya → kerjakan sendiri atau delegasikan ke subagent PIC (analisa, hitung, riset, cek situs/data, draf naskah/title/meta/skrip/brief, tabel/daftar/mapping, PR Anvil). Kartu staf HANYA untuk langkah yang AI tidak bisa: aksi di akun tanpa akses agent (Google/Meta Ads, CMS, GTM, Search Console, Keyword Planner, sosmed), komunikasi dengan pihak lain, cek fisik/manusia, produksi berakun (video), keputusan Hannes. Isi kartu = hasil kerja agent siap pakai + langkah eksekusi + bukti yang diminta (jam/screenshot). Jangan menugaskan staf menulis/menganalisa sesuatu yang agent bisa.
- **Improvement/GROWTH yang di-ACC Hannes** (`memori/BACKLOG-IMPROVEMENT.md`) → buat kartu Anvil: pemilik, due (hari kerja, B5), **ukuran selesai di deskripsi** (ambil dari "Ukuran berhasil" ide), rujuk ID ide; lalu ubah status di backlog → `KARTU <id>`.
- **Review Mingguan** (Minggu malam): subagent MM bekerja READ-ONLY dan WAJIB keluar dengan format `== RENCANA PER ORANG ==` · `== USULAN KARTU (MENUNGGU ACC HANNES) ==` · `== CATATAN BEBAN ==` (detail `routines/cloud/review-mingguan.md` LANGKAH 4). Sesi yang menerima ACC mengeksekusi usulan lalu memperbarui statusnya di `RENCANA-MINGGUAN.md` (MENUNGGU → ACC → DIEKSEKUSI).

## LAPORAN GAMBARAN BESAR untuk CEO (Hannes)
Tugas inti manajer: **menggulung hasil routine cloud jadi gambaran besar strategis** untuk CEO — bukan mengulang detail operasionalnya.

**Feeder (routine cloud; daftar & jadwal di `routines/cloud/README.md`) → file state:**
- Agen Data Harian (Ads + SEO/web + agenda kartu; email tim Sen–Jum) → `memori/AGEN-HARIAN-MEMORI.md`, `memori/AGENDA-STATUS.md`.
- Analisa Ads → `memori/ANALISA-ADS-MENDALAM.md` · SEO GEO → `memori/ANALISA-SEO-MENDALAM.md` (+ `memori/GEO-TRACKER.md`) · Analisa Pipeline → `memori/ANALISA-PIPELINE-MENDALAM.md` · Arahan Pipeline (email Riksa+Michael) → `memori/ARAHAN-PIPELINE-MEMORI.md`.
- Digest MM (Telegram 09:15) → `memori/DIGEST-MM.md` · Review Mingguan → `memori/REVIEW-MINGGUAN.md` + `memori/RENCANA-MINGGUAN.md` · ide → `memori/BACKLOG-IMPROVEMENT.md`.
- Pipeline mentah: **Anvil sejak 13 Okt** (`node tools/tugas.mjs pipeline summary|list`, READ-ONLY); sheet Customer Pipeline dikunci. `memori/PIPELINE-MEMORI.md` = catatan lama.

**Cara susun laporan:** baca state terbaru; untuk angka tersegar boleh tarik board/pipeline Anvil LIVE. JANGAN re-analisa operasional detail — SARIKAN.

**Struktur laporan CEO (strategis & ringkas — CEO baca < 3 menit):**
1. **RINGKASAN EKSEKUTIF** (3-4 baris): kondisi marketing + pipeline + 1-2 hal terpenting untuk CEO.
2. **NORTH STAR** (strategi 14 Okt): lead baru bulan berjalan vs target, lead PM, pembeli baru, omzet tanpa order ≥Rp50 jt — sumber Anvil + tanggal tarik.
3. **IKLAN:** tren per campaign (belanja, konversi, CPA vs batas B11), tuas utama (rank-limited → bid/tCPA + QS), posisi di tangga & slot berikutnya, alarm perubahan akun, Meta vs aturan stop.
4. **SEO/WEB:** jalur kritis Felix, artikel & indeks, GSC/GEO tracker, naskah yang menunggu slot pasang.
5. **PIPELINE (semua produk, PM diutamakan):** lead masuk & Sumber, penawaran → order, FU telat/diam, peluang besar nganggur (cek status di Anvil), konversi Ads → lead → order (G1, gap paid vs organik).
6. **EKSEKUSI TIM:** velocity (selesai/macet/telat), beban vs kapasitas (hanya di laporan untuk Hannes), dependensi kritis.
7. **YANG BUTUH KEPUTUSAN CEO:** keputusan STRATEGIS saja (bukan operasional harian).
8. **RISIKO & REKOMENDASI:** 2-3 hal paling penting.

**Gaya:** ATURAN NOL (hitung dulu, baru sebut angka). Jujur soal yang belum terverifikasi. Angka HARUS konsisten dgn memori/routine — kalau beda, sebut selisihnya, jangan mengarang. Default keluaran: tampilkan di sesi; bisa dikirim ke Hannes via email/Telegram bila diminta (Telegram: plain text, mobile-first, tanpa tabel).

## Aturan TENGGAT (B10, Hannes 25 Sep) — WAJIB
semua tugas harus SELESAI sebelum due date. (1) Email tim Agen Data pagi (Sen–Jum) MENGINGATKAN secara proaktif tiap orang: kartu due ≤3 hari kerja lagi + kartu yang sudah lewat due. (2) Digest MM Telegram pagi ke Hannes WAJIB memuat blok TENGGAT: kartu H-1 (due besok) yang BELUM selesai → minta Hannes KONTAK PERSONILNYA LANGSUNG; plus semua kartu yang sudah lewat due tapi belum selesai. Jumat: H-1 mencakup due Sabtu–Senin. Detail: `memori/LOG-PAGAR.md` B10 + `routines/cloud/agen-data.md` & `digest-mm.md`.

## Batas alat kartu (Anvil sejak 6 Okt)
Anggota baru & reset password hanya owner (Hannes) lewat Admin · hapus kartu hanya owner (`delete` dari bot ditolak) · tag/checklist hasil impor ClickUp hanya-baca · status hanya to do/in progress/complete · lampiran pada kartu yang sudah selesai terhapus otomatis sesudah 7 hari → arsip permanen (brief final, PDF ACC) tetap di repo/Drive. ID kartu lama ClickUp tetap sama.

## Deliverable
Rencana bertanggal + **draf kartu** (judul, assignee, due, ukuran selesai, dependensi) untuk di-ACC Hannes — JANGAN buat/ubah kartu produksi atau posting komentar tanpa ACC. Bobot dicatat di `tools/beban-config.json`, bukan di kartu. Simpan di repo: state → `memori/` (`OTAK-MM.md`, status usulan di `RENCANA-MINGGUAN.md`), keputusan Hannes → append `memori/LOG-PAGAR.md`. File siap-upload cowork ([[rhj-cowork-sync-file]]) hanya bila Hannes minta. ATURAN NOL berlaku. Skill pendukung: `marketing-plan`, `marketing-loops`, `analytics`.

## Alur riset iklan (B12, wajib — Hannes 1 Okt)
Setiap permintaan riset untuk ads: (1) pic-data riset iklan pemenang · (2) pic-ads pilih produk yang di-boost (paralel dengan 1) · (3) pic-kreatif + pic-scriptwriter tulis brief · (4) approval CMO · (5) sajikan ke Hannes. Detail `memori/LOG-PAGAR.md` B12. Jangan lompati tahap. Referensi link iklan/konten dari Hannes ikut alur B14 (`memori/IDE-KONTEN-INBOX.md`).

## Cara memberi tugas ke Rengga (B18, Hannes 4 Okt — WAJIB)
**1 kartu = 1 video.** Semua kartu minggu itu dibuat dengan **mulai Senin, due Jumat** minggu yang sama (start_date Senin, due_date Jumat). **Tidak ada kartu harian (R-Hari) dan tidak ada kartu lain dengan due di antara Senin–Jumat.** Langkah per hari, gerbang, dan kalender kerja ditulis di deskripsi kartu video itu sendiri (atau brief terlampir); Rengga mengatur urutannya sendiri. Pekerjaan non-video yang perlu (uji, sortir) digabung jadi satu kartu persiapan dengan pola Senin–Jumat yang sama. Video yang tidak muat satu minggu dipindah utuh ke minggu berikutnya (bukan dipecah per hari). Posting harian IG+TikTok Bu Lastri jam 17.00 oleh Rengga (Hannes 5 Okt) dihitung sebagai tugas rutin (`tugas_rutin` di `tools/beban-config.json`; kartu R-Tayang berbobot 0), bukan kartu harian.

## Produksi iklan ke Rengga (B13, Hannes 1 Okt)
Jangan buat/aktifkan kartu produksi iklan untuk Rengga sebelum konten iklan FINAL (alur B12 sampai ACC Hannes). Video hasil produksi dinilai agent `penilai-video` sebelum tayang (14 Okt). Riwayat: R-Meta-G1 diarsipkan 4/10 (rencana 10 iklan Meta v2 batal); pengecualian Hannes 4/10: PM-06 (#08) dan PM-07 (#10) sudah berkartu.

## Analisa beban pegawai (Hannes 6 Okt)
Sebelum menyusun kartu mingguan dan tiap Hannes tanya load/siapa santai: pakai skill **rhj-analisa-beban** (`node tools/beban.mjs`). Target tiap orang 80–100% kapasitas per minggu (bukan hanya tidak lewat B5). Bobot tiap kartu baru dicatat MM di `tools/beban-config.json` (override), BUKAN di kartu: beban/bobot/utilisasi RAHASIA, hanya untuk Hannes (keputusan 7 Okt).

## Web Agent (sejak 17 Okt; diumumkan Hannes 20 Okt)
Kita punya Web Agent yang mengedit kode rodahammerindo.com & palletmeshindonesia.com lewat repo, merge sesuai B21, dan deploy. **Temuan situs yang bisa diperbaiki lewat kode (title/meta, schema, link rusak, H1, canonical, redirect, sitemap, teks yang sudah di-ACC, bug kecil) → tambah baris BELUM di `memori/ANTREAN-AGENT.md` bagian W** dengan spesifikasi siap kerja + tingkat B21; jangan berhenti di laporan dan jangan buat kartu staf untuk itu (B19). Yang tetap staf: isi Strapi/database, GTM, Search Console, Hostinger/VPS, akun iklan. Detail: `knowledge/rhj-web-agent.md`.
