# Referensi: metode bedah akun kreator (umum) + pelajaran dua akun

Dipakai pic-data saat Hannes atau agent lain meminta "bedah akun X, pelajari video teratasnya". Tugas pic-data: menyiapkan **dasar angka** supaya temuan agent konten (kreatif, scriptwriter, sosmed) bisa diuji, lalu men-challenge temuan itu di putaran 2.

Kasus yang sudah dikerjakan (baca laporan dan skripnya sebelum mulai, salin skrip lalu ganti kamus):
| Akun | Tanggal | Laporan | Skrip |
|---|---|---|---|
| @agunkperkasa (film AI, ID, 5,5 rb follower) | 6 Okt 2026 | `deliverables/riset-sosial/BEDAH-AGUNKPERKASA-06Okt/BEDAH-ANGKA-PICDATA.md` + `CHALLENGE-PICDATA-PUTARAN2.md` | `.../BEDAH-AGUNKPERKASA-06Okt/picdata-skrip/` |
| @jazziesillona (rekaman HP asli, HK, 643 rb follower) | 6 Okt 2026 | `deliverables/riset-sosial/BEDAH-JAZZIESILLONA-06Okt/BEDAH-ANGKA-PICDATA.md` + `CHALLENGE-PICDATA-PUTARAN2.md` (44 klaim: 34 lolos, 7 turun, 3 gugur) | `.../BEDAH-JAZZIESILLONA-06Okt/picdata-skrip/` |

Detail kasus pertama tetap di `REFERENSI-AGUNKPERKASA.md`. File ini = metode umum yang sudah diuji di dua akun.

## Langkah

1. **Tarik semua media**, bukan hanya teratas (Meta Business Discovery, paging `after`, dedup id). Catat `media_count` vs terbaca dan jumlah `like_count` tersembunyi (jazzie: 11 reel).
2. **Saring REELS saja.** `view_count` hanya ada di `media_product_type=REELS`. Reproduksi setiap angka brief dengan skrip dan tulis lama/baru berdampingan. Persentil: pakai `numpy` linear dan sebut metodenya (brief jazzie p90 986.667 = metode *higher*; linear 982.473).
3. **Distribusi sebelum pola**: median, p10–p99, rata-rata geometrik, Gini (+ tanpa top-1/top-2), HHI, top-1/5/10/20, reel untuk 50/80/90%, median/follower, ambang top-20 (× median dan persentil peringkat).
4. **⚑ boost SEBELUM membaca top-k.** Hitung like/views, ambang absolut <0,5% dan <1%, dan lihat juga relatif terhadap median akun (jazzie 4,90%, agunk 1,65%). Cek arah like/views vs views di reel non-⚑ (jazzie rho +0,34: reel organik besar justru like tinggi, jadi like rendah pada views jutaan = anomali). Tabel "pengaruh ⚑": total, median, Gini, top-1/5/20 untuk semua / tanpa ⚑ / tanpa #1 / tanpa ⚑ dan kolab.
5. **Era/umur dipisah dari topik.** Tabel per kuartal (n, reels/minggu, median, p75, maks, % total, like/views, komposisi kelas, ⚑). Lalu OLS log10(views) ~ kelas, tanpa dan dengan efek tetap kuartal, CI bootstrap; plus rasio median kelas vs kelas rujukan **di dalam tahun yang sama**. Laporkan R² kuartal saja vs tambahan dari kelas.
6. **Klasifikasi caption dengan aturan tertulis** (modul berversi, prioritas eksplisit, multi-label + kelas utama). Pisahkan teks: (a) bio standar yang menyebut semua seri, (b) hashtag, (c) baris mention, (d) baris lokasi, (e) **baris kredit** (alat, preset, kamera). Topik dibaca dari teks utama saja. Kredit (tool/produk) dihitung sebagai bendera terpisah.
7. **Audit**: 30 sampel acak per seed, nilai benar/salah/ambigu, perbaiki kamus, audit lagi dengan seed baru. Laporkan angka di luar sampel perbaikan (agunk 80%, jazzie 92% dari 90).
8. **Uji beda**: median + n + p25/p75 + n ≥ambang + % total; MWU punya vs tidak dengan **Holm** untuk banyak bendera; Kruskal-Wallis lintas kelas. Median dulu, p sebagai deskriptif.
9. **Halo & unggah ulang**: jendela simetris 30/60/90 hari di sekitar tiap viral besar (keluarkan reel viral dan reel <14 hari). Pasangan unggah ulang: caption baris-1 sama + pasangan manual dari frame.
10. **Craft top-20 + kontrol** dengan skrip bedah yang sama: durasi, shot (crop, ambang 0,18), rata/median shot, potong/10 dtk, ucapan %, kata/dtk, format isi dari crop. Judul di 0,0/0,1/1,0 dtk, teks layar, jenis huruf judul **dibaca manual** dari lembar frame (`frame_sheet.py`) dan disimpan sebagai JSON berdefinisi.
11. **Kontrol non-terseleksi** wajib sebelum menyebut ciri craft sebagai pemicu. Dua desain yang sudah dipakai: 9 reel terbaru non-top (agunk) dan 9 reel terbaru di kisaran 0,5–2× median (jazzie, lebih bersih karena views sepadan dengan median). Kalau kontrol belum lengkap: tulis "v1", sebut kode yang kurang, tandai semua klaim craft "belum ada kontrol".
12. **Perbandingan lintas akun** (tabel pola × akun × status: sama / khas / berlawanan) lalu **tingkat bukti A/B/C**.

## Jebakan (wajib dicek)

| Jebakan | Gejala | Cara cek | Kasus |
|---|---|---|---|
| Survivorship | Semua top-20 punya ciri X | Kontrol + ciri X di seluruh akun | jazzie top-20 = 3,3% teratas (≥12,4× median) |
| Topik pemicu | Meledak karena tokoh/peristiwa | Bendera topik, median per topik, silang craft × topik | agunk politik 83,8% views |
| ⚑ boost / iklan | Views jutaan, like/views ≪ median akun | ⚑ dua ambang + tabel pengaruh top-k + Ad Library | jazzie #1 0,008% = 16,2% total; agunk #8 0,05% |
| ⚑ di corong toko kreator | Like rendah di posting jualan sendiri | ⚑ per kelas | jazzie 3/4 ⚑ non-#1 = tutorial seri corong preset; agunk ⚑ terbanyak di demo tool |
| Era akun | Reel lama tampak "lebih bagus" | Efek tetap kuartal; median per tahun | jazzie kuartal R² 0,124 vs kelas +0,033 |
| Bio/kredit di caption | Semua reel baru terbaca "produk"/"tutorial" | Potong bio, pisah baris kredit | jazzie: bio menyebut semua seri; "colorgraded with Day Star" di tiap caption |
| Nama tempat = kata umum | "Cat Street", "a nice sunset" | Kamus pengecualian + audit | jazzie v1 → v1.2 |
| Tag akun ≠ merek | Handle orang/kafe terbaca sponsor | Tingkat "tag akun" terpisah dari "sponsor/kolab" | jazzie v1.1 |
| Teks di gambar, bukan caption | Tutorial/politik hanya di layar | Baca frame 0–1 dtk top-20 | jazzie #16 "How To" di layar; agunk #14 bendera One Piece |
| Wadah vs isi | Letterbox / pita bertumpuk dihitung vertikal | Crop + lihat frame | jazzie #17 tiga pita 16:9 dalam 9:16 |
| Lirik = ucapan | `speech_pct` tinggi tanpa VO | Baca transkrip + `lang` | jazzie #2 lirik Turki 54% |
| Unggah ulang | Footage sama muncul dua kali di top | Durasi + jumlah shot + frame sama | jazzie #4 dan #7 (flicker 2023/2025) |
| Umur <14 hari | Reel baru dianggap gagal | Tandai | 2 dari 9 kontrol jazzie berumur 12–13 hari |
| Rate-limit unduhan | Bedah tidak lengkap saat menulis | Skrip membaca folder data apa adanya; status v1 di kepala laporan | jazzie v1: 19/20 + 0/9; v2: 20/20 + 9/9 |

## Pelajaran dua akun (6 Okt 2026)

**Muncul di dua akun (kandidat aturan):**
1. Ringkas dengan median + top-k **sesudah buang ⚑**. Satu reel bisa memegang 16–50% total views (jazzie #1 ⚑ iklan 16,2%; agunk #1 politik organik 50,3%, ⚑ #8 terpisah).
2. **Tidak ada halo** sesudah viral: agunk 60 hari 0,48×; jazzie (#2) 0,41×, (#1) ±1×.
3. **Sponsor/kolab tidak mengangkat median**: agunk 1.507 vs 1.919; jazzie 0,84× (0,85× setelah kontrol kuartal).
4. **⚑ mengumpul di posting yang menjual barang kreator sendiri** (demo tool / tutorial corong preset). Arah, belum aturan.
5. Video teratas **lebih pendek dari reel biasa**: agunk 28,8 vs kontrol 129,5 dtk; jazzie 15,2 vs 27,1 dtk (p=0,003; kota saja 10,1 vs 27,1, p=0,002). Di dua akun kontrol berasal dari era lain, jadi tetap arah (B).
5b. **Potong cepat bukan pemicu**: agunk rata shot sama di 3 kelompok; jazzie top 2,51 dtk vs kontrol 1,91 dtk (top tidak lebih cepat, p=0,52).
6. Median reels ≈ **0,29× follower** di dua akun yang ukurannya beda 100×. Catat sebagai patokan kasar; perlu akun ke-3.

**Gugur sesudah kontrol (pelajaran utama v2 jazzie):** judul/premis ≤1 dtk, teks layar, huruf serif, dan tanpa VO ada di 18/19 top **dan** 8/9–9/9 kontrol. Di agunk judul 0 dtk adalah pembeda (kontrol 0/9); di jazzie itu standar produksi. Jadi ciri yang sama di top dua akun belum tentu pemicu di keduanya. Kontrol per akun wajib.

**Khas satu akun (jangan digeneralisasi):** pemicu topik (agunk politik; jazzie tutorial HP + kota/kucing), bentuk distribusi (ekor vs badan tebal), seri (part menyusut 0,80× vs seri format Five Simple Shots 4,2× median), unggah ulang (agunk 2,4× hari sama; jazzie median 0,14×), color grading.

**Berlawanan:** demo/tutorial. Demo tool AI agunk tidak naik; tutorial HP jazzie naik 1,57× di 4 tahun. Riset B2B RHJ 27/9: edukasi produk pabrik kalah. Bedanya kemungkinan "penonton bisa langsung mempraktikkan dengan alat yang dipegang" vs "pamer hasil/produk". Jangan jadikan aturan RHJ tanpa uji di akun sendiri.

## Template tabel

**A. Distribusi** (kolom tambahan: pembanding akun sebelumnya)

| Ukuran | Akun ini | Akun pembanding |
|---|---|---|
| n reels / total / rentang / FEED tanpa views / like tersembunyi | | |
| p10 · p25 · median · p75 · p90 · p95 · p99 (metode persentil) | | |
| median / follower | | |
| Gini · tanpa top-1 · tanpa top-2 · HHI | | |
| top-1 · top-5 · top-20 · reel untuk 50/80/90% | | |
| ambang top-20 (× median, persentil peringkat) | | |

**B. ⚑ dan pengaruhnya**: daftar ⚑ per ambang + tabel himpunan (semua / tanpa ⚑ / tanpa #1 / tanpa ⚑ dan kolab) × (n, total, median, Gini, top-1, top-5, top-20).

**C. Era**: kuartal × (n, reels/minggu, median, p75, maks, % total, like/views, % kelas, ⚑) + OLS kelas tanpa/dengan kuartal + rasio kelas di dalam tahun.

**D. Kelompok**: kelas utama, bendera (Holm), kolab, kota/topik, seri.

**E. Craft**: top-20 + kontrol; kolom judul 0,1 dtk / ≤1 dtk / huruf judul / format isi dari crop.

**F. Dua akun**: pola × akun A × akun B × status (sama / khas / berlawanan).

**G. Tingkat bukti**

| Klaim | Kelas (A aturan / B arah / C jangan) | n | Dasar angka | Yang membuatnya naik kelas |
|---|---|---|---|---|

Syarat kelas: **A** = konsisten di seluruh akun (bukan hanya top-20), tahan kontrol waktu, n ≥20 per sisi, sejalan riset RHJ sebelumnya (atau sama di ≥2 akun). **B** = beda terlihat, tetapi n kecil, kontrol belum ada, ada pengacau, atau berlawanan dengan riset RHJ. **C** = hanya dari video terseleksi, n <10, ⚑, atau tumpang penuh dengan topik/kolab.

## Checklist challenge putaran 2

- [ ] Angka views/median di laporan agent cocok dengan skrip (REELS saja, metode persentil disebut)?
- [ ] Contoh video di laporan bukan reel ⚑ (cek daftar ⚑ dua ambang)?
- [ ] Setiap "pola video meledak" disertai n/20 DAN pembanding (kontrol / sisa top-20 / seluruh akun)?
- [ ] Pola dicek terhadap era (tahun/kuartal) dan topik pemicu?
- [ ] Ciri yang ternyata sama di kontrol ditulis sebagai **gaya akun**, bukan pemicu?
- [ ] Format dari isi (crop/frame), bukan ukuran file; unggah ulang tidak dihitung dua kali sebagai bukti?
- [ ] Batas metode ditulis: agent tidak mendengar, Whisper bisa salah (lirik), shot otomatis?
- [ ] Klaim yang dijadikan aturan Lastri/iklan lolos kelas A, atau ditulis sebagai uji (B)?
- [ ] Pola yang berlawanan dengan riset RHJ sebelumnya (mis. edukasi B2B) disebut terang?
- [ ] Laporan v1 (kontrol belum lengkap) tidak dipakai untuk menaikkan klaim craft ke A?
- [ ] Bila kontrol bertambah sesudah agent menulis (jazzie: 7 → 9), hitung ulang tiap proporsi dan tulis lama/baru berdampingan; ukur kontrol baru dengan alat agent sendiri dan ukur ulang satu kontrol lama untuk cek reproduksi.
- [ ] Bukti "penanda kolab/iklan" tidak memakai reel ⚑ (jazzie: burst "kolab 3/4" bertumpu pada #1 ⚑; tanpa ⚑ 2/5).
- [ ] Tafsir pagar teknis dicek ke LOG-PAGAR terbaru, termasuk di REFERENSI lama (jazzie: true peak "> −1 dBTP = TAHAN" sudah ditegaskan, tetapi dua file sosmed masih menulis ">0").
- [ ] Tally verdict (lolos/turun/gugur + angka dikoreksi) dihitung skrip dari tabel klaim, bukan dihitung tangan.

## Skrip yang bisa dipakai ulang (versi jazzie = paling baru)

`deliverables/riset-sosial/BEDAH-JAZZIESILLONA-06Okt/picdata-skrip/`:
- `aturan_klasifikasi.py` (v1.2): pola potong bio + baris kredit + baris mention; ganti kamus per akun.
- `analisa_angka.py`: distribusi, ⚑ + pengaruh top-k, kuartal + OLS kuartal, kelas/bendera Holm/kolab/kota/seri, halo, unggah ulang, craft top-20 vs kontrol (membaca `data/NN_*.json` dan `data/K_*.json` apa adanya, jadi aman dijalankan ulang saat unduhan bertambah).
- `audit_klasifikasi.py <seed>`, `frame_sheet.py <vids> <out> <kode...>`, `frame_manual.json` (definisi judul 0,1 dtk dan VO di dalam file), `challenge_putaran2.py` (hitung ulang klaim agent + tally verdict).
Bedah video (shot, audio, Whisper) memakai `bedah.py` + `recut.py` di scratchpad sesi (crop bingkai hitam, ambang scene 0,18).
