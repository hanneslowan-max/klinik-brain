# TEMPLATE BRIEF RENGGA (v3 general) — Hannes 6/10

**Berlaku untuk:** brief video yang dikirim ke Rengga (video editor). **Versi:** v1 = PDF panjang (PSK1 v1.2 = 54 halaman) → v2 ringkas (tabel shot per detik; **dicabut**, Hannes: "terlalu detail") → **v3 general (ini)**. Prinsip Hannes: **Rengga bebas berkreasi; brief = jalan cerita + script per scene**, bukan detik, frame, atau daftar shot.

**Paket 3a/3b/3c tetap dokumen kerja agent** (konsep, naskah 3b, sinematografi, log revisi, QC); brief v3 **diturunkan** dari paket itu dan tidak menggantikannya. Contoh jadi: `deliverables/swipe-file-kreatif/2026-10-04-hotline-water/BRIEF-RENGGA-PSK1-v3.md` dan `PROMPT-PSK1.md`.

## 1. Keluaran per video

| File | Isi | Panjang |
|---|---|---|
| `BRIEF-RENGGA-<KODE>-v3.pdf` | Bagian 2 di bawah | **target 1 halaman A4, maksimal 2** |
| `PROMPT-<KODE>.pdf` (opsional) | Prompt EN per klip dari 3c, diberi label **"REFERENSI: boleh dipakai, diubah, atau diabaikan"** | tidak dibatasi |

Log revisi tidak dikirim ke Rengga.

## 2. Isi brief (urutan tetap)

1. **Judul dan meta (1 baris):** `BRIEF RENGGA — <KODE> "<Nama>" (v3 general)`; untuk, dari, status ACC, format 9:16, durasi.
2. **Tujuan:** 1 kalimat.
3. **Durasi:** maksimal saja, tanpa frame (mis. "±20 dtk, maksimal di bawah 60 dtk").
4. **Jalan cerita:** 3–5 kalimat: siapa, apa yang terjadi, punchline, penutup. Tulis juga kanon yang menentukan lucunya (mis. siapa yang memegang punchline, apa yang tidak boleh terjadi).
5. **Per scene** (Scene 1, 2, 3, …; kelompokkan shot 3c jadi 3–6 scene). Tiap scene:
   - apa yang terjadi, 1–2 kalimat;
   - **script:** dialog per tokoh, VO, dan teks layar, **kata persis dari naskah final 3b**, dengan penutur;
   - mood singkat bila perlu.
6. **Kebebasan Rengga (tulis eksplisit):** sudut kamera, urutan shot, potongan, transisi, musik, gerak, dan cara generate bebas, asal cerita dan script tersampaikan dan pagar dipenuhi; mengubah cerita atau kata script = tanya pic-kreatif.
7. **Yang wajib (pagar), maksimal 6 butir:** (1) kanon tokoh (wajah dari LST-xxx, kostum, sifat tokoh; tokoh yang suara saja disebut) · (2) label AI platform ON, tanpa tulisan "AI" dari kita · (3) K3 · (4) teks, huruf, angka, dan merek dibuat lewat overlay di editing, bukan AI; produk dari foto acuan asli · (5) tanpa harga, Rp, KW, "galvanis", "Stocky", janji kirim atau stok, elemen film referensi, dan kata terlarang video itu · (6) kata script tidak diubah tanpa tanya.
8. **Aset acuan (opsional):** daftar nama file atau folder saja.
9. **Selesai =** 1 baris: draf diunggah ke `/draft` dengan label AI ON, lalu QC pic-kreatif dan ACC Hannes.

**Dilarang di brief v3:** detik, frame, ukuran shot, persen headroom atau posisi, gerak kamera, kode klip, tabel shot, prompt EN, rentang durasi ucap, gerbang dan tangga fallback, jalur produksi per hari, log revisi, penjelasan untuk CMO. Boleh ada urutan dan irama dalam kata biasa ("jeda hening sebentar", "mesin mati sesaat sesudah kalimat Lastri") bila itu bagian dari lucunya.

## 3. Aturan tampilan

- A4 portrait, margin 12 mm, font isi 9,5 pt (tidak kurang dari 9 pt), judul ≤15 pt. Melebihi 1 halaman: potong kata, bukan kecilkan font; 2 halaman = batas.
- Bahasa Indonesia ringkas; humanizer pada prosa (bukan pada kata script, angka, dan pagar).
- Teks tidak boleh terpotong di tepi halaman.

## 4. Cara menurunkan dari 3a/3b/3c

| Bagian brief | Ambil dari |
|---|---|
| Tujuan | 3c bagian 2 "Tujuan" (1 kalimat) |
| Jalan cerita | logline 3b + tujuan/kanon 3c (kanon "alarm palsu" dsb. dalam kata biasa) |
| Scene | 3c 1.3 (per shot) dikelompokkan jadi scene; **buang** lensa, frame, posisi, gerak kamera |
| Script | **3b** (kata final; bila beda dengan 3c, 3b menang); warna subtitle per penutur boleh disebut sebagai kanon akun |
| Pagar | 3c 2.8 dan 2.9, dipadatkan ke ≤6 butir |
| Aset acuan | 3c 2.1, nama saja |
| PROMPT (opsional) | 3c 2.2 + 2.4 + 2.4b + 2.5, **salin persis**, tambah label referensi di paragraf meta; kode klip dipetakan ke scene |

**Aturan turun:** kata script dan pagar tidak boleh berubah saat ganti format. Cek sebelum kirim: setiap kata final 3b ada di brief; prompt di PROMPT = teks 3c karakter demi karakter.

## 5. QC pic-kreatif sesudah video jadi (v3)

Menilai **cerita** (jalan cerita dan punchline sampai, kanon tokoh dan "alarm palsu" terjaga), **script** (kata persis 3b, penutur benar, teks layar sesuai) dan **pagar** (6 butir di atas, plus pagar RHJ di rhj-pagar-inti). **Tidak menilai detik, frame, atau pilihan shot.** Vonis LULUS / REVISI + daftar perbaikan konkret (adegan mana → masalah → ganti jadi apa). Mutlak untuk REVISI: kata script berubah, tulisan buatan AI muncul, K3 dilanggar, label AI tidak ON. Syarat CMO yang berbasis waktu (mis. mesin mati 0,07 dtk, hening ≥0,50 dtk, laju Selo) **tidak lagi diperiksa sebagai angka**; yang dinilai tetap maksud ceritanya.

## 6. Pengiriman

PDF brief (dan PROMPT bila dipakai) **dilampirkan di kartu tugas Rengga di aplikasi tugas** (Anvil, `node tools/clickup.mjs`; `tools/README.md`). **Deskripsi kartu = ringkasan maksimal 5 baris.** Kartu dibuat sesi MM sesudah ACC Hannes (B14 langkah 6, B18); agent kreatif tidak membuat atau mengubah kartu tanpa ACC Hannes.

## 7. Render PDF (Chromium headless)

1. Markdown → HTML: python `markdown` (ekstensi `tables`, `fenced_code`, `sane_lists`) + CSS di bawah; `- [ ]` diganti `- ☐`; baris `- ` harus didahului baris kosong.
2. `/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless=new --no-sandbox --no-pdf-header-footer --print-to-pdf=<out.pdf> file://<in.html>`
3. **Cek dengan pymupdf (`import pymupdf`):** jumlah halaman brief (1, maksimal 2); setiap kata script final 3b ada di teks brief (bandingkan tanpa spasi); setiap prompt 3c ada utuh di PROMPT; tidak ada kata di luar margin 12 mm (bbox); lihat gambar halaman (`get_pixmap`).
4. Font Montserrat tidak terpasang di sandbox cloud; PDF memakai Liberation Sans. "Montserrat" di teks brief = spesifikasi video.

```css
@page { size: A4 portrait; margin: 12mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Liberation Sans", Arial, "DejaVu Sans", sans-serif; font-size: 9.5pt; line-height: 1.28; color: #111; margin: 0; }
h1 { font-size: 15pt; margin: 0 0 3px; color: #B51B1B; line-height: 1.15; }
h2 { font-size: 11.5pt; margin: 0 0 4px; color: #B51B1B; }
p { margin: 0 0 4px; }
p.meta { font-size: 9pt; color: #333; margin-bottom: 5px; }
ul { margin: 2px 0 4px; padding-left: 0; list-style: none; }
li { margin: 0 0 2.2px; padding-left: 14px; text-indent: -14px; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; margin: 4px 0 5px; font-size: 9pt; line-height: 1.22; }
th, td { border: 0.6pt solid #888; padding: 2px 3.5px; vertical-align: top; text-align: left; overflow-wrap: anywhere; word-break: break-word; }
th { background: #eee; font-weight: 700; }
tr { page-break-inside: avoid; break-inside: avoid; }
pre { white-space: pre-wrap; word-break: break-word; overflow-wrap: anywhere; font-family: "Liberation Mono", "DejaVu Sans Mono", monospace; font-size: 8.8pt; line-height: 1.3; background: #f4f4f4; border: 0.6pt solid #bbb; padding: 4px 6px; margin: 2px 0 7px; }
pre code { white-space: pre-wrap; word-break: break-word; overflow-wrap: anywhere; font-family: inherit; }
code { font-family: "Liberation Mono", monospace; font-size: 8.8pt; }
.pagebreak { break-after: page; page-break-after: always; height: 0; }
table.shots th:nth-child(1){width:9%} table.shots th:nth-child(2){width:36%} table.shots th:nth-child(3){width:14%} table.shots th:nth-child(4){width:19%} table.shots th:nth-child(5){width:22%}
table:not(.shots) th:nth-child(1){width:17%} table:not(.shots) th:nth-child(2){width:28%} table:not(.shots) th:nth-child(3){width:55%}
```
