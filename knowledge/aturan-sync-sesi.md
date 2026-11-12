# Aturan sinkronisasi sesi (klinik-brain)
Disalin dari rhj-brain 12 Nov 2026, disesuaikan untuk klinik.

Tiap sesi/routine cloud bekerja di salinan repo sendiri. Perubahan menyambung antar-sesi lewat git (commit → push → pull), bukan memori real-time.

## Dua branch, satu isi
Setiap push = commit yang SAMA ke `main` DAN `claude/state`. `main` = otak stabil (skill, pagar, agent, tools); `claude/state` = state hidup (`memori/`). Keduanya selalu identik.

## Otomatis (hook `.claude/settings.json`)
- SessionStart → `tools/session-start-sync.sh`: merge `origin/main` lalu `origin/claude/state` ke branch sesi.
- Stop → `tools/auto-push.sh`: commit otomatis `memori/ knowledge/ deliverables/ docs/`, merge kedua branch, push ke `main` dan `claude/state`. File lain (agent, skill, tools, config) di-commit manual tapi ikut ter-push.
- Konflik/jaringan: merge dibatalkan bersih, hook exit 2 → bereskan konflik (log append-only: gabung kedua sisi) lalu `bash tools/auto-push.sh </dev/null`.
- Matikan sementara: env `AUTO_PUSH_DISABLE=1`. Tidak pernah rebase/force-push.

## Manual (sesi tanpa hook)
Awal: `git fetch origin && git pull --no-rebase origin claude/state && git pull --no-rebase origin main`.
Akhir: `git add memori knowledge deliverables` (bukan `-A`) → commit → pull kedua branch → `git push origin HEAD:claude/state && git push origin HEAD:main`.

## Banyak pengguna (Bapak + Andrew)
Bapak dan Andrew bisa membuka sesi di repo yang sama. Satu penulis per file sebisanya; file log (`LOG-PAGAR`, `PELAJARAN`, `ANTREAN-KEPUTUSAN`) append-only sehingga konflik cukup digabung. Routine dijadwal berjenjang agar tidak push bersamaan.
