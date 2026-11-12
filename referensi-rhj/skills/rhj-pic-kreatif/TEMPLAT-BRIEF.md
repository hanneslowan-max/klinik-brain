# Templat brief pic-kreatif v1.3 (RESMI sejak 9 Okt 2026, ACC Hannes; disusun 8 Okt 2026; v0 = Fase 0, v1 = + @almostaaamovie, v1.1 = + @actuallyaway, v1.2 = + @wenjiang_courtyards: humor, v1.3 = + @angankara: rumah produksi, BTS, cover)

**Status:** v1 = v0 + temuan 35 video @almostaaamovie (34 film, `almostaaamovie/ANALISA-SINEMATOGRAFI-ALMOSTAAAMOVIE.md`; n = 1 akun, hanya pola akun ini, bukan hukum). Program 500 video dihentikan Hannes 8/10, jadi `PLAYBOOK-SINEMATOGRAFI-VIDEO-PENDEK.md` tidak dibuat; bagian `[PLAYBOOK]` kini diisi rentang akun ini dan ditandai `[AAA n=34]`. Perubahan v1 ditandai **[v1]**. **v1.1** menambah temuan @actuallyaway (seri "The Last Train", 8 episode, merek Away; `actuallyaway/ANALISA-SINEMATOGRAFI-ACTUALLYAWAY.md`; n=8 episode, satu merek besar): ditandai **[v1.1]** dan **[AA n=...]**. Tidak mengubah brief yang sudah ada di kartu Anvil (RD-01 v3, PM-06 v3). **v1.2** menambah humor (@wenjiang_courtyards; B12, aturan 16-19) dan **v1.3** menambah rumah produksi, BTS, cover (@angankara; B13-B14, aturan 20-24). **RESMI 9 Okt 2026 (ACC Hannes):** ini templat brief baku pic-kreatif; usulan di `USULAN-UPDATE-SKILL-KREATIF.md` sudah diterapkan ke skill dan agent. **Salinan kerja** ada di `.claude/skills/rhj-pic-kreatif/TEMPLAT-BRIEF.md` (dan `skills/rhj-pic-kreatif/`); bila berkas ini diubah, salin ulang dan cek `diff`. Path analisa di templat relatif terhadap `deliverables/belajar-kreatif/`. Label rentang: [AAA n=34] @almostaaamovie, [AA] @actuallyaway, [WJ n=51] @wenjiang_courtyards, [AN] @angankara (diringkas **[ANG]** di skill); semua rentang acuan satu akun, bukan hukum.

**Dua lapis, karena dua pembaca:**
- **Lapis A, Brief Cerita** (untuk Rengga/manusia): mengikuti `TEMPLATE-BRIEF-RENGGA.md` v3 (Hannes 6/10: cerita + script per scene, bebas berkreasi, 1–2 halaman, tanpa detik/frame/ukuran shot/gerak kamera/tabel shot). Tambahan yang tetap dalam kata biasa: baris **Referensi** dan baris **Rasa/tampilan**.
- **Lapis B, Lembar Produksi Sinematik** (untuk pic-produksi-video dan QC; **tidak dikirim ke Rengga** kecuali Hannes meminta): target tampilan terukur, tabel shot, rencana suara, standar produksi. Ini yang selama ini hilang: v3 menghapus target tampilan, v1 menumpuknya jadi prompt panjang.

## 0. Sembilan aturan keras (7 dari Hannes 8/10 + 2 dari SKILL produksi) + aturan 10-24 dari temuan akun referensi
1. **Frame target wajib.** Sebelum shot ditulis: 3–5 frame referensi dengan kode (T1…T5) dan lembar banding hasil vs target tiap shot. Referensi yang belum ditonton tidak boleh dipakai.
2. **Prompt = sinematografer, pendek.** Sudut + lensa/kedalaman · cahaya (arah, jam, warna) · susunan benda · **satu aksi** · gerak kamera · suasana suara. Larangan maksimal satu baris ("No text, no logos").
3. **2–4 variasi untuk shot kunci** (`count`); pilih take yang **sambung** dengan shot sebelumnya, bukan yang paling cantik sendiri.
4. **Musik/ambien dirancang**, bukan hening: ambien + SFX di titik aksi + musik berlisensi/Sound Collection; mix −14 LUFS; hening disengaja hanya sebelum punchline.
5. **Tidak ada render final 480p.** Iterasi `draft` 480p, finalize take terpilih ke ≥720p (idealnya 1080p).
6. **Pagar di checklist QC, bukan di prompt.** Huruf/logo/angka/K3/FAKTA PRODUK dicek di hasil (zoom 100%); acuan yang berhuruf/berpelat dibersihkan sebelum diunggah.
7. **Shot masalah dan shot pahlawan produk tidak boleh dibuang tanpa alasan tertulis** (kolom B2). Dua shot itu kerja iklan, bukan hiasan.
8. **Still sebelum animasi harus sudah sinematik** dan diukur terhadap target (luma, p98, R−B, saturasi). Still datar = video datar.
9. **Produk asli kita sebagai acuan belum terbukti** (uji #11 memakai benda generik): rencanakan omni_reference 1–2 foto bersih dan uji 1 shot sebelum produksi penuh (±35 kr).

10. **[v1] Sistem identitas seri atau cover wajib dirancang** (B10): judul 2–4 kata, satu warna merek (#B51B1B), satu tipografi (Montserrat), satu kartu akhir, cover bukan frame acak. Akun referensi: 35 dari 35 cover = poster rancangan; cover = frame 0 hanya 3 dari 35 [AAA n=35].
11. **[v1] Kartu judul/ pembayaran punch di AKHIR** untuk cerita; hook awal memakai gambar atau satu kalimat. Akun referensi: kartu akhir/tengah 25 dari 34, kartu awal 6 dari 34 [AAA n=34]. Tahan 1,5–2 dtk sesudah punch (iklan ≤30 dtk); episode haru boleh 6–12% durasi.
12. **[v1] Suara tidak boleh hening panjang.** Rentang akun referensi: RMS rata-rata −21,4 .. −16,8 dBFS (median −18,7), hening (<−45 dB) 0–15,3% (median 3,15%) [AAA n=34]. Master PM-06 70% hening = di luar rentang. Hening disengaja hanya sebelum punch dan ≤10% durasi.
13. **[v1] Penempatan produk harus dipilih dari 4 cara** (B2): alat cerita, properti set, ECU tangan memakai produk (4–5 dtk), atau klaim langsung. Klaim langsung dan grafis korporat di tengah cerita tidak dipakai (pagar klaim). Akun referensi: produk sebagai alat ±10–35% layar tanpa merek disebut vs iklan langsung ±49% (views terendah, n=1 vs 2, bukan bukti sebab).

14. **[v1.1] Produk dipakai, bukan dipajang.** Tiap kemunculan produk berupa tindakan (diduduki, ditarik, dibuka, dibawa, dipasang), bukan foto produk diam atau kalimat fitur. Akun referensi: koper tampak 29,0% sampel (n=449 sampel 2 dtk), hero/ECU 6,2%, merek terbaca di barang 0 dari 9 video [AA]. Untuk iklan ≤30 dtk: produk tampil maks 1 shot ECU 1,5-2 dtk + sisanya sebagai alat.
15. **[v1.1] Satu shot pahlawan produk di AKHIR cerita**, sesudah punch (bukan di hook): akun referensi menyimpan 3 ECU bergaya iklan (±14 dtk, 10% durasi) di episode terakhir dan menutup musim dengan produk [AA Ep08]. Hook memuat benda sebagai pertanyaan (frame 0), bukan sebagai penjelasan.

16. **[v1.2] Brief humor menulis teknik primer dari Kamus (H1-H18, `wenjiang/ANALISA-VISUAL-HUMOR-WENJIANG.md`) dan detik PUNCH + panjang TAHAN sesudahnya (B12).** Akun referensi humor [WJ n=51 fiksi]: shot akhir median 6,7 dtk, ≥4 dtk pada 39 dari 51; ritme melambat di sepertiga akhir (2,92 / 2,82 / 1,97 shot per 10 dtk). Punch tanpa tahan = tidak terbaca.
17. **[v1.2] Humor lewat REAKSI, bukan aksi:** 39 dari 51 [WJ] memuat CU reaksi datar; waktu CU 35% durasi (IQR 16-59%). Brief menulis siapa bereaksi, ukuran, dan tahan (dtk). Komedi fisik (jatuh, pukul, ketinggian, alat potong, api, listrik) tidak ditulis di brief RHJ (K3); tunjukkan AKIBAT, bukan aksinya (H12).
18. **[v1.2] Premis harus terbaca tanpa suara dan tanpa bahasa:** 1 benda atau 1 ekspresi sebagai bukti visual (uji: tonton tanpa suara, tanpa teks; premis masih terbaca?). Teks layar satu kalimat per tampil (H15). Akun referensi ini ditonton lintas bahasa dengan subtitle Inggris; kita berbahasa Indonesia, jadi teks boleh, tetapi bukti visual tetap wajib.
19. **[v1.2] 'Dunia serius' dijaga:** cahaya siang datar, kostum seragam, set yang berulang; tokoh berwajah lurus. Lucunya dari situasi, bukan dari merendahkan orang (pekerja, pelanggan, penerima). Jangan campur dua look dalam satu seri (humor siang-datar [WJ luma 113, p98 224] vs drama gelap [AAA luma 73, p98 186]).
20. **[v1.3] Brief rumah produksi manusia memuat PAKET SERAHAN, bukan "satu video":** master 16:9 ≥1920×1080 + versi 9:16 asli 1080×1920 dipotong ulang (tolak berkas yang isinya <90% luas kanvas: @angankara punya 13 file 2023-Jan 2025 dengan isi 22-32% luas), cover poster bertitel + file sumber, 2 still, 1 klip BTS 15-20 dtk, kartu akhir wordmark 1-2 dtk, .srt + subtitle tertanam, proyek/EDL, lisensi musik, rilis talent/lokasi (B13).
21. **[v1.3] Target look ditulis dengan angka dan frame; default vendor bukan target RHJ.** Rumah produksi ini menyetel look per klien: luma 49,5 (seri sendiri, n=9), 82,5 (klien musik, n=38), 117,5 (iklan merek, n=3) [AN n=65]. Tulis T1-T5 + luma/p98/R−B/sat sasaran; lembar banding di G2.
22. **[v1.3] Hook ≤3 dtk dan tidak ada layar hitam >0,5 dtk di awal.** Seri sendiri [AN-UN n=9]: cut pertama median 1,5 dtk, 8 dari 9 membuka dengan dialog/teks premis; film dengan 13 dtk hitam di awal = 2.137 views. Judul seri = overlay, bukan layar penuh di awal.
23. **[v1.3] Satu warna kunci per proyek; "dua palet = dua waktu" bila perlu.** Palet produk dipakai pada kostum/set (Nipis Madu: hijau). Merah #B51B1B hanya aksen.
24. **[v1.3] BTS adalah aset kontrak, bukan konten kebetulan.** Format "BTS vs FINAL" terbagi dua adalah dua BTS tertinggi (14,7-14,8 rb vs median 3.711 untuk 7 BTS lain; n=2: deskripsi). RHJ: footage asli gudang vs hasil iklan (bukti produk asli; label AI platform ON).

## Lapis A — Brief Cerita (1–2 hal)
1. Judul/meta: `BRIEF <KODE> "<Nama>" (v<n>)` · untuk · dari · status ACC · format 9:16 (+4:5 bila Meta Feed) · maks durasi.
2. **Tujuan** (1 kalimat; tujuan bisnis + halaman tujuan/WA, message-match).
3. **Referensi** (baru): link referensi, tanggal ditonton, dan satu kalimat "yang ditiru = …; acuan pola saja". Kartu produksi tanpa link referensi tidak dibuat (pelajaran 8/10).
4. **Jalan cerita** (3–5 kalimat) + kanon yang menentukan lucu/harunya.
5. **Per scene** (3–6): apa yang terjadi + script persis (penutur) + mood. **Wajib ada scene "masalah"** (apa yang rusak/macet/menghambat terlihat) dan **scene "pahlawan produk"** (produk menyelesaikan masalah dan tampil sebagai pahlawan), atau satu kalimat alasan bila dibuang.
6. **Rasa/tampilan (kata biasa, 2–3 baris, baru):** mis. "cahaya emas sore dari samping, bayangan panjang; meja baja gelap; satu warna menonjol: hijau roda; tenang, tidak terburu". Angka target ada di Lapis B, bukan di sini.
7. **Kebebasan Rengga** (eksplisit) · **Pagar ≤6 butir** · **Aset acuan** (nama) · **Selesai =**.
8. **[v1] Benda tanam-bayar** (1 baris): benda atau bunyi yang ditanam di awal dan dibayar di akhir (pintu, HP bergetar, roda hijau). Dikodekan di B3 sebagai insert 1,2–2 dtk.
9. **[v1] Cara produk tampil** (1 baris dari 4 pilihan aturan 13) + kapan produk pertama terlihat + sisa layar yang diizinkan (≤35% sebagai alat; ≤15% sebagai properti).
10. **[v1] Sistem identitas** (1 baris; rincian B10): judul kartu akhir, warna, cover.

## Lapis B — Lembar Produksi Sinematik
### B0. Gerbang referensi (G0)
| Isi | Wajib |
|---|---|
| Link, platform, tanggal ditonton, siapa yang menonton (agent/Hannes), durasi, resolusi file yang dilihat | ya |
| Ukuran terukur (`skrip/ukur.py`): n shot, median shot, cut pertama, luma, p98, R−B, saturasi, hening%, RMS | ya, atau "tidak terukur" + alasan (mis. #08: video tak terbaca → tidak boleh dijadikan standar mutu) |
| Frame target T1…T5 (detik + deskripsi 1 baris: ukuran/sudut/cahaya/komposisi) | ya; gambar di lembar banding (tidak masuk repo bila milik kreator) |
| "Apa yang membuatnya bekerja" 1 kalimat (mekanisme, bukan topik) | ya |
| Bukti performa referensi + bias (iklan konsep? organik? ukuran akun?) | ya |

### B1. Struktur referensi vs versi kita
| Elemen referensi | Dipertahankan / diubah / dibuang | Alasan (pagar, K3, produk, pembeli) |
|---|---|---|
| (beat 1 … n, ritme, lokasi, cahaya, suara) | | |
Aturan: perubahan > 3 elemen inti = tulis ulang kenapa referensi ini masih dipilih (uji "apakah premisnya masih lucu/menyentuh bagi pembeli kita", bukan bagi penonton referensi).

### B2. Shot masalah, shot pahlawan, dan penempatan produk **[v1]**
| | Shot (kode) | Terlihat apa | Durasi tampil | Alasan bila dibuang |
|---|---|---|---|---|
| Masalah | | | | |
| Pahlawan produk | | cara tampil: gerak + cahaya + sudut + suara material (bukan foto katalog) | | |
**Penempatan produk [v1, +v1.1]:** kapan produk pertama terlihat (dtk) · % sampel 1 frame per 2 dtk memuat produk · dtk hero/ECU · cover memuat produk (y/n, ukuran) · kartu merek (dtk dan lama) · cara = `alat cerita` / `properti set` / `ECU tangan memakai produk` / `klaim langsung` · detik produk pertama terlihat · total detik tampil dan % durasi (hitung; ATURAN NOL) · ukuran di frame (ECU / ≥50% tinggi / ≤20% tinggi) · dipegang tokoh ya/tidak · logo atau label terbaca ya/tidak (hanya dari foto asli, overlay) · kalimat yang menyebut produk (kutip, ≤1) · klaim angka (hanya setelah dicek Hannes). Rentang akun referensi [AAA n=11 film dengan benda/merek kunci]: alat cerita ±10–35% layar; ECU bukti 4–5 dtk; properti set ±4%; klaim langsung ±49%.

### B3. Tabel shot (satu baris per shot; semua kolom terisi)
`# | dtk | beat | ukuran | sudut | gerak | cahaya (arah, jam, warna) | **sumber cahaya yang terlihat di bingkai (y/n, apa)** [v1] | DOF | komposisi (posisi subjek, lapisan depan/tengah/latar) | **lapis depan buram (y/n, apa)** [v1] | frame target | sumber (t2v/omni/I2V/asli/edit) | variasi | suara/SFX | teks`
- Ukuran: ECU/CU/MCU/MS/WS/OVH/INS/OTS/POV. Gerak: satu per klip (STATIC/PUSH/HAND/PAN/ORBIT/FPV; klip AI ≤5 dtk).
- Total: ≥3 ukuran berbeda bila ≥15 dtk. **Cut pertama dibandingkan dengan referensi** (usulan v0: tidak lebih dari ±1 dtk dari referensi tanpa alasan tertulis; angka ini dikalibrasi ulang dari katalog). Tiap shot satu fungsi beat.
- Hitung otomatis di brief: jumlah shot, median, kata layar, kata/dtk, kata sebelum punchline (ATURAN NOL).
- **[v1] Rentang akun referensi [AAA n=34 film]:** shot median 2,45 dtk (IQR 1,90–3,35); cut pertama median 2,0 dtk (18 dari 33 ≤2 dtk, 10 >4 dtk, satu >60 dtk di UI webcam); 3,0 shot/10 dtk (IQR 2,4–3,2); komedi 2,44, horor+thriller 2,76, drama 3,01 dtk (n=19/7/6). Ritme tidak berkorelasi dengan views (rho +0,23 shot median; n=34); jangan menjadikan "lebih cepat" sebagai target.
- **[v1] Frame 0:** komedi premis terbaca tanpa suara 15 dari 19; horor 3 dari 7; drama 3 dari 6 [AAA]. Wajah jelas ≤2 dtk 18 dari 34, ≤4 dtk 28 dari 34. Brief menyebut kenapa frame 0 membaca atau, bila gelap/ruang kosong, alasannya.
- **[v1] Satu tokoh per bingkai:** 'single bergantian' di 31 dari 34 film; dua orang satu frame hanya di WS pembuka/penutup atau 2shot khusus.

### B4. Kitab tampilan (terukur)
| Ukuran | Target (dari referensi terukur) | Toleransi | Cara cek |
|---|---|---|---|
| Luma rata-rata | mis. 111 (ref #11) | ±15, dan dalam 85–115 target RHJ | `ukur_still.py` pada still; `ukur.py` pada klip |
| Highlight p98 | 185–215 | tidak >235 | idem |
| Hitam p2 | ≥8 | | |
| Saturasi | ref ±0,05 (RHJ 0,28–0,40) | | |
| R−B | ref ±10 | | |
**[v1] Rentang akun referensi [AAA n=34]:** luma 73,0 (IQR 52–89; komedi 86, horor+thriller 54), p98 186 (IQR 164–204), p2 9, saturasi 0,40 (IQR 0,30–0,46), R-B +15,9. Target RHJ luma 85–115 berada di sisi terang rentang ini; tentukan target dari referensi iklan (ref #11: 111), bukan dari akun drama ini. Cahaya hampir selalu SATU sumber yang bisa ditunjuk (lilin, lampu meja, jendela, tabung fluoresen). DOF dangkal 27 dari 34.
Tulis juga: sumber cahaya (di mana, arah, jam), palet + **satu warna pahlawan** (merah #B51B1B untuk overlay/merek; hijau roda; dll), grain, fps (24), lensa setara (35 mm lebar; 50–85 mm CU), satu LUT. Still yang gagal ukur diperbaiki **sebelum** animasi.

### B5. Rencana suara
**[v1] Rentang akun referensi [AAA n=34]:** RMS rata-rata −18,7 dBFS (−21,4..−16,8); hening 3,15% (maks 15,3%); modulasi 2–8 Hz median 0,38 (dialog); pola suara 'musik' (dugaan dari RMS dan onset) pada 5 dari 34, dialog alami pada 27. Seedance bawaan −36,9 dB (n=1) tidak boleh menjadi master.
Ambien (apa, level) · SFX per titik aksi (kode shot + detik) · musik (sumber berlisensi, mood, BPM, di mana masuk/berhenti; **berhenti ≤0,5 dtk sebelum punchline** bila komedi) · VO/dialog (sumber, penutur) · mix −14 LUFS, true peak ≤ −1 dBTP · bunyi yang tidak boleh ada.

### B6. Teks layar
**[v1] Subtitle:** akun referensi memasang subtitle dua baris (ID atas, EN bawah, kuning tebal) pada 33 dari 34 film di ±75–85% tinggi frame, yaitu di zona UI bawah; RHJ memasang subtitle di pita aman. Kartu akhir: judul tebal di hitam + garis kredit kecil.
Pita aman **y 285–1248 px dari 1920 (50,2%)**, kanan 130 px kosong; tinggi huruf ≥3% (58 px); kata terkunci dari naskah; gradasi gelap di pita bila latar terang; **tidak menimpa tangan/benda kunci** (cek lembar frame); kata/dtk ≤ batas pic-scriptwriter.

### B7. Standar produksi dan biaya
Model (Seedance 2.5 / Kling 3.0), mode (t2v / omni_reference / I2V + `end_image`), `draft` → finalize, resolusi akhir, jumlah variasi per shot (aturan 3), **kredit dihitung dengan `get_cost` per jenis operasi** (ATURAN NOL; t2v ≠ omni_reference), plafon dan siapa yang ACC.

### B8. Checklist QC (pagar; dicek di hasil)
☐ nol huruf/angka/logo terbaca dari AI (zoom 100%) · ☐ produk cocok foto acuan (bentuk, warna) · ☐ FAKTA PRODUK (pallet mesh custom ya; lemari arsip tidak; finishing electroplating, bukan "galvanis"; tanpa harga/KW/Stocky) · ☐ K3 (APD, tak ada orang di bawah/di dalam pallet mesh, alat manual) · ☐ 1 orang per frame sampai uji multi-tokoh lulus · ☐ wajah tak mirip orang nyata · ☐ HP/UI tidak terbaca · ☐ tanpa merek pihak ketiga/klien · ☐ label AI platform ON, tanpa tulisan "AI" dari kita · ☐ tiap shot dibanding frame target · ☐ bookend sebingkai · ☐ audio −14 LUFS, tanpa clipping · ☐ teks di pita aman, tidak menimpa subjek · ☐ durasi ≤59 dtk (B16).

### B9. Gerbang keputusan
Sebelum produksi penuh: (1) G0 lulus · (2) uji 1 shot dengan produk asli lulus (aturan 9) · (3) ACC kredit. Sesudah draf: lembar banding hasil vs frame target → QC pic-kreatif (cerita, script, pagar, tampilan vs target terukur) → ACC Hannes. Brief tidak menulis "ulang maksimal sekali tanpa tanya": cantumkan **opsi tanpa kredit (perbaikan di editing)** di samping opsi generate ulang.

### B10. Sistem identitas seri dan cover **[v1]**
| Elemen | Isi (satu pilihan) | Cek |
|---|---|---|
| Nama seri atau judul episode | 2–4 kata kapital, satu kalimat yang dibayar di akhir | tidak menjelaskan punch |
| Kartu akhir | judul tebal di hitam, 1–1,5 dtk, garis kredit kecil (nama akun), tanpa CTA kedua | huruf di editing |
| Warna dan tipografi | #B51B1B + putih/hitam; Montserrat (judul), Roboto (kecil) | sama di semua episode seri |
| Penanda nomor | angka/pita bertumpuk pada judul (referensi: Part 2 = angka magenta di atas lime) | warna kedua hanya untuk nomor |
| Cover/thumbnail | rancangan poster: still sinematik + judul 2–3 baris di sepertiga atas (y 285–700) + wajah atau benda; bukan frame 0 acak | zona aman; tanpa huruf AI |
| Set/kostum seri | satu set + satu kostum yang dipakai ulang (efisiensi kredit; akun referensi memakai ulang ruang yang sama di beberapa film) | konsistensi look antar-episode |
| Format pengenalan tokoh | satu tokoh per bingkai di latar polos, satu cahaya samping, nama + peran sebagai overlay (referensi: part 1 'rekrutmen') | Soul ID kanon, tanpa wajah mirip orang nyata |
| **[v1.1]** Blok judul cover | posisi tetap di semua episode: baris merek kecil di ±37% tinggi, nama seri besar di ±45-56%, "Episode n" kiri dan nama seri kanan di ±62-66% [AA, 9 dari 9 cover]; foto latar berubah per episode | cek zona aman 4:5 dan potongan grid 3:4 |
| **[v1.1]** Kartu merek | "Produksi [merek]" 2-3 dtk di detik ±6-20 sesudah janji visual (bukan di 0 dtk dan bukan di tengah cerita); satu kali per episode atau tidak sama sekali [AA: trailer 6,6-9,2; Ep01 20-23; Ep02-08 tidak ada] | huruf di editing; label AI platform ON; satu merek per episode (dua domain) |
| **[v1.1]** Label seri | satu kalimat tetap di tiap episode (referensi: "inspired by an actual story" 9 dari 9 video) | RHJ hanya bila isi benar (kiriman nyata + izin); selain itu label netral "Serial [nama]" |
| **[v1.1]** Grading seri | satu LUT/kurva: hitam p2 15-25, highlight p98 150-185, R-B +20..+30, saturasi 0,30-0,35, CV luma antar-episode ≤0,15 [AA ep01-07 n=7: CV luma 0,10; sat 0,05] | beda dengan target iklan (ref #11 luma 111, p98 194): jangan dicampur |

### B11. Peluncuran seri **[v1.1]**
| Elemen | Isi | Catatan referensi [AA] |
|---|---|---|
| Teaser | 1 hari sebelum part 1, ≤40 dtk: benda di frame 0, label, kartu seri di detik 6-9, pertanyaan tema, kartu tanggal di akhir | trailer 37,3 dtk, 91.411 views (15,8% dari Ep01) |
| Jadwal | tanggal part berikutnya ditulis di caption tiap part (caption = pic-sosmed) | "Episode 05 releases 8/26" |
| Rilis serentak | bila ukuran = views per part, jangan rilis ≥3 part sama hari | Ep01-03 sama hari: Ep02 −57,0%, Ep03 +2,1% |
| Ajakan | "kirim ceritamu" lewat WA yang sudah ada, bukan "beli"; tanpa hardsell di video | caption Ep08 dan carousel |
| Penutup musim | carousel di balik layar dari foto/footage asli + kredit tim (dengan izin) | carousel 4 gambar, 1.313 likes |
| Distribusi | **[keputusan Hannes 9 Okt]** kanal seri/episode = **akun Bu Lastri**; TIDAK membuat akun IG merek terpisah dan TIDAK memakai post kolaborasi dengan akun merek RHJ/OYAMA untuk episode; satu merek per episode (dua domain disjoint; episode roda dan episode pallet mesh tidak dicampur dalam satu video) | [AA] semua 9 post kolab @away (8.528 vs 768.482 followers): pola referensi, TIDAK ditiru; RHJ memakai akun Bu Lastri |

### B12. Humor **[v1.2]** (hanya bila brief bertujuan lucu)
Satu blok per video; semua baris terisi (angka dihitung, ATURAN NOL). Rentang [WJ n=51 fiksi, 60 konten unik; satu akun, pola bukan hukum].
| Elemen | Isi yang ditulis | Rentang akun referensi [WJ] |
|---|---|---|
| Teknik primer (+1 sekunder) | kode Kamus H1-H18 dan satu kalimat 'apa yang lucu' | LOG 17, SALAH 11, FISIK 8, SOL 5, METAFORA 4 (teknik utama, n=51) |
| Panggung | WS terkunci: apa yang terjadi di bingkai, posisi subjek, ruang kosong (kolom komposisi B3) | 8 dari 51 sepenuhnya tanpa kata; sisanya WS lalu CU |
| Reaksi | siapa, ukuran (CU/MS), tahan dtk, ekspresi (datar, melirik, diam) | CU 35% durasi; CU median 2,77 dtk per shot; tahan akhir 4-7 dtk |
| PUNCH | detik jatuh punch dan apa yang menjadi punch (kalimat, benda, wajah, akibat) | penutup reaksi-CU 21 dari 51; EWS dua sosok menjauh 10 dari 51 |
| TAHAN | panjang shot terakhir (dtk), ada musik atau ambien, ada teks atau tidak | shot akhir median 6,7 dtk; ≥4 dtk 39 dari 51 |
| Benda/properti | benda sebagai argumen (ECU 1-2 dtk) dan lapis depan (tepi bingkai) | METAFORA 4; benda di teknik lain belum dihitung |
| Suara humor | ambien kontinu di bawah dialog; titik SFX; hening hanya bila disengaja | RMS −20,5 dBFS, hening median 0%, akhir ≥6 dB lebih pelan 15 dari 51 |
| Cut pertama | detik (target ≤3 dtk bila organik) | median 3,4 dtk; ≤2,5 dtk 17 dari 45 |
| Uji tanpa suara/teks | 'premis terbaca? y/n' dan benda/ekspresi pembuktinya | belum diukur di akun referensi |
| Bukan-lucu (pagar) | daftar yang tidak boleh: kekerasan, ketinggian, api, listrik, alat potong, merendahkan pekerja/pelanggan, politik, klaim angka produk | |
Catatan kalibrasi: B5 aturan 4 'musik berhenti ≤0,5 dtk sebelum punchline' berasal dari [AAA]; akun humor [WJ] tidak memakai hening sebelum punch (ambien tetap). Dua sekolah; belum ada bukti mana yang lebih baik untuk kita. Uji satu klip masing-masing bila Hannes ACC.
Korelasi views: hanya cut pertama yang konsisten (rho −0,43, n=45; klaster unggahan identik berbeda 63x-2.536x), jadi 'cut pertama cepat' boleh jadi target, bukan 'lebih lucu = lebih banyak views'.

### B13. Brief rumah produksi manusia **[v1.3]** (hanya bila vendor, bukan agent/Rengga)
Satu halaman, semua baris terisi. Rentang [AN n=65 milik + 7 kolab; satu rumah produksi].
| Elemen | Isi yang ditulis | Rentang akun referensi [AN] |
|---|---|---|
| Tujuan + halaman tujuan | message-match, satu merek (dua domain disjoint), segmen | - |
| Paket serahan | master 16:9 + 9:16 asli + cover poster + 2 still + BTS + kartu akhir + .srt + proyek + lisensi | 13 file kanvas 9:16 berisi gambar 22-32% luas (2023-Jan 2025); 0 dari 19 sejak Feb 2025 |
| Target look | T1-T5 + luma/p98/R−B/sat | luma 49,5-117,5; p98 160-211; sat 0,28-0,56; R−B +12,8..+43,5 |
| Warna kunci | satu per proyek; merah #B51B1B hanya aksen | magenta/merah-pink/hijau/kuning per proyek |
| Cahaya + set | sumber terlihat, 1 lapis depan buram, tanpa jib/dolly/drone | 3-10 kru; kamera 6 dari 9 BTS; panel/pemantul 4 dari 9 |
| Hook + ritme | hook ≤3 dtk; cut pertama ≤2 dtk; shot median 2-3 dtk; <60 dtk | UN: cut1 1,5; shot 2,0; 60 dtk |
| Suara | −14 LUFS; ambien kontinu; subtitle 1 baris | RMS −17,4 dBFS; hening 0,5% |
| K3 + FAKTA PRODUK | induksi, APD, zona forklift; tanpa orang di bawah/di dalam pallet mesh; electroplating (zinc plating) bukan galvanis; tanpa harga Rp pallet mesh; lemari arsip tidak custom | - |
| Gerbang | G0 referensi, G1 shot list+K3, G2 rough cut (lembar vs target), G3 final (checklist), ACC Hannes | - |
| Biaya | kotasi per deliverable | belum dihitung (tidak ada data) |

### B14. BTS dan pasangan aset **[v1.3]**
Pilih satu pola: (a) layar terbelah 'BTS SHOT / FINAL SHOT' 9:16 (FFmpeg vstack, label kecil, 15-18 dtk); (b) rekaman ponsel handheld 9-20 dtk dengan judul seragam 'BEHIND THE SCENE' 1-3 dtk + kartu akhir wordmark; (c) skit kru: tidak dipakai (kru bukan pemeran). Tulis: apa yang terlihat (alat, jumlah orang), izin tampil, dan label. BTS RHJ memakai footage asli gudang.

## Pola prompt (dari uji #11, 1 shot, text-to-video, 2 variasi, 35 kr)
`<ukuran + sudut + gerak kamera>. <lokasi + jam + arah cahaya + warna>, <kedalaman/lensa>. <susunan benda, 1 kalimat>. <satu aksi, kata kerja konkret>. <suasana suara>. No text, no logos.`
Contoh yang berhasil: "Static low-angle close-up on a sunlit city sidewalk in late afternoon. Warm golden low sun from the left, long soft shadows, shallow depth of field, cinematic 35mm look, subtle film grain. … A woman's hand … reaches in from the top right, passes over the handbag without touching it, picks up the lip balm and lifts it out of frame. Camera locked off. Natural, unhurried motion. Quiet street ambience. No text, no logos." Yang dihindari: 10 baris larangan, spesifikasi teknis produk, banyak foto acuan berlabel.

## Contoh terisi singkat: RD-01 C (hanya B2 dan B3, memakai ref #11)
B2: Masalah = **tidak terlihat di lembar frame draf C** (roda lama/rusak hanya ada di v2; di C masalah hanya hidup di teks) → keputusan: tambah 1,5 dtk roda lama aus di S2 atau tulis alasan buang. Pahlawan = S2 (roda hijau, close-up rendah, DOF dangkal) 1,8 dtk + S4 roda berputar 1,4 dtk.
B3 (cuplikan): `1 | 0–3,6 | HOOK/SETUP | OVH | tinggi | STATIC | matahari sore dari kiri lewat bilah pintu gulung, ±16.00, hangat | sedang | HP kiri-atas, roda kanan-bawah, tangan masuk dari atas; lapisan: bayangan bilah | T1 | omni (1 foto Osaka) | 2 | getar HP di baja, ambien gudang | lencana 1 (0,3–1,0)`; `2 | 3,6–5,4 | CHOOSE | CU rendah | rendah | STATIC | sama | dangkal | roda tajam di tengah, HP/dompet buram | T3 | omni | 2 | "tuk" roda diangkat | —`.
