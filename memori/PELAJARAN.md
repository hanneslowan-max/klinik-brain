# Pelajaran agent klinik (append-only)

Format: `- <tgl> · <peran/sesi> · masalah → solusi`

- 12 Nov 2026 — Pindah agent RHJ → klinik: semua file agent RHJ penuh fakta RHJ (16/16), jadi salinan mentah tidak aman. Pola yang dipakai: pertahankan struktur peran + blok bersama (Baca dulu, Pagar klinik, Keputusan pop-up) yang dibangkitkan satu skrip agar konsisten; cek akhir dengan grep kata kunci RHJ.

- 12 Nov 2026 · Masalah: salin alat RHJ → klinik · Gejala: banyak alat memuat default akun RHJ (ID app TikTok, ref Supabase RHJ, domain, akun IG) yang akan diam-diam dipakai bila env klinik kosong · Diagnosis: default tersembunyi lebih berbahaya daripada error · Solusi: ganti semua default akun RHJ dengan env klinik WAJIB (kosong = gagal), grep kata kunci RHJ sesudahnya, cek sintaks semua alat · Prinsip: saat memisah usaha, hapus default kredensial/ID, jangan sekadar ganti teks.
