#!/usr/bin/env bash
# routine-git.sh — langkah git DETERMINISTIK untuk routine cloud klinik.
# Kenapa: 23/9 routine Analisa Ads diam-diam kerja di atas main basi lalu push ke branch sesinya
# sendiri (fetch/checkout gagal disembunyikan 2>/dev/null). Skrip ini gagal KERAS dan jelas.
#
#   bash tools/routine-git.sh start
#       -> ambil origin/claude/state + origin/main (refspec eksplisit), checkout claude/state = versi remote
#          terbaru, gabung main kalau ada yang belum masuk. Cetak "START OK ...". Exit != 0 = BERHENTI.
#   bash tools/routine-git.sh finish "<pesan commit>" [path ...]
#       -> commit path (default: memori perusahaan), gabung remote terbaru (merge, tanpa rebase/force),
#          push ke claude/state DAN main (aturan Hannes 23/9: dua branch satu isi). Coba ulang 4x.
#          Konflik -> exit 2 + daftar file; JANGAN push ke branch lain, bereskan lalu jalankan finish lagi.

set -u
STATE=claude/state
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "routine-git: BUKAN repo git"; exit 1; }
[ -n "$(git config user.email)" ] || git config user.email "hanneslowan@gmail.com"
[ -n "$(git config user.name)" ] || git config user.name "Klinik Cloud"

fetch_both() {
  local d
  for d in 2 4 8 16; do
    git fetch -q origin "+refs/heads/$STATE:refs/remotes/origin/$STATE" "+refs/heads/main:refs/remotes/origin/main" && return 0
    sleep "$d"
  done
  return 1
}

merge_remote() {  # gabung origin/claude/state lalu origin/main ke HEAD
  local src
  for src in "origin/$STATE" origin/main; do
    git merge-base --is-ancestor "$src" HEAD && continue
    if ! git merge -q --no-edit "$src" >/dev/null 2>&1; then
      echo "routine-git: KONFLIK saat menggabung $src. File:"
      git diff --name-only --diff-filter=U | sed 's/^/  - /'
      git merge --abort 2>/dev/null
      return 2
    fi
  done
}

case "${1:-}" in
  start)
    for f in MERGE_HEAD rebase-merge rebase-apply; do
      [ -e "$(git rev-parse --git-path "$f")" ] && { git merge --abort 2>/dev/null; git rebase --abort 2>/dev/null; }
    done
    if [ -n "$(git status --porcelain)" ]; then
      git stash push -q -u -m "routine-git start $(date -u +%FT%TZ): sisa run sebelumnya" \
        && echo "routine-git: PERINGATAN ada perubahan belum di-commit dari run sebelumnya -> disimpan di git stash (tidak ikut run ini)."
    fi
    fetch_both || { echo "routine-git: FETCH GAGAL 4x (jaringan/izin). BERHENTI - jangan kerja di atas state basi."; exit 1; }
    git checkout -q -B "$STATE" "origin/$STATE" || { echo "routine-git: checkout $STATE GAGAL. BERHENTI."; exit 1; }
    merge_remote >/dev/null || echo "routine-git: PERINGATAN main tak bisa digabung (konflik) - lanjut di $STATE apa adanya."
    echo "START OK: $STATE @ $(git rev-parse --short HEAD) ($(git log -1 --format='%cd' --date=format:'%Y-%m-%d %H:%M UTC' HEAD)) - $(git log -1 --format=%s HEAD)"
    ;;
  finish)
    msg=${2:-"routine $(TZ=Asia/Jakarta date '+%Y-%m-%d %H:%M') WIB"}
    shift 2 2>/dev/null || shift $#
    paths=("$@"); [ ${#paths[@]} -eq 0 ] && paths=(memori perusahaan)
    existing=(); for p in "${paths[@]}"; do [ -e "$p" ] && existing+=("$p"); done
    [ ${#existing[@]} -gt 0 ] && git add -- "${existing[@]}"
    git diff --cached --quiet || git commit -q -m "$msg" || { echo "routine-git: COMMIT GAGAL"; exit 1; }
    for d in 2 4 8 16; do
      fetch_both || { sleep "$d"; continue; }
      merge_remote; rc=$?
      [ $rc -eq 2 ] && { echo "routine-git: commit lokal $(git rev-parse --short HEAD) BELUM ter-push. Bereskan konflik (log append-only: gabung kedua sisi; bagian domain lain: ambil versi remote), commit, lalu jalankan finish lagi. JANGAN push ke branch lain."; exit 2; }
      if git push -q origin "HEAD:$STATE" 2>/dev/null && git push -q origin "HEAD:main" 2>/dev/null; then
        echo "FINISH OK: ter-push ke $STATE + main @ $(git rev-parse --short HEAD)"
        exit 0
      fi
      sleep "$d"
    done
    echo "routine-git: PUSH GAGAL 4x. Commit lokal $(git rev-parse --short HEAD) belum ter-push."
    exit 1
    ;;
  *)
    echo "pakai: bash tools/routine-git.sh start | finish \"<pesan>\" [path ...]"; exit 1 ;;
esac
