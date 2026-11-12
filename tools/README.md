# tools/ — alat klinik

Sebagian besar disalin dari `rhj-brain/tools` pada 12 Nov 2026 (ACC Bapak, pop-up); semua rujukan akun/domain/staf RHJ dibuang. **Semua kredensial lewat env var / secret environment KLINIK. JANGAN pakai token RHJ, jangan commit secret.** Env belum ada → alat gagal dengan pesan jelas; laporkan perintah + error-nya.

| Alat | Fungsi | Env / config |
|---|---|---|
| `notify.mjs` | Kirim teks ke Telegram (plain text) | `TELEGRAM_BOT_TOKEN`, `NOTIFY_CHAT_ID` (bot klinik) |
| `telegram-baca.mjs`, `telegram-balasan.mjs` | Baca pesan grup / balasan Telegram bot klinik ke memori | idem + `tools/telegram-tujuan.json` |
| `clickup.mjs`, `tugas.mjs` | Kartu Anvil klinik | `TUGAS_BACKEND=tugas`, `TUGAS_API_URL`, `TUGAS_API_TOKEN`, `TUGAS_FOLDER_DEFAULT` |
| `sapuan-anvil.mjs` | Cari kartu yang komentar terakhirnya dari staf (belum dijawab) | env Anvil + `TUGAS_WEB_URL` |
| `beban.mjs` | Analisa beban kerja per orang (RAHASIA, hanya untuk Bapak) | env Anvil + `beban-config.json` (masih kosong) |
| `cek-tonggak.mjs` | Bandingkan due kartu vs tonggak kalender | env Anvil + `tonggak-kalender.json` (kosong) |
| `gsc.mjs` | Google Search Console API, baca saja | `GSC_SA_JSON`/`GSC_SA_JSON_B64`/`GSC_SA_FILE`, `KLINIK_DOMAIN` (alias `klinik`) |
| `seo-peluang.py` | Peluang SEO dari GSC + Autocomplete | `seo-klinik.json` (isi merek/benih sesudah profil klinik lengkap) |
| `crawl-situs.py` | Crawl situs klinik sendiri (GET/HEAD) | `KLINIK_SITUS` (alias `klinik`) atau URL langsung |
| `cek-tag-browser.sh/.py` | Cek tag GA4/GTM/Pixel/JSON-LD yang benar-benar aktif (browser) | — |
| `meta.mjs` | Analitik Instagram + Meta Ads, baca saja | `META_ACCESS_TOKEN`, `META_IG_USER_ID`, `META_AD_ACCOUNT_ID`, `META_PAGE_ID` (akun KLINIK) |
| `tiktok.mjs` | Analitik TikTok, baca saja | `TIKTOK_USERNAME`, `TIKTOK_APP_ID`, `TIKTOK_REDIRECT_URI`, `TIKTOK_VAULT_PROJECT` (project Supabase KLINIK) |
| `ig-reel.py` | Unduh reel/post IG publik untuk dibedah | — |
| `higgsfield.mjs` | Generate video/gambar (berbayar: `--ya` hanya sesudah ACC) | kredensial Higgsfield klinik |
| `rakit_video.py`, `sfx_sintetis.py`, `video/` | Rakit video, efek suara, bedah video, transkrip | ffmpeg (`video/pasang_ffmpeg.sh`), whisper (`video/pasang_dengar.sh`) |
| `animasi/hf.sh` | CLI HyperFrames terkunci (pin 0.9.8, telemetri mati, perintah unggah/berbayar ditolak) | `cd tools/animasi && npm ci` sekali |
| `md2pdf.py` | Markdown → PDF | — |
| `arsip_memori.py` | Arsipkan memori lama | — |
| `cek-alat.py` | Cek alat video terpasang | — |
| `audit-skill.py` | Cari/audit/pasang skill pihak ketiga (lewat skill `cari-skill`) | — |
| `auto-push.sh`, `session-start-sync.sh`, `routine-git.sh` | Sinkron git (lihat `knowledge/aturan-sync-sesi.md`) | `AUTO_PUSH_DISABLE=1` untuk mematikan |

Tidak disalin (RHJ-spesifik, menyangkut chat WA/data pelanggan RHJ atau ERP): `kapso-catat.py`, `kapso-transkrip.py`, `lead-wa-otomatis.py`, `mutu-meta.py`, `profil-lead.py`, `jadwal-fu.py`, `pantau-*`, `pesan-pantau-jam.py`, `abaikan-wa.py`, `erp-*`, `backlog-acc.py`, `sync-desktop-to-repo.sh`. Versi klinik dibuat sesudah nomor WA/Kapso klinik dan aturan bot klinik ada (data klien = data kesehatan).

Hook `.claude/hooks/supabase-readonly.sh`: konektor MCP Supabase di akun ini bisa tersambung ke project RHJ, jadi `execute_sql` lewat MCP dipaksa baca-saja.
