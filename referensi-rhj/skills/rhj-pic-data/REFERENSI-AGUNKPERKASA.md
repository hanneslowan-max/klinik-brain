# Referensi: metode bedah akun kreator (kasus @agunkperkasa, 6 Okt 2026)

> **Metode umum terbaru + pelajaran dua akun (@agunkperkasa, @jazziesillona): `REFERENSI-BEDAH-AKUN.md`.** File ini tetap sebagai detail kasus pertama.

Dipakai pic-data saat Hannes atau agent lain meminta "bedah akun X, pelajari video teratasnya". Tugas pic-data: menyiapkan **dasar angka** supaya temuan agent konten (kreatif, scriptwriter, sosmed) bisa diuji, lalu men-challenge temuan itu. Kasus lengkap: `deliverables/riset-sosial/BEDAH-AGUNKPERKASA-06Okt/BEDAH-ANGKA-PICDATA.md`, skrip di folder `picdata-skrip/` yang sama.

## Langkah

1. **Tarik semua media akun, bukan hanya teratas.** Meta Business Discovery (`business_discovery.username(<akun>){followers_count,media_count,media{...}}`), paging lewat cursor `after` sampai kosong, dedup per id. Catat `media_count` vs jumlah yang terbaca (kasus ini: 586 vs 577).
2. **Saring dulu, baru hitung.** `view_count` hanya ada di `media_product_type=REELS`. Video FEED tidak punya views. **Jangan** menghitung median dari daftar "semua video" (kasus ini: angka brief 1.081 / p90 5.212 ternyata berasal dari 272 video dengan 68 video tanpa views; median reels yang benar 1.594, p90 6.545).
3. **Distribusi sebelum pola.** Hitung median, persentil p10–p99, rata-rata geometrik, Gini, HHI, porsi top-1/5/20, dan "berapa reel menyumbang 50/80/90% views". Kalau top-1 menyumbang ≥30% atau Gini ≥0,8, akun ini akun **ekor**: rata-rata tidak berarti, dan "20 teratas" sebagian besar sampel biasa.
4. **Klasifikasi dari caption dengan aturan tertulis** (modul regex, prioritas eksplisit, multi-label + topik utama). Pisahkan teks untuk topik (caption utuh + hashtag) dari teks untuk demo/tutorial (caption tanpa hashtag dan tanpa baris kredit tool). Simpan aturan sebagai file, beri versi.
5. **Audit klasifikasi**: sampel acak 30 (seed tertulis), nilai manual: benar / salah / ambigu. Perbaiki kamus, lalu audit ulang dengan seed BARU (audit di sampel yang sama = in-sample). Laporkan kedua angka.
6. **Median per kelompok + n + jumlah ≥10 rb.** Median dulu (tahan ekor), lalu Mann-Whitney sebagai deskriptif. Ulangi di dalam periode yang sama (kontrol waktu) dan silangkan topik × kolab.
7. **Tren waktu**: per bulan (n, median, maks, total, % topik pemicu), lalu efek pasca-viral dengan beberapa jendela (30/60/90 hari, semua, tanpa topik pemicu, tanpa top-20). Tandai reel berumur <14 hari.
8. **Sinyal craft di video teratas**: durasi, rata shot, potong per 10 dtk, `speech_pct`, kata/dtk, judul di 0,1 dtk, format isi (crop, bukan ukuran wadah). Spearman dengan log views + p permutasi, split ≥100 rb vs sisanya, Fisher untuk biner.
9. **Kelompok kontrol non-terseleksi**: bedah N reel TERBARU di luar top-20 dengan skrip yang sama. Ini satu-satunya cara memisahkan "ciri video meledak" dari "gaya akun".
10. **Tingkat bukti**: aturan / arah / jangan disimpulkan, dengan syarat yang membuat sebuah klaim naik kelas.

## Jebakan (wajib dicek)

| Jebakan | Gejala | Cara cek |
|---|---|---|
| **Survivorship** | Semua 20 teratas punya ciri X, lalu X dijadikan aturan | Bandingkan dengan kontrol non-top (langkah 9) dan dengan ciri X di seluruh akun. Kalau kontrol juga punya X, X = gaya akun, bukan pemicu |
| **Topik viral** | Video meledak karena tokoh/peristiwa, bukan craft | Bendera topik dari caption + bingkai 0 dtk; median per topik; silang craft × topik (judul di 0 dtk ikut tumpang dengan politik) |
| **Kolab/sponsor/boost** | Views besar dengan like/views <1% | Tandai ⚑ (ambang riset 29/9). Kasus ini: #8 164.692 views, like 0,05% |
| **Ekor satu video** | Rata-rata, total, atau "views per bulan" didominasi 1 reel | Selalu sertakan median dan versi "tanpa top-2" |
| **Wadah vs isi** | Video 16:9 diunggah dalam wadah 9:16 (letterbox) terhitung "vertikal" | Format dari crop bingkai hitam (`cropdetect`), bukan `w×h` file |
| **Pengacau waktu** | Pra/pasca viral dibanding tanpa melihat frekuensi posting dan hype tool | Jendela simetris + n per periode + median per bulan |
| **Umur video** | Reel baru (<14 hari) masih naik | Tandai dan jangan dipakai sebagai bukti "gagal" |
| **Kamus caption bolong** | Konteks politik ada di gambar, bukan caption (bendera One Piece, logo Badan Gizi Nasional) | Cek bingkai 0–1 dtk untuk top-20; tulis "caption-only" sebagai batas |
| **Angka orang lain** | Median/persentil di brief tidak cocok | Reproduksi angka brief dengan skrip; tulis lama dan baru berdampingan |

## Template tabel

**A. Distribusi**

| Ukuran | Nilai |
|---|---|
| n reels / total views / rentang tanggal | |
| p10 · p25 · median · p75 · p90 · p95 · p99 | |
| rata-rata · rata-rata geometrik · maks/median | |
| Gini · Gini tanpa top-2 · HHI (setara N reel) | |
| top-1 · top-5 · top-20 (% total) | |
| reel untuk 50% / 80% / 90% views | |

**B. Kelompok (topik utama / bendera / kolab)**

| Kelompok | n | median views | p25 | p75 | maks | n ≥10 rb | % total views |
|---|---|---|---|---|---|---|---|

**C. Craft video teratas + kontrol**

| # | kode | views | topik | dur | shot | rata shot | potong/10 dtk | ucapan % | kata/dtk | judul 0 dtk | format isi |
|---|---|---|---|---|---|---|---|---|---|---|---|

Ringkasan: median fitur ≥100 rb | sisa top-20 | kontrol; Spearman rho + p permutasi; Fisher untuk biner.

**D. Tingkat bukti**

| Klaim | Kelas (aturan / arah / jangan) | n | Dasar angka | Yang membuatnya naik kelas |
|---|---|---|---|---|

Syarat kelas: **aturan** = konsisten di seluruh akun (bukan hanya top-20), tahan kontrol waktu, n ≥20 per sisi, dan sejalan dengan riset RHJ sebelumnya. **Arah** = muncul di top-20 dan kontrol menunjukkan beda, tetapi n kecil atau ada pengacau. **Jangan disimpulkan** = hanya dari video terseleksi, n <10, atau tumpang-tindih penuh dengan topik/kolab.

## Checklist cepat (pakai saat challenge laporan agent konten)

- [ ] Angka views/median di laporan cocok dengan skrip (reels saja, bukan semua video)?
- [ ] Setiap "pola video meledak" disertai n/20 DAN pembanding (kontrol atau sisa top-20)?
- [ ] Pola itu dicek terhadap topik pemicu (politik/tokoh publik) dan ⚑ like/views <1%?
- [ ] Format dibaca dari isi (crop), bukan ukuran file?
- [ ] Batas metode ditulis: agent tidak mendengar audio, Whisper bisa salah, potongan shot otomatis?
- [ ] Klaim yang dijadikan aturan konten Lastri lolos syarat kelas "aturan" di tabel D?
- [ ] Pola dari video demo tool atau tokoh publik tidak dijadikan aturan Lastri tanpa alasan pagar?

## Skrip yang bisa dipakai ulang

`deliverables/riset-sosial/BEDAH-AGUNKPERKASA-06Okt/picdata-skrip/`: `aturan_klasifikasi.py` (ganti kamus per akun), `analisa_angka.py` (distribusi, kelompok, tren, craft, kontrol), `audit_klasifikasi.py <seed>`, `kontrol_ringkas.py <folder_bedah>`. Bedah video (shot, audio, Whisper) memakai `bedah.py` + `recut.py` di scratchpad sesi (crop bingkai hitam, ambang scene 0,18).
