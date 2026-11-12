#!/usr/bin/env bash
# Auto-push klinik-brain di akhir tiap giliran Claude (hook "Stop", .claude/settings.json).
#
# Alur:
#   1. Commit otomatis folder state (memori, perusahaan, knowledge, deliverables, docs).
#      File lain (kode, skill, agent, config) tetap commit manual, tapi ikut ter-push.
#   2. Tarik main + claude/state (otak + state hidup rutin) ke branch ini lewat MERGE (tanpa rebase,
#      tanpa force), supaya sesi selalu memegang state terbaru dan push ke state
#      selalu fast-forward.
#   3. Push branch ini ke origin (branch sesi sendiri).
#   4. Push HEAD yang sama ke origin/claude/state DAN origin/main -> keduanya selalu satu isi
#      (Hannes 23 Sep: "push langsung ke main dan state, jadi tidak bingung").
#
# Gagal (konflik / jaringan) -> exit 2 sekali supaya Claude membereskan. Tidak loop.
# Matikan sementara: AUTO_PUSH_DISABLE=1.

INPUT=$(cat)
[ "${AUTO_PUSH_DISABLE:-0}" = "1" ] && exit 0
cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}" || exit 0
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

STATE=claude/state
PATHS=(memori perusahaan knowledge deliverables docs)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
[ "$BRANCH" = "HEAD" ] && exit 0   # detached, jangan sentuh

fail() {
  # Sudah dalam putaran hook -> jangan paksa Claude lagi.
  echo "$INPUT" | grep -q '"stop_hook_active": *true' && exit 0
  echo "auto-push GAGAL: $1. Cek 'git status', bereskan, lalu jalankan: bash tools/auto-push.sh </dev/null" >&2
  exit 2
}

# Jangan ganggu merge/rebase yang sedang berjalan.
for f in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD; do
  [ -e "$(git rev-parse --git-path "$f")" ] && fail "ada merge/rebase yang belum selesai ($f)"
done

# 1. Commit folder state.
EXISTING=()
for p in "${PATHS[@]}"; do [ -e "$p" ] && EXISTING+=("$p"); done
if [ ${#EXISTING[@]} -gt 0 ] && [ -n "$(git status --porcelain -- "${EXISTING[@]}")" ]; then
  git add -- "${EXISTING[@]}"
  git commit -q -m "auto-push $BRANCH $(TZ=Asia/Jakarta date '+%Y-%m-%d %H:%M') WIB

Co-Authored-By: Claude <noreply@anthropic.com>" || fail "commit gagal"
fi

pull_state() {  # tarik main (otak, dokumen sesi lain) + claude/state (state rutin)
  local src
  for src in main "$STATE"; do
    [ "$src" = "$BRANCH" ] && continue
    git fetch -q origin "+refs/heads/$src:refs/remotes/origin/$src" 2>/dev/null || continue   # branch belum ada -> lewati
    git merge-base --is-ancestor "origin/$src" HEAD && continue
    git merge -q --no-edit "origin/$src" >/dev/null 2>&1 || { git merge --abort 2>/dev/null; FAILED_SRC=$src; return 1; }
  done
}

push_to() {  # $1 = branch tujuan
  local target=$1
  for delay in 2 4 8 16; do
    git push -q origin "HEAD:$target" 2>/dev/null && return 0
    # Ditolak: kemungkinan remote gerak duluan -> merge lalu coba lagi.
    git fetch -q origin "+refs/heads/$target:refs/remotes/origin/$target" 2>/dev/null
    if git rev-parse -q --verify "origin/$target" >/dev/null && ! git merge-base --is-ancestor "origin/$target" HEAD; then
      git merge -q --no-edit "origin/$target" >/dev/null 2>&1 || { git merge --abort 2>/dev/null; return 2; }
    fi
    sleep "$delay"
  done
  return 1
}

# 2. Tarik main + state hidup (yang bukan branch ini sendiri).
pull_state || fail "konflik saat menggabung origin/$FAILED_SRC ke $BRANCH"

# 3. Push branch sendiri (kalau ada yang belum ter-push).
git fetch -q origin "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH" 2>/dev/null
if ! git rev-parse -q --verify "origin/$BRANCH" >/dev/null || ! git merge-base --is-ancestor HEAD "origin/$BRANCH"; then
  push_to "$BRANCH"; rc=$?
  [ $rc -eq 2 ] && fail "konflik dengan origin/$BRANCH"
  [ $rc -ne 0 ] && fail "push ke origin/$BRANCH gagal (jaringan?)"
fi

# 4. Push HEAD yang sama ke claude/state DAN main (Hannes 23 Sep: selalu dua-duanya, satu isi).
for TARGET in "$STATE" main; do
  [ "$TARGET" = "$BRANCH" ] && continue
  git fetch -q origin "+refs/heads/$TARGET:refs/remotes/origin/$TARGET" 2>/dev/null
  if ! git merge-base --is-ancestor HEAD "origin/$TARGET" 2>/dev/null; then
    push_to "$TARGET"; rc=$?
    [ $rc -eq 2 ] && fail "konflik dengan origin/$TARGET"
    [ $rc -ne 0 ] && fail "push ke origin/$TARGET gagal (jaringan?)"
    # Merge di dalam push_to bisa menambah commit -> samakan branch sendiri juga.
    git push -q origin "HEAD:$BRANCH" 2>/dev/null
  fi
done

# Merge di push_to (mis. state gerak saat push ke main) bisa bikin satu target tertinggal -> samakan lagi.
for TARGET in "$STATE" main; do
  [ "$TARGET" = "$BRANCH" ] && continue
  git fetch -q origin "+refs/heads/$TARGET:refs/remotes/origin/$TARGET" 2>/dev/null
  git merge-base --is-ancestor HEAD "origin/$TARGET" 2>/dev/null || push_to "$TARGET" >/dev/null || fail "push ulang ke origin/$TARGET gagal"
done

exit 0
