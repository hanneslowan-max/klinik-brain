---
name: rhj-prompt-flow
description: Playbook Prompter Seedance RHJ (dulu Google Flow; Flow diarsipkan 27 Okt 2026) — menulis prompt video Seedance (ByteDance; 2.5 / 2.0 / Mini) dan prompt gambar start/end frame per scene/shot serial Bu Lastri, memilih mode (start frame, start+end, omni_reference dengan acuan gambar/video/audio, video edit/extension, satu scene multi-beat), mengarahkan akting & aksi, mengecek hasil per frame dengan cek_klip.py, dan mencatat pelajaran ke memori/PELAJARAN-PROMPT-FLOW.md. Dipakai agent prompter-flow. Bahasa Indonesia.
---

# Playbook Prompter Seedance RHJ (dibuat 22 Okt 2026 untuk Google Flow; pindah ke Seedance 27 Okt 2026)

Keputusan Bapak Hannes 27 Okt: "Kita jadi nya ga pakai google flow, terlalu sulit. Kita pakai seedance." Alat produksi video serial Bu Lastri = **Seedance (ByteDance)**. Platform tempat menjalankannya **belum dipastikan** (Higgsfield, Dreamina/CapCut, atau lainnya), jadi playbook ini ditulis tidak bergantung platform; perbedaan per platform ada di §2. Pelajaran khas Flow ada di §11 (arsip).

Agent menulis prompt (bahasa Inggris, siap tempel), mengecek hasil, dan mencatat pelajaran. **Baca `memori/PELAJARAN-PROMPT-FLOW.md` di awal; append pelajaran baru di akhir.** Nama file skill/agent/buku pelajaran sengaja tetap supaya rujukan lain tidak putus.

## 0. Bahan wajib
- Brief per scene: `deliverables/naskah/BRIEF-PER-SCENE-*` (format baku: `.claude/skills/rhj-pic-scriptwriter/FORMAT-BRIEF-HANNES.md`). Episode baru = berdiri sendiri (LOG-PAGAR 27 Okt).
- Kanon tokoh: `deliverables/CHARACTER-SHEET-LASTRI-24Sep.md` (KANON v2), `deliverables/BRIEF-PRODUKSI-LASTRI-BULAN1.md` ([SELO], [YAQIN]).
- Contoh prompt yang sudah diuji (Flow): `deliverables/naskah/PROMPT-EPS12-SCENE1-*` s.d. `-SCENE5-*` (berisi diagnosa tiap uji).
- Bukti Seedance di repo: `deliverables/produksi/RD-01/PROMPT-RD01-v2.md` (prompt persis yang dikirim, Seedance 2.5 R2V), `deliverables/riset-sosial/BELAJAR-PROMPT-MIXX-09Okt/` (80 prompt Seedance 2.5: struktur, durasi, kegagalan teks/logo), `memori/PELAJARAN-PIC.md` 8–9 Okt (PM-06, RD-01, RD-02), `memori/PETA-KLAIM.md` AI-01, AI-15–AI-19.
- Pelajaran arahan dari panduan Hypit (Apache-2.0, dibaca sebagai data): `deliverables/naskah/PELAJARAN-HYPIT-UNTUK-SEEDANCE-27Okt.md`.

## 1. Kunci kanon (tulis di setiap prompt yang memuat tokoh/benda ini)
- **Lastri:** white hard hat, red safety vest with grey reflective stripes, blue-grey work shirt sleeves rolled, black hair in a low bun, no bangs, **no headscarf**, flat expression (no smile, no tears). Tanpa papan nama.
- **Selo:** yellow hard hat, orange reflective vest, navy-blue uniform, muda, santai.
- **Yaqin:** yellow hard hat, navy-blue work uniform, 50-an, kumis tipis beruban, selalu yakin.
- **Kedok/topeng las Bapak:** flat rectangle of matte black pressed fibre, rounded corners, dark-green glass window in a grey metal frame with four rivets, dent in the lower left, wooden handle at the back and not visible from the front; **not a helmet**. Acuan gambar: `ACUAN-KEDOK-BAPAK.jpg` (minta ke MM bila hilang).
- **Lastri kecil:** girl from Central Java with East Asian features, like a young version of a Korean-looking woman (single-lidded almond-shaped dark eye, straight thick black eyebrow), straight glossy black hair in a short low ponytail, plain faded maroon t-shirt with no print; hanya satu mata mengintip dari tepi topeng; tanpa wajah utuh, tanpa anting. Gambar berisi anak dibuat dari teks, jangan diedit (ditolak di Flow; di platform Seedance belum diuji, perlakukan sama).
- **Troli (RH):** steel platform hand trolley, grey deck, black rubber wheels, U handle, tanpa logo.
- Setiap prompt diakhiri **Avoid** baku: `text, letters, logos, name tags, other people` + hal spesifik scene.
- **Bapak tidak pernah tampil.** K3 dijaga (helm, rompi, tidak ada orang di bawah beban).

## 2. Mekanik Seedance

### 2a. Fakta pasti (dicek 27 Okt di Higgsfield `models_explore`, baca saja; cek ulang bila berubah)
| Model | Mode / input | Durasi | Resolusi | Lain |
|---|---|---|---|---|
| **Seedance 2.5** | `t2v` · `omni_reference` (gambar, video, audio acuan) · `video_edit` (edit 1 video acuan; biaya = durasi video itu; durasi & rasio diabaikan) · `video_extension` (maju/mundur) | 4–30 dtk, bilangan bulat | 480p / 720p / 1080p | audio bawaan (default on); `draft` 480p bisa di-finalize ke 1080p ≤7 hari dengan take yang sama |
| **Seedance 2.0** | peran media sama | 4–15 dtk | 480p–4k (1080p/4k hanya mode `std`, paket Plus ke atas; mode `fast` 480/720p) | parameter `genre` (auto/action/horror/comedy/noir/drama/epic) |
| **Seedance 2.0 Mini** | peran media sama | 4–15 dtk | 480p / 720p | murah, `genre` ada |
| Seedance 1.5 Pro | hanya start/end image | 4 / 8 / 12 dtk | 480p–1080p | — |

Peran media yang tersedia di 2.5 / 2.0 / Mini: `start_image`, `end_image`, `image_references`, `video_references`, `audio_references`. Rasio: auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16.

### 2b. Perilaku yang sudah terbukti di produksi RHJ (Seedance 2.5, Okt 2026)
- **Durasi tertulis = durasi hasil** ±1 dtk (mixx 49/51); **urutan beat bertimecode diikuti** (13/13), detik bisa bergeser.
- **Isi gambar acuan ikut terbawa** walau dilarang (pelat, label, papan tanda; PM-06) → bersihkan/potong acuan sebelum dipakai.
- **Jumlah benda mengikuti acuan, bukan kata** ("five" tetap satu unit) → buat still komposisi dulu, lalu animasikan.
- **Video acuan menurunkan semua perilakunya** (kepala orang muncul di tepi; PM-06) → rekam acuan gerak yang bersih (tangan saja, latar polos).
- **Orientasi acuan ditiru harfiah** (roda berdiri di pelat → pelat di bawah) → putar/edit acuan ke posisi yang diinginkan.
- **Frame klip sebelumnya sebagai acuan menyalin komposisinya** → pakai hanya untuk bookend yang memang harus identik.
- **Huruf/logo tetap bisa muncul** walau dilarang (logo Apple di HP, salah eja di mixx) → pagar dicek di hasil; teks & logo dipasang di editing.
- **Audio bawaan pelan** (rata-rata −36,9 dB, n=1) → selalu dimix; tulis "No music" di prompt.
- **Prompt sinematografer pendek bisa setara referensi** (t2v 720p, AI-01); prompt panjang terstruktur menang di Kling S5 (AI-03, arah). Kesimpulan: struktur jelas, boilerplate tidak diulang.
- Job gagal → kredit kembali ±4 menit; 2 take per shot kunci berguna (pilih yang SAMBUNG dengan shot sebelumnya).

### 2c. Belum dipastikan (tulis "belum dipastikan" bila ditanya; catat begitu terbukti)
- Jumlah maksimal gambar / video / audio acuan per request.
- Apakah `start_image` bisa digabung dengan `image_references` dalam satu request (di Flow tidak bisa), dan apakah `end_image` bisa tanpa `start_image`.
- Cara menyebut acuan di prompt per platform: korpus mixx (Seedance 2.5) memakai `@Image1`/`@Video1`; API RD-01 memakai urutan ("Reference image 1 is …") dan berhasil.
- Apakah foto wajah realistis (tokoh AI kita) diterima sebagai acuan, dan apakah gambar berisi anak ditolak.
- Mutu lip-sync dan logat untuk bahasa Indonesia; batas kata per detik.
- Harga kredit saat ini (angka Okt di §9 bisa sudah berubah).

### 2d. Per platform
- **Higgsfield** (bukti: MCP `models_explore` 27 Okt, API RD-01 8 Okt, korpus mixx): Seedance 2.5 / 2.0 / 2.0 Mini / 1.5 Pro tersedia; model gambar untuk start frame di platform yang sama: Nano Banana Pro / 2 / 2.1, Seedream 4.5 / 5.0, GPT Image 2.5, Soul. Saldo aplikasi (kredit langganan) terpisah dari saldo API (US$).
- **Dreamina / CapCut / lainnya:** belum ada bukti di repo. Saat Bapak memakai platform baru, minta tangkapan layar panel setelan sekali, lalu catat nama mode, batas acuan, dan cara memanggil acuan di buku pelajaran.

## 3. Memilih mode

**ATURAN UTAMA (Hannes 22 Okt, terbukti di Flow; berlaku juga di Seedance sampai uji A/B membuktikan lain): setiap video tokoh dari START FRAME.** Rantai: MASTER gambar dari teks + acuan kanon → start frame shot lain = EDIT dari master/shot sebelumnya → image-to-video satu shot per generate; **ukuran shot di prompt = ukuran shot di start frame**.

| Situasi | Mode Seedance |
|---|---|
| Shot tokoh biasa / momen spesial | Gambar start frame (model gambar) → `start_image` → video |
| Aksi fisik A → B (tabrakan, angkat, buka kardus, jatuh) | `start_image` + `end_image`; **end frame = edit dari start frame** ("Do not move the camera … same framing"); 4 dtk; urutkan gerak per detik |
| Klip bicara satu tokoh | Start frame saja (end frame membuat bibir kaku) |
| Gerak tangan detail / ritme / kontak yang harus persis | `video_references` dari rekaman HP asli yang bersih (tangan saja) + peran tertulis "motion reference only"; gabung dengan start frame bila platform mengizinkan (belum dipastikan) |
| Shot lanjutan tokoh yang sama | Frame terakhir shot sebelumnya → edit jadi sudut baru → `start_image` |
| Satu scene 2–4 shot di satu lokasi | **Uji dulu:** `omni_reference` (acuan tokoh + ruang + benda) dengan struktur multi-beat §4. Simpan beat yang bagus, ulang yang meleset per shot dari start frame |
| Jumlah benda tertentu / komposisi rumit | Still komposisi dulu, QC, lalu animasikan |
| Hasil 90% bagus, satu cacat | `video_edit` (ganti benda, warna, arah pandang) sebelum generate ulang; perlu lebih panjang → `video_extension` |
| Iterasi murah | Seedance 2.5 `draft` 480p → finalize 1080p (take sama), atau 2.0 Mini 480/720p. Render final ≥720p |
| Shot benda/produk tanpa tokoh | `omni_reference` dengan foto produk bersih (terbukti RD-01) |

Tunda video sampai **start frame lolos QC** (wajah, kanon, ukuran shot, tanpa huruf).

## 4. Struktur prompt baku

**Per shot dari start frame (default):** pendek, ≤45 kata/dtk, tanpa boilerplate yang sudah dipikul gambar.
```text
Vertical 9:16, <N> seconds. Same framing, lens and light as the start image, <camera: locked / very slow push-in>.
<Sikap tokoh dalam satu kalimat>. <Aksi dengan kata kerja harfiah, urut per detik bila fisik>. <Arah pandang>.
Audio: <dialog persis berkutip + suara (umur, nada, logat Jawa ringan) + "Only <nama> speaks">; <SFX>; quiet room tone. No music.
Avoid: text, letters, logos, name tags, other people, <risiko spesifik shot>.
```

**Multi-beat satu generate (omni_reference / t2v):** urutan blok dari 80 prompt Seedance 2.5 (mixx, 91%) dan uji templat 9 Okt.
```text
Format: vertical 9:16, <N> seconds, Seedance <versi>, <resolusi>.
References: Image 1 = <tokoh>: face, hair and outfit only, do not copy its background. Image 2 = <ruang>: keep <benda penanda, cahaya>. Video 1 = motion reference only: <gerak>; do not copy <orang/ruang>.
Continuity: <kunci kanon §1 sekali tulis>. Location: <ruang + 2–3 benda penanda>. The same people, clothes, props and room in every beat.
Tone: <blok gaya §6> + <satu frasa cahaya yang sama di semua shot satu scene>.
(00:00–00:03) <ukuran shot/cut>. <sikap + aksi>. <kamera>.
(00:03–00:06) Cut to <ukuran shot>. ...
Audio: <dialog berkutip per beat + siapa bicara>; <SFX>. No music.
Avoid: text, letters, logos, name tags, other people, <spesifik>.
```
Aturan tulis: kunci tokoh/benda ditulis **sekali** di Continuity lalu "the same …"; satu beat 1–3 dtk; kalimat pertama beat = ukuran shot; larangan satu baris spesifik (larangan panjang tidak mencegah logo).

## 5. Arahan akting & aksi
- **Sikap dulu, gerak secukupnya** (Hypit): satu kalimat apa yang tokoh pikirkan tentang lawan bicara/benda, lalu 1–2 detail yang menentukan cara kalimat mendarat. Jangan menempelkan gerak tangan di tiap frasa.
- **Lastri datar = sikap yang ditahan:** `flat expression, no smile` tetap ditulis, ditambah sikapnya, mis. "weighs Yaqin's claim with dry, unimpressed skepticism … one eyebrow lifts slightly … lands the line with one small, decisive nod". Punchline: satu kata diberi tekanan datar + satu jeda.
- **Kata kerja harfiah, tanpa kiasan:** "slip out of his hands … does not throw them", bukan "fly up". Nyatakan apakah aksi benar terjadi atau hanya gestur.
- **Yang diucapkan tidak diperagakan:** bila dialog menyebut angka/ukuran/benda, tulis "she only says it; no numbers, signs, labels or extra objects appear". Angka dengan jari tidak andal → angka di editing.
- **Kontak fisik:** satu tokoh DIAM di jalur tokoh lain sejak start frame, hanya satu yang bergerak; tanpa end frame model melunakkan benturan → pakai end frame momen benturan; akhiri klip tepat saat benturan; cairan hanya di gambar diam.
- **Start frame = keadaan yang sedang berlangsung** (sedang mengerjakan sesuatu, wajah netral), bukan puncak reaksi.
- **Tepi adegan:** tokoh masuk sudah sibuk, keluar mulai pergi; tidak berpose, **tidak menatap kamera**.
- **Sumbu pandang:** buat master dua orang dulu (siapa di kiri menghadap ke mana), lalu edit jadi sudut per sisi; tulis arah pandang tiap shot supaya saling bertemu.
- **Satu dunia, sektor berbeda:** shot balik menyebut apa yang kini tampak di belakang tokoh, palet & frasa cahaya sama.
- **Durasi dari naskah:** kalimat + jeda + reaksi (Lastri ≤2 kata/dtk, NSK-18 belum diuji); pecah di tempat pikiran berbelok. Potongan pasti, freeze, cut on action dibuat di editing (prompt "cut" tidak memotong hasil).
- **Tokoh lengkap:** selalu tulis jenis kelamin, umur, rambut, pakaian.

## 6. Gaya
- **Sinematik Hollywood (pilihan Hannes 22 Okt untuk serial):** `Cinematic film still / Hollywood drama, anamorphic lens look, shallow depth of field, soft film grain, warm golden late-afternoon light through a dusty window, motivated practical lighting, slow push-in, off-center composition, restrained acting`. Hindari `glossy, commercial look, perfect lighting`. Seedance 2.0/Mini punya parameter `genre` (`drama`/`comedy`): belum diuji, jangan diandalkan menggantikan blok gaya.
- **Realisme HP (cadangan):** BLOK-REALISME di `PROMPT-EPS12-SCENE3-22Okt.md`.
- Jangan pakai "photorealistic" sendirian; tanpa arahan cahaya/lensa hasilnya foto stok simetris.
- Latar = beberapa benda penanda (kabel las tergulung, rak pipa kotak, beton bekas percikan) dan palet yang dibawa benda nyata, bukan daftar panjang.

## 7. Dialog & suara
- Kalimat Indonesia ditulis persis dalam tanda kutip + karakter suara (umur, nada, logat Jawa ringan) + "Only he/she speaks in this shot". Satu pembicara per klip.
- Bila dubbing terpisah: `mouth closed with lips together, no speech` dan `generate_audio` boleh off.
- Audio bawaan Seedance pelan → selalu dimix di editing; musik dari editing, prompt "No music".
- Suara tokoh konsisten lewat `audio_references`: **belum diuji**; uji sekali sebelum dipakai serial.
- Audio hasil diukur (dB), **tidak didengar** → minta Bapak cek kata yang terucap dan logatnya.

## 8. Cek hasil (wajib sebelum vonis)
`python3 .claude/skills/rhj-prompt-flow/cek_klip.py <video.mp4> <folder_scratch>` → `LEMBAR.jpg` (frame 4 fps), daftar lompatan antar frame (potongan rencana vs patah), dB per 0,1 dtk (di mana ada suara), frame awal/tengah/akhir. Lihat LEMBAR dan frame kunci, bandingkan dengan kunci kanon §1 dan brief. Cek khusus Seedance: isi acuan yang ikut terbawa, jumlah tangan/orang per frame, huruf/logo (zoom), lonjakan zoom di tengah klip. Vonis per shot: PAKAI / PAKAI BERSYARAT / ULANG + alasan yang bisa dilihat + prompt perbaikan (sebut juga opsi 0 kredit: potong/blur/zoom di editing). Link shared yang butuh login tidak bisa dibuka → minta file diunggah.

## 9. Biaya & generate sendiri
**Default (Bapak 27 Okt): Rengga yang generate DAN menulis prompt Seedance sendiri; Bapak hanya butuh brief.** Agent menyerahkan brief (cerita, adegan, dialog, pagar, kanon) dalam paragraf, bukan prompt. Prompt dari agent hanya bila Bapak/Rengga memintanya, sebagai referensi yang boleh diabaikan. Cek hasil klip (§cek) tetap bisa dikerjakan agent bila videonya dikirim. Generate di Higgsfield hanya bila Bapak eksplisit meminta: `get_cost:true` dulu untuk **tiap jenis klip** (t2v ≠ omni_reference), laporkan saldo sesudahnya. Angka Okt (cek ulang, bisa berubah): Seedance 2.5 kredit aplikasi 3 kr/dtk 480p, 7 kr/dtk 720p; omni_reference 720p 5 dtk = 35 kr, 1080p 5 dtk = 60 kr; t2v 720p 5 dtk = 17,5 kr. API (US$): 480p US$0,2056/dtk, 720p US$0,4622/dtk, 1080p US$1,1372/dtk. Nano Banana Pro 2K = 2 kr/gambar.

## 10. Format pelajaran (append ke `memori/PELAJARAN-PROMPT-FLOW.md`)
`- **<tgl> · <eps/scene/shot> · <platform/model/mode>** — Gejala: … · Sebab: … · Perbaikan: … · Status: terbukti / dugaan`
Satu pelajaran per temuan. Bila pelajaran yang sama muncul ≥2× atau berhasil diuji, naikkan ke §2–§7 dan catat di changelog. Sebut platform (Higgsfield/Dreamina/…) di setiap entri Seedance.

## 11. Arsip Google Flow (tidak dipakai sejak 27 Okt; simpan sebagai sejarah & pembanding)
- Karakter dipanggil dengan `@` lalu dipilih sampai jadi chip; `@Lastri` hasil tempel tidak jadi chip → hapus dan ketik ulang `@`.
- Start frame (first-frame I2V) tidak bisa digabung dengan @karakter: pilih start frame ATAU reference-to-video.
- Batas acuan: Veo 3.1 R2V maks 3 gambar & hanya 8 dtk; Omni Flash 1.1 maks 7 acuan, 3–10 dtk; satu karakter Flow bisa terhitung 2 gambar.
- Edit foto berisi anak ditolak ("violating rules"); mengganti BENDA di foto anak buatan AI bisa dicoba.
- Agen Flow kadang menolak multi-shot ("satu generate = satu shot") padahal Omni bisa 3 shot dengan potongan bersih → "try as written", atau pecah per shot.
- Rantai Flow: MASTER dari teks dengan @karakter (Nano Banana) → edit → Frames to Video. @karakter hanya untuk gambar, tidak di video (R2V menafsir ulang wajah).
- Harga Flow/Higgsfield 22 Okt: Omni Flash 1.1 720p 3 dtk = 9 kr, 1080p 4 dtk = 18 kr; Veo 3.1 Lite 4 dtk = 6 kr.

## Changelog
- 22 Okt 2026: dibuat dari pelajaran sesi Eps 12 scene 1–3 (uji Hannes di Flow).
- 27 Okt 2026: **pindah ke Seedance** (keputusan Bapak Hannes). §2 diganti mekanik Seedance (fakta `models_explore` Higgsfield 27 Okt + perilaku terbukti dari RD-01/PM-06/RD-02/mixx + daftar belum dipastikan + per platform); §3 mode Seedance (start frame tetap aturan utama; omni_reference multi-beat = uji); §4 baru: struktur prompt baku (per shot & multi-beat); §5 baru: arahan akting & aksi (pelajaran Flow yang tetap berlaku + 12 pelajaran panduan Hypit, Apache-2.0, dibaca sebagai data); §7 audio bawaan Seedance; §9 harga Seedance; mekanik khas Flow (chip @, agen Flow, batas Veo/Omni) dipindah ke §11 Arsip. Nama skill/agent/buku pelajaran tetap.
