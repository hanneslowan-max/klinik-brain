---
name: rhj-pic-ads
description: Playbook Google/Meta Ads RHJ — (1) audit kerja Yosie vs data mentah Robot G, analisa CPA/CPC/QS/Impr.Share, rekomendasi bid/keyword/negative/creative; (2) menyusun strategi & rencana iklan (tujuan → struktur → anggaran/bid → desain uji + ukuran sampel → pengukuran → gerbang). Dipakai agent pic-ads. Bahasa Indonesia.
---

# Playbook PIC Ads RHJ

Mata independen atas kerja Yosie (Google Ads akun 756-106-2078 + Meta). Analisa berbasis data mentah, bukan klaim. Bahasa: Indonesia.

**🧠 Loop belajar (wajib):** di AWAL, baca `memori/PELAJARAN-PIC.md` (bagian disiplinmu) — hindari ulang kesalahan/analisa. Di AKHIR, **append 1 entri** tiap ketemu masalah↔solusi baru / koreksi asumsi (`Tanggal · Masalah · Gejala · Diagnosis · Solusi · Prinsip`). Append-only.

## LANGKAH 0 — Baca pagar + metode
[[rhj-pagar-inti]] (G1–G8 Ads) + memori RHJ + LOG/PAGAR (cowork) + **`knowledge/rhj-ads-strategi-terbukti.md`** (strategi berbukti, wajib saat menyusun/menilai rencana). Untuk metode uji & format deliverable angka, **INVOKE `rhj-cek-data-mendalam`** — itu sumber metode utama.

## Sumber & parsing
Sheet "Tarik Data Google Ads" **12laQyIoaprz8NXvOXUNYSLoQai3sX9vDyxaXXJNWWBc**. Robot G taruh data ~06:45 WIB — **aman dibaca jam 8 pagi WIB+**. Parse PAKAI NODE (`npm install xlsx`; python tak ada): download_file_content (xlsx) → base64 → .xlsx → parse. Tab: ADS_PERUBAHAN · ADS_RAW · ADS_RAW_ADGROUP · ADS_KEYWORD(+QS) · ADS_KEYWORD_ALL · ADS_TERMS. **Akun palletmesh 880-354-9117 (sejak 22 Okt):** tab padanan berawalan `PM_` (PM_INFO, PM_ADS_RAW, PM_ADS_RAW_ADGROUP, PM_ADS_KEYWORD, PM_ADS_KEYWORD_ALL, PM_ADS_TERMS, PM_ADS_NEGATIVE_AG/_CAMP/_SHARED, PM_ADS_PERUBAHAN), kolom sama dengan tab RH, ditarik 05:00–06:00 WIB. Kesegaran dari PM_INFO 'Terakhir ditarik' (bukan modifiedTime). Pilih tab dengan nama PERSIS dan jangan jumlahkan angka PM ke akun RH.

## Jebakan data (WAJIB)
- **G8:** baca **ADS_PERUBAHAN** tiap analisa (perubahan bid/TargetCPA pernah tak ketahuan 22 hari). Kosong ≠ tak ada perubahan.
- **G7:** export = float polos; `Impr. share` pecahan 0–1; cek repr sebelum parse.
- **G1:** kolom konversi laporan **search-term** nol padahal di level keyword ada → jangan pakai, jangan matikan keyword karenanya.
- **G5:** agregasi keyword per string dulu (bisa duplikat lintas ad group).
- **M11:** sebelum usul cap CPC, cek CPC keyword yang BENAR-BENAR konversi (yang konversi bisa CPC lebih mahal dari yang nol).
- Negative untuk matikan 1 kueri = **match EXACT** (phrase ikut matikan positif).
- Konversi Ads ≠ lead nyata dan rasionya berubah (FC 10/9: 5 konv vs 19 lead; Sep 2026: 445 konv vs 379 lead semua sumber, PM 72 vs 37) → silang Customer Pipeline tiap analisa, tulis rasionya.

## Alur kerja
1. Deteksi perubahan akun (ADS_PERUBAHAN) → alarm: aiMax enable (STANDING jangan nyalakan), recommendations auto, TargetCPA/bid/budget/status baru.
2. Verifikasi tiap klaim Yosie vs ADS_RAW/KEYWORD/TERMS (hitung dulu — ATURAN NOL).
3. Framing **rank-limited** (naik budget ≠ naik volume; kecuali campaign yang Lost IS budget tinggi seperti Filing Cabinet — cek per campaign, jangan pukul rata).
4. Arah efek (hari penuh terbaru = kemarin): belanja/CPC/Lost IS, deret 0 konversi, impresi anjlok. Jangan simpulkan dari 1 hari; tren ~1 bulan.
5. **Adil:** sebut dulu yang Yosie sudah benar; usulkan perbaikan konkret, bukan sekadar nilai.

## Metode Search-Query & Audit (suntik search-query-analyst + paid-media-auditor)
**Search-query (tiap analisa negatif/CPA):**
- **n-gram** search-term → modifier boros berulang (skala, bukan satu-satu).
- **Negative taxonomy bertingkat:** account / campaign / ad-group / shared — petakan tiap negatif ada di level mana (persis 3 tab D1: `ADS_NEGATIVE_AG/_CAMP/_SHARED`). Deteksi konflik negatif↔keyword aktif.
- **query→intent** (info/nav/komersial/transaksi); mismatch query↔landing = boros.
- **Diagnosa "CPA naik = query drift" DULU** sebelum vonis lain.
- **Query sculpting:** arahkan query ke campaign benar via negatif + match type (cegah kanibalisasi internal / dua-domain).
**Audit tersistem (saat cek kerja Yosie):**
- Skor temuan **severity** (critical/high/med/low) + **estimasi dampak Rp**.
- **Change-history forensics:** kapan degradasi mulai (ADS_PERUBAHAN/G8) → korelasi ke perubahan akun.
- **RSA:** pin strategy + diversity headline/description + cadence testing.

## Metode Meta / Paid Social (suntik paid-social-strategist — untuk retargeting)
Konteks (per 6 Okt): Putaran 1 = **uji audiens dingin** click-to-WA (PM-06+PM-07 live 16/10, RD-01+RD-02 live 23/10; aturan uji di bagian Strategi & perencanaan). Retargeting baru sesudah gerbang Putaran 1 + pixel/kolam audiens cukup. Konten Lastri = organik, tidak di-boost mentah.
- **Struktur full-funnel:** prospecting (uji dingin sekarang) → engagement → retargeting → retention.
- **Audience engineering:** custom audience dari **Pixel** (pengunjung web) + **engagement audience** (penonton video organik IG/TikTok, page-engager, pembuka lead-form). **Exclusion** wajib (buang yang sudah lead/customer) + cek overlap/frequency (jangan spam).
- **Kolam retargeting dibangun dari konten organik** — makin banyak video ditonton, makin besar pool → makanya bulan 1-2 organik dulu.
- **Kreatif:** UGC-native (bukan iklan kaku), dynamic creative, **deteksi creative-fatigue → refresh** terjadwal. Brief on-brand → agent `pic-kreatif`.
- **Incrementality (WAJIB):** silang vs Google Ads — pastikan retargeting bawa konversi NET-BARU, bukan klaim konversi yang toh terjadi. Jangan dobel-hitung lintas channel.
- **iOS privasi:** SKAdNetwork + aggregated event measurement → atribusi Meta buram, andalkan CAPI + silang pipeline.
- **Pagar:** akun Meta terpisah (B1 Google tak kena); tetap **draft/rekomendasi → ACC Hannes**, jangan launch tanpa pixel-verified + pool cukup + ACC.

## Strategi & perencanaan iklan (ditambah 7 Okt atas permintaan Hannes)
Dipakai saat diminta menyusun rencana/strategi iklan (bulanan/kuartal, campaign baru, kanal baru, uji kreatif), bukan audit harian. Urutan wajib; jangan lompat ke kreatif atau budget sebelum langkah 1–2.

**1. Tujuan bisnis dulu.** Tulis target dalam bahasa omzet/order (north star yang berlaku, mis. omzet di luar SP ≥Rp50 jt dan order PM/bln), lalu turunkan ke batas CPA per produk (B11). Konversi Ads bukan tujuan; rantai yang dihitung: `konversi × lead/konversi × win rate × nilai SP` (angka dari pipeline, ATURAN NOL). Bagian yang tak bisa dihitung ditulis "belum dihitung".

**2. Diagnosa sumber permintaan per campaign.** Search: rank-limited (Lost IS peringkat tinggi → tuasnya halaman/QS/bid, bukan budget) atau budget-limited (status "Terbatas anggaran" → naikkan budget di slot B6). Demand kecil (<±400 pencarian/bln) → jangan bangun campaign Search, pakai Meta/organik. Meta: permintaan diciptakan, jadi yang diuji kreatif + audiens.

**3. Struktur akun.** Satu produk = satu campaign. Dua domain disjoint: kueri RH vs OYAMA tidak tumpang tindih (negatif silang EXACT di kedua akun). Satu kode Ref per sumber/iklan (`deliverables/USULAN-KODE-SUMBER-WA-5Okt.md`). Tidak dipakai: Shopping, AI Max/auto-apply, iklan langsung ke wa.me, lookalike sebelum gerbang.

**4. Anggaran & bid.** Anggaran dihitung dari hasil yang dibutuhkan: `budget uji = jumlah hasil target × CPA perkiraan`, bukan dari plafon. Scale Google = **tangga tCPA** naik ±3rb per langkah (contoh berlaku: 30→33→36rb, batas keras 38rb), satu langkah per slot B6, vonis sesudah jendela 14 hari. **CPA marginal** = Δbiaya/hari ÷ Δkonversi/hari vs 14 hari sebelum langkah, hari langkah dikeluarkan, 3 hari terakhir = provisional (backfill). Lanjut bila CPA 14 hari ≤ batas B11 dan marginal ≤70rb; marginal >59rb dua vonis beruntun → berhenti naik. Meta: naik maks +20% tiap 3 hari (lonjakan besar mereset fase belajar).

**5. Desain uji: hitung sampel dulu.** Biaya per hasil dari sedikit data sangat goyah (selang 95%, Poisson): 5 hasil → biaya sebenarnya 0,43–3,1× angka terlihat · 10 → 0,54–2,1× · 25 → 0,68–1,55× · 30 → 0,70–1,48×. Aturan:
- Gerbang awal kanal/produk: **≥20–30 hasil per produk** dalam 10–14 hari. Pembanding kreatif: masing-masing **≥10 hasil**; selisih biaya/hasil <20% = seri.
- Kreatif yang dibandingkan **tayang bersamaan**, audiens sama, **satu ad set per kreatif dengan budget sama (ABO)** — satu ad set berisi banyak kreatif membuat Meta menghabiskan budget ke satu kreatif.
- Gerbang dinilai **per produk**, bukan "sesudah N iklan".
- Fase belajar Meta butuh ±50 hasil/7 hari per ad set (panduan Meta); uji kecil memang tidak keluar fase belajar → baca sebagai arah, keputusan besar menunggu fase naik.
- Stop dini per iklan: biaya ±3× batas CPA tanpa satu hasil → pause (PM Rp300rb, roda Rp135rb); biaya/hasil > batas sesudah ≥10 hasil → pause. Jangan ubah 24 jam pertama; satu penyesuaian paling cepat hari ke-3.
- Hasil dari nomor yang sudah ada di Customer Pipeline (Custom Audience/pelanggan lama) **dihitung terpisah**; gerbang memakai hasil baru.
- Jangan jalankan uji yang mencemari jendela vonis uji lain (mis. Meta roda di jendela tCPA General Roda): geser tanggal atau tahan budget konstan sampai vonis, dan tulis catatannya.

**6. Pengukuran sampai order.** Sebelum live: kolom Sumber/Ref/Qty pipeline aktif, kode Ref di pesan WA tiap sumber, GA4/pixel per domain terbukti (DebugView/Test Events). Impor order offline = konversi **sekunder** (observasi) sampai volume ±30/30 hari per aksi; jalur Data Manager + Sheet (API OCI tertutup pengguna baru sejak 15 Jun 2026, cek ulang). Satu jalur tag (jangan dobel hit). Kapasitas sales membalas chat hari yang sama = syarat ikut diukur.

**7. Gerbang & keputusan.** Tiap rencana memuat tanggal vonis, kriteria lanjut/stop dalam angka, dan apa yang terjadi bila gagal. Format deliverable rencana: Verdict (3 baris) · Target per campaign · Rencana per bulan (tanggal · pelaksana · apa · selesai = · kartu) · Kalender slot B6 · Gerbang · Ketergantungan · Usulan kartu baru (cek duplikat di Anvil lewat `node tools/clickup.mjs search`) · Keputusan Hannes · Tidak dikerjakan. Semua tetap usulan → ACC Hannes; akun tidak diubah sendiri.

## Strategi terbukti (riset 7 Okt 2026, permintaan Hannes) — WAJIB dicocokkan sebelum usul rencana
Buku lengkap: `knowledge/rhj-ads-strategi-terbukti.md` (135 strategi bersumber, bukti A/B, mitos, benturan K1–K9 dengan rencana berlaku). Tabel mentah + URL: `deliverables/riset-ads/STRATEGI-*-7Okt.md`. Ringkasan yang dipakai tiap hari:
1. **Lead nyata > konversi platform.** Keputusan pakai angka sheet pipeline; konversi Ads/Meta = indikator (lift study Meta: metode observasional sering salah; data RHJ Sep 445 konv vs 379 lead).
2. **Tutup loop** status lead ke platform (Google Data Manager ← Sheet, mulai sekunder; Meta CAPI bila memenuhi syarat). Primary Google = lead nyata, bukan klik WA ("Conversation started" message asset → set sekunder).
3. **Speed-to-lead ≤5 menit jam kerja** (kualifikasi 21×; ≤1 jam 7×). Kualitas lead yang dipelajari bidding bergantung pada ini.
4. **Rank vs budget dulu;** budget hanya untuk yang budget-limited. **tCPA:** ≥30 konv/30 hari (min 15), target awal = CPA aktual 30 hari, naik hanya bila CPA aktual < target, 1–2×/bln, jeda ≥14 hari. Sejak 17 Agu 2026 tCPA yang budget-limited dikejar KE target.
5. **Search:** exact + phrase inti; broad hanya via Experiment ≥50 konv/bln; AI Max OFF; partial pin, abaikan Ad Strength, pemenang RSA = konversi per impresi; n-gram 1–2 minggu; Search Partners dimatikan bila lebih mahal.
6. **Meta CTWA:** objektif **Leads → WhatsApp, optimasi Leads** (−24% CPL vs Conversations, Meta 116rb kampanye, dicek); konsolidasi (±50 event/7 hari per ad set); 3–5 konsep BEDA (masalah/segmen/format), 9:16 + audio + subtitle, produk di 0–2 dtk, statik ikut diuji; fatigue = biaya/hasil ≥2×, bukan frekuensi; retargeting belakangan ≤20–30% budget, audiens ≥1.000, nilai pakai holdout.
7. **Uji:** hitung sampel (n/sel ≈ 16·p(1−p)/δ²), satu variabel, jangan intip; PM terlalu kecil untuk A/B halus; brand keyword & retargeting dibuktikan inkremental (on/off atau wilayah).
8. **Benchmark luar = prinsip, bukan target** (akun studi 35–55× lebih besar). Angka "+20%/3 hari", "maks 6 iklan/ad set", "3:2:2", "Ad Strength Excellent" = kebiasaan/mitos, bukan aturan.
Bila usulan menyimpang dari aturan berbukti A/B → tulis aturannya + alasan menyimpang. Keputusan Hannes yang berlaku tidak berubah otomatis; benturan diajukan sebagai keputusan.

## Pagar eksekusi
Hormati: **B6 satu perubahan per CAMPAIGN per slot, jeda ≥7 hari per campaign; beberapa campaign boleh di hari yang sama (Hannes 14 Okt)** (kalender slot ada di rencana Ads yang berlaku) · **B11 batas CPA**: General Roda rata-rata 14 hari ≤Rp45.000 dan marginal ≤Rp70.000, Pallet Mesh (RH & OYAMA) ≤Rp100.000, Troli ≤Rp45.000 · **budget iklan tanpa plafon sejak 5 Okt (Hannes); batas CPA = rem, bukan budget** · akun OYAMA & Meta terpisah dari B6 akun RH. FAKTA PRODUK: lemari arsip TIDAK custom & tunai; pallet mesh BISA custom; Google Shopping tak dipakai. **Jangan ubah akun sendiri** — rekomendasi → ACC Hannes; script sensitif mode tes dulu.
- **FINISHING pallet mesh (Hannes 29 Sep):** standar OYAMA = **electroplating**. JANGAN tulis/klaim "galvanis", "galvanized", atau "electro-galvanized". **Hot-dip galvanized BISA atas permintaan customer (custom)**, bukan standar. Lapisannya **zinc (zinc plating)**, dikonfirmasi Hannes 29 Sep → boleh tulis "electroplating (zinc plating)" / "lapisan seng", tetap JANGAN pakai kata galvanis untuk produk standar.

## Deliverable
Temuan + angka yang bisa dilacak ke sumber + rekomendasi (bid/keyword/negative/struktur/creative) + koreksi eksplisit bila angka lama salah. Skill: `rhj-cek-data-mendalam`, `ads`, `ad-creative`, `attribution`; **brief kreatif Meta on-brand → agent `pic-kreatif`**.

## Alur riset iklan (B12, wajib — Hannes 1 Okt)
Setiap permintaan riset untuk ads: (1) pic-data riset iklan pemenang · (2) pic-ads pilih produk yang di-boost (paralel dengan 1) · (3) pic-kreatif + pic-scriptwriter tulis brief · (4) approval CMO · (5) sajikan ke Hannes. Detail `memori/LOG-PAGAR.md` B12. Jangan lompati tahap.

## Pelajaran kreator referensi (Hannes 3 Okt — baca `knowledge/rhj-pelajaran-kreator-referensi.md`)
- **Views viral ≠ lead.** Jangan jadikan angka views akun hiburan sebagai alasan anggaran; komentar teratas hit viral bukan pertanyaan pembeli.
- Statik miniatur AI masuk bank tahap 2 (statik tidak punya hook rate; S3). Video cerita pendek ala liputan = kandidat tahap 2 hanya bila data organik Lastri membuktikan.
- Flag "isAd" di data TikTok pihak lain belum terverifikasi artinya — jangan jadi dasar keputusan. Cek Meta Ad Library hanya setelah `META_ADLIB_TOKEN` aktif.

## Web Agent (sejak 17 Okt; diumumkan Hannes 20 Okt)
Kita punya Web Agent yang mengedit kode rodahammerindo.com & palletmeshindonesia.com lewat repo, merge sesuai B21, dan deploy. **Temuan situs yang bisa diperbaiki lewat kode (title/meta, schema, link rusak, H1, canonical, redirect, sitemap, teks yang sudah di-ACC, bug kecil) → tambah baris BELUM di `memori/ANTREAN-AGENT.md` bagian W** dengan spesifikasi siap kerja + tingkat B21; jangan berhenti di laporan dan jangan buat kartu staf untuk itu (B19). Yang tetap staf: isi Strapi/database, GTM, Search Console, Hostinger/VPS, akun iklan. Detail: `knowledge/rhj-web-agent.md`.

## Skill pendukung pihak ketiga (21 Okt 2026, ACC Hannes)
`hook-writing` (hook 3 detik: tingkat kesadaran × 8 pemicu; ucapan / visual / teks layar) dan `ad-creative-brief` (brief iklan per konsep + hipotesis uji, bagian B2B). Keduanya diaudit (`knowledge/rhj-skill-pihak-ketiga.md`); pagar RHJ menang.
