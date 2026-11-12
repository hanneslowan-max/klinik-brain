# JANGKAR & DATA HASIL — supaya penilaian bisa dibandingkan dan dikoreksi (14 Okt 2026)

Menilai satu video tanpa pembanding = berisik. Setiap penilaian WAJIB menyebut ≥2 video jangkar dan menempatkan video yang dinilai relatif terhadapnya ("hook lebih lemah dari X karena ...", "cerita sejelas Y").

## 1. Kolam jangkar (pilih yang paling mirip format/genre)

**A. Akun Bu Lastri sendiri — jangkar UTAMA begitu ada data.**
- Sumber: tabel "Angka per video" di `memori/SOSMED-MEMORI.md` + `memori/PENILAIAN-VIDEO-LOG.md`.
- Status 14/10: belum ada video tayang di IG (`node tools/meta.mjs ig-media` = kosong), jadi kolam A belum bisa dipakai.
- Begitu ≥5 video punya angka 48 jam: tetapkan 3 jangkar = terbaik, tengah (median), terburuk. Perbarui tiap 5 video baru.
- Tingkat viral dibaca relatif ke median akun sendiri: RENDAH < median · SEDANG = median s/d 3× median · TINGGI > 3× median. Sebelum kolam A ada, tingkat viral = penilaian kualitatif dan WAJIB ditulis "belum ada basis angka akun".

**B. Video pendek AI Indonesia (format & kemasan).**
- `deliverables/riset-sosial/BEDAH-AGUNKPERKASA-06Okt/` (204 reels; median 1.594, p90 6.545; tabel 20 teratas + bedah per video).
- JANGAN pakai sebagai jangkar viral: video yang naik karena tokoh publik/politik/MBG/IP berhak cipta (#1, #2, #3, #5, dll.; lihat kolom catatan). RHJ tidak memakai itu, jadi perbandingannya tidak adil.
- `deliverables/riset-sosial/BEDAH-JAZZIESILLONA-06Okt/` (akun konsisten tinggi; pakai untuk kemasan teks & ritme, bukan target angka).

**C. Humor kerja / sitkom pendek (cerita & timing).**
- `deliverables/swipe-file-kreatif/`: `2026-10-04-whites-sitkom`, `2026-10-05-brooklyn99-parsel`, `2026-10-05-corporatenatalie-tagihan`, `2026-10-04-lolita-meme-kerja`, `2026-10-05-mamazohara-*`, `2026-10-03-dipa-utomo` (+ `SWIPE-FILE.md`, `BELAJAR-PER-PIC.md`).
- Pakai untuk: setup → punchline → reaksi, panjang jeda, cara karakter "deadpan".

**D. Iklan industri / B2B (kelayakan iklan).**
- `deliverables/riset-sosial/RISET-ADS-INDUSTRI-CATCONSTRUCTION-29Sep.md`, `RISET-ADS-AI-SINEMATIK-PESOCHNITSA-29Sep.md`, dan swipe-file `2026-10-04-hornbach-just-a-board`, `2026-10-05-toast-built-for-busy`, `2026-10-04-motilal-spesialis`.

Aturan pakai: jangkar = alat ukur relatif, BUKAN template yang harus ditiru. Video Hannes boleh berbeda format; yang dibandingkan hanya hook, kejelasan cerita, timing humor, kealamian dialog, kelayakan iklan.

## 2. Data hasil nyata (bahan kalibrasi)

Organik (diisi pada 48 jam dan 7 hari):
- IG: `node tools/meta.mjs ig-report` → views, reach, share, simpan, rata-rata waktu tonton (`avg_watch_time_dtk`). **% ditonton = avg_watch_time_dtk / durasi video.**
- TikTok: belum ada API; ambil dari `memori/SOSMED-MEMORI.md` (diisi pic-sosmed/Rengga). Kosong → tulis "TikTok: belum ada angka".

Iklan Meta (bila video dipakai iklan; `node tools/meta.mjs ads-insights --level ad --since <tgl> --until <tgl>`):
- **Hook rate = putar 3 detik / impresi.** Putar 3 detik = `action_type: "video_view"` di `actions_mentah`.
- **Hold rate = thruplay / putar 3 detik.**
- Biaya per chat WA (`biaya_per_chat_wa`) = ukuran akhir; hook/hold = ukuran kreatif.
- Patokan awal: belum ada data iklan video RHJ. Sampai ada ≥5 iklan video dengan ≥1.000 impresi masing-masing, bandingkan antar-varian saja (A vs B), jangan dengan angka "umum" dari internet.

## 3. Membaca hasil vs prediksi
- Isi kolom hasil nyata di `memori/PENILAIAN-VIDEO-LOG.md` untuk semua video lama yang sudah lewat 48 jam/7 hari sebelum menilai video baru.
- Meleset jauh (prediksi TINGGI tapi < median, atau RENDAH tapi > 3× median; LAYAK IKLAN tapi hook rate terendah di antara varian) → tulis 1 kalimat pelajaran: kompetensi mana yang salah baca (hook? humor? cacat AI?).
- Setelah ≥10 video: hitung berapa vonis yang tepat arah. Ambang di `dengar.py` (nada datar, cepat, ketimpa latar) disetel ulang bila tandanya tidak berhubungan dengan hasil.
