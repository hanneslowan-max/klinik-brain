#!/usr/bin/env python3
"""Bedah teknis video referensi: shot (potongan otomatis), audio per detik, lembar frame, transkrip.

Pakai:
  python3 bedah.py <file.mp4 | URL publik> <folder_keluar> [--ambang 0.18] [--tanpa-transkrip]

Keluaran di <folder_keluar> (taruh di scratchpad, JANGAN di repo — video & frame milik kreator):
  bedah.json     durasi, resolusi, fps, daftar shot (mulai/selesai/panjang), ritme (rata-rata & median
                 panjang shot, shot/10 dtk), audio per detik (dB), lonjakan energi (kandidat SFX/hit/drop),
                 % hening, transkrip bertimestamp (bila faster-whisper tersedia)
  SHOTS.jpg      1 frame tengah tiap shot, berlabel nomor + detik mulai
  PER-DETIK.jpg  1 frame tiap detik, berlabel detik
  shot_NNN.jpg   frame per shot ukuran besar
URL diunduh dengan yt-dlp (dipasang otomatis ke cache bila belum ada; tanpa login). YouTube dari cloud
sering ditolak 403 → minta Andrew/Bapak unggah file ke Drive.
Batas: agent tidak mendengar audio; musik/SFX = dugaan dari data audio + transkrip + visual.
"""
import json, os, re, shutil, statistics, subprocess, sys


def _pastikan_pil():
    # PIL bawaan sistem di container cloud bisa rusak (ImportError _imaging, 8 Nov 2026).
    # Bila gagal, pasang Pillow ke cache sendiri lalu pakai itu (pola sama dengan yt-dlp).
    try:
        from PIL import Image  # noqa: F401
        return
    except ImportError:
        pass
    cache = os.path.expanduser("~/.cache/klinik-pil")
    if not os.path.isdir(os.path.join(cache, "PIL")):
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--target", cache, "pillow"], check=True)
    for m in [m for m in sys.modules if m == "PIL" or m.startswith("PIL.")]:
        del sys.modules[m]
    sys.path.insert(0, cache)


_pastikan_pil()

DIR =os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def ffmpeg():
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    if shutil.which("ffmpeg"):
        return shutil.which("ffmpeg")
    return subprocess.run(["bash", os.path.join(DIR, "pasang_ffmpeg.sh")], capture_output=True, text=True,
                          check=True).stdout.strip()


def unduh(url, out):
    cache = os.path.expanduser("~/.cache/klinik-ytdlp")
    if not os.path.exists(os.path.join(cache, "yt_dlp")):
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--target", cache, "yt-dlp"], check=True)
    env = dict(os.environ, PYTHONPATH=cache)
    tujuan = os.path.join(out, "sumber.%(ext)s")
    subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-playlist", "-f", "mp4/best",
                    "-o", tujuan, url], check=True, env=env, cwd=out)
    for f in os.listdir(out):
        if f.startswith("sumber.") and not f.endswith(".json"):
            return os.path.join(out, f)
    sys.exit("GAGAL unduh: file video tidak ditemukan")


def info(ff, src):
    r = subprocess.run([ff, "-hide_banner", "-i", src], capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r)
    d = int(dur[1]) * 3600 + int(dur[2]) * 60 + float(dur[3]) if dur else 0.0
    v = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", r)
    fps = re.search(r"([\d.]+) fps", r)
    return {"durasi": round(d, 2), "lebar": int(v[1]) if v else None, "tinggi": int(v[2]) if v else None,
            "fps": float(fps[1]) if fps else None, "ada_audio": "Audio:" in r}


def potongan(ff, src, ambang, dur):
    r = subprocess.run([ff, "-hide_banner", "-i", src, "-vf",
                        f"cropdetect=24:2:0,select='gt(scene,{ambang})',showinfo", "-an", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    titik = [float(m) for m in re.findall(r"pts_time:([\d.]+)", r)]
    batas = [0.0] + [t for t in titik if 0.25 < t < dur - 0.1] + [dur]
    shots = []
    for i in range(len(batas) - 1):
        a, b = batas[i], batas[i + 1]
        if b - a < 0.12 and shots:  # pecahan flash → gabung ke shot sebelumnya
            shots[-1]["selesai"] = round(b, 2); shots[-1]["panjang"] = round(b - shots[-1]["mulai"], 2); continue
        shots.append({"no": len(shots) + 1, "mulai": round(a, 2), "selesai": round(b, 2), "panjang": round(b - a, 2)})
    return shots


def audio_per_detik(ff, src, dur):
    r = subprocess.run([ff, "-hide_banner", "-i", src, "-af",
                        "asetnsamples=48000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level",
                        "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    db = []
    for m in re.findall(r"RMS_level=(-?[\d.]+|-inf)", r):
        db.append(-90.0 if m == "-inf" else round(float(m), 1))
    db = db[: int(dur) + 1]
    hening = round(100 * sum(1 for x in db if x < -45) / len(db), 1) if db else None
    lonjak = [i for i in range(1, len(db)) if db[i] - db[i - 1] >= 8 and db[i] > -30]
    return {"db_per_detik": db, "persen_hening": hening, "lonjakan_detik": lonjak}


def frame(ff, src, t, out, w, label):
    """Ambil 1 frame, perkecil, beri label (Pillow; FFmpeg portabel tidak punya drawtext)."""
    subprocess.run([ff, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1",
                    "-vf", f"scale={w}:-2", out])
    if not os.path.exists(out):
        return
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(out).convert("RGB"); d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, max(14, w // 12))
    d.text((8, 6), label, font=f, fill="yellow", stroke_width=2, stroke_fill="black")
    im.save(out, quality=88)


def lembar(files, out, kol=6):
    from PIL import Image
    files = [f for f in files if os.path.exists(f)]
    if not files:
        return
    ims = [Image.open(f) for f in files]
    w, h = ims[0].size; kol = min(kol, len(ims)); bar = (len(ims) + kol - 1) // kol; pad = 4
    sheet = Image.new("RGB", (kol * (w + pad) + pad, bar * (h + pad) + pad), "white")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), (pad + (i % kol) * (w + pad), pad + (i // kol) * (h + pad)))
    sheet.save(out, quality=85)


def transkrip(src):
    cache = os.path.expanduser("~/.cache/klinik-whisper")  # dipasang tools/video/pasang_dengar.sh
    if os.path.isdir(cache) and cache not in sys.path:
        sys.path.insert(0, cache)
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return {"status": "faster-whisper tidak terpasang (bash tools/video/pasang_dengar.sh); transkrip dilewati"}
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, inf = model.transcribe(src, vad_filter=True)
    return {"bahasa": inf.language, "segmen": [{"mulai": round(s.start, 1), "selesai": round(s.end, 1),
                                                 "teks": s.text.strip()} for s in segs]}


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], os.path.abspath(sys.argv[2])
    ambang = float(sys.argv[sys.argv.index("--ambang") + 1]) if "--ambang" in sys.argv else 0.18
    os.makedirs(out, exist_ok=True)
    if re.match(r"https?://", src):
        src = unduh(src, out)
    elif not os.path.isfile(src):
        sys.exit(f"GAGAL: file tidak ada: {src}")
    ff = ffmpeg()
    data = info(ff, src)
    data["sumber"] = os.path.basename(src)
    data["shots"] = potongan(ff, src, ambang, data["durasi"])
    pj = [s["panjang"] for s in data["shots"]]
    data["ritme"] = {"jumlah_shot": len(pj), "rata2_dtk": round(statistics.mean(pj), 2) if pj else None,
                     "median_dtk": round(statistics.median(pj), 2) if pj else None,
                     "shot_per_10dtk": round(10 * len(pj) / data["durasi"], 2) if data["durasi"] else None,
                     "ambang_scene": ambang}
    if data["ada_audio"]:
        data["audio"] = audio_per_detik(ff, src, data["durasi"])
    tmp = os.path.join(out, "_f"); os.makedirs(tmp, exist_ok=True)
    for i, s in enumerate(data["shots"]):
        tengah = (s["mulai"] + s["selesai"]) / 2
        frame(ff, src, tengah, os.path.join(tmp, f"s{i:03d}.jpg"), 240, f"#{s['no']} {s['mulai']:.1f}s")
        frame(ff, src, tengah, os.path.join(out, f"shot_{s['no']:03d}.jpg"), 540, f"#{s['no']} {s['mulai']:.1f}s")
    lembar([os.path.join(tmp, f"s{i:03d}.jpg") for i in range(len(data["shots"]))], os.path.join(out, "SHOTS.jpg"))
    detik = int(data["durasi"])
    for t in range(detik):
        frame(ff, src, t + 0.5, os.path.join(tmp, f"d{t:03d}.jpg"), 180, f"{t}s")
    lembar([os.path.join(tmp, f"d{t:03d}.jpg") for t in range(detik)], os.path.join(out, "PER-DETIK.jpg"), kol=8)
    shutil.rmtree(tmp, ignore_errors=True)
    if "--tanpa-transkrip" not in sys.argv and data["ada_audio"]:
        data["transkrip"] = transkrip(src)
    json.dump(data, open(os.path.join(out, "bedah.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = data["ritme"]
    print(f"OK: {data['durasi']} dtk · {data['lebar']}x{data['tinggi']} · {r['jumlah_shot']} shot "
          f"(median {r['median_dtk']} dtk, {r['shot_per_10dtk']} shot/10 dtk) → {out}")


if __name__ == "__main__":
    main()
