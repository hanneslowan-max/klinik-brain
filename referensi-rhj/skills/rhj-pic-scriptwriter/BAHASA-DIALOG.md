# Panduan Bahasa Dialog — Bu Lastri (pic-scriptwriter)

**Status:** panduan tetap pic-scriptwriter, ditulis 1 Okt 2026 atas program latih bahasa CMO (permintaan Hannes 1/10).
**Dasar:** korpus pic-data `deliverables/riset-sosial/KORPUS-DIALOG-SHORTMOVIE-01Okt.md` + `.json` (129 video short movie TikTok, 43 akun, 34.698 kata). Persentil per video dihitung dari kolom json (n=129; subset video ≤60 dtk n=20).
**Latihan pertama:** `deliverables/LATIHAN-DIALOG-SCRIPTWRITER-01Okt.md` (Eps 1–4, CC1, S1, C3).
**Skrip cek:** `cek_dialog.py` di folder skill ini (bagian F).

Kesimpulan pic-data: naskah kita kaku bukan karena kata baku. Penyebabnya sapaan di ujung hampir tiap kalimat, partikel yang nyaris tidak ada, kalimat yang terpotong jadi fragmen, dan tokoh yang jarang bertanya. Panduan ini memperbaiki keempatnya **tanpa** membuat Lastri cerewet.

---

## A. Target angka per tokoh

Cara baca: angka per 100 kata baru stabil di tingkat season atau batch (≥100 kata per tokoh). Di naskah 260 kata, satu kata saja sudah menggeser rasio ±0,38 per 100 kata. Untuk satu episode, pakai **aturan hitungan** di kolom kanan.

| Metrik | Korpus (gabungan · per video p25–p75 · video ≤60 dtk) | Naskah v4.3.1 | **Lastri** | **Yaqin & Selo** | **Bos (telepon)** |
|---|---|---|---|---|---|
| Partikel per 100 kata | 5,91 · 3,97–8,0 · median 7,46 | 0,76 (Lastri 0,72; Y+S 1,10) | **2–4**, sengaja di bawah korpus (setara p10–p25 per video: 2,27–3,97) | **4–8** (p25–p75 korpus) | 0–3 |
| Aturan per episode | | | 0–1 partikel (maks 2 di episode ≥35 dtk) | ≥1 partikel per tokoh bila ia punya ≥2 baris | boleh 0 |
| Kata per kalimat | 5,12 · 4,22–5,68 · ≤60 dtk p25–p75 3,19–4,87 | 2,45 (Lastri 2,62; Y+S 2,33) | **2,5–3,5**, di bawah korpus. Fragmen boleh bila jadi ketukan lucu | **3,2–4,9** (≤60 dtk p25–p75) | 2,5–4 |
| % kalimat ≤5 kata | 61,7% · 53,3–75,9% · median 81,4% | 99,1% | bebas | ≤92% (≤60 dtk p75 = 91,9%) | bebas |
| % kalimat tanya | 19,5% · 12,9–27,0% · median 20,4% | 8,5% (Lastri 7,5%; Y+S 5,1%) | **10–20%** (tanya pendek dan datar) | **15–30%** | bebas |
| Sapaan Pak/Bu/Mas/Mbak | 1,16/100 kata; kalimat bersapaan per video median 1,8%, p75 8,3%, p90 14,5% | 12,31/100; 30,2% kalimat (Y+S 51,3%) | **≤1 sapaan per episode** di luar kanon dan punchline; ≤10% kalimat | **≤1 per tokoh per episode**, di awal giliran; ≤15% kalimat per season | 0; cukup "Lastri." |
| % kalimat dibuka penanda (eh/ya/oh/wah/aduh…) | 13,7% · per video 5,5–18,6% | 2,8% | ≤10% | 8–20% | bebas |
| Bentuk tak baku (nggak/udah/aja) | 88–96% | sebagian "sudah/saja" | ≥90%. Pengecualian kanon: "Nggih", "Es tehnya sudah siap." (Eps 12) | 100% | boleh baku saat memutuskan (kesan) |
| Kata/dtk per baris | bicara 2,15 | maks 2,33 | **≤2,0** (tempo tenang; brief CC1 "batas Lastri ±2"). Batas keras tetap 2,6 | ≤2,6 | ≤2,6 |

Yang **tidak** dihitung sebagai sapaan: nama bergelar sebagai rujukan ("Pak Yaqin. Operator senior."). Skrip memisahkan "sapaan vokatif" dari total token.
Sapaan yang **dibebaskan dari jatah**: sapaan yang menjadi bahan lelucon (Eps 1 Selo memanggil tukang las "Mas"; jawaban Lastri "Nggak apa-apa, Mas."), kalimat khas kanon ("Yaqin, Pak?"), dan jawaban Lastri ke Bos ("Nggih, Pak.").

---

## B. Partikel: fungsi dan contoh

Angka korpus = per 100 kata · jumlah akun pemakai dari 43. Semua contoh buatan sendiri dalam konteks pabrik, bukan kutipan korpus.

| Partikel | Fungsi | Korpus | Contoh | Siapa |
|---|---|---|---|---|
| **ya** | minta persetujuan; menutup perintah supaya tidak galak | 2,14 · 42 | "Besok truk masuk jam tujuh, ya." | Lastri boleh (perintah), Y+S |
| **kan** | mengingatkan hal yang dianggap sudah jelas; juga dipakai ngeles | 0,72 · 37 | "Kan tadi udah dibilang, lipat dulu." · Yaqin: "Kan dari dulu juga begini, Bu." | Lastri (datar), Y+S |
| **kok** | protes atau heran | 0,56 · 35 | "Kok rodanya beda sebelah?" | Lastri (heran datar, bukan marah), Y+S |
| **sih** | melunakkan, atau penasaran | 0,57 · 32 | "Ini kawatnya berapa mili, sih?" · "Nggak salah sih, cuma kebalik." | Y+S. Lastri jarang (bisa terdengar kesal) |
| **deh** | menyerah, atau menyuruh dengan halus | 0,27 · 30 | "Ya udah deh, saya angkat lagi." · "Cek labelnya dulu deh, Mas." | Y+S. Lastri jarang |
| **tuh** | menunjuk yang agak jauh; "lihat sendiri" | 0,43 · 33 | "Tuh, engselnya kebalik." | Lastri (sambil menunjuk pulpen), Y+S |
| **nih** | menunjuk yang dekat; menyodorkan | 0,56 · 29 | "Nih, label spek rodanya." | semua |
| **dong** | mendesak | 0,25 · 27 | Selo ke Yaqin: "Geser dong, truknya mau mundur." | Y+S ke sesama. **Lastri tidak** (terdengar galak atau manja) |
| **lho/loh** | kaget ringan; memperingatkan. Rasa Jawa, ada di kanon logat Lastri | 0,15 · 22 | "Lho, ini kan kardus kemarin?" · "Jangan diinjak, lho." | Lastri (≤1 per episode), Y+S |
| **kali** | dugaan, sering sambil menyindir | 0,07 · 15 | "Salah baca label kali, Pak." | Y+S (jarang) |
| mah | penanda Sunda/Betawi | 0,18 · 14 | tidak dipakai | tokoh kita bukan Sunda/Betawi |
| to/toh | penanda Jawa | 0,01 · 3 (kesan) | tidak dipakai dulu | belum ada di daftar logat ACC (lho, wes, nggih, ra popo) |

Aturan pakai: maksimal 1 partikel per kalimat pendek. Untuk Lastri, partikel berfungsi sebagai alat (mengingatkan, menunjuk, memperingatkan), bukan hiasan.

---

## C. Pola percakapan

Label dari korpus: **kuat** = ≥10 dari 43 akun · **sedang** = 5–9 akun · **kesan** = <5 akun atau tidak bisa diukur andal (whisper tidak memisahkan penutur).

| # | Pola | Label | Cara pakai di naskah kita | Contoh buatan |
|---|---|---|---|---|
| 1 | **Protes lewat pertanyaan:** "Kok…?" (29 akun), "Masa…?" (16), "Apaan sih" (15), "Kok bisa?" (12) | kuat | Saat tokoh tidak setuju, tulis sebagai tanya, bukan pernyataan. Lastri bertanya datar, tidak menghardik | Selo: "Masa saya lagi yang angkat?" · Lastri: "Kok kosong semua?" |
| 2 | **Pertanyaan balik pendek** (hah?, apa?, serius?, maksudnya?) | kuat (34 akun) | Reaksi Y+S terhadap perintah atau kabar mengejutkan. Lastri memakai versi gema yang datar | Selo: "Hah? Dilipat?" · Lastri: "Seminggu?" |
| 3 | **Pembuka "eh"** (27 akun), **"ya udah"** (20), **"oh iya"** (20), wah/wih (26), aduh | kuat | eh = kaget, menyela, teringat · ya udah = menerima, menutup debat · oh iya = baru ingat, sering untuk ngeles. Y+S cukup 1 pembuka per episode | Yaqin: "Oh iya, kardusnya… belum diangkat." · Selo: "Ya udah, saya pinggirin." |
| 4 | **Akhiran "-in" lebih umum dari "-kan"** (83× di 26 akun vs 14× di 9 akun) | kuat | Y+S: beresin, pinggirin, lipetin, naikin. Lastri lebih sering memakai bentuk dasar atau di- ("Lipat." "Dilipat."); "-in" boleh. "-kan" hanya untuk teks resmi yang dibacakan (SOP, surat) | "Rapiin dulu, baru pulang." |
| 5 | **Ngeles:** "sebenernya" (19 akun), "maksudnya" (11), "nggak kok", "nggak apa-apa" (19), "nggak usah" (19) | kuat | Senjata utama Yaqin dan Selo saat ketahuan. Ngeles yang baik memberi alasan yang salah tapi yakin | Yaqin: "Sebenernya itu stok, Bu. Stok… cadangan." · Selo: "Nggak kok, cuma lewat." |
| 6 | **Menyindir.** "Masa… aja nggak…?" (bagian dari pola Masa, kuat), "tuh kan" (8), "enak aja" (6), "ya ampun" (8) | sedang | Sindiran Lastri berupa pertanyaan pura-pura polos, satu kalimat, tanpa senyum. Jangan nyinyir panjang | Lastri: "Forkliftnya ikut istirahat juga?" |
| 7 | **Atasan ke bawahan:** perintah pendek ditutup "ya"; tokoh berwenang bergeser ke bentuk baku saat memutuskan | kesan | Lastri memerintah tanpa marah, sering tanpa subjek. Bos boleh lebih baku dan tegas karena perannya ancaman | Lastri: "Lipat dulu, ya." · Bos: "Lastri. Besok saya sidak." |
| 8 | **Bawahan ke atasan:** sapaan di **awal** giliran, bukan di ujung tiap kalimat | kuat (37 akun memakai sapaan, hanya 5,4% kalimat) | "Bu, …" sekali di depan, lalu kalimat berjalan tanpa sapaan | Yaqin: "Bu, gudang belum siap, gimana nih?" |
| 9 | **Sapaan beruntun waktu gugup** | kesan (1 contoh) | Boleh sebagai lelucon, maks 1× per episode, dan tetap dihitung | Selo: "Siap, Bu. Sebentar, Bu. Hampir, Bu." |
| 10 | **Gaya bapak-bapak** (Yaqin): yakin, merujuk pengalaman, plesetan, nasihat | kesan | "Dari dulu juga…", "Percaya sama saya", plesetan. Selalu dipatahkan Lastri | Yaqin: "Dari zaman saya muda, pallet ya kayu, Bu." |
| 11 | **Kata ganti:** aku/kamu (37 akun), gue/lu (31), saya (36; dipakai ke atasan atau dalam peran resmi) | kuat | Semua tokoh memakai "saya" ke Lastri dan Bos. Yaqin ke Selo boleh "kamu". **Tidak memakai gue/lu** | |
| 12 | **"Makasih"** dipakai 78% (vs "terima kasih") | kuat | Semua tokoh, kecuali teks resmi | "Makasih, Pak." |
| 13 | **Interupsi, kalimat tak selesai ("…")** | kesan | Pakai untuk ketukan lucu saja. Naskah lama memakai "…" di 7,5% kalimat, korpus 1,0% | "Itu… cadangan." |
| 14 | **Tokoh datar menjawab sangat pendek ke lawan yang bicara wajar** | kesan (terlihat di 1–2 video, tidak dihitung) | Datarnya Lastri baru lucu kalau Yaqin dan Selo bicara cair. Kalau semua tokoh bicara pendek, yang terasa kaku, bukan datar | Yaqin (panjang dan yakin) → Lastri: "Spek?" |
| 15 | **Logat daerah** | kesan (korpus kurang mewakili Jawa; whisper merusak ucapan Jawa) | Yang memandu adalah kanon, bukan korpus: Lastri "nggih / lho / wes / ra popo", ≤1 per episode | "Ra popo. Diulang." |

---

## D. Kaku → natural (contoh buatan)

| # | Tokoh | Kaku | Natural | Yang berubah |
|---|---|---|---|---|
| 1 | Selo | "Maaf, Bu. Saya terlambat." | "Aduh, telat lagi. Bannya kempes, Bu." | pembuka "aduh", alasan ngeles, sapaan pindah |
| 2 | Yaqin | "Troli itu tidak bisa didorong, Bu." | "Bu, trolinya kok seret, ya?" | protes jadi tanya; kok + ya; sapaan di depan |
| 3 | Lastri | "Apakah forklift sudah diparkir?" | "Forklift udah diparkir?" | "apakah" dan "sudah" dibuang; tetap pendek |
| 4 | Lastri | "Tolong rapikan tumpukan tersebut." | "Rapiin yang itu, ya." | "tersebut" jadi tunjukan; -in; "ya" penutup perintah |
| 5 | Yaqin | "Saya sudah memeriksa labelnya, Bu." | "Udah saya cek, Bu. Tenang aja." | udah/aja; nada yakin khas Yaqin |
| 6 | Selo | "Saya tidak tahu, Bu." | "Hah? Saya nggak tahu, Bu." | pertanyaan balik pendek; nggak |
| 7 | Selo | "Mari kita makan siang." | "Makan dulu, yuk." | "mari kita" jadi "yuk" |
| 8 | Lastri | "Mengapa helm Anda tidak dipakai?" | "Helmnya mana?" | pertanyaan datar 2 kata; tanpa "Anda" |
| 9 | Yaqin | "Ini sudah biasa, Bu. Tidak ada masalah." | "Dari dulu juga begini, Bu. Aman." | gaya bapak-bapak: merujuk pengalaman |
| 10 | Yaqin ke Selo (bisik) | "Mas, Bu Lastri datang, Mas." | "Eh, eh, diem. Orangnya lewat." | sapaan ganda dibuang; "eh" berulang |
| 11 | Selo | "Baik, Bu. Akan saya kerjakan." | "Siap, Bu. Saya beresin." | "akan… kerjakan" jadi "beresin" |
| 12 | Lastri | "Terima kasih, Pak." | "Makasih, Pak." | bentuk yang dipakai 78% penutur |
| 13 | Yaqin | "Bu, itu bukan saya, Bu." | "Bukan saya. Sebenernya… itu Selo." | ngeles "sebenernya"; sapaan dobel dibuang |
| 14 | Lastri | "Saya tidak suka dibilang mirip artis Korea." | "Saya dari Klaten." | penjelasan diganti kalimat kanon yang lebih pendek |
| 15 | Selo | "Bu, kenapa saya yang disuruh, Bu?" | "Kok saya lagi, Bu?" | kok-protes; sapaan sekali |
| 16 | Lastri | "Apakah kalian sudah makan?" | "Udah makan?" | sisi hangat kanon, tetap 2 kata |
| 17 | Yaqin | "Jangan khawatir, Bu. Saya yakin." | "Tenang, Bu. Yakin banget saya." | "banget"; susunan lisan (predikat di depan) |
| 18 | Bos | "Lastri, saya akan datang untuk melakukan sidak." | "Lastri. Besok saya sidak." | "akan… untuk melakukan" dibuang; tetap tegas |
| 19 | Lastri | "Kardus tersebut berisi apa, Pak?" | "Itu isinya apa?" | "tersebut" jadi "itu"; tanpa sapaan |
| 20 | Selo | "Saya sedang beristirahat, Bu." | "Lagi istirahat, Bu. Bentar aja." | sedang→lagi; aja |

---

## E. Anti-pola

1. **Sapaan di ujung tiap kalimat.** "Cadangan, Bu." "Biar kelihatan penuh, Bu." "Antre kayak tukang cukur, Bu." Di naskah lama 51% kalimat Yaqin dan Selo begini. Korpus: 5,4%, dan biasanya di depan. Kecuali sapaan yang menjadi bahan lelucon atau gugup yang disengaja (C9).
2. **Kalimat lengkap seperti terjemahan.** Subjek, predikat, dan objek lengkap ditambah "akan / sedang / untuk / dengan / melakukan". "Saya akan pergi untuk mengambil pallet." → "Saya ambil palletnya dulu."
3. **Kata baku kaku:** tersebut, apakah, mari kita, merupakan, oleh karena itu, dengan demikian, bagaimana, sangat, Anda; juga tidak/sudah/saja di dialog. Korpus: "tersebut" dan "merupakan" dipakai 0 akun, "apakah" 4 akun, "mari kita" 1 akun.
4. **Slang yang tidak cocok dengan pabrik di Jakarta Barat dan tokoh Jawa:** gue/lu, guys, bestie, wkwk, literally, anjir/buset, "kau" gaya sinetron, "mah/kagak" (Sunda/Betawi). Gue/lu memang ada di 31 akun korpus, tetapi itu gaul anak muda Jakarta. Pabrik kita berbicara dengan "saya", dan atasannya perempuan dari Klaten.
5. **Partikel ditabur.** Lebih dari 1 partikel di kalimat pendek, partikel di tiap baris Lastri, "dong/deh/sih" di mulut Lastri. Kalau partikel Y+S di atas 8 per 100 kata, buang yang paling tidak perlu.
6. **Lastri jadi cerewet:** menjelaskan leluconnya sendiri, kalimat di atas 8 kata, dua alasan dalam satu baris, membalas protes dengan protes, nada kesal ("!" beruntun). Temuan kuat skill §1: nada kesal menurunkan.
7. **Telegraf tanpa ketukan:** fragmen beruntun yang tidak membawa jeda lucu ("Maaf, Bu. Macet."). Fragmen hanya dipakai sebagai ketukan punchline.
8. **"…" di banyak baris.** Pakai untuk satu ketukan lucu, bukan sebagai gaya.
9. **Memaksa angka korpus ke satu baris.** Target berlaku per season dan per tokoh. Jangan menambah partikel ke kalimat kanon ("Yang ngelas juga saya.") supaya angkanya naik.

---

## F. Cara cek otomatis

Skrip: `.claude/skills/rhj-pic-scriptwriter/cek_dialog.py` (Python 3, tanpa pustaka luar). Definisi kata, kalimat, partikel, sapaan, kalimat tanya, dan pembuka penanda **sama dengan skrip korpus pic-data**, jadi angkanya bisa dibandingkan langsung. Uji 1/10: dijalankan pada 70 ujaran dialog brief v4.3.1, hasilnya cocok dengan laporan pic-data (2,45 kata/kalimat · sapaan 12,31/100 · 30,2% kalimat bersapaan · 8,5% tanya · Lastri 2,62/0,72/8,63 · Y+S 2,33/1,10/21,98/51,3%). Partikel total keluar 0,77, sedangkan laporan menulis 0,76 karena menjumlahkan nilai per partikel yang sudah dibulatkan.

**Format masukan** (satu baris dialog per baris, UTF-8):
```
## Eps3
Lastri | 3 | Macetnya di mana?
Selo | 3 | Di kepala. Baru lancar.
Lastri VO | 4 | Mas Selo. Sopir. Forklift. Selow.
Yaqin | 3 | Paling seminggu.
Selo VO | + | Taruhan? Es teh satu pabrik.
```
Kolom: tokoh (tambahkan `VO` untuk narasi atau suara luar frame) · durasi baris dalam detik (`+` = masih di shot baris sebelumnya, tempo dihitung gabungan seperti di brief) · teks yang diucapkan. Baris `##` = kelompok (episode/video).

**Jalankan:**
```
python3 .claude/skills/rhj-pic-scriptwriter/cek_dialog.py naskah.txt
python3 .claude/skills/rhj-pic-scriptwriter/cek_dialog.py sebelum.txt sesudah.txt
```

**Keluaran:** per tokoh (dan Yaqin+Selo) jumlah kata dan kalimat, kata/kalimat, % ≤5 kata, partikel/100 dan rinciannya, sapaan/100 (total dan vokatif), % kalimat bersapaan, % tanya, % dibuka penanda, porsi tak baku, kata baku-kaku yang ditemukan; sapaan vokatif per tokoh per episode beserta jatah "Yaqin, Pak?"/"Selow" (>1 ditandai); kata/dtk per baris dengan tanda `MELANGGAR tempo >2,6`, `Lastri >2,0: cek di uji suara`, dan `klip lip-sync >5 dtk`; pencarian kata pagar (harga/Rp/promo/KW/galvanis/Stocky/kisah nyata).

**Batas skrip:** ia tidak menilai lucu atau tidak; "…" dihitung sebagai pemisah kalimat (ketukan lucu ikut menurunkan kata/kalimat); kamus partikel tertutup; "kali" dan "ya" sesekali salah tangkap; angka per 100 kata belum stabil di bawah ±100 kata per tokoh.

**Urutan kerja:** tulis naskah → isi berkas masukan → jalankan → cocokkan ke tabel A (season) dan aturan per episode → perbaiki baris yang keluar batas → catat angka sebelum/sesudah di bagian "Hitungan (skrip)" format serah.

---

## G. Temuan @agunkperkasa (6 Okt 2026)

Sumber: `deliverables/riset-sosial/BEDAH-AGUNKPERKASA-06Okt/BEDAH-NASKAH-DIALOG.md` §4. Dialog Indonesia yang terbaca jelas hanya 160 kata dari 3 video (#03, #05, #06), jadi semua butir di bawah berlabel **kesan**, kecuali G1 yang merupakan pagar merek. Target di tabel A tidak berubah.

| # | Temuan | Angka | Cara pakai |
|---|---|---|---|
| G1 | **Makian sebagai punch** (tolol, anjing, asu/wasu) dipakai akun referensi | 3/20 video (#02 gestur, #05, #14) | **Terlarang** di naskah RHJ, termasuk sebagai plesetan. `cek_dialog.py` kini mencetak baris "Makian/hinaan" (daftar `MAKIAN` di skrip); harus "bersih". [pic-data 6/10] Pindai berbasis kata: "anjing" (hewan) dan "bodoh" non-hinaan ikut tertandai (diuji: "asuransi" tidak tertandai); tinjau manual, catat bila harfiah |
| G2 | **Straight man bertanya lebih dari separuh kalimatnya** di sketsa salah paham | Kepala #05: 5 tanya dari 9 kalimat (55,6%) | Di episode berbentuk interogasi, porsi tanya Lastri boleh melewati 20%. Target season tetap 10–20%; jangan dua episode interogasi berturut-turut |
| G3 | **Punch memakai kata dari kalimat setup** ("kayak manusia" → "kita kan anjing") | #05; gema serupa di #10 ("Radical Break" diulang) | Lastri menggemakan satu kata Yaqin/Selo dengan datar ("Beranak?"), dan tag mengulang kata itu sekali lagi. Paling banyak 2 kali per video supaya tidak jadi pola tetap |
| G4 | **Sapaan di ujung kalimat sebagai penanda pangkat** saat melapor | Petugas #05: "pak" di 4 dari 6 kalimat (66,7%) | Tidak mengubah anti-pola E1. Boleh hanya sebagai bagian lelucon (C9), mis. "Lapor, Bu." di kalimat pertama |
| G5 | **Monolog berbeda dari dialog** | Monolog #10: 7,29 kata/kalimat, partikel 0,91/100; dialog sketsa 4,71 dan 7,50 | Narasi VO Lastri boleh lebih panjang per kalimat dari dialognya, asal ≤2,0 kata/dtk dan tanpa ceramah |
| G6 | **Tempo sketsa terpadat** | #05: 2,09 kata/dtk durasi total, per baris ±2,0–3,0 (segmen whisper kasar) | Batas ≤2,6 (Y+S) dan ≤2,0 (Lastri) tidak perlu dinaikkan |
