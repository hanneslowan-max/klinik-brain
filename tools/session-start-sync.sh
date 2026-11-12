#!/usr/bin/env bash
# Sync awal sesi (hook "SessionStart", .claude/settings.json).
# Sesi cloud biasanya mulai dari main, padahal state hidup ada di claude/state.
# Script ini menggabung origin/claude/state ke branch sesi (merge, tanpa force),
# supaya memori yang dibaca Claude selalu yang terbaru. Output stdout masuk ke
# konteks Claude sebagai info.

cat >/dev/null
cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

STATE=claude/state
BRANCH=$(git rev-parse --abbrev-ref HEAD)
[ "$BRANCH" = "HEAD" ] && exit 0

git fetch -q origin "+refs/heads/$STATE:refs/remotes/origin/$STATE" 2>/dev/null || { echo "[sync] origin/$STATE tidak bisa diambil, memori mungkin belum terbaru."; exit 0; }

# Tarik main dulu: dokumen/mandat yang ditulis sesi lain di main ikut terbaca.
if [ "$BRANCH" != "main" ] && git fetch -q origin "+refs/heads/main:refs/remotes/origin/main" 2>/dev/null && ! git merge-base --is-ancestor origin/main HEAD; then
  if git merge -q --no-edit origin/main >/dev/null 2>&1; then
    echo "[sync] origin/main digabung ke $BRANCH (dokumen/mandat terbaru dari sesi lain)."
  else
    git merge --abort 2>/dev/null
    echo "[sync] PERINGATAN: gagal menggabung origin/main ke $BRANCH (konflik). Cek dokumen baru dengan: git log HEAD..origin/main --stat"
  fi
fi

if [ "$BRANCH" = "$STATE" ]; then
  git pull -q --no-rebase --no-edit origin "$STATE" >/dev/null 2>&1 \
    && echo "[sync] $STATE sudah ditarik ke versi terbaru." \
    || { git merge --abort 2>/dev/null; echo "[sync] PERINGATAN: pull $STATE konflik, bereskan dulu sebelum baca memori."; }
  exit 0
fi

if git merge-base --is-ancestor "origin/$STATE" HEAD; then
  echo "[sync] $BRANCH sudah memuat state terbaru ($STATE)."
  exit 0
fi

if git merge -q --no-edit "origin/$STATE" >/dev/null 2>&1; then
  echo "[sync] origin/$STATE digabung ke $BRANCH. Memori (memori/, knowledge/) = versi terbaru rutin."
else
  git merge --abort 2>/dev/null
  echo "[sync] PERINGATAN: gagal menggabung origin/$STATE ke $BRANCH (konflik). Memori di working tree mungkin basi; baca versi state dengan: git show origin/$STATE:memori/<file>"
fi
exit 0
