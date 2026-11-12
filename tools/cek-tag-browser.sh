#!/usr/bin/env bash
# Cek tag tracking (GA4/GTM/Meta Pixel/JSON-LD) dengan browser sungguhan via Scrapling.
# Pakai: bash tools/cek-tag-browser.sh <url> [url ...]   -> JSON per baris ke stdout.
# Venv dibuat sekali di /tmp (bukan di repo). Butuh Chromium Playwright (/opt/pw-browsers/chromium di cloud).
set -euo pipefail
VENV=/tmp/scrapling-venv
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -x "$VENV/bin/python" ] || ! "$VENV/bin/python" -c "import scrapling.fetchers" 2>/dev/null; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q "scrapling[fetchers]==0.4.15" >&2
fi
exec "$VENV/bin/python" -I "$DIR/cek-tag-browser.py" "$@" 2> >(grep -v "^\[20" >&2)
