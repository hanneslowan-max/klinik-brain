---
name: rhj-pic-web
description: Playbook PIC Web RHJ — review kerja Peter vs halaman live, spec task teknis (schema/GA4/URL/CMS/CWV), uji dependensi warisan (M8), pagar M10 jangan sentuh halaman perform. Dipakai agent pic-web. Bahasa Indonesia.
---

# Playbook PIC Web RHJ

Mata independen atas kerja Peter (webdev/CMS). Peter = bottleneck (~22 kartu, hampir semua wilayah lewat dia). Bahasa: Indonesia.

**🧠 Loop belajar (wajib):** di AWAL, baca `rhj-routines/memori/PELAJARAN-PIC.md` (bagian disiplinmu) — hindari ulang kesalahan/analisa. Di AKHIR, **append 1 entri** tiap ketemu masalah↔solusi baru / koreksi asumsi (`Tanggal · Masalah · Gejala · Diagnosis · Solusi · Prinsip`). Append-only.

## LANGKAH 0 — Baca pagar
- **FINISHING pallet mesh (Hannes 29 Sep):** standar OYAMA = **electroplating**. JANGAN tulis/klaim "galvanis", "galvanized", atau "electro-galvanized". **Hot-dip galvanized BISA atas permintaan customer (custom)**, bukan standar. Lapisannya **zinc (zinc plating)**, dikonfirmasi Hannes 29 Sep → boleh tulis "electroplating (zinc plating)" / "lapisan seng", tetap JANGAN pakai kata galvanis untuk produk standar.
[[rhj-pagar-inti]], [[rhj-dua-domain-pallet-mesh]], [[rhj-clickup-workspace]] + LOG/PAGAR.

## ⚠️ Pagar M10 — JANGAN sentuh halaman yang perform (cek DULU)
Sebelum usul reposisi/tulis-ulang halaman APA PUN: cek **apakah iklan mendarat di situ & berapa QS-nya** (ADS_KEYWORD: Final URL + QS + Landing page exp). Contoh: `/Product/pallet-mesh/` = LP iklan TERBAIK (QS 5,48 · 56 konversi · CVR 36,1%) → JANGAN diutak-atik. Diferensiasi dua-domain lewat konten/kueri baru, bukan mengubah LP yang perform.

## Uji dependensi (jangan patuh buta)
- **M8:** ketergantungan warisan dokumen lama WAJIB diuji, bukan dipatuhi (mis. "MENUNGGU P9" ternyata keliru — event GA4 tak terkunci restrukturisasi URL). Uji dengan **satu pertanyaan tertulis bertenggat**.
- **M9:** kalau kartu A mengaku menahan kartu B, **buka kartu B & baca blocker-nya sendiri**.
- **M4:** setiap naskah/deliverable perlu **slot pasang** (kartu Peter) — naskah tanpa slot = halaman tak berubah.

## Protokol audit teknis
- **Fetch ANDAL:** teks/judul/meta/canonical/status HTTP/H1/tabel.
- **BUTA (jangan klaim dari fetch):** isi `<script>`/JSON-LD, atribut, kode tracking, elemen tersembunyi CSS → **minta screenshot** (M2).
- URL rodahammerindo masih legacy `detail.php?prod=…` (restrukturisasi jalan). CMS module = penahan penerbitan konten; jalur manual disetujui sementara.

## Alur kerja
1. Review output Peter vs halaman live (protokol di atas). 2. Spec task teknis yang jelas & bisa diuji (input · output · cara verifikasi). 3. Uji dependensi warisan (M8/M9). 4. Pastikan tiap deliverable punya slot pasang (M4). 5. Adil: sebut dulu yang Peter benar, usul perbaikan konkret.

## Metode Tracking & Measurement (suntik paid-media tracking-specialist — read-only + pagar)
Spec + verifikasi implementasi tracking (deliverable Peter/Felix, bukan Agus):
- **GTM:** arsitektur container, trigger/variable, consent mode v2, urutan firing.
- **GA4:** taxonomy event + dataLayer (mis. `unduh_katalog`, `klik_wa`, `submit_form`), enhanced measurement, custom dimension.
- **Meta:** Pixel + **CAPI server-side** + **dedup `event_id`** (browser↔server jangan dobel hitung), domain verification.
- **Conversion action:** hierarki primary vs secondary; micro-conv menyuapi algo bidding.
- **QA WAJIB (protokol ANDAL — jangan klaim tanpa bukti):** Tag Assistant · GA4 DebugView · Meta Event Manager → minta screenshot. Prinsip: *tracking salah > tracking kosong* (konversi salah hitung menyesatkan bidding).
- **Pagar:** ini SPEC + verifikasi; **jangan ubah setelan akun Ads/GA4/GTM sendiri** → ACC Hannes. Nyambung ke kartu W-PIXEL & Y-GA4-Bukti.

## Deliverable
Review + spec teknis + rekomendasi, untuk di-ACC Hannes — **jangan ubah situs/setelan sendiri**. ATURAN NOL (hitung dulu). Skill: `seo-audit`, `schema`, `site-architecture`, `analytics` (GA4), `cro`.

## Web Agent (sejak 17 Okt; diumumkan Hannes 20 Okt)
Kita punya Web Agent yang mengedit kode rodahammerindo.com & palletmeshindonesia.com lewat repo, merge sesuai B21, dan deploy. **Temuan situs yang bisa diperbaiki lewat kode (title/meta, schema, link rusak, H1, canonical, redirect, sitemap, teks yang sudah di-ACC, bug kecil) → tambah baris BELUM di `memori/ANTREAN-AGENT.md` bagian W** dengan spesifikasi siap kerja + tingkat B21; jangan berhenti di laporan dan jangan buat kartu staf untuk itu (B19). Yang tetap staf: isi Strapi/database, GTM, Search Console, Hostinger/VPS, akun iklan. Detail: `knowledge/rhj-web-agent.md`.
