---
name: rhj-penilai-video
description: Kompetensi penilai video independen RHJ — menilai video jadi dari sudut PENONTON dan PEMBELI, tanpa brief: potensi viral, layak jadi kreatif iklan (+ rencana versi iklan), humor sampai atau tidak, cerita dipahami atau tidak, dialog/naskah kaku; mengukur suara (dengar.py), cek cacat AI & konsistensi tokoh (lembar_tokoh.py), menilai relatif ke video jangkar dan belajar dari hasil nyata (JANGKAR.md). Dipakai agent penilai-video. Bahasa Indonesia.
---

# Skill penilai video independen (Hannes 14 Okt 2026)

Ukurannya **apa yang tampil di layar dan apa yang dirasakan penonton**, bukan brief. Hannes sering mengubah arah saat produksi, jadi brief tidak dipakai sebagai patokan. Video dinilai seperti penonton asing menilainya: dalam 1-3 detik dia memutuskan menonton atau menggeser.

## Lima pertanyaan yang wajib dijawab
1. **Bisa viral?** (organik TikTok/IG Reels)
2. **Layak jadi kreatif iklan?** (Meta Ads: retargeting/akuisisi B2B RHJ)
3. **Humornya sampai?** (kalau video berniat lucu)
4. **Ceritanya dimengerti?**
5. **Naskah/dialognya kaku?**

## Kompetensi 1 — Hook & retensi video pendek
- Penonton memutuskan dalam ±1-3 detik. Frame pertama harus sudah "terjadi sesuatu": gerak, wajah dekat, benda ganjil, konflik, pertanyaan, angka mengejutkan. Pembuka logo, salam, pemandangan kosong, atau "Halo guys" = hook lemah.
- Tiga lapis hook: **visual** (frame 0), **teks layar** (terbaca ≤1,5 dtk, ≤7 kata), **audio/kalimat pertama**. Yang terkuat kalau ketiganya menyampaikan satu ketegangan yang sama.
- **Curiosity gap:** ada pertanyaan yang baru terjawab di akhir? Kalau jawabannya sudah kelihatan di detik 3, penonton tidak punya alasan bertahan.
- **Titik rawan ditinggal:** shot > 3 dtk tanpa info baru, hening tidak sengaja, pengulangan, penjelasan produk yang panjang di tengah, transisi lambat. Sebut detiknya.
- Ending: punchline kuat lalu selesai cepat, atau loop (akhir menyambung ke awal) supaya ditonton ulang.

## Kompetensi 2 — Cerita
- **Tes cerita ulang:** tulis isi video dalam 2 kalimat seperti menceritakan ke teman. Gagal → cerita tidak jelas.
- Unsur minimum: siapa tokohnya, dia mau apa, apa halangannya, apa yang berubah di akhir. Untuk 15-60 dtk cukup satu konflik.
- Penonton tidak kenal konteks internal RHJ (nama produk teknis, tokoh, lelucon kantor). Kalau butuh penjelasan dari luar video, berarti belum jelas.
- Sebab-akibat harus terlihat, bukan diceritakan narator ("show, don't tell").

## Kompetensi 3 — Humor (khususnya selera Indonesia)
- **Tes jelaskan lelucon:** tulis "leluconnya adalah ..." dalam 1 kalimat. Tidak bisa → humornya tidak sampai.
- Mekanisme umum: kejutan/ketidaksesuaian (harapan vs kenyataan), relate ("ini gue banget": kerja gudang, bos, admin, pelanggan rewel, gaji/lembur), melebih-lebihkan, salah paham, ironi, deadpan/reaksi datar, callback, roasting ringan.
- **Timing:** jeda sebelum punchline, punchline di akhir kalimat/shot, reaksi ditahan setelahnya (diam sejenak menambah lucu). Punchline yang diucapkan terburu-buru atau ditimpa musik = hilang.
- Humor Indonesia yang kuat di short video: situasi kerja sehari-hari, logat/bahasa daerah ringan, ekspresi wajah, "plot twist" receh, karakter emak-emak/bapak-bapak yang tegas. Hindari: lelucon yang butuh tahu istilah teknis, merendahkan SARA/fisik, atau terlalu "kantor" sehingga hanya orang dalam yang paham.
- Bedakan: lucu buat penonton umum vs lucu hanya buat tim internal.
- Rujukan kosakata (bukan patokan): `.claude/skills/rhj-pic-scriptwriter/KAMUS-HUMOR.md`, `.claude/skills/rhj-pic-kreatif/KAMUS-VISUAL-HUMOR.md`. Pakai untuk memberi NAMA pada teknik yang terlihat, bukan untuk menilai kepatuhan.

## Kompetensi 4 — Dialog natural vs kaku
Tanda dialog KAKU (sebut contohnya + detik):
- Bahasa tulis/baku: "Anda", "tidak", "apakah", kalimat lengkap S-P-O-K, tanpa partikel (sih, dong, kok, deh, nih, lho, kan, ya).
- Eksposisi: tokoh menjelaskan hal yang sama-sama mereka tahu supaya penonton paham ("Seperti yang kita tahu, pallet mesh ini...").
- Iklan terselip di mulut tokoh: tokoh menyebut fitur/keunggulan produk seperti brosur.
- Semua tokoh bicara dengan gaya yang sama; tidak ada ciri tokoh.
- Kalimat terlalu panjang untuk diucapkan satu napas; tidak ada interupsi, potongan, atau "eh", "hah?", "lho".
- Suara AI/TTS: intonasi rata, jeda janggal, penekanan salah kata, emosi tidak cocok dengan wajah.
Tanda NATURAL: kalimat pendek, saling potong, partikel, respons emosional ("hah, serius?"), bahasa sehari-hari daerah setempat secukupnya.
Alat bantu objektif: `python3 .claude/skills/rhj-pic-scriptwriter/cek_dialog.py` pada transkrip (lihat cara pakai di file itu) dan `BAHASA-DIALOG.md` sebagai rujukan register bahasa. Hasil alat = data tambahan, bukan vonis.

### 4b. Mendengar lewat ukuran — `dengar.py` (wajib bila video berdialog/VO)
Agent tidak mendengar. Humor dan kekakuan paling banyak ketahuan dari suara, jadi suara DIUKUR:
```
export FFMPEG=$(bash .claude/skills/rhj-pic-produksi-video/pasang_ffmpeg.sh)
export PYTHONPATH=$(bash .claude/skills/rhj-penilai-video/pasang_dengar.sh)   # sekali per sesi, ±1 menit + model ±480 MB
python3 .claude/skills/rhj-penilai-video/dengar.py <video> <scratchpad>/dengar-<kode>
```
Keluaran: `DENGAR.txt` (per kalimat: detik, jeda sebelum/sesudah, kata per detik, rentang nada, berapa dB di atas latar, tanda), `dengar.json`, `BICARA.jpg` (frame tiap kalimat).
Cara baca:
- **Timing punchline:** jeda sebelum punchline idealnya terasa (±0,3-0,8 dtk) dan ada ruang reaksi sesudahnya. Punchline tanpa jeda atau langsung ditimpa kalimat/musik = lucunya hilang.
- **Ketimpa latar:** suara dialog ≤6 dB di atas latar (musik/ambience di celah dialog) = rawan tak terdengar di HP, terutama punchline.
- **Nada datar:** rentang nada p10-p90 ≤4 semiton pada kalimat ber-emosi (kaget, marah, menyindir) = indikasi suara AI/TTS rata. Kalimat netral memang lebih datar; nilai dalam konteks.
- **Terburu-buru:** >4 kata/dtk pada kalimat ≥4 kata = sulit ditangkap, apalagi tanpa subtitle.
- **BICARA.jpg:** siapa yang bicara di tiap kalimat terlihat? Mulut bergerak bila tokohnya di layar? (Suara off-screen yang disengaja tidak dihitung salah.)
- Batas: transkrip bisa salah dengar (logat, suara AI, musik); nada bisa kacau bila ada musik/SFX di bawah dialog. Ambang = titik awal, dikalibrasi (JANGKAR.md §3). Tulis "diukur, bukan didengar" di laporan.

## Kompetensi 5 — Potensi viral (organik)
- Sinyal algoritma TikTok/Reels: tonton sampai habis (retensi), tonton ulang, share/kirim ke teman, simpan, komentar. Nilai video dari "alasan apa orang melakukan itu".
- Pemicu sebar: relate kuat (tag teman sekantor), debat/pendapat terbelah (komentar), info berguna (simpan), emosi tinggi (kaget/lucu/haru), punchline yang bisa dikutip.
- Penghambat: terasa iklan sejak detik awal, logo besar, terlalu panjang untuk isinya, kualitas AI janggal (wajah berubah, tangan aneh) yang membuat orang komentar negatif.
- Jujur: viral tidak bisa dipastikan. Beri peluang RENDAH/SEDANG/TINGGI + alasan, bandingkan dengan angka akun (`memori/SOSMED-MEMORI.md`) dan log prediksi (`memori/PENILAIAN-VIDEO-LOG.md`).

## Kompetensi 6 — Layak jadi kreatif iklan (Meta)
Video viral belum tentu iklan yang bagus. Cek terpisah:
- **3 detik pertama** menghentikan scroll calon pembeli B2B (purchasing, kepala gudang, pemilik usaha, otomotif/logistik/AMDK) — bukan hanya penonton umum.
- **Produk terlihat dan dimengerti** dalam ±5 dtk pertama; masalah pembeli → produk sebagai jalan keluar.
- **Bisa ditonton tanpa suara:** teks layar/caption cukup untuk paham.
- **Satu pesan, satu ajakan** (CTA: chat WA / cek harga / lihat katalog) yang cocok dengan tujuan klik.
- **Zona aman teks** (tidak di 15% bawah/12% kanan; tidak menutup wajah) dan tanpa huruf AI rusak.
- **Kepatuhan iklan Meta:** tidak menjanjikan yang tidak bisa dibuktikan, tidak ada klaim sertifikasi tanpa dasar, tidak meniru merek lain.
- **Kesesuaian merek:** satu merek per video (rodahammerindo ATAU palletmesh/OYAMA), FAKTA PRODUK benar (pallet mesh bisa custom min 30 unit; lemari arsip tidak custom; roda scaffolding/teflon/gerbang tidak dijual).
Hasil: LAYAK IKLAN / LAYAK DENGAN EDIT / TIDAK UNTUK IKLAN.

### 6b. Rencana versi iklan (wajib bila LAYAK atau LAYAK DENGAN EDIT)
Vonis tanpa rencana potong tidak bisa dieksekusi. Tulis:
- **Versi 6 dtk** (hook + produk + CTA), **15 dtk**, dan **≤30 dtk**: detik mulai-selesai potongan dari video asli; yang dibuang dan alasannya. Versi yang tidak masuk akal untuk video ini → tulis "tidak disarankan" + alasan.
- **3 varian hook** untuk diuji (frame/detik pembuka berbeda atau teks layar berbeda, ≤7 kata), satu kalimat alasan masing-masing. Ini bahan desain uji pic-ads (A/B), bukan keputusan akhir.
- **Versi tanpa suara:** teks layar apa yang perlu ditambah supaya paham tanpa audio (detik + teks).
- **Frame pertama** yang disarankan (detik di video asli) dan teks CTA akhir (chat WA / cek harga / katalog), satu merek saja.
- Ukuran sesudah tayang: hook rate & hold rate per varian (JANGKAR.md §2). Ingat: eksekusi iklan lewat pic-ads/Yosie dan pagar B6; penilai hanya mengusulkan.

## Kompetensi 7 — Cacat AI & konsistensi tokoh
Video Rengga dibuat dengan AI. Penonton Indonesia cepat menulis "ini AI" / "mukanya ganti", dan komentar itu bisa mengalahkan cerita yang bagus. Cek terpisah dari selera:
```
python3 .claude/skills/rhj-penilai-video/lembar_tokoh.py <folder bedah> deliverables/aset-lastri/KANON-01-master-24Sep.jpg
```
→ `TOKOH.jpg` (acuan berbingkai merah + frame tiap shot). Acuan identitas = `deliverables/aset-lastri/KANON-01-master-24Sep.jpg` + `deliverables/CHARACTER-SHEET-LASTRI-24Sep.md` bagian 3 (penampilan kanon) dan `deliverables/QC-KANON-TOKOH-28Sep.md` (Pak Yaqin, Mas Selo). Ini identitas tokoh, BUKAN brief: dipakai hanya untuk "apakah tokohnya tetap orang yang sama".
Periksa dan sebut detik/shot:
- **Wajah berubah antar-shot** (bentuk muka, usia, warna kulit, rambut) di adegan yang sama; tokoh terlihat seperti orang lain.
- **Kostum/atribut** berubah (helm, rompi, logo, name tag) tanpa alasan cerita.
- **Tangan & jari** (jumlah, melebur ke benda), **teks/huruf rusak** di benda/papan, **benda melebur** atau berubah bentuk, gerak yang melanggar fisika (pallet menembus, roda melayang).
- **Bibir vs suara:** di BICARA.jpg, mulut tokoh yang bicara bergerak? Lip-sync meleset jelas lebih merusak daripada suara off-screen.
- **Latar melompat** di adegan yang sama (rak, lampu, posisi barang).
- **Mata & kedip** kosong/menatap kosong terlalu lama, ekspresi tidak cocok dengan kalimat.
Klasifikasi tiap cacat: **ULANG KLIP** (terlihat jelas di ukuran HP, di tokoh utama, atau di hook) / **TUTUP DI EDITING** (potong lebih cepat, crop, tutup teks) / **BIARKAN** (hanya terlihat bila di-pause). Sebut berapa yang ULANG KLIP; ≥1 cacat ULANG KLIP di 3 detik pertama = tidak boleh vonis TAYANG.

## Kompetensi 8 — Menilai relatif & belajar dari hasil
Lihat `JANGKAR.md`: tiap penilaian menyebut ≥2 video jangkar (akun Lastri sendiri bila sudah ada angka; selain itu kolam riset/swipe-file yang paling mirip), menempatkan video relatif terhadapnya, dan mengisi hasil nyata video lama (IG via `meta.mjs ig-report`; iklan via hook rate & hold rate) sebelum menilai yang baru.

## Lampu merah (bukan skor, wajib dicek walau tanpa brief)
FAKTA PRODUK salah · K3 berbahaya terlihat (mis. naik forklift tanpa pengaman) · wajah mirip orang nyata/tokoh publik · merek pesaing · konten SARA/merendahkan · klaim yang bisa jadi masalah hukum/iklan. Ada lampu merah → sebut di baris paling atas laporan, apa pun nilainya.

## Kalibrasi
Setiap penilaian dicatat di `memori/PENILAIAN-VIDEO-LOG.md`. Saat hasil nyata (views 48 jam/7 hari, % ditonton, hook rate & hold rate iklan) tersedia, isi dan tulis pelajarannya (cara hitung: `JANGKAR.md` §2-3). Penilai yang baik bukan yang selalu keras atau selalu lunak, tapi yang prediksinya makin dekat ke hasil nyata.
