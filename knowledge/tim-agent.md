# Tim agent klinik

Operator harian: **Andrew** (digital marketing, ACC aksi marketing). Dibentuk 12 Nov 2026 (ACC Bapak lewat pop-up): 16 agent di `.claude/agents/`, struktur & cara kerja dari `referensi-rhj/agents/`, isi diganti untuk klinik (fakta/domain/staf RHJ dibuang, pagar klinik dipasang di tiap agent). Fakta layanan/harga/terapis diambil dari `knowledge/profil-klinik.md`; yang kosong ditulis "belum diisi".

| Agent | Peran | Model |
|---|---|---|
| chief-marketing-officer | Strategi, prioritas lintas kanal, apa yang dihentikan | opus |
| marketing-manager | Rencana bertanggal, koordinasi PIC, kartu Anvil klinik, laporan mingguan | opus |
| admin-booking | Calon klien → booking (WA + form), template pesan, pembayaran, skrining krisis, rekap agregat. Pengganti sales-manager RHJ | opus |
| pic-data | Sumber kebenaran angka, hanya agregat | opus |
| pic-ads | Iklan Meta/Google layanan kesehatan, patuh kebijakan iklan kesehatan | sonnet |
| pic-seo | SEO lokal, Google Business Profile, GEO | sonnet |
| pic-web | Situs, form booking aman, tracking tanpa data klien, iPaymu | sonnet |
| pic-konten | Artikel/copy edukasi tanpa klaim medis | sonnet |
| pemindai-kreatif | Swipe-file konten publik | sonnet |
| pic-kreatif | Brief kreatif & QC | sonnet |
| pic-scriptwriter | Naskah video | opus |
| pic-produksi-video | Resep produksi & rakit video | sonnet |
| prompter-flow | Prompt video/gambar AI + pelajaran prompting | sonnet |
| penilai-video | Penilai independen sebelum tayang (termasuk cek pagar kesehatan) | opus |
| pic-sosmed | Operasional IG/TikTok klinik, triase komentar & eskalasi krisis | sonnet |
| verifikator-task | Verifikasi kartu "complete" ke artefak | sonnet |

Belum ada: skill peran khusus klinik (agent memakai skill marketing umum di `.claude/skills/`). Disusun setelah profil klinik lengkap.
