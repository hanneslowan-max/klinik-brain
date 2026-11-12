# Format brief baku Hannes (ACC Hannes 22 Okt 2026)

Hannes: "hafalkan format brief seperti ini. Jadi setiap kali saya minta brief, kamu buatkan format seperti ini. Untuk rengga, nanti kartu nya per episode ya. Saya review dulu ceritanya, kalo ok, baru buatkan kartu untuk rengga."

Contoh acuan (ikuti persis bentuknya):
- Brief singkat untuk ACC: `deliverables/naskah/BRIEF-ACC-SEQUENCE-EPS12-20-22Okt.md` (v3.1)
- Brief per scene + ringkasan episode: `deliverables/naskah/BRIEF-PER-SCENE-EPS12-20-22Okt.md` (+ `.pdf`)

Berlaku untuk setiap permintaan "brief" video dari Hannes: serial, konten lepas, dan video iklan. Untuk iklan Meta, alur riset B12 tetap berjalan lebih dulu; format ini dipakai saat brief disajikan ke Hannes.

## Alur

1. **Brief singkat untuk ACC** (±2–4 halaman). Bahasa awam, tanpa kode teknik (KOM/R/W/INS), tanpa label sumber `[.. n=..]`, tanpa istilah beat/payoff/cliff.
2. **Cek sebelum dikirim ke Hannes:**
   - **Pembaca buta:** agent baru membaca ringkasan yang sudah dibuang label rasa dan klaim penulisnya. Ia menilai tiap episode: berhenti scroll di 3 detik pertama, nonton sampai habis, rasa yang ditangkap, share, flat, dan bisa dipahami tanpa episode lain. Kalau ada episode flat, diperbaiki lalu diuji ulang oleh pembaca buta yang baru.
   - **pic-data:** cek pagar, kanon, K3, FAKTA PRODUK, dan kembar premis.
   - **penilai-video TIDAK membaca brief.** Ia disimpan untuk menilai video jadi.
3. **Brief per scene** dengan ringkasan episode di awal tiap episode (format di bawah). Dikirim ke Hannes dalam PDF.
4. **Hannes me-review ceritanya.** Selama belum di-ACC, tidak ada kartu Rengga yang dibuat.
5. **Sesudah ACC:** satu kartu Anvil per episode untuk Rengga. Isinya ringkasan episode dan tabel scene episode itu, dengan PDF brief per scene terlampir.

## Isi brief singkat untuk ACC (tahap 1)

- **Ceritanya tentang apa:** 2–3 kalimat.
- **Urutan rasa:** satu rasa utama per episode, tanpa dua episode berturut-turut yang sama, dan 2–3 puncak.
- **Per episode:**
  - judul · rasa utama · produk · bisa ditonton sendiri (ya/tidak)
  - **Hook 3 detik pertama:** teks layar ≤36 karakter (dihitung skrip), apa yang penonton lihat di detik 0–3, dan kenapa penonton penasaran
  - **Momen spesial:** satu adegan atau kalimat yang membuat penonton tertawa keras, berkaca-kaca, atau merinding
  - **Kenapa orang share/simpan:** 1 kalimat
- **Tidak boleh ada episode flat** (Hannes 22 Okt: "yg flat, pasti orang gamau nonton").
- **Yang berubah dari versi sebelumnya:** singkat.
- **Keputusan untuk Hannes:** maksimal 5, tiap butir 1 kalimat dengan pilihan. Perubahan atas naskah yang sudah di-ACC ditandai ✱.

## Isi brief per scene (tahap 3)

**Kepala dokumen:**
- **Untuk / Dari / tanggal / turunan dari:** brief singkat versi berapa.
- **Cara baca:**
  - ★ = momen spesial
  - ✱ = mengubah naskah yang sudah ACC
  - detik = perkiraan
  - teks layar = ditambahkan saat edit, bukan buatan AI
- **Berlaku di semua episode:** pagar K3 dan pagar uang, ditulis sekali di sini.

**Per episode:**

`## Eps N · Judul · RASA · produk: … · ±xx detik`

Lalu kotak kuning:

```
> **Ringkasan episode (untuk Rengga)**
>
> - **Ceritanya:** 2–3 kalimat awal → tengah → akhir
> - **Rasa:** rasa yang harus sampai + scene/detik puncaknya (★)
> - **Jangan salah:** (1) … (2) … (3) …  ← ekspresi, jeda, benda kunci, APD/K3, produk sebagai alat
> - **Tokoh & lokasi:** masa kini / kilas balik + produk
> - **Pembuka:** gambar hook · **Penutup:** gambar terakhir
> - **Nyambung:** benda atau kalimat yang ditanam/dibayar di episode lain
```

Baris `>` kosong sesudah judul kotak wajib ada supaya daftarnya terbaca rapi di PDF.

Lalu tabel scene:

`| # | Detik | Yang terlihat | Dialog / suara | Teks di layar |`

- Scene 1 = hook 3 detik.
- Dialog ditulis persis. Kalau tidak ada dialog, tulis "tanpa dialog".
- ★ dan ✱ diletakkan di kolom #.
- Baris terakhir = gambar akhir.
- Kalimat yang dibuang dari naskah ACC ditulis di bawah tabel.

**Hitungan:** durasi dan tempo dihitung skrip (Lastri ≤2,0 kata/dtk; tokoh lain ≤2,6; klip bicara ≤5 dtk; total ≤59 dtk), lalu `cek_dialog.py` dijalankan. Hasil cek ditulis di akhir file, bukan di badan brief.

**PDF:** `python3 tools/md2pdf.py <brief.md> <brief.pdf> --landscape` untuk brief per scene. Brief singkat memakai orientasi tegak (tanpa `--landscape`).
