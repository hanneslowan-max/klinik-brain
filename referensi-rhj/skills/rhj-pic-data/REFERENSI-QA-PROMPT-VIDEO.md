# Referensi: QA prompt video (rubrik v1 + pelajaran @ai_studio_mixx)

Dipakai pic-data untuk mengecek prompt video buatan pic-kreatif (Lampiran prompt di brief) dan pic-produksi-video (prompt yang benar-benar dikirim). **Status: DRAF BELUM TERUJI (Hannes 9/10: jangan jadi standar sebelum diuji). Tidak dipakai untuk meluluskan atau menolak prompt; skor = catatan saja sampai uji generate + ACC Hannes.** Rubrik ini alat cek; ia tidak mengubah templat brief v1.3 (`.claude/skills/rhj-pic-kreatif/TEMPLAT-BRIEF.md`). Bila rubrik dan templat berbeda, templat yang berlaku; bedanya dicatat sebagai usulan.

Sumber belajar: 80 prompt @ai_studio_mixx (Higgsfield · Seedance 2.5 · ChatGPT), ditranskripsi dari layar → `deliverables/riset-sosial/BELAJAR-PROMPT-MIXX-09Okt/` (`PROMPT-KORPUS.md`, `BEDAH-STRUKTUR-PROMPT.md`, `KALIBRASI-PROMPT-RHJ.md`, `RINGKASAN.md`).

## 0. Sebelum menilai

1. **Nilai prompt yang dikirim, bukan yang ditulis di brief.** Ambil dari log produksi; bila log hanya berisi label (PM-06 dan PM-07: 0 dari 37 entri submit memuat teks prompt), tarik dari job Higgsfield (`show_generation_by_ids` dengan job id di `hf-log.jsonl`; baca saja, 0 kredit). Bandingkan dengan Lampiran prompt brief: info yang hilang di jalan dinilai di S5.
2. **Tentukan mode**: (a) **klip per shot** ≤5 dtk dari start_image/acuan (jalur kita: Kling 3.0 pro still-first, Seedance reference-to-video per scene); (b) **multi-shot satu prompt** (>5 dtk atau beberapa cut dalam satu generate; gaya mixx). Beberapa butir dinilai beda per mode.
3. Rubrik menilai **prompt**. Hasil video tetap dicek di QC brief B8 (zoom 100%): larangan di prompt tidak menjamin (lihat §3).

## 1. Rubrik (maks 21)

**Wajib (0 / 1 / 2)**

| # | Butir | 2 = | 1 = | 0 = |
|---|---|---|---|---|
| W1 | Format dan parameter | rasio, durasi, model + mode tercatat (teks atau parameter API); durasi generate cocok dengan jendela yang dipakai; resolusi final ≥720p (aturan 5) | satu tidak ada atau final 480p | tidak tercatat |
| W2 | Subjek dan identitas | mode a: rujuk start image/acuan (peran tiap acuan bila >1) + 1 kalimat bentuk produk yang cocok foto; mode b: blok Continuity sekali tulis (tokoh, produk, lokasi) lalu beat memakai "the same …" | subjek disebut umum ("the cage") | tidak ada / bertentangan dengan foto acuan |
| W3 | Aksi dan waktu | mode a: satu aksi, kata kerja konkret; mode b: beat bertimecode 1–3 dtk, kalimat pertama = ukuran shot/cut | aksi kabur atau beberapa aksi tanpa waktu | tidak ada aksi |
| W4 | Kamera | ukuran + sudut + gerak (atau "locked") di tiap shot/beat | salah satu | tidak ada |
| W5 | Cahaya | arah + warna/jam, sama dengan B3b brief | hanya disebut ("warm light") | tidak ada |
| W6 | Suara | SFX/ambien konkret + "No music" (musik dari editing, aturan 4) + "no voices/speech" bila VO dibuat di editing | salah satu | tidak ada (padahal suara bawaan on) |
| W7 | Pagar RHJ di prompt (**0 atau 2, mutlak**) | tidak meminta huruf/angka/logo/label/UI/kartu akhir dari AI · tanpa wajah orang nyata, IP, merek pihak ketiga, atau pancingan merek ("authentic UFC-style") · K3 (tanpa orang di bawah/di dalam pallet mesh, tanpa forklift/stunt) · FAKTA PRODUK (bentuk sesuai foto, pallet mesh tanpa roda, tanpa klaim finishing) · dua domain (produk domain lain tidak muncul) · Lastri: tag tokoh + kanon | — | satu saja dilanggar |
| W8 | Jejak | prompt persis + parameter + job id tersimpan di log/folder produksi | job id ada, teks prompt hanya di job | tidak bisa dilacak |

**Sebaiknya (0 / 1; tidak relevan = 1)**

| # | Butir |
|---|---|
| S1 | Larangan ringkas: mode a ≤1 baris ("No text, no logos" + risiko khusus shot); mode b satu blok berisi risiko konsep, bukan boilerplate yang diulang di semua shot |
| S2 | Kunci kontinuitas: bookend/bingkai sama ditulis ("same framing, lens and light as the start image, camera locked"); tokoh/produk lintas shot "the same …" |
| S3 | Fisika/berat untuk benda yang diangkat, dilepas, ditumpuk, berputar |
| S4 | Kepadatan: mode a 30–90 kata (start image memikul tampilan); mode b ±20–45 kata per detik video (mixx median 31, IQR 23–44) |
| S5 | Brief → prompt utuh: sudut, lensa, cahaya, SFX, dan detail pagar dari B3a/B3b/Lampiran tidak hilang waktu prompt dipendekkan |

**Keputusan:** LOLOS = W7 = 2, semua W ≥1, total ≥15 · REVISI KECIL = W7 = 2 dan (total 12–14 atau satu W lain = 0) · GAGAL = W7 = 0, atau ≥2 W = 0, atau total <12. Skor adalah penilaian satu orang sampai ada dua penilai (pic-data + pic-kreatif) pada 10 prompt pertama dengan kappa berbobot ≥0,6 per butir (sama dengan syarat rubrik naskah).

## 2. Contoh

**LOLOS (PM-07 S3, Kling 3.0 pro, start_image, 4 dtk, 56 kata, skor 19/21):** "Low-angle medium shot at floor level, the camera tilts up slowly along a tower of three stacked wire-mesh pallet cages full of plain cartons. The tower stays perfectly still and straight, warm skylight glows behind it, thin dust drifts in the light. A short metallic settle sound of steel frames. No people, no text, no logos." Kurang: "No music", teks prompt tidak ada di hf-log.

**REVISI KECIL (PM-07 S2, 14/21):** kamera, aksi, dan K3 jelas ("stays above the rim … never pass through the wire"), tetapi cahaya hilang sama sekali (brief: "warm side light from the left"). Perbaikan: tambah satu frasa cahaya dari B3b.

**GAGAL untuk RHJ (gaya mixx, golf tabir surya):** meminta label "BLUEMIST SUNCARE / AQUA SUN CREAM / SPF 50+" dibuat AI (W7 = 0). Hasilnya label terbaca, tetapi logo pihak ketiga muncul di topi pemain. Di akun yang sama label UI "FULL AUTONOMOUS" keluar "FULL AUTONOMUS". Untuk RHJ: produk polos di prompt, huruf dipasang di editor.

**GAGAL untuk RHJ (gaya mixx, UFC):** "authentic UFC-style octagon … broadcast" memancing logo UFC/ESPN/Monster di hasil walau ada "logo distortion" di larangan (W7 = 0: pancingan merek).

## 3. Pelajaran mixx yang dipakai rubrik (tanda bukti)

- **KUAT** (n = 80): struktur baku Format → Continuity → Tone & Manner → Negative → beat bertimecode (91%); kunci identitas "same/identical" 95%; beat bertimecode 99%, median 8 beat, 2,5 dtk per beat; durasi tertulis = durasi hasil ±1 dtk pada 49/51.
- **KUAT**: panjang median 640 kata untuk 20 dtk (±71 kata per beat). Per beat setara prompt shot kita, jadi aturan 2 "pendek" tetap masuk akal **per shot**.
- **KESAN** (13 pasangan prompt vs hasil, satu penilai): urutan beat dipatuhi 13/13; detik bergeser terlihat 2/13; huruf/logo bermasalah 3/13 walau 90% prompt melarang teks/logo. Sejalan dengan produksi RHJ (RD-01 v1: logo Apple, huruf di sarung tangan; PM-07: kastor muncul walau "no wheels"). Larangan di prompt ≠ jaminan; pagar dicek di hasil (aturan 6).
- **ARAH** (59 konsep, dikoreksi era ±7 hari): konsep "rekaman nyata" (POV 2,08×, handheld/HP/CCTV 1,54×, dialog berkutip 1,65×) di atas median sezaman; panjang prompt tidak terkait views (Spearman −0,01). Akun kecil (median 864 views; satu reel = 45,9% total views), satu akun: bukan aturan.
- Badge "AI CONTENT" di 13/13 video penuh: sejalan label AI RHJ.
- **Jangan ditiru**: wajah tokoh nyata/sejarah, IP kartun, merek nyata, stunt berbahaya, label/logo/kartu akhir dibuat AI.

## 4. Pertentangan dengan aturan kita (dicatat, tidak diubah)

- Aturan 2 (pendek, larangan 1 baris) vs mixx (640 kata, larangan median 19 butir): beda mode. Usulan ke pic-kreatif: tulis bahwa aturan 2 berlaku per shot; bila memakai multi-shot satu prompt (Seedance >5 dtk), pakai struktur mixx dengan larangan tetap ringkas. Menunggu keputusan Hannes.
- Aturan 6 (pagar di QC): **didukung** temuan mixx.
- Pagar huruf/logo bukan AI: mixx melanggar 19% prompt; jangan ditiru.

## 5. Cara kerja pic-data saat diminta cek prompt

1. Kumpulkan prompt yang dikirim (log → job Higgsfield) dan Lampiran brief; catat mode, model, durasi, resolusi.
2. Isi tabel per prompt (W1–W8, S1–S5, total, keputusan) + satu kalimat alasan per butir yang tidak penuh.
3. Hitung kata dan kata/dtk (ATURAN NOL; jangan kira-kira). Catat info brief yang hilang (S5) per butir.
4. Tulis 3–5 perbaikan konkret berupa frasa yang bisa langsung ditempel. Jangan menulis ulang prompt orang lain dan jangan mengubah file pic-kreatif/produksi.
5. Bila hasil video sudah ada, sandingkan frame per 1 dtk dengan beat prompt (subjek, urutan, kamera, huruf/logo) sebagai lampiran QC; tandai KESAN.
