---
name: rhj-cek-data-mendalam
description: Metode dalam uji angka RHJ — tarik & parse data mentah (NODE/xlsx), jebakan Ads G1–G8 & Pipeline P1–P4, silang wajib, uji CPC/keputusan (M10/M11), 1-hari vs tren, & format deliverable angka yang terlacak ke sumber. Sumber metode utama yang disandari pic-ads & pic-data. Bahasa Indonesia.
---

# Metode Uji Angka & Deliverable — RHJ

Sumber **metode dalam** untuk angka yang bisa dipertahankan. pic-ads (angka Ads) & pic-data (silang lintas-corong) menyandar ke sini. Bahasa: Indonesia.

## LANGKAH 0 — ATURAN NOL (M1, mengikat)
**Jangan sebut angka sebelum menghitung/memverifikasinya.** Rekam jejak salah hitung: 9 vs 10 wilayah · 46 vs 47 baris · 33 vs 24 keyword · 3 vs 8 kartu · parser Rp 24 miliar. **Hitung dulu, baru sebut.** Kalau belum dihitung → tulis **"belum dihitung"**, bukan tebakan. Sumber pagar: LOG-PAGAR (`rhj-routines/memori/LOG-PAGAR.md`) + [[rhj-pagar-inti]].

## 1. Sumber & cara tarik (jangan pakai angka orang, tarik mentah)
- **Google Ads:** sheet "Tarik Data Google Ads" `12laQyIoaprz8NXvOXUNYSLoQai3sX9vDyxaXXJNWWBc`. Robot G taruh data ~06:45 WIB → **aman dibaca jam 8 pagi WIB+**. Tab: `ADS_PERUBAHAN` · `ADS_RAW` · `ADS_RAW_ADGROUP` · `ADS_KEYWORD`(+QS) · `ADS_KEYWORD_ALL` · `ADS_TERMS`. **Akun palletmesh 880-354-9117 (sejak 22 Okt):** tab padanan berawalan `PM_` (PM_INFO, PM_ADS_RAW, PM_ADS_RAW_ADGROUP, PM_ADS_KEYWORD, PM_ADS_KEYWORD_ALL, PM_ADS_TERMS, PM_ADS_NEGATIVE_AG/_CAMP/_SHARED, PM_ADS_PERUBAHAN), kolom sama dengan tab RH, ditarik 05:00–06:00 WIB. Kesegaran dari PM_INFO 'Terakhir ditarik' (bukan modifiedTime). Pilih tab dengan nama PERSIS dan jangan jumlahkan angka PM ke akun RH.
- **Customer Pipeline:** sheet sales; **hanya sampai kolom N** (P4 — tak ada kolom O/"TglOK"). Kolom kunci: Item, Remark, Respon, Status, Nilai/SP. **[Saklar 12 Okt]** Sesudah hari pindah (`routines/cloud/PIPELINE-SUMBER.md` = `SUMBER: ANVIL`), sumber data pipeline = **Anvil** lewat `node tools/tugas.mjs pipeline list|get|summary` (READ-ONLY); sheet di atas hanya riwayat sebelum tanggal pindah.
- **Parse PAKAI NODE** (`npm install xlsx`; python tak tersedia): `download_file_content` (xlsx) → base64 → `.xlsx` → parse. `text/csv` hanya ekspor sheet PERTAMA — untuk semua tab pakai xlsx.

## 2. Parsing yang benar (jebakan diam)
- **G7:** ekspor = float polos; `Impr. share` **pecahan 0–1** (bukan %). `print(repr(row))` SEBELUM tulis parser (parser format Indonesia pernah menghasilkan Rp 24 miliar).
- **G5:** baris keyword **duplikat lintas ad group** → agregasi per string dulu; baca baris pertama saja = salah (`lemari arsip 2 pintu` terbaca 0 klik padahal 11/1 konv).
- **G3:** kolom "Budget harian" di ADS_RAW = nilai **SEKARANG** disalin ke semua baris, bukan historis. Riwayat hanya di ADS_PERUBAHAN.

## 3. Jebakan angka — Ads (G1–G8)
- **G1/G2:** kolom konversi laporan **search-term** = NOL padahal di level keyword ada (FC: 0 di term, 5 di keyword). **Jangan matikan keyword karena konversi term nol.** Ads catat 5 konv vs **19 lead pipeline (3,8×)** — tunggu P10 sebelum memangkas.
- **G4:** klaim setelan akun **dari ADS_PERUBAHAN/data**, bukan catatan kartu (bisa basi berminggu).
- **G6:** negative untuk matikan 1 kueri = **match EXACT** (phrase ikut mematikan positif berstring sama).
- **G8:** baca **ADS_PERUBAHAN tiap analisa**. Satu baris `targetCpaMicros` 19 Ags menaikkan CPC 3× tak ketahuan **22 hari**. Kosong ≠ tak ada perubahan.

## 4. Jebakan angka — Pipeline (P1–P4)
- **P1:** kolom Item sering **salah tag** → filter Item saja undercount **±25%**; cari juga di Remark & Respon.
- **P2:** salah tag = lead **hilang dari radar sales** (nol follow-up), bukan sekadar salah catat.
- **P3:** kolom Status hampir tak pernah diperbarui — "Customer Baru" ≠ masih hidup; sebab gagal hanya dari sales manual.
- **P4:** pipeline **hanya sampai kolom N**.

## 5. Silang wajib & uji keputusan
- **Silang ≥2×:** Ads mencatat konversi **≠ lead nyata pipeline** — cross-check tiap klaim ke sumber lain (FC pernah 5 vs 19; belakangan 6 vs 7 — nyaris cocok). Diagnosa bisa **bergeser** (FC: dari "tracking bocor" → "konversi lead→order"); nyatakan ulang saat data berubah.
- **M11 — "klik yang mana, bukan berapa klik":** sebelum usul cap/ubah CPC, cek sebaran CPC keyword yang **BENAR-BENAR konversi**. FC: keyword konversi CPC Rp 22.475 > nol-konversi Rp 14.241 — cap Rp 7.000 menolak 4/4 keyword konversi. Hitung "berapa klik" TAK cukup.
- **M10 — cek QS sebelum sentuh halaman:** sebelum usul reposisi/tulis-ulang halaman, cek `ADS_KEYWORD` Final URL + QS + LP exp. `/Product/pallet-mesh/` QS 5,48/CVR 36,1% = aset, jangan diutak-atik.
- **M8/M9 — dependensi:** ketergantungan warisan **diuji, bukan dipatuhi**; blocker dibaca dari kartu yang DIblok, bukan yang mengaku memblok.

## 6. 1-hari vs tren (jangan menamai "anjlok" prematur)
Penurunan **satu hari** pada campaign berimpresi kecil (<250/hari) = **derau**. Jangan sebut "anjlok/rusak" sebelum **hari kedua** mengonfirmasi (FC "226→36" ternyata balik 154 keesokannya). Tren minimal ~1 bulan; hari penuh terbaru = kemarin.

## Deliverable & pagar
Temuan + **angka yang bisa dilacak ke sumber** (tab/kolom/tanggal) + **daftar gap** (yang belum dihitung — jangan tebak) + **koreksi eksplisit** bila angka lama salah (gaya LOG-PAGAR: "pernah ditulis X / yang benar Y"). Edit dokumen/prompt panjang: **substitusi terkendali M7** (daftar `(label,lama,baru)`, tiap `count==1`, gagal → batalkan semua). Jangan eksekusi aksi keluar / ubah akun tanpa ACC Hannes. Skill pendukung: `analytics`, `attribution`, `revops`.
