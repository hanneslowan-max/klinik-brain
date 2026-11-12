# LOG KEPUTUSAN & PAGAR KLINIK — append-only

Aturan: tulis saat keputusan diambil; baris lama tidak dihapus (koreksi = baris baru).

| Tanggal | Keputusan | Oleh | Status |
|---|---|---|---|
| 12 Nov 2026 | Project klinik hipnoterapi dibuat TERPISAH dari RHJ (usaha terpisah): repo `klinik-brain` (otak agent, kerangka dari rhj-brain tanpa memori/fakta RHJ) + `klinik-tugas` (Anvil klinik, salinan rhj-tugas dengan upstream rhj-tugas; Supabase & domain sendiri, belum dibuat — butuh ACC karena biaya). Data klien = data kesehatan, pagar `knowledge/pagar-inti.md`. | Bapak (pop-up sesi rhj-brain) | tetap |
| 12 Nov 2026 | Profil klinik (pop-up): format sesi offline saja; badan usaha belum ada/perorangan; booking = WA + konfirmasi admin DAN form booking online; bayar = transfer bank, QRIS, payment gateway iPaymu. | Bapak (pop-up) | tetap |
| 12 Nov 2026 | Semua 16 agent RHJ dipindah ke `.claude/agents/` klinik dengan isi diganti klinik (fakta RHJ dibuang, pagar klinik dipasang). `sales-manager` diganti `admin-booking`. | Bapak (pop-up) | tetap |
