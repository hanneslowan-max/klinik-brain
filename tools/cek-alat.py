#!/usr/bin/env python3
"""Cek cepat kesehatan alat repo (tanpa jaringan, tanpa memasang apa pun). Dibuat 8 Nov 2026.

Kenapa: alat bisa rusak diam-diam di container baru (contoh 8 Nov: PIL sistem rusak, cache whisper
dibangun untuk Python lain). Agent yang menemui error lalu menyerah dengan "tidak bisa". Cek ini
jalan di SessionStart dan HANYA mencetak masalah, supaya rusaknya ketahuan sebelum alat dibutuhkan.

Pakai: python3 -I tools/cek-alat.py   (keluar 0 selalu; cetak 'OK semua alat' bila bersih dan --verbose)
"""
import os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")
masalah = []


def py_import(mod, path=None):
    env = dict(os.environ)
    if path:
        env["PYTHONPATH"] = path
    r = subprocess.run([sys.executable, "-c", "import " + mod], capture_output=True, text=True, env=env, timeout=60)
    return r.returncode == 0


# 1. berkas alat wajib ada
for f in ["tools/ig-reel.py", "tools/meta.mjs", "tools/gsc.mjs", "tools/clickup.mjs", "tools/notify.mjs",
          "tools/animasi/hf.sh", "tools/video/bedah.py",
          "tools/video/dengar.py", "tools/video/pasang_dengar.sh"]:
    if not os.path.exists(os.path.join(ROOT, f)):
        masalah.append(f"berkas hilang: {f}")

# 2. program sistem
for prog in ["ffmpeg", "ffprobe", "node", "git"]:
    if not shutil.which(prog):
        masalah.append(f"program tidak ada: {prog}")

# 3. Pillow (bedah.py & dengar.py memasang sendiri ke ~/.cache/klinik-pil bila PIL sistem rusak)
if not py_import("PIL.Image") and not py_import("PIL.Image", os.path.join(HOME, ".cache/klinik-pil")):
    masalah.append("Pillow rusak/tidak ada (akan dipasang otomatis ke ~/.cache/klinik-pil saat bedah.py/dengar.py jalan)")

# 4. cache whisper: kalau ada tapi tidak bisa diimpor oleh python3 ini -> dengar.py membangun ulang otomatis
w = os.path.join(HOME, ".cache/klinik-whisper")
if os.path.isdir(w) and not py_import("faster_whisper, av", w):
    masalah.append("cache whisper tidak cocok dengan python3 ini (dengar.py akan membangun ulang otomatis, ±2 menit)")

# 5. HyperFrames terpasang (node_modules tidak di repo)
if not os.path.isdir(os.path.join(ROOT, "tools/animasi/node_modules/hyperframes")):
    masalah.append("HyperFrames belum terpasang: cd tools/animasi && npm ci")

if masalah:
    print("[cek-alat] Perhatian, alat repo yang perlu dicek sebelum dipakai:")
    for m in masalah:
        print("- " + m)
elif "--verbose" in sys.argv:
    print("[cek-alat] OK semua alat")
