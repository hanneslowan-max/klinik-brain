#!/usr/bin/env python3
"""cek_klip.py — cek cepat hasil video AI (Google Flow / Higgsfield) sebelum memberi vonis.

Pakai:
  python3 cek_klip.py <video.mp4> <folder_keluar> [--fps 4]

Keluaran di <folder_keluar> (taruh di scratchpad, bukan repo):
  LEMBAR.jpg           lembar frame (default 4 fps) untuk dilihat sekaligus
  awal.jpg tengah.jpg akhir.jpg   frame kunci resolusi penuh
  ringkasan.txt        durasi, resolusi, lompatan antar frame (potongan rencana atau "patah"),
                       dan dB per 0,1 dtk (di mana ada suara)
Catatan: lompatan besar di detik yang memang direncanakan = potongan shot; di luar itu = patah/morph.
Audio hanya diukur, tidak didengar.
"""
import glob, os, re, shutil, subprocess, sys, wave

import numpy as np


def ffmpeg():
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    if shutil.which("ffmpeg"):
        return shutil.which("ffmpeg")
    c = glob.glob("/usr/local/lib/python3*/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-*")
    if c:
        return c[0]
    sys.exit("ffmpeg tidak ditemukan (set env FFMPEG)")


def main():
    argv = sys.argv[1:]
    fps = 4
    if "--fps" in argv:
        i = argv.index("--fps")
        fps = float(argv[i + 1])
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    src, out = args
    os.makedirs(out, exist_ok=True)
    F = ffmpeg()
    info = subprocess.run([F, "-i", src], capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    dur_s = int(dur.group(1)) * 3600 + int(dur.group(2)) * 60 + float(dur.group(3)) if dur else 0
    W, H = map(int, re.search(r", (\d{3,5})x(\d{3,5})", info).groups())
    fr = re.search(r"([\d.]+) fps", info)
    vfps = float(fr.group(1)) if fr else 24.0

    n_tiles = max(1, int(dur_s * fps))
    cols = 8
    rows = -(-n_tiles // cols)
    subprocess.run([F, "-loglevel", "error", "-y", "-i", src, "-vf",
                    f"fps={fps},scale=200:-2,tile={cols}x{rows}", "-frames:v", "1",
                    os.path.join(out, "LEMBAR.jpg")], check=True)
    for nama, t in (("awal", 0.05), ("tengah", dur_s / 2), ("akhir", max(0, dur_s - 0.1))):
        subprocess.run([F, "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1",
                        "-q:v", "2", os.path.join(out, f"{nama}.jpg")], check=True)

    w = 160
    h = round(H * w / W)
    h += h % 2
    raw = subprocess.run([F, "-loglevel", "error", "-i", src, "-vf", f"scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (w * h)
    a = np.frombuffer(raw[: n * w * h], np.uint8).reshape(n, h, w).astype(float)
    d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2)) if n > 1 else np.array([0.0])
    med = float(np.median(d)) if len(d) else 0.0
    lompat = [(i + 1, (i + 1) / vfps, v) for i, v in enumerate(d) if v > max(2.5 * med, 4.0)]

    lines = [f"berkas: {os.path.basename(src)}", f"durasi: {dur_s:.2f} dtk · {W}x{H} · {vfps:g} fps · {n} frame",
             f"selisih antar frame: median {med:.2f}, maks {float(d.max()):.1f}"]
    if lompat:
        lines.append("lompatan (potongan rencana atau patah):")
        lines += [f"  frame {i} · dtk {t:.2f} · selisih {v:.1f}" for i, t, v in lompat]
    else:
        lines.append("lompatan: tidak ada")

    wavp = os.path.join(out, "_a.wav")
    r = subprocess.run([F, "-loglevel", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wavp])
    if r.returncode == 0 and os.path.exists(wavp) and os.path.getsize(wavp) > 1000:
        wv = wave.open(wavp)
        x = np.frombuffer(wv.readframes(wv.getnframes()), np.int16).astype(float) / 32768
        win = 1600
        db = [20 * np.log10(np.sqrt(np.mean(x[i:i + win] ** 2)) + 1e-9) for i in range(0, len(x) - win, win)]
        lines.append("dB per 0,1 dtk: " + " ".join(f"{v:.0f}" for v in db))
        keras = [i / 10 for i, v in enumerate(db) if v > -35]
        if keras:
            lines.append(f"ada suara keras (> -35 dB) sekitar dtk {keras[0]:.1f}–{keras[-1]:.1f}")
        os.remove(wavp)
    else:
        lines.append("audio: tidak ada trek")
    open(os.path.join(out, "ringkasan.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
