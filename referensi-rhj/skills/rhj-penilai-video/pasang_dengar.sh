#!/usr/bin/env bash
# Pasang mesin transkrip faster-whisper (tanpa root) ke cache; cetak path-nya.
# Pakai: export PYTHONPATH=$(bash pasang_dengar.sh)
# Model "small" (~480 MB) diunduh otomatis dari HuggingFace saat pertama dipakai.
set -e
D="${HOME}/.cache/rhj-whisper"
# Pakai "python3 -m pip", bukan "pip": di container cloud "pip" bisa milik Python lain (3.13),
# sehingga modul biner (av/_core) terpasang untuk versi yang salah dan import gagal (8 Nov 2026).
if [ ! -d "$D/faster_whisper" ]; then
  python3 -m pip install -q --target "$D" faster-whisper >&2
fi
# faster-whisper 1.2.1 memanggil av.open(metadata_errors=...), yang ditolak PyAV >=15.
# 14.2.0 = versi <15 terakhir yang punya wheel cp313 (14.4.0 tidak ada wheel). Dicek 15 Okt.
if ! PYTHONPATH="$D" python3 -c 'import av,sys; sys.exit(int(av.__version__.split(".")[0]) >= 15)' 2>/dev/null; then
  python3 -m pip install -q --only-binary=:all: --no-deps --upgrade --target "$D" "av==14.2.0" >&2
fi
# Cek akhir: modul biner harus cocok dengan python3 yang dipakai; kalau tidak, pasang ulang av.
# Cache lama yang dibangun untuk Python lain: bangun ulang seluruhnya untuk python3 ini.
if ! PYTHONPATH="$D" python3 -c 'import av, faster_whisper' 2>/dev/null; then
  rm -rf "$D"
  python3 -m pip install -q --target "$D" faster-whisper >&2
  python3 -m pip install -q --only-binary=:all: --no-deps --upgrade --target "$D" "av==14.2.0" >&2
  PYTHONPATH="$D" python3 -c 'import av, faster_whisper' >&2
fi
echo "$D"
