#!/usr/bin/env bash
# Pembungkus CLI HyperFrames (disalin dari rhj-brain 12 Nov 2026; audit asli di rhj-brain 3 Nov 2026).
# Pakai:  bash tools/animasi/hf.sh <perintah hyperframes> [argumen...]
# - CLI terkunci 0.9.8 dari tools/animasi/node_modules (dipasang dengan `npm ci --ignore-scripts` bila belum ada).
# - Telemetri dan pembaruan otomatis dimatikan.
# - Perintah yang mengirim berkas/data ke luar atau memasang sesuatu DITOLAK.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$DIR/node_modules/.bin/hyperframes"

if [ ! -x "$BIN" ]; then
  echo "[hf.sh] CLI belum terpasang di sesi ini, memasang versi terkunci (tanpa skrip install)..." >&2
  (cd "$DIR" && npm ci --ignore-scripts --no-audit --no-fund >&2)
fi

export HYPERFRAMES_NO_TELEMETRY=1
export DO_NOT_TRACK=1
export HYPERFRAMES_NO_UPDATE_CHECK=1
export HYPERFRAMES_NO_AUTO_INSTALL=1
export HYPERFRAMES_SKIP_SKILLS=1   # init tidak boleh memasang skill sendiri (skill hanya lewat cari-skill)

if [ -z "${HYPERFRAMES_BROWSER_PATH:-}" ]; then
  for b in /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell; do
    [ -x "$b" ] && export HYPERFRAMES_BROWSER_PATH="$b" && break
  done
fi

cmd="${1:-}"
case "$cmd" in
  publish|feedback|cloud|lambda|cloudrun|auth|login|logout|usage|upgrade|skills|events|billing|update|reverse)
    echo "[hf.sh] DITOLAK: '$cmd' mengirim data ke luar / memasang / berbayar. Pagar klinik (audit 3 Nov)." >&2
    exit 2 ;;
  telemetry)
    if [ "${2:-}" = "enable" ]; then echo "[hf.sh] DITOLAK: telemetri tetap mati." >&2; exit 2; fi ;;
esac
for a in "$@"; do
  case "$a" in
    --file-issue|--file-issue=*) echo "[hf.sh] DITOLAK: --file-issue mengunggah repro ke URL publik." >&2; exit 2 ;;
    --describe|--describe=*) echo "[hf.sh] DITOLAK: --describe mengirim frame ke Gemini." >&2; exit 2 ;;
  esac
done

exec "$BIN" "$@"
