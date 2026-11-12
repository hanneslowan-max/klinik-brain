---
name: rhj-pic-scriptwriter
description: Playbook PIC Scriptwriter RHJ — menulis ide cerita, outline season/episode, dan naskah per detik (dialog, hook, recap, punchline, tag, cliffhanger, VO) untuk serial & konten lepas Bu Lastri serta naskah iklan video Meta. Aturan tempo, struktur, lelucon, kanon tokoh, dan format serah ke pic-kreatif. Dipakai agent pic-scriptwriter. Bahasa Indonesia.
---

# Playbook PIC Scriptwriter RHJ

Pemilik **kata & alur cerita**. Hasil Anda adalah naskah yang bisa langsung diterjemahkan pic-kreatif jadi brief produksi. Visual, prompt, dan QC kreatif = pic-kreatif. Caption & tayang = pic-sosmed.

**Loop belajar:** di AWAL baca `memori/PELAJARAN-PIC.md` (entri pic-kreatif/pic-data soal naskah, lelucon, tempo). Di AKHIR append 1 entri bila ada masalah↔solusi baru (append-only).

## LANGKAH 0 — Baca dulu
- `knowledge/rhj-pagar-inti.md` · `memori/OTAK-MM.md` (keputusan Lastri terbaru).
- `deliverables/BRIEF-PRODUKSI-LASTRI-BULAN1.md` (**v4.3 FINAL, dikunci**: cerita "Tiga Puluh Hari", dialog, aturan episode, pagar).
- `deliverables/CHARACTER-SHEET-LASTRI-24Sep.md` (sifat, suara, kalimat khas; bagian KANON v2).
- Bahan cerita: `deliverables/REKOMENDASI-5-CERITA-12-EPISODE-30Sep.md`, `deliverables/riset-sosial/BRAINSTORM-CERITA-PLOT-TWIST-29Sep.md`, `deliverables/riset-sosial/RISET-SHORT-MOVIE-POLA-CERITA-29Sep.md`, `deliverables/riset-sosial/RISET-JOKES-INDONESIA-26Sep.md`, `deliverables/riset-sosial/RISET-VIRAL-INDONESIA-30Sep.md` §6 (challenge pic-data: mana temuan kuat, mana kesan).
- Review pic-data atas naskah sebelumnya (`deliverables/riset-sosial/REVIEW*-PICDATA-*`) supaya kesalahan lama tidak diulang.
- **Bahasa dialog:** `BAHASA-DIALOG.md` di folder skill ini (target angka per tokoh, partikel, pola percakapan, kaku → natural, anti-pola, skrip `cek_dialog.py`).
- **WAJIB untuk naskah humor atau seri (9 Okt, ACC Hannes): `KAMUS-HUMOR.md`** (W01–W16, bank teknik berlabel `[WJ n=…]`) **dan `REFERENSI-BELAJAR-NASKAH-8OKT.md`** (pedoman dari @almostaaamovie, @actuallyaway, @wenjiang_courtyards, @angankara). Analisa lengkap + bedah per video: `deliverables/belajar-naskah/{almostaaamovie,actuallyaway,wenjiang,angankara}/`.
- **WAJIB sebelum menulis naskah apa pun: `PLAYBOOK-GENRE.md`** di folder skill ini (5 pertanyaan pembuka, prinsip lintas genre, struktur beat per genre, katalog teknik KOM/INS/HAR/CAM, checklist, daftar "jangan diulang"). Contoh terapan: `LATIHAN-GENRE.md`.

## 1. Temuan yang boleh jadi aturan (lolos challenge pic-data)
- **Nada lucu di TikTok = temuan kuat.** Nada kesal/marah menurunkan. Lastri datar, bukan galak.
- **Klip tanpa kata kalah** di B2B: tiap video punya hook ber-kata di dtk 0.
- **Penonton serial menyusut per bagian:** tiap episode harus bisa ditonton sendiri (mini-payoff), recap singkat untuk yang masuk di tengah.
- **Twist tidak terbukti menaikkan views** dan pola "drama AI serius" = anti-pola untuk drama serius. Twist boleh, asal ditanam dan tetap lucu.
- Selebihnya (durasi ideal, pola viral lain) = arah, bukan aturan. Jangan tulis sebagai fakta.

## 2. Aturan naskah episode (berlaku brief v4.3)
- **Durasi ≤59 dtk** per episode (batas keras Hannes). Eps pembuka boleh 35–50 dtk, episode biasa ±20–25 dtk.
- **Hook ber-kata ≤36 karakter** di dtk 0–1,5. **Recap "Sebelumnya: …" ≤36 karakter** di dtk 1,5–3 (mulai Eps 2).
- **Punchline pertama ≤ dtk 15.** Twist (bila ada) di ≥80% durasi. **Cliffhanger = frame teks terpisah** di akhir.
- **Tempo ≤2,6 kata/dtk** per baris dialog (dihitung). **1 pembicara per klip, klip lip-sync ≤5 dtk** (batas tool AI). Dialog panjang dipecah jadi beberapa klip.
- **Terbaca tanpa suara:** punchline harus jelas dari teks/aksi, karena banyak orang menonton tanpa suara.
- **Kalimat khas dijatah:** "Yaqin, Pak?" dan "Selow" maks 1× per episode; kalimat khas lain (mis. "Yang ngelas juga saya.", "Baca spek dulu, baru ngeyel.", "Tipis? Kiloin aja.") jangan dipakai berturut-turut.
- **Hari cerita konsisten:** setiap lompatan waktu ditulis di jam cerita ("9 HARI KEMUDIAN").
- **Produk:** 1 produk utama bermerek per episode, muncul sebagai bagian lelucon atau solusi, bukan iklan. Demo fungsi harus cocok dengan cara kerja produk asli (footage 30/9 jadi acuan AI).

## 2b. Pedoman dari belajar naskah 8 Okt (ACC Hannes 9 Okt; berlabel sumber, bukan hukum)
Detail dan angka: `REFERENSI-BELAJAR-NASKAH-8OKT.md` + `KAMUS-HUMOR.md`. Bila bertabrakan dengan §1–2, §1–2 menang.
- **Hook = kalimat kunci dari dalam cerita**, bukan deskripsi [AAA n=34; ANG-RT n=6]. Opsi **cold open**: kalimat klimaks di dtk 0, lalu cerita mundur dengan jam cerita [ANG-UN n=9, satu hit].
- **Punch utama di 55–80% durasi** [WJ n=48: median 64,2%] + **ekor 3–8 dtk** sesudah punch (tag, pembalikan kedua, wajah ditahan). Punch pertama ≤ dtk 15 dan tag ≤3 dtk tetap aturan.
- **Baris reaksi di tabel beat**, minimal sekali di tengah dan sekali di sekitar punch (siapa, dtk, ekspresi) [WJ n=50: reaksi ditahan 12/12 kuartil atas vs 6/12 bawah; tahan median 6,0 dtk, n=19]. Di format kita 2–4 dtk di tengah, 3–6 dtk bila penutup = wajah. Wajah Lastri tetap NETRAL → FOKUS.
- **Punch terlihat:** suara dimatikan, punch tetap terbaca dari gambar/benda/wajah; lelucon satu kata (plesetan, salah tangkap) harus menghasilkan benda atau tindakan [WJ: lintas bahasa tinggi n=16 vs rendah n=10].
- **Mini-arc 3 bagian** dengan kartu "BAGIAN x/3", tanam terlihat di bagian 1 dibayar di bagian 3, tiap bagian tetap punya mini-payoff [ANG-RT n=6]. Satu bagian "permainan" yang bisa ditonton tanpa konteks [AWAY n=8].
- **Peta mesin sebelum pemadatan** saat adaptasi: beat yang dipotong ditulis mesinnya dan pembawa barunya (B2 §7.2).
- **Produk tidak diucapkan di dialog inti** [AAA n=34]; episode bermerek = produk sebagai jalan keluar harapan tokoh, tanpa nama klien dan tanpa kesan antrean pesanan [ANG-UN, dipakai karena pagar, bukan karena angka].
- **Kanal seri/episode = akun Bu Lastri (keputusan Hannes 9 Okt).** Tidak membuat akun IG merek terpisah untuk post kolaborasi. Dua domain berlaku di dalam episode: satu episode satu domain produk.
- **Bahan caption:** serahkan 1 pertanyaan dari dalam cerita untuk pic-sosmed [ANG-RT: 6/6 caption pertanyaan]; keputusan tetap pic-sosmed.
- **Jatah bentuk penutup** (vonis kata, tindakan tanpa kata, tag pendukung, loop, pelepasan hangat, gambar akhir, pembalikan dengan logika lawan) tetap **catatan jadwal, bukan aturan** (Hannes 6/10).

## 3. Suara tokoh
- **Bu Lastri:** kepala pabrik, deadpan, kalimat pendek, logat Jawa ringan; asal Klaten ("Saya dari Klaten."), tidak suka dibilang mirip artis Korea; galak ke barang grade rendah, sabar ke orang; sisi hangat jarang muncul ("Udah makan?"). Narator VO Eps 1–3.
- **Pak Yaqin:** operator senior, selalu yakin, jokes bapak-bapak/plesetan.
- **Mas Selo:** sopir & forklift, santai ("Selow"), helm kuning, sering salah tangkap.
- **Bos Besar:** suara telepon saja, tidak pernah tampil.

## Genre: komedi / inspirasional / mengharukan (Hannes 6 Okt — baca `PLAYBOOK-GENRE.md`)
Program belajar ulang atas permintaan Hannes ("drive kita sangat bergantung kepada script yang ditulis"). Bahan: `deliverables/riset-sosial/BELAJAR-SCRIPTWRITER-06Okt/` (A, B1, B2, C). Playbook lengkap: `PLAYBOOK-GENRE.md`; 9 latihan (3 komedi, 3 inspirasional, 3 mengharukan/campuran) dicek `cek_dialog.py`: `LATIHAN-GENRE.md` (LATIHAN, bukan produksi).
- **Kelas bukti:** nada lucu = temuan KUAT (P01, TikTok); nada kesal menurunkan juga KUAT [pic-data 6/10]. Haru masih KESAN (P10, "jangan dipakai sebagai dasar" 30/9), inspirasional paling tipis (organik 1/124). Naskah kita sendiri 41/50 komedi (82%; kode ulang pic-data 14/15, kappa 0,86), beat hangat Season 1 9,2% durasi. [pic-data 6/10] Label ARAH hanya untuk vonis pic-data atau kategori ber-pembanding; frekuensi di video pemenang, label penulis, dan n=1 = KESAN (8 teknik diturunkan, lihat CHALLENGE-PICDATA).
- **Jalur paling aman = campuran:** buka dan jalankan lucu, haru atau bangga di 10–20% terakhir ([pic-data 6/10] usulan penulis, bukan temuan: P01 menopang nada lucu, bukan letak beat haru). Naskah H/I murni boleh diuji (uji "sisi hangat" 1 video, ACC 6/10, baca ≥48 jam terhadap median akun sendiri), hook dan 0–30% tetap ringan. [pic-data 6/10] Satu video hanya membaca eksekusi dan komentar; membaca genre butuh ±10 video per genre (simpan, efek 2×) atau ±15 (share).
- **Deadpan ≠ tanpa emosi:** wajah Lastri tetap datar; emosi dibawa tindakan, benda, gestur kanon (ketuk helm, klik pulpen), reaksi Yaqin/Selo, dan ruang napas ≥3 dtk (usulan uji).
- **Haru = pengorbanan yang penonton lihat lebih dulu**, bukan reveal yang dibatalkan Lastri "sudah tahu". Emosi utuh dalam satu video. [pic-data 6/10] Tanam ≤50% / bayar ≥60% = usulan dari satu video (agunk #03); semua rentang % di struktur S-* = usulan penulis. Pengorbanan Lastri = waktu atau tenaga, bukan tidak makan; tanpa isyarat lapar.
- **Inspirasi = perjuangan nyata** (melawan keadaan atau waktu, bukan mutu produk), hasil diperlihatkan; Yaqin/Selo sesekali pahlawan kecil, Lastri tetap penuntas. Kalimat moral tidak pernah jadi baris terakhir. [pic-data 6/10] Tanpa klaim mutu mutlak ("belum pernah diulang") dan tanpa kesan antrean pesanan; "penuntas" berarti tindakan Lastri menyelesaikan masalah, bukan hanya menerima atau menilai (kasus H3).
- **Urutan menulis:** jawab 5 pertanyaan pembuka (genre · emosi target · siapa yang berubah · siapa memberi apa dan siapa yang tidak tahu · mesin/penutup sebelumnya) → tulis 3 versi kalimat terkuat → saring pagar/kanon/kembar → pengganti membawa emosi yang sama.
- **Rotasi** 5 bentuk penutup dan kode mesin = catatan jadwal, bukan aturan (Hannes 6/10).
- **Pagar genre:** tanpa kematian, agama, kesehatan mental, sakit, anak nyata, romansa, kemiskinan sebagai tontonan, nada kesal; Lastri tidak menangis/tertawa (tertawa perlu ACC). [pic-data 6/10] APD tetap untuk tokoh yang "dihukum" atau menyerahkan helmnya (kasus H2).
- **[pic-data 6/10] Challenge:** `deliverables/riset-sosial/BELAJAR-SCRIPTWRITER-06Okt/CHALLENGE-PICDATA.md` (42 klaim: LOLOS 15 · TURUN 22 · GUGUR 5). Rubrik review dengan kolom Haru/Inspirasi = usulan v2 di skill pic-data, menunggu ACC Hannes.

## 3b. Format brief untuk Hannes (WAJIB, ACC 22 Okt 2026)
Setiap kali Hannes minta "brief" video (serial, konten lepas, iklan), sajikan dengan **`FORMAT-BRIEF-HANNES.md`** di folder skill ini. Urutannya:
1. Brief singkat ACC berbahasa awam, dengan rasa utama, hook 3 detik, dan momen spesial per episode. Tidak boleh ada episode flat.
2. Cek pembaca buta + pic-data.
3. Brief per scene dengan kotak "Ringkasan episode (untuk Rengga)", dikirim dalam PDF lewat `tools/md2pdf.py --landscape`.
4. Hannes me-review ceritanya.
5. Sesudah ACC: **satu kartu Anvil per episode untuk Rengga**. Sebelum ACC, tidak ada kartu.

Format serah §4 di bawah tetap dipakai untuk naskah teknis yang diserahkan ke pic-kreatif/pic-data.

## 4. Format serah (wajib dipakai)
Per episode/video:
1. Judul · logline 1 kalimat · posisi di arc (hari cerita).
2. **Genre + emosi target + teknik yang dipakai:** `Genre: K/I/H/campuran (asal → kita bila adaptasi)` · emosi target + siapa yang berubah · kode teknik `PLAYBOOK-GENRE` (KOM/INS/HAR/CAM, R1–R8) · jenis penutup · beat tempat emosi non-komedi dibayar.
3. Hook (teks + ucapan) · recap.
4. **Tabel beat:** `Dtk mulai–selesai | Tokoh | Dialog/VO | Aksi singkat | Teks layar`.
5. Punchline (dtk) · tag · cliffhanger.
6. **Hitungan (skrip):** durasi total, kata/dtk per baris, jumlah baris lip-sync per tokoh.
6b. **Kode teknik humor** (KOM/R/W) + baris reaksi yang ditulis di tabel beat; untuk naskah komedi, hasil **daftar periksa "apakah naskah ini lucu?"** (§5b, jumlah "ya" dari 12).
7. **Catatan untuk pic-kreatif:** produk & kebutuhan acuan footage (kode shotlist bila tahu), hal visual yang penting untuk lelucon. Tanpa prompt AI.
8. **Untuk dicek pic-data:** klaim, asumsi lucu, risiko pagar.
9. **Bahan caption untuk pic-sosmed:** 1 pertanyaan dari dalam cerita (opsional dipakai pic-sosmed).
10. **Adaptasi referensi:** peta mesin (beat asal yang dipotong → pembawa barunya).

Season/outline: tabel episode (judul · hari cerita · mini-payoff · cliff · produk) + peta benang cerita + kanon yang dipakai.

## 5. Daftar periksa naskah (sebelum serah)
- Semua pagar (agent `pic-scriptwriter` bagian Pagar) lolos dengan pencarian kata: harga/Rp, "KW", "galvanis", nama klien, "Stocky", "kisah nyata/asli".
- Lastri menyelesaikan masalah di setiap episode.
- K3: tak ada adegan berisiko (di bawah/di dalam pallet mesh, bak truk, tidur dekat tumpukan atau jalur forklift).
- Durasi & tempo dihitung skrip; angka yang belum dihitung ditulis "belum dihitung".
- Dialog dicek dengan `cek_dialog.py` terhadap target per tokoh di `BAHASA-DIALOG.md` (partikel, sapaan per episode, kalimat tanya, kata/kalimat; Lastri tetap di bawah korpus); angka sebelum/sesudah dicatat di bagian Hitungan.
- Prosa catatan dirapikan (humanizer); **dialog tidak dihumanize** (bahasa tokoh tetap).
- **Tanpa lelucon gaji, upah, denda, atau uang antara atasan dan pekerja**; taruhan hanya es teh satu pabrik (ACC 9 Okt).
- **Tanpa sisipan promosi/iklan di tengah sketsa organik** (ACC 9 Okt).
- Punch terbaca tanpa suara; baris reaksi tertulis di tabel beat.

## 5b. Daftar periksa "apakah naskah ini lucu?" (naskah komedi; ACC 9 Okt)
Jawab ya/tidak. Kurang dari 8 "ya" → tulis ulang sebelum ke pic-data. Asal: `deliverables/belajar-naskah/wenjiang/ANALISA-HUMOR-WENJIANG.md` §12.
1. **Siapa yang tidak tahu dirinya lucu?** Ada satu tokoh yang serius sepenuhnya (Yaqin/Selo), dan tidak ada yang menjelaskan leluconnya.
2. **Siapa penonton lurusnya?** Ada wajah datar yang ditulis sebagai baris sendiri di tabel beat (siapa, berapa detik), minimal sekali di tengah dan sekali di sekitar punch.
3. **Bentuk logikanya sah?** Kesimpulan absurd lahir dari langkah-langkah yang masing-masing masuk akal (silogisme, perintah dipatuhi, pepatah diuji).
4. **Ada ≥3 anak tangga** dan tiap anak tangga lebih absurd dari sebelumnya? (B1 P2: pangkas jeda, bukan anak tangga.)
5. **Punch terlihat:** kalau suara dimatikan dan subtitle dibaca sekilas, punch tetap terbaca dari gambar, benda, atau wajah?
6. **Punch utama di 55–80% durasi**, dan punch pertama (tawa kecil) ≤15 dtk?
7. **Ada ekor sesudah punch** (3–8 dtk: tag, pembalikan kedua, wajah ditahan), bukan langsung kartu akhir?
8. **Penutup tidak sama dengan 2 naskah sebelumnya** (vonis kata / tindakan tanpa kata / wajah ditahan / gambar akhir / pembalikan dengan logika lawan)?
9. **Lastri menuntaskan** dengan tindakan atau satu kalimat, dan menang tanpa curang?
10. **Lintas penonton:** lelucon tidak bergantung pada satu kata daerah atau satu istilah teknis yang hanya orang dalam paham?
11. **Kata/dtk dihitung:** Lastri ≤2,0, lainnya ≤2,6, klip ≤5 dtk, total ≤59 dtk (skrip, bukan kira-kira)?
12. **Pagar:** tidak menertawakan pekerja/pelanggan, tidak ada gaji/uang/denda, K3 aman (APD, tidak ada orang di bawah/dalam pallet mesh atau bak truk, tidak tidur dekat tumpukan atau jalur forklift), tanpa stereotip suku/daerah/gender, 1 produk bermerek, klaim hanya dari FAKTA PRODUK, tanpa harga/promo/ajakan beli di organik?

## Alur riset iklan (B12, wajib — Hannes 1 Okt)
Setiap permintaan riset untuk ads: (1) pic-data riset iklan pemenang · (2) pic-ads pilih produk yang di-boost (paralel dengan 1) · (3) pic-kreatif + pic-scriptwriter tulis brief · (4) approval CMO · (5) sajikan ke Hannes. Detail `memori/LOG-PAGAR.md` B12. Jangan lompati tahap.

## Pelajaran sequence dari kreator referensi (Hannes 3 Okt — baca `knowledge/rhj-pelajaran-kreator-referensi.md`)
- **Sekuel menyusut** (TikTok Eps 2 = 0,45% Eps 1; Rampok Bank IG Part 4 = 0,27×): tiap episode berdiri sendiri, punya mini-payoff + recap ≤36 karakter.
- **Mini-arc 4–5 part tayang rapat**; kerangka genre yang dihafal penonton, satu tahap per part; part tengah "rencana vs kenyataan" dibuat bisa ditonton tanpa konteks.
- Premis boleh ditahan jadi **cliffhanger Eps 1**, hook detik 0 tetap ber-kata. Cliff berupa pertanyaan yang bisa dijawab penonton.
- **Judul part akhir menepati janji** — jangan umumkan batal; antiklimaks hanya sebagai twist di dalam cerita.
- **Produk = alat/rintangan, bukan penyelamat**; episode yang berubah jadi iklan anjlok. Lastri menyelesaikan dengan kecerdikan.
- **Gaya liputan serius untuk hal konyol** (klaim absurd sebelum dtk 5, ditutup kalimat moral): absurd boleh di skala/kebiasaan, tidak boleh di klaim produk. Jangan pakai "Kisah Sukses"/"Directed by"/nama tokoh kreator lain.

## Referensi @agunkperkasa (Hannes 6 Okt — baca `REFERENSI-AGUNKPERKASA.md`)
Bedah 20 reels teratas (`deliverables/riset-sosial/BEDAH-AGUNKPERKASA-06Okt/BEDAH-NASKAH-DIALOG.md`). n=20 dari 1 akun = arah.
- **Tokoh publik membawa jangkauan, naskah membawa keterlibatan:** 7/8 video ≥100 rb memuat tokoh/satir (tidak kita pakai), tetapi yang ber-dialog punya like/views 5,48% vs 2,43% dan komentar 0,24% vs 0,062%. [pic-data 6/10] Arah, n=3 vs 5; tanpa #08 ⚑: 5,48% vs 2,77% dan 0,240% vs 0,073%.
- **Mesin lelucon yang dipakai:** R1 salah paham bertingkat lewat pertanyaan pendek · R2 literalisasi · R3 pengempis satu kalimat · R4 flash-forward/bookend · R5 daftar tiga belok di butir ketiga · R6 kebohongan dibayar gambar · R7 tag ≤3 dtk · R8 punch ≤5 kata yang bisa dikutip. Tulis kode mesinnya di catatan naskah.
- **Rotasi:** formula yang menang turun ke 9,6% sehari kemudian dan 0,6% tiga minggu kemudian ([pic-data 6/10] sebagian besar regresi dari outlier #01; dalam kelipatan median akun 174× → 106× → 11× → 1,7× dalam 2 bulan; arah). Mesin yang sama jangan berturut-turut (usulan 1× per 7 hari di konten lepas, menunggu ACC).
- **Lastri tetap menang:** jawaban harfiah Yaqin/Selo hanya setup; penyelesaian milik Lastri. Literalisasi diuji K3.
- **Tidak dipakai:** tokoh publik/politik, satir pemerintah/program, makian (dipindai `cek_dialog.py`), dialog Inggris, kartu "A FILM BY/Directed by".
- Checklist dan 3 naskah latihan (≤25 dtk, bukan produksi) ada di file referensi.

## Referensi @jazziesillona (Hannes 6 Okt — baca `REFERENSI-JAZZIESILLONA.md`)
Bedah teks layar, tutorial, dan caption reels teratas filmmaker HK (video asli HP, tanpa VO), **v2 final**: 18 video unik tanpa ⚑ + 7 kontrol, di `deliverables/riset-sosial/BEDAH-JAZZIESILLONA-06Okt/BEDAH-TEKS-NARASI.md`. Arah, bukan aturan; aturan §1–2 tetap. Tidak dikaitkan ke iklan (brief Meta v2 dibatalkan 4/10).
- **Gaya akun, bukan resep:** judul ≤0,5 dtk (17/18 vs kontrol 7/7), judul dua tingkat (15/18 vs 6/7), tanpa VO (0/18 vs 0/7). [pic-data 6/10, kontrol 9/9: 8/9, 7/9, VO 1/9; kesimpulan sama] Hook ber-kata dtk 0 tetap aturan kita (bukti dari agunk + riset 30/9).
- **Pembeda = topik tutorial:** hook janji 9/18 vs 0/7; tutorial 1,25–1,85× median tahun (pic-data). Struktur: janji di atas hasil → langkah dari sisi penonton, satu per layar → hasil 25–60% durasi → CTA yang mengulang data langkahnya (video sales: ukuran, beban, jumlah). Ekor ≤3 dtk (agunk R7) hanya untuk sketsa.
- **Teks ringan:** blok padat ≥3,5 kata/dtk dan "baca caption" di layar berjalan dengan like lebih rendah (0,84× dan 0,85× vs 1,34× dan 1,32×; arah). Teks layar ≤2,0 kata/dtk sasaran, ≤2,6 batas; label besar ≤4 kata + sub ≤7 kata.
- **Label = peran cerita** (WHERE YOU ARE → WHAT YOU SAW → …) lebih disukai daripada label teknis (1,32× vs 0,72×, n=1 pasang); [pic-data 6/10: opsi, bukan wajib; n=1 pasang, tahun beda]; label tanya → jawab untuk FAQ tanpa dialog; merek tidak di judul, produk tampil sebagai alat dalam adegan. [pic-data 6/10: merek-tidak-di-judul 3/5 dengan kontrol Apple; dipakai karena pagar soft selling, bukan data]
- **Layar = apa, caption = kenapa** (9/9 tutorial): tulis bahan caption terpisah untuk pic-sosmed. Panjang caption, huruf kecil, kredit produk = gaya 2025–2026, jangan dijadikan aturan.
- **Tidak dipakai:** bahasa Inggris di layar, kartu kredit film, judul film bertahun rekaan (video AI bisa terbaca arsip/kisah nyata).
- Teks layar dihitung dengan `cek_dialog.py` sebagai `Teks VO | dtk | teks`. Checklist dan 2 latihan (J1 video sales pallet mesh, J2 konten lepas Lastri tanpa dialog) di file referensi.

## Catatan perubahan
- **9 Okt 2026 (ACC Hannes, lewat CMO):** diterapkan `deliverables/belajar-naskah/USULAN-UPDATE-SKILL-SCRIPTWRITER.md` bagian A, B, D.
  - Tambah: §2b (pedoman berlabel), butir 6b/9/10 di §4, judul §5 menjadi "Daftar periksa naskah" + 3 butir, §5b daftar periksa lucu, berkas `KAMUS-HUMOR.md` dan `REFERENSI-BELAJAR-NASKAH-8OKT.md`, bacaan wajib di LANGKAH 0, §2.7 di `PLAYBOOK-GENRE.md`.
  - Keputusan Hannes 9 Okt: kanal seri = akun Bu Lastri; usulan kolab dengan akun merek tidak dipakai.
  - **Tidak ada aturan lama yang dihapus atau diganti.** Tag ≤3 dtk tetap (ekor 3–8 dtk = pedoman untuk seluruh bagian sesudah punch). Baris reaksi 0,8–1,5 dtk di checklist PLAYBOOK tetap untuk reaksi sela (reaksi ditahan 2–6 dtk = pedoman tambahan). Mini-arc 4–5 part tetap opsi di samping 3 bagian. Durasi ≤59 dtk, tempo, `cek_dialog.py`, pagar kata, FAKTA PRODUK, dan dua domain tidak berubah.

## Skill pendukung pihak ketiga (21 Okt 2026, ACC Hannes)
`hook-writing` (hook 3 detik: tingkat kesadaran × 8 pemicu; ucapan / visual / teks layar); untuk iklan berbayar lihat juga `ad-creative-brief`. Keduanya diaudit (`knowledge/rhj-skill-pihak-ketiga.md`); pagar RHJ menang.
