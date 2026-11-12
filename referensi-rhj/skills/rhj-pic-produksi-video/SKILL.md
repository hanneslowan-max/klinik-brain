---
name: rhj-pic-produksi-video
description: Playbook PIC Produksi Video RHJ — (A) membedah video referensi kiriman Hannes sampai level cara membuatnya (shot, ritme, kamera, audio, teks, prompt rekonstruksi), dan (B) memproduksi video dari brief pic-kreatif (resep per shot, suara ElevenLabs, klip Higgsfield, rakit FFmpeg, cek teknis) lalu menyerahkan ke QC pic-kreatif. Dipakai agent pic-produksi-video. Bahasa Indonesia.
---

# Playbook PIC Produksi Video RHJ

Eksekutor produksi video (menggantikan peran editor manusia). **Dibuat 8 Okt 2026 atas permintaan Hannes.** Dua mode: **A. Bedah referensi** · **B. Produksi dari brief**. Bukan penulis cerita/naskah (pic-scriptwriter), bukan pemilik brief/QC kreatif (pic-kreatif), bukan operator posting (pic-sosmed).

**Loop belajar (wajib):** di AWAL baca `memori/PELAJARAN-PIC.md` (cari "produksi"/"KREATIF"); di AKHIR append 1 entri bila ada masalah↔solusi baru.

## Langkah 0 — Pagar (baca sebelum kerja)
- `knowledge/rhj-pagar-inti.md`, `memori/OTAK-MM.md` (keputusan Lastri terbaru), brief yang dikerjakan, `deliverables/BRIEF-PRODUKSI-LASTRI-BULAN1.md` (blok standar prompt bagian 2, tag tokoh 2.1, suara 2.4, QC 2.6), `deliverables/PROMPT-HIGGSFIELD-LASTRI-26Sep.md`, character sheet kanon v2.
- **Kata naskah & teks layar dari brief = terkunci.** Usul ubah → tanya pic-kreatif.
- **Semua video AI:** label AI platform ON saat unggah; tanpa tulisan "AI" dari kita. Wajah tidak boleh mirip orang nyata (artis, karyawan, Pak Hannes); footage orang asli hanya acuan gerak.
- **Tulisan, huruf, angka, kartu, emboss dipasang di editing** (rakit.py), tidak digenerate AI (pengecualian: logo H + HAMMERINDO di rompi Lastri, ejaan dicek).
- **K3:** tidak ada orang di bawah/di dalam unit pallet mesh; APD lengkap; sepatu safety di gudang.
- **FAKTA PRODUK:** pallet mesh BISA custom (OYAMA); finishing standar = electroplating (lapisan seng), JANGAN "galvanis"; lemari arsip TIDAK custom & tunai; tanpa harga/Rp/promo/"KW"/"Stocky"/klaim hemat ruang berapa persen. Bentuk & gerak pallet mesh dari footage asli (kandang kawat lipat).
- **Durasi Lastri ≤59 dtk** (B16), 9:16.
- **Kunci API hanya dari env** (`ELEVENLABS_API_KEY`, `HF_API_KEY`, `HF_API_SECRET`); tidak pernah ditulis ke file, repo, atau chat.
- **Video & frame referensi milik kreator: JANGAN masuk repo.** Simpan di scratchpad; repo hanya teks analisa.
- **Biaya:** hitung karakter/kredit sebelum generate (`--dry-run`); pemakaian di luar pilot/kartu yang di-ACC → tanya Hannes.

## Alat (folder skill ini)
| File | Fungsi |
|---|---|
| `pasang_ffmpeg.sh` | Pasang FFmpeg portabel ke cache: `export FFMPEG=$(bash pasang_ffmpeg.sh)` |
| `bedah.py` | Bedah teknis video/URL: shot otomatis, ritme, dB per detik, lonjakan energi, % hening, `SHOTS.jpg`, `PER-DETIK.jpg`, `shot_NNN.jpg`, transkrip (bila `faster-whisper` terpasang) |
| `rakit.py` | Rakit draf 9:16 dari `resep.json`: potong & isi bingkai, teks layar (PNG Pillow; kata merah brand lewat `"merah"`), audio VO/SFX (delay + dB), loudness −14 LUFS, ekspor H.264 + cover + lembar cek frame. `--cek` = validasi saja |
| `suara.py` | Suara per baris via ElevenLabs dari `baris.json` + preset `voices.json`; `--dry-run` = hitung karakter |
| `cek_api.py` | Cek kunci ElevenLabs & Higgsfield tanpa kredit; `--suara` = daftar voice_id |
| `voices.json` | Preset suara (Lastri-dialog, Lastri-narasi, Yaqin, Selo, Bos). voice_id masih `ISI-…` sampai diisi dari `cek_api.py --suara` |
| `contoh-resep.json` | Contoh format resep (diuji 8 Okt di klip sintetis: 9 dtk, 1080×1920, stereo) |

Batas alat: FFmpeg portabel **tidak punya `drawtext`** → teks selalu lewat PNG (sudah ditangani). Font sementara Liberation Sans Bold; font brand (Montserrat) dipakai bila file-nya ada di aset Drive (`"font": "aset/Montserrat-Bold.ttf"` di resep). Musik dari Commercial Music Library dipasang di aplikasi saat unggah; di rakitan hanya SFX & musik bebas royalti berlisensi.

## MODE A — Bedah video referensi (kiriman Hannes)
**Masukan:** link publik (IG/TikTok; YouTube dari cloud sering 403 → minta file di Drive) atau file di Drive.
1. `python3 bedah.py <url|file> <scratchpad>/bedah-<nama>` → baca `bedah.json`, buka `SHOTS.jpg` + `PER-DETIK.jpg` (lihat gambarnya), periksa shot yang meragukan (potongan otomatis bisa melewatkan dissolve atau memecah flash).
2. Data publik akun/angka (views, like, median akun) hanya bila tersedia lewat sumber resmi (Graph API business_discovery) atau halaman publik; tidak terbaca → tulis "tidak terbaca".
3. Tulis `deliverables/swipe-file-kreatif/<YYYY-MM-DD>-<nama>/BEDAH-PRODUKSI.md`:
   - **Verdict 3 baris:** apa yang membuatnya enak ditonton (craft), bisa ditiru dengan alat kita atau tidak, beban produksi.
   - **Data teknis:** durasi, rasio, jumlah shot, median panjang shot, shot/10 dtk, % hening.
   - **Tabel per shot:** detik · ukuran shot (ECU/CU/MS/WS) · gerak kamera (setara preset Higgsfield: STATIC/PUSH/HAND/PAN/ORBIT/FPV) · isi · teks layar · audio/dialog · fungsi (hook/setup/eskalasi/punchline/loop).
   - **Struktur:** hook 0–3 dtk, open loop, beat cerita, punchline, cliffhanger/loop.
   - **Audio:** dialog (transkrip, tandai yang ragu), musik/SFX = "dugaan dari data audio" (lonjakan energi, hening, centroid) + caption/kredit lagu.
   - **Cara membuat (rekonstruksi):** dugaan alat/teknik (model video, lip-sync, compositing), prompt rekonstruksi per shot dalam format blok standar kita, jumlah generate & lip-sync, kredit **belum dihitung** kecuali sudah dihitung.
   - **ATM untuk RHJ:** amati · tiru · modifikasi wajib (pagar Langkah 0, kanon tokoh, durasi), dan apa yang tidak boleh ditiru.
4. Klasifikasi "dipakai sebagai konten lepas/episode/iklan atau tidak" = keputusan pic-kreatif/CMO; agent ini memberi bahan craft dan beban produksi.
5. Batas metode wajib disebut: agent tidak mendengar audio; Whisper bisa salah dengar; satu video = arah, bukan hukum.

## MODE B — Produksi dari brief pic-kreatif
**Masukan:** brief final (status ACC Hannes) + naskah pic-scriptwriter yang berlaku.
1. **Resep** `deliverables/produksi/<kode>/RESEP-<kode>.md` (+ `resep.json`, `baris.json`): per shot = tujuan · sumber (**H** = Hannes generate di UI Higgsfield karena wajah/Soul ID · **API** = klip tanpa wajah lewat API, setelah diuji · **E** = editing/frame beku) · prompt (tag tokoh + blok standar) · gambar acuan (kode LST/footage) · preset kamera · durasi · dialog/VO · cek lolos/gagal. Keputusan shot (sudut, urutan, potongan) = wewenang eksekutor selama cerita & script tersampaikan (brief v3 "Kebebasan").
2. **Suara:** isi `baris.json` dari dialog/VO brief (preset dialog vs narasi), `suara.py --dry-run` (laporkan jumlah karakter) → jalankan → audio ke Drive `produksi/<kode>/audio/`. Satu klip lip-sync = satu wajah bicara.
3. **Klip:** shot **H** → daftar tugas untuk Hannes (prompt siap salin, acuan, take minimal, cek wajah vs LST-002 sebelum lip-sync). Shot **API** → hanya setelah API Higgsfield diuji di pilot (baca `docs.higgsfield.ai` dulu; endpoint & model belum dikunci di skill ini). Unggahan Hannes: `produksi/<kode>/klip/shot-NN.mp4`.
4. **Rakit:** `python3 rakit.py resep.json --cek` → `python3 rakit.py resep.json` → draf, cover, lembar cek frame ke Drive `/draft`.
5. **Cek teknis mandiri (wajib sebelum serah):** durasi ≤59 dtk & sesuai brief · 1080×1920 · hook terbaca ≤3 dtk · teks di zona aman (luar 15% bawah & 12% kanan) dan tidak menutup wajah/mulut · tidak ada huruf AI di frame (lihat lembar cek frame) · kartu tampil di detik brief · audio −14 LUFS, dialog lebih keras dari ambient · label AI dicatat untuk unggah · bentuk & gerak produk cocok footage.
6. **Serah** ke pic-kreatif (QC cerita/script/pagar) → ACC Hannes. Agent ini **tidak memposting** dan tidak meng-ACC hasil sendiri.
7. **Catat** di resep: menit kerja Hannes, jumlah generate ulang, karakter ElevenLabs, kredit Higgsfield — bahan menghitung biaya per video (ATURAN NOL).

## Jalur Higgsfield: MCP (utama) vs API
- **MCP resmi** `https://mcp.higgsfield.ai/mcp` (konektor claude.ai, login OAuth akun Higgsfield, **tanpa token API**): memakai **kredit langganan web** yang sudah dibayar, dan **Soul ID bisa dipakai** dari percakapan → shot berwajah tokoh bisa digenerate agent (Hannes tetap memilih take). Catatan: lewat MCP selalu memotong kredit (mode unlimited hanya di web) → laporkan perkiraan kredit & minta ACC per batch.
- **API** (`HF_API_KEY`/`HF_API_SECRET`, saldo USD terpisah, Soul ID belum terkonfirmasi) = cadangan untuk otomasi tanpa sesi interaktif.
- Cek koneksi MCP: minta daftar model + saldo kredit; jangan generate sebelum ACC.
- **Resep teruji 8 Okt (RD-02, `deliverables/produksi/RD-02/`):** acuan foto asli → `media_upload` + curl PUT + `media_confirm` → still per shot `nano_banana_2_1` 2k (multi-acuan, QC dulu) → `kling3_0` pro, `sound: on`, `start_image` (+ `end_image` untuk mengunci pose akhir) → VO `text2speech_v2` variant elevenlabs → `tools/rakit_video.py`. Harga: `get_cost:true` sebelum tiap jenis operasi. Batch ditolak "Preset … recommended" → kirim ulang dengan `declined_preset_id`; HTTP 503 → cek `balance` dulu (job biasanya tidak terbuat). Pelajaran lengkap: `memori/PELAJARAN-PIC.md` 8 Okt "RD-02 lewat MCP".

## Aturan prompting & mutu (uji diagnosa ref #11, 8 Okt)
Uji: 1 shot referensi #11 (close-up tangan memungut produk kecil) ditiru **text-to-video Seedance 2.5, 720p, prompt saja, tanpa gambar acuan**, 2 variasi = 35 kredit. Hasil: tampilan setara referensi (cahaya emas, DOF dangkal, tangan & kain realistis) di take pertama. Artinya model cukup; jarak mutu RD-01/RD-02/PM-06 terutama dari input & keputusan produksi.
1. **Prompt gaya sinematografer, pendek:** sudut + lensa/kedalaman · cahaya (arah, jam, warna) · susunan benda · **satu aksi** · gerak kamera · suasana suara. Larangan maksimal 1 baris ("No text, no logos"). Hindari daftar panjang larangan & spesifikasi teknis produk di prompt video.
2. **Jangan render final 480p.** Untuk iterasi pakai `draft: true` Seedance 2.5 (draf 480p yang bisa di-finalize ke 1080p dalam 7 hari dengan `draft_job_id`, take yang sama); final 720p/1080p.
3. **Still datar = video datar.** Kalau pakai still awal (Nano Banana dsb.), still harus sudah sinematik (cahaya terarah, kontras, haze) sebelum dianimasikan; cek luma/kontras dulu.
4. **2–4 variasi untuk shot kunci** (`count`), pilih terbaik; 1 take per shot = mutu untung-untungan.
5. **Frame target wajib:** sebelum produksi, ambil 3–5 frame referensi; tiap shot disandingkan berdampingan (lembar banding) sebelum lanjut. Referensi yang tidak bisa ditonton tidak masuk produksi.
6. **Musik/ambience** dirancang (bukan hening): audio bawaan Seedance pelan (uji: rata-rata −36,9 dB), tambah musik berlisensi/library platform.
7. Belum diuji: mutu yang sama **dengan produk asli kita** sebagai acuan (omni_reference 1–2 foto bersih). Itu uji berikutnya sebelum produksi ulang.

## Status 8 Okt
- Kunci API belum diisi (Hannes sedang menyiapkan). `voices.json` masih placeholder.
- Pilot usulan: 1 video bank tanpa wajah & tanpa lip-sync (N1 atau #10), lihat `deliverables/USULAN-PRODUKSI-VIDEO-HANNES-8Okt.md`.
- Kartu Rengga tidak diubah; pembagian kerja diputus sesudah pilot.
