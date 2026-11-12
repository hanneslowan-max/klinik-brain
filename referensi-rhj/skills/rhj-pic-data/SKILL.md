---
name: rhj-pic-data
description: Playbook Analis Data/RevOps RHJ — satu sumber kebenaran angka, silang pipeline↔Ads↔omzet, atribusi, margin. Menyandar ke rhj-cek-data-mendalam. Dipakai agent pic-data. Bahasa Indonesia.
---

# Playbook Analis Data / RevOps RHJ

Menjaga semua orang & agent jujur dengan data — dari klik sampai order. Bahasa: Indonesia.

**🧠 Loop belajar (wajib):** di AWAL, baca `rhj-routines/memori/PELAJARAN-PIC.md` (bagian disiplinmu) — hindari ulang kesalahan/analisa. Di AKHIR, **append 1 entri** tiap ketemu masalah↔solusi baru / koreksi asumsi (`Tanggal · Masalah · Gejala · Diagnosis · Solusi · Prinsip`). Append-only.

## Metode uji ada di skill lain — pakai itu
Untuk metode uji angka & format deliverable: **INVOKE `rhj-cek-data-mendalam`**. Skill ini menambah fokus RevOps + pagar silang-corong.

## LANGKAH 0 — Baca pagar
[[rhj-pagar-inti]] (G1–G8, P1–P4, M1–M11), [[rhj-bisnis-inti]], [[rhj-clickup-workspace]].

## Yang masih rusak & jadi fokus
- **Atribusi belum beres:** konversi Ads vs lead pipeline pernah 1,80:1 (Jul) lalu berbalik 0,89:1 (Agt); pipeline tak punya kolom Sumber. Tracking timpang: Ads 5 konversi FC vs 19 lead nyata (3,8×).
- **Margin per kategori tak diketahui** — membatasi presisi sizing (plafon CPA, prioritas). Angkat sebagai gap, jangan tebak.
- **Nilai lead pallet mesh Rp4,5 jt (n=18) rapuh** — plafon CPA mode-volume bertumpu padanya.

## Pagar data (patuh MUTLAK)
- **M1:** hitung DULU baru sebut angka (rekam jejak salah hitung berkali-kali). **M11:** sebelum usul cap CPC, cek CPC keyword yang benar-benar konversi.
- **G7:** export float polos, Impr. share pecahan 0–1, cek repr sebelum parse. **G8:** baca ADS_PERUBAHAN tiap analisa.
- **P1:** Item pipeline salah tag ±25% (cek Remark/Respon). **P3:** Status jarang update. **P4:** sampai kolom N.

## Sumber & waktu
Ads dari Robot G (Sheet **12laQyIoaprz8NXvOXUNYSLoQai3sX9vDyxaXXJNWWBc**) — **baca jam 8 pagi WIB+**. Pipeline: Sheet Customer Pipeline (**1o-KEweLNVOg7c550DPZ_g0sCFqoCjQvcxztcK4gMdoU**) / ERP-Supabase. SEO Task List **1LEsrynVkAWDjf7UEH1dHr1fOXvZPckOsxNptp8O0rm0**. Parse NODE (xlsx), jangan read_file_content (terpotong). **[Saklar 12 Okt]** Sesudah hari pindah (`routines/cloud/PIPELINE-SUMBER.md` = `SUMBER: ANVIL`), sumber data pipeline = **Anvil** lewat `node tools/tugas.mjs pipeline list|get|summary` (READ-ONLY); sheet di atas hanya riwayat sebelum tanggal pindah.

## Alur kerja
1. **Silang corong:** klik → konversi Ads → lead pipeline → SP/order; tandai di mana angka tak nyambung. 2. Verifikasi klaim angka (agent lain/vendor) vs sumber. 3. Koreksi eksplisit bila angka lama salah (sebut lama & baru berdampingan). 4. **Jangan ubah data/akun** — hanya analisa & verifikasi; sajikan angka yang bisa dilacak ke sumber + gap yang belum bisa dijawab.

## Metode Measurement & Atribusi (suntik tracking-specialist + search-query-analyst)
- **Silang 3 arah WAJIB:** konversi platform (Ads) vs API/DebugView vs CRM/pipeline (order nyata). Diskrepansi >5% = alarm (bidding bisa salah arah). Ini yang membongkar **FC 8 konv / 10 lead / 0 order**.
- **Dedup:** cek Pixel vs CAPI (`event_id`) jangan dobel hitung.
- **Offline conversion:** rantai GCLID → order (kalau dipasang) buktikan lead→sale. INGAT: konversi Ads = **LEAD, bukan penjualan** — jangan sebut "penjualan".
- **Query-data:** n-gram search-term (modifier boros berulang) + **spend-weighted irrelevance scoring** (bukan cuma zero-conv).
- **Pagar:** read-only + ATURAN NOL (M1). Rekomendasi → ACC.

## Deliverable
Temuan + angka terlacak + daftar gap (jangan tebak). Skill: `rhj-cek-data-mendalam`, `attribution`, `analytics`.

## Membuka link Instagram yang dikirim Hannes (WAJIB cara ini — 20 Okt)
Hannes cukup kirim link reel; jangan minta screenshot/rekam layar. Urutan:
1. **Video:** `python3 -I tools/ig-reel.py <link> <scratchpad>/ig` → mp4 + caption/angka. Lalu `bedah.py` (frame, buka PER-DETIK.jpg) + `dengar.py` (transkrip). Detail & jebakan di `tools/README.md` (ig-reel.py).
2. **Caption & angka banyak post satu akun:** Graph API Business Discovery `business_discovery.username(<akun>){media{caption,permalink,like_count,comments_count,timestamp}}` (token META_ACCESS_TOKEN). Tidak memberi file video reel.
3. Jangan: yt-dlp/halaman reel langsung (429 dari cloud), UA Chrome desktop di embed (halaman kosong), minta login/cookie IG, situs pengunduh pihak ketiga.

## Bedah akun kreator / referensi konten (6 Okt: @agunkperkasa, @jazziesillona)
Saat agent konten membedah "video teratas" sebuah akun, pic-data menyiapkan dasar angka lalu men-challenge temuan mereka. Metode umum, jebakan, template tabel, checklist putaran 2, dan pelajaran dua akun: **`REFERENSI-BEDAH-AKUN.md`** (folder skill ini; baca ini dulu). Detail kasus pertama: `REFERENSI-AGUNKPERKASA.md`. Inti:
- Hitung distribusi SEMUA reels dulu (median, Gini, porsi top-1/5/20, median/follower). Views hanya ada di REELS; sebut metode persentil.
- **Cek ⚑ like/views sebelum membaca top-k** (dua ambang + tabel pengaruh). Satu reel bisa memegang 16–50% total views (jazzie: reel ⚑ iklan 16,2%; agunk: reel politik organik 50,3%).
- **Pisahkan era dari topik** (median per kuartal/tahun, OLS dengan efek tetap kuartal, rasio di dalam tahun yang sama).
- Klasifikasi caption dengan aturan tertulis: potong bio standar + baris kredit + mention dulu; audit 30 sampel, perbaiki, audit seed baru.
- Video teratas = sampel terseleksi. Bandingkan dengan **kontrol non-top** (kisaran 0,5–2× median lebih bersih) sebelum menyebut ciri sebagai "pemicu". Kontrol belum lengkap → laporan "v1".
- Tutup dengan perbandingan lintas akun (sama / khas / berlawanan) dan tingkat bukti A/B/C.

## QA prompt video (DRAF — uji A/B 9 Okt: TIDAK TERBEDAKAN, bukan standar) — 9 Okt
**Uji A/B 9/10 (12 klip, 1 penilai buta): A 1 · B 0 · seri 5 → rubrik tidak terbukti memperbaiki hasil (`deliverables/riset-sosial/BELAJAR-PROMPT-MIXX-09Okt/UJI-AB/HASIL-UJI-AB.md`).**
**Hannes 9/10: "Ini belum teruji jadi jangan disimpan menjadi standar untuk kita prompting. Ini harus diuji dulu sebelum kita meloloskannya."** Rubrik di bawah TIDAK dipakai untuk meluluskan/menolak prompt, TIDAK masuk templat brief atau skill pic-kreatif/pic-produksi-video, dan skornya hanya catatan. Statusnya naik hanya sesudah uji generate (rubrik tinggi vs rendah pada shot yang sama, hasil dinilai buta) + ACC Hannes.
Saat diminta mengecek prompt video pic-kreatif (Lampiran prompt brief) atau pic-produksi-video (prompt yang dikirim): pakai rubrik v1 di **`REFERENSI-QA-PROMPT-VIDEO.md`** (folder skill ini). Asal: 80 prompt @ai_studio_mixx ditranskripsi dan dibedah (`deliverables/riset-sosial/BELAJAR-PROMPT-MIXX-09Okt/`). Inti:
- Nilai prompt **yang dikirim**: tarik dari log; bila log hanya label (PM-06/PM-07), baca job Higgsfield (`show_generation_by_ids`, 0 kredit). Bandingkan dengan Lampiran brief (info yang hilang = butir S5).
- 8 butir wajib (format/parameter, subjek-identitas, aksi-waktu, kamera, cahaya, suara, **pagar RHJ 0/2 mutlak**, jejak) + 5 butir sebaiknya; maks 21; LOLOS ≥15 dengan pagar = 2 dan semua wajib ≥1. Penilaian satu orang sampai kappa dua penilai ≥0,6.
- Tentukan mode dulu: klip per shot dari start image (prompt pendek wajar, 30–90 kata) vs multi-shot satu prompt (struktur mixx: Format → Continuity → Tone → larangan → beat bertimecode 1–3 dtk; ±20–45 kata/dtk).
- Larangan di prompt tidak menjamin hasil (mixx: huruf/logo bermasalah 3 dari 13 walau 90% prompt melarang); pagar tetap dicek di hasil (aturan 6). Jangan tiru: label/logo dibuat AI, wajah tokoh nyata, IP, merek nyata, stunt.
- Kalibrasi pertama (PM-07 terkirim rata-rata 16,4; RD-01 18; perbaikan utama: simpan teks prompt di log, bawa cahaya B3b, "No music, no voices", jangan buang kunci brief) di `KALIBRASI-PROMPT-RHJ.md`.

## Alur riset iklan (B12, wajib — Hannes 1 Okt)
Setiap permintaan riset untuk ads: (1) pic-data riset iklan pemenang · (2) pic-ads pilih produk yang di-boost (paralel dengan 1) · (3) pic-kreatif + pic-scriptwriter tulis brief · (4) approval CMO · (5) sajikan ke Hannes. Detail `memori/LOG-PAGAR.md` B12. Jangan lompati tahap.

## Rubrik review naskah v2 (usulan, menunggu ACC Hannes) — 6 Okt
Asal: usulan pic-scriptwriter (`PLAYBOOK-GENRE.md` §9) + challenge pic-data (`deliverables/riset-sosial/BELAJAR-SCRIPTWRITER-06Okt/CHALLENGE-PICDATA.md` §5). **Belum berlaku.** Sampai ACC, review tetap memakai skala lucu 1–5, dengan catatan bahwa naskah H/I tidak dinilai dari skala itu saja.

**Kolom per naskah**
| Kolom | Skala | Cara isi | Dipakai untuk |
|---|---|---|---|
| Genre target | K / I / H / campuran (`K → H di beat X`) | dari kepala naskah | menentukan kolom mana yang dibaca |
| Lucu | 1–5 | jangkar tertulis (1 tidak ada kejutan · 3 senyum, punch terbaca tanpa suara · 5 dikutip/dikirim) | K dan campuran; tidak untuk menolak naskah H/I murni |
| Haru | 1–5 | jangkar (1 tidak terasa · 3 hangat, pengorbanan terlihat · 5 ingin disimpan/dikirim) | H dan campuran |
| Inspirasi | 1–5 | jangkar (1 tidak terasa · 3 bangga, hambatan nyata terlihat · 5 "aku mau begitu") | I dan campuran |
| Emosi target tercapai | ya / sebagian / tidak | dibaca terhadap genre target | review |
| Siapa berubah terbaca tanpa suara | ya / tidak | dari tabel beat + teks layar | review |
| Ruang napas sesudah puncak | dtk, **dihitung** dari tabel beat (sesudah render: segmen tanpa ucapan) | angka | H/I; ≥3 dtk = usulan uji, bukan aturan |
| Nada kesal | ada / tidak | aturan tertulis + pindai "!" dan kata | semua genre (anti-pola KUAT) |
| Kalimat moral sebagai baris terakhir | ada / tidak | baris terakhir dialog/teks | semua genre (G19) |
| Pagar genre | lolos / tidak | lapar/miskin, klaim mutu mutlak, APD semua tokoh, Lastri penuntas lewat tindakan | semua genre |

**Syarat sebelum skor 1–5 dipakai memutus naskah:** dua penilai (pic-data + pic-kreatif) menilai terpisah 10 naskah pertama; kappa berbobot ≥0,6 per kolom. Di bawah itu skor = pendapat, ditulis "penilaian satu orang".

**Baca sesudah tayang (≥48 jam, simpan% dan share% per views vs median akun sendiri):**
- Median akun Lastri baru dipakai sesudah ±20 video (presisi ±1,5× simpan, ±1,7× share; `min_n.py`). Sebelum itu tulis "belum ada dasar".
- **Minimum per genre** sebelum menyebut temuan (alpha 0,05, power 0,8; SD per video dari DB-VIRAL dalam akun): efek 2× → **±10 video (simpan), ±15 (share)**; efek 1,5× → 27 (simpan), 42 (share); H vs K langsung, efek 2× → 19–29 per kelompok. Uji tanda: "≥10 dari 12 di atas median" atau "≥15 dari 20".
- **Satu video tidak dibaca sebagai bukti genre** (variasi biasa ÷4,3–×4,3 simpan, ÷6,2–×6,2 share). Uji "sisi hangat" 1 video = uji eksekusi + kode komentar (aturan tertulis; 😭 sering untuk tawa).
- Genre diselang di minggu yang sama (pisahkan efek umur akun). Hitung ulang SD dengan data Lastri sesudah ±20 video.
