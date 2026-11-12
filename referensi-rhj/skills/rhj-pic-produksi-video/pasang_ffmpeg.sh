#!/usr/bin/env bash
# Pasang FFmpeg portabel (tanpa root) lewat paket imageio-ffmpeg ke cache; cetak path-nya.
# Pakai: export FFMPEG=$(bash pasang_ffmpeg.sh)
set -e
D="${HOME}/.cache/rhj-ffmpeg"
if ! ls "$D"/imageio_ffmpeg/binaries/ffmpeg* >/dev/null 2>&1; then
  pip install -q --target "$D" imageio-ffmpeg >&2
fi
ls "$D"/imageio_ffmpeg/binaries/ffmpeg* | head -1
