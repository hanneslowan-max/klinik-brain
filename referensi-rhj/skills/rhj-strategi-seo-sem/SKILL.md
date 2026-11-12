---
name: rhj-strategi-seo-sem
description: Metode dalam strategi & audit SEO/SEM/GEO RHJ — peta 10 wilayah, ruang lingkup kontrak Agus (7 aturan), 9 jebakan penilaian raker, rantai sebab QS↔CPC, baseline terverifikasi, protokol audit verbatim (ANDAL/BUTA). Sumber metode utama yang disandari pic-seo. Bahasa Indonesia.
---

# Metode Strategi & Audit SEO/SEM/GEO RHJ

Sumber **metode dalam** untuk kerja SEO RHJ. `rhj-pic-seo` (irama audit Agus) dan pic-ads/pic-web menyandar ke sini untuk framework. Bahasa: Indonesia.

## LANGKAH 0 — baca pagar dulu
Sumber kebenaran = **LOG-PAGAR** (`rhj-routines/memori/LOG-PAGAR.md`, append-only, jangan dirapikan) + memori [[rhj-pagar-inti]], [[rhj-dua-domain-pallet-mesh]], [[rhj-clickup-workspace]], [[rhj-bisnis-inti]]. **ATURAN NOL (M1):** hitung/verifikasi dulu baru sebut angka — rekam jejak salah hitung (9 vs 10 wilayah · 46 vs 47 baris · 33 vs 24 keyword). Angka baseline di bawah **drift** → cek ulang live/LOG sebelum mengutip.

## 1. Peta 10 wilayah SEO (petakan fungsi UTUH dulu, baru pilih yang masuk periode)
Jangan menyusun rencana dari kartu yang sudah ada di board — mulai dari peta, supaya yang hilang kelihatan. Tiap wilayah ditandai **pemiliknya**: `[A]`=deliverable Agus · `[P]`=eksekusi webdev Peter/Felix · `[~]`=dipantau (hasil, di luar kendali pelaksana).

1. **Riset kata kunci & niat** `[A]` — per segmen (otomotif · logistik/pergudangan · AMDK); tandai tiap kueri milik domain mana (disjoint, §8).
2. **On-page** `[A]` — title tab, H1, meta description, struktur heading, isi body per halaman.
3. **Konten & otoritas topikal** `[A]` — artikel /panduan/ (OYAMA) & /blog/ (roda/troli), model pilar–kluster.
4. **Arsitektur situs & internal linking** `[A]` spec / `[P]` eksekusi — struktur URL, silo, tautan internal (BUKAN backlink).
5. **SEO teknis** `[P]` — crawlability, indexation, sitemap, robots, canonical, status HTTP, kecepatan/Core Web Vitals.
6. **Structured data / schema (JSON-LD)** `[A]` spec / `[P]` pasang — jangan markup harga/rating yang tak ada di halaman.
7. **Off-page / otoritas** `[A]` usaha (pitch terkirim) / `[~]` hasil — backlink, PR, direktori. Nilai usahanya, bukan jumlah backlink.
8. **Local SEO** `[A/P]` — Google Business Profile, konsistensi NAP.
9. **GEO / AI-search** `[A]` — kutipan LLM (ChatGPT/Perplexity/AI Overview); konten terstruktur untuk mesin jawab (skill `ai-seo`).
10. **Pengukuran & analitik** `[P]` pasang / `[A]` baca — GSC, GA4, atribusi organik vs ads, LP experience → QS → tagihan iklan (§4).

> Peta ini = kerangka kerja; kalau LOG cowork punya enumerasi kanonik berbeda, LOG menang. Yang **tak boleh geser**: jumlahnya **10**, bukan 9 (M1).

## 2. Rantai sebab QS↔CPC (kenapa kerja SEO bayarannya terbaca di iklan)
- **Ad Rank ≈ bid × Quality Score** (+ konteks/ekstensi). QS naik → posisi naik pada bid sama, **CPC aktual turun**, ambang Ad Rank lebih mudah dilewati.
- **QS = 3 komponen:** expected CTR · ad relevance · **landing page experience**.
- **Rantai RHJ:** halaman tipis/tak relevan → LP experience buruk → **QS rendah** → **CPC mahal** → volume tertekan. Akun **rank-limited, BUKAN budget-limited** → menaikkan budget ≠ menambah volume; **perbaikan halaman → QS → CPC** yang menambah volume.
- Karena itu **perbaikan LP experience = kerja SEO yang bayarannya terbaca** (CPC/QS), bukan cuma ranking organik. **Tapi M10:** jangan utak-atik halaman yang QS-nya sudah tinggi (lihat baseline).

## 3. Baseline terverifikasi (per ~12–15 Sep — CEK ULANG sebelum mengutip)
- **Akun Ads:** QS akun **3,24** · CPC **~Rp9.357** · Impr. share **~35%** (rank-limited). CPA akun **44.765**, tanpa FC **34.504** (Gerbang A dinilai di luar FC, B4).
- **Halaman iklan terbaik = `/Product/pallet-mesh/`:** QS **5,48** (tertinggi), CVR **36,1%**, 56 konversi. **JANGAN direposisi (M10).**
- **rodahammerindo.com:** otoritas mapan (200+ klien), URL legacy `detail.php`; punya `/Product/pallet-mesh/` + **6** detail Stocky (2/3/5/7/9/Jumbo — bukan 7); sitemap entri terbaru **2026-01-13**, **memuat** URL blog.
- **palletmeshindonesia.com (OYAMA):** modern (kalkulator, halaman industri, panduan) tapi **SEO muda ~1 bulan, otoritas ≈ nol**.
- **Gerbang A:** target 5/5 H1 live — verifikasi ulang lewat fetch tiap kali, jangan percaya klaim "Done".

## 4. Protokol audit verbatim (mengikat — M2/M3)
- **ANDAL lewat fetch:** teks terlihat, judul tab, meta description, canonical, og, status HTTP, H1, isi tabel.
- **BUTA (jangan klaim dari fetch):** isi `<script>`/JSON-LD, atribut HTML, kode tracking, elemen disembunyikan CSS, dropdown JS → **minta screenshot** (atau baca via browser MCP `read_page`).
- **Satu fetch = satu pertanyaan**, minta **kutipan verbatim**. Jangan gabung pertanyaan.
- **Pisahkan DINILAI vs DIPANTAU:** dinilai = naskah/laporan tepat waktu (100% kendali Agus); dipantau = ranking/impresi organik/LP experience/lead organik — **jangan jadikan dasar penilaian pelaksana**.
- **Uji yang berguna** bukan "katanya ada di halaman", tapi **"ada di judul tab & H1 — dan uangnya balik?"**

## 5. Sembilan (9) jebakan penilaian raker
1. **Kerja webdev dihitung deliverable SEO** (schema/kompresi/layout/API/tracking) → itu ranah Peter; pindahkan (buat kartunya, jangan dihapus).
2. **Tautan antar situs sendiri diklaim backlink** (palletmesh↔rodahammerindo = **internal link**).
3. **KPI di luar kendali pelaksana** dipakai menilai (jumlah backlink, posisi PAA, ranking) — nilai yang dikendalikan (pitch/naskah terkirim).
4. **Metrik pihak ketiga dijadikan kebenaran** (DA Moz) — buang.
5. **Markup harga/rating diklaim padahal tak ada di halaman** — cek live; jangan pasang schema fiktif.
6. **Status dari klaim/sheet, bukan artefak live** (H1 pernah "Done" padahal live tak berubah; **M5:** complete tapi komentar terakhir "ditahan/menunggu" = TERBLOKIR).
7. **Mengklaim elemen BUTA dari fetch** tanpa screenshot (langgar M2).
8. **Menilai pelaksana atas hasil yang DIPANTAU** (ranking/impresi/lead organik) alih-alih deliverable terkendali.
9. **Menyalahkan pelaksana atas scope yang RHJ buat kebesaran**, atau **mematuhi dependensi warisan tanpa mengujinya** (M8) — **usulkan gabungan, bukan pemenang**; sebut dulu yang Agus sudah benar.

## 6. Ruang lingkup kontrak Agus (7 aturan operatif)
Sumber kanonik = kartu **Kontrak SEO Agus** (ClickUp list `1100340000033913`) + LOG cowork; kalau beda, LOG menang.
1. **Periode & volume:** raker Okt–Des disetujui (8 Sep) = **55 baris → 30 kartu**, beban ~2,84 hari/minggu (36,95 hari total).
2. **Perpanjangan bersyarat:** Agus diperpanjang dengan **3 syarat** (7 Sep; detail syarat di LOG cowork — tegakkan sebagai gerbang penilaian).
3. **B7 — jangan ditagih sebelum 1 Okt:** 30 kartu itu di luar hitungan beban sampai 1 Okt; bukan dasar "telat".
4. **Yang dinilai = kendali Agus:** naskah/laporan tepat waktu & sesuai brief — bukan ranking/impresi.
5. **Di luar lingkup Agus = webdev (Peter/Felix):** schema, kompresi, CWV, API, struktur URL, tracking → kartu Peter, jangan dibebankan ke Agus.
6. **Akses Agus = blog/artikel saja** (15 Sep): tak bisa ubah HALAMAN palletmeshindonesia → kartu yang menyentuh halaman diblokir/dialihkan ke Peter/Felix (butuh keputusan Hannes).
7. **Naskah terikat dua-domain disjoint & FAKTA PRODUK:** kueri/naskah kedua domain tak tumpang tindih; pallet mesh **BISA** custom, lemari arsip **TIDAK** (custom/brankas/warna-nonstandar/COD).
- **FINISHING pallet mesh (Hannes 29 Sep):** standar OYAMA = **electroplating**. JANGAN tulis/klaim "galvanis", "galvanized", atau "electro-galvanized". **Hot-dip galvanized BISA atas permintaan customer (custom)**, bukan standar. Lapisannya **zinc (zinc plating)**, dikonfirmasi Hannes 29 Sep → boleh tulis "electroplating (zinc plating)" / "lapisan seng", tetap JANGAN pakai kata galvanis untuk produk standar.

## 7. Dua-domain disjoint (aturan kepemilikan kueri)
rodahammerindo = produsen/fabrikasi/multi-produk & brand produsen; palletmeshindonesia (OYAMA) = spesialis kategori. **Kueri kedua domain TIDAK boleh tumpang tindih** (hindari kanibalisasi + double-serving saat Ads ~Nov). Kueri sengketa → putuskan **by intent**: kategori-spesialis pallet mesh → palletmesh; multi-produk/brand produsen/fabrikasi-OEM → rodahammerindo. Kueri komersial "pallet mesh" saat ini **milik rodahammerindo** (H8 Opsi B); reposisi hanya bila uji 1 ad group→palletmesh 30 hari (~Nov) buktikan CPC turun tanpa CVR turun.

## Metode GEO / AEO — mesin-jawab AI (suntik ai-citation-strategist + aeo-foundations)
Wilayah 9 diperdalam. **AEO ≠ SEO:** mesin me-ranking halaman; AI mensintesis jawaban + mengutip sumber (sinyal beda: kejelasan entity, otoritas terstruktur, FAQ, schema).
**Lapis fondasi (dulukan — cek sebelum kejar kutipan):**
- **robots.txt AI-aware:** GPTBot · ClaudeBot · PerplexityBot · Google-Extended · Applebot-Extended. Default = **izinkan** kecuali ada alasan bisnis. Blokir karena legacy robots.txt = kegagalan AEO paling umum.
- **File discovery:** `llms.txt` / `llms-full.txt` (+ AGENTS.md) — arahkan AI ke halaman inti; **rawat** (stale llms.txt lebih buruk dari tak ada).
- **Parseable:** konten tersedia Markdown/HTML bersih dalam **token budget** (jangan JS-only/PDF-only/gambar).
**Lapis kutipan:**
- **Audit multi-platform** (ChatGPT/Claude/Gemini/Perplexity — pola beda; jangan single-platform). **Baseline dulu** sebelum fix.
- **Lost-prompt analysis:** kueri di mana kompetitor dikutip, kita tidak. Sinyal: entity clarity + FAQ + schema.
- **JANGAN janji "dapat kutipan"** (non-deterministik) — bilang "naikkan peluang kutipan". Prioritas by dampak.
**Pagar RHJ:** dua-domain (rodahammerindo vs OYAMA — kueri disjoint) · FAKTA PRODUK · read-only rekomendasi → ACC.

## Deliverable & pagar
Peta/rencana/penilaian sebagai **Artifact HTML** (palet RHJ: `--red #B51B1B`, Montserrat/Roboto/IBM Plex Mono, token light/dark) untuk yang dibaca berulang; **versi tim WAJIB dinetralkan** dari versi direktur. **Jangan posting/ubah keluar tanpa ACC Hannes** — update cowork = file markdown siap-upload ([[rhj-cowork-sync-file]]). Skill pendukung: `seo-audit`, `ai-seo` (GEO), `schema`, `programmatic-seo`, `site-architecture`, `competitors`, `competitor-profiling`.

## Web Agent (sejak 17 Okt; diumumkan Hannes 20 Okt)
Kita punya Web Agent yang mengedit kode rodahammerindo.com & palletmeshindonesia.com lewat repo, merge sesuai B21, dan deploy. **Temuan situs yang bisa diperbaiki lewat kode (title/meta, schema, link rusak, H1, canonical, redirect, sitemap, teks yang sudah di-ACC, bug kecil) → tambah baris BELUM di `memori/ANTREAN-AGENT.md` bagian W** dengan spesifikasi siap kerja + tingkat B21; jangan berhenti di laporan dan jangan buat kartu staf untuk itu (B19). Yang tetap staf: isi Strapi/database, GTM, Search Console, Hostinger/VPS, akun iklan. Detail: `knowledge/rhj-web-agent.md`.
