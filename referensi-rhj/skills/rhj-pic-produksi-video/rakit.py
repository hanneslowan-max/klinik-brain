#!/usr/bin/env python3
"""Rakit draf video 9:16 dari resep JSON (klip AI + audio + teks layar) memakai FFmpeg.

Pakai:
  python3 rakit.py resep.json            # rakit draf + cover + lembar cek frame
  python3 rakit.py resep.json --cek      # hanya validasi resep & file (tanpa render)

Path di resep relatif terhadap folder file resep. FFmpeg dicari dari env FFMPEG,
lalu PATH, lalu paket imageio-ffmpeg (jalankan pasang_ffmpeg.sh bila belum ada).
"""
import json, os, shutil, subprocess, sys, tempfile

POSISI = {  # (perataan, x relatif, y relatif, ukuran font relatif tinggi) — zona aman: hindari 15% bawah & 12% kanan
    "label":    ("kiri", 0.05, 0.06, 0.022),
    "label2":   ("kiri", 0.05, 0.085, 0.018),
    "hook":     ("tengah", 0.5, 0.16, 0.048),
    "tengah":   ("tengah", 0.5, 0.45, 0.040),
    "kartu":    ("kiri", 0.07, 0.55, 0.034),
    "subtitle": ("tengah", 0.5, 0.70, 0.030),
    "cliff":    ("tengah", 0.5, 0.40, 0.040),
}
MERAH = "#B51B1B"
FONT_CADANGAN = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"  # sementara; font brand diunggah ke Drive aset
FONT_MIRING = "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"


def cari_ffmpeg():
    if os.environ.get("FFMPEG"):
        return os.environ["FFMPEG"]
    if shutil.which("ffmpeg"):
        return shutil.which("ffmpeg")
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("GAGAL: ffmpeg tidak ada. Jalankan: bash pasang_ffmpeg.sh lalu ulangi dengan env FFMPEG=<path>")


def render_teks(t, W, H, font, font_miring, out):
    """Teks layar → PNG transparan seukuran frame (Pillow; FFmpeg portabel tidak punya drawtext).
    t["merah"] = daftar kata yang diwarnai merah brand (#B51B1B)."""
    from PIL import Image, ImageDraw, ImageFont
    rata, xr, yr, rel = POSISI[t.get("posisi", "subtitle")]
    size = int(H * float(t.get("ukuran", rel)))
    f = ImageFont.truetype(font_miring if t.get("miring") else font, size)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    stroke = max(2, size // 12); maks = int(W * (0.80 if rata == "tengah" else 0.78))
    merah = {w.strip(".,!?").upper() for w in t.get("merah", [])}
    baris, cur = [], []
    for kata in t["isi"].split():
        uji = " ".join(cur + [kata])
        if cur and d.textlength(uji, font=f) > maks:
            baris.append(cur); cur = [kata]
        else:
            cur.append(kata)
    baris.append(cur)
    tinggi = int(size * 1.25); y = int(H * yr)
    lebar_baris = [d.textlength(" ".join(b), font=f) for b in baris]
    if t.get("kotak"):
        lb = max(lebar_baris); x0 = (W - lb) / 2 if rata == "tengah" else W * xr
        d.rounded_rectangle([x0 - 24, y - 16, x0 + lb + 24, y + tinggi * len(baris) + 8], 14, fill=(0, 0, 0, 140))
    for b, lb in zip(baris, lebar_baris):
        x = (W - lb) / 2 if rata == "tengah" else W * xr
        for kata in b:
            isi = kata + " "
            c = MERAH if kata.strip(".,!?").upper() in merah else t.get("warna", "#FFFFFF")
            d.text((x, y), isi, font=f, fill=c, stroke_width=stroke, stroke_fill="black")
            x += d.textlength(isi, font=f)
        y += tinggi
    img.save(out)


def validasi(r, basis):
    galat = []
    for k in ("kode", "shots"):
        if k not in r:
            galat.append(f"resep tanpa '{k}'")
    for i, s in enumerate(r.get("shots", []), 1):
        p = os.path.join(basis, s.get("file", ""))
        if not os.path.isfile(p):
            galat.append(f"shot {i}: file tidak ada: {s.get('file')}")
        if float(s.get("durasi", 0)) <= 0:
            galat.append(f"shot {i}: durasi wajib > 0")
    for i, a in enumerate(r.get("audio", []), 1):
        if not os.path.isfile(os.path.join(basis, a.get("file", ""))):
            galat.append(f"audio {i}: file tidak ada: {a.get('file')}")
    total = sum(float(s.get("durasi", 0)) for s in r.get("shots", []))
    for i, t in enumerate(r.get("teks", []), 1):
        if t.get("posisi", "subtitle") not in POSISI:
            galat.append(f"teks {i}: posisi '{t.get('posisi')}' tidak dikenal ({', '.join(POSISI)})")
        if float(t.get("selesai", total)) > total + 0.01:
            galat.append(f"teks {i}: selesai {t.get('selesai')} > durasi total {total:.2f}")
    return galat, total


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    jalur = os.path.abspath(sys.argv[1])
    basis = os.path.dirname(jalur)
    r = json.load(open(jalur, encoding="utf-8"))
    galat, total = validasi(r, basis)
    print(f"resep {r.get('kode')}: {len(r.get('shots', []))} shot, durasi total {total:.2f} dtk")
    if galat:
        print("GALAT:\n- " + "\n- ".join(galat))
        sys.exit(1)
    if "--cek" in sys.argv:
        print("OK: resep valid")
        return

    ff = cari_ffmpeg()
    W, H = r.get("resolusi", [1080, 1920])
    fps = r.get("fps", 30)
    font = os.path.join(basis, r["font"]) if r.get("font") else FONT_CADANGAN
    font_miring = os.path.join(basis, r["font_miring"]) if r.get("font_miring") else FONT_MIRING
    keluar = os.path.join(basis, r.get("keluaran", f"draft-{r['kode']}.mp4"))
    tmp = tempfile.mkdtemp(prefix="rakit-")

    args, fc, n = [ff, "-y", "-hide_banner", "-loglevel", "error"], [], 0
    # 1) video per shot: potong, isi bingkai 9:16, samakan fps
    vlabel, alabel_klip = [], []
    for i, s in enumerate(r["shots"]):
        args += ["-i", os.path.join(basis, s["file"])]
        d = float(s["durasi"]); m = float(s.get("mulai_klip", 0))
        fc.append(f"[{n}:v]trim=start={m}:duration={d},setpts=PTS-STARTPTS,"
                  f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={fps}[v{i}]")
        vlabel.append(f"[v{i}]")
        vol = s.get("volume_klip")  # dB; None = bisukan
        if vol is not None and s.get("ada_audio", True):
            fc.append(f"[{n}:a]atrim=start={m}:duration={d},asetpts=PTS-STARTPTS,volume={vol}dB,"
                      f"apad=whole_dur={d}[ak{i}]")
        else:
            fc.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d}[ak{i}]")
        alabel_klip.append(f"[ak{i}]")
        n += 1
    fc.append("".join(f"{v}{a}" for v, a in zip(vlabel, alabel_klip)) +
              f"concat=n={len(vlabel)}:v=1:a=1[vcat][acat]")

    # 2) teks layar: PNG transparan di-overlay sesuai jendela waktu
    vcur = "[vcat]"
    for j, t in enumerate(r.get("teks", [])):
        png = os.path.join(tmp, f"t{j}.png")
        render_teks(t, W, H, font, font_miring, png)
        args += ["-i", png]
        a, b = float(t.get("mulai", 0)), float(t.get("selesai", total))
        fc.append(f"{vcur}[{n}:v]overlay=0:0:enable='between(t,{a},{b})'[vt{j}]")
        vcur = f"[vt{j}]"; n += 1

    # 3) audio tambahan (VO, dialog, SFX, musik): delay + volume, lalu campur
    amix = ["[acat]"]
    for k, au in enumerate(r.get("audio", [])):
        args += ["-i", os.path.join(basis, au["file"])]
        ms = int(float(au.get("mulai", 0)) * 1000)
        dur = f",atrim=duration={au['durasi']}" if au.get("durasi") else ""
        fc.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo{dur},"
                  f"volume={au.get('volume', 0)}dB,adelay={ms}|{ms}[ax{k}]")
        amix.append(f"[ax{k}]")
        n += 1
    fc.append("".join(amix) + f"amix=inputs={len(amix)}:normalize=0:duration=first,"
              f"atrim=duration={total},loudnorm=I=-14:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[aout]")

    args += ["-filter_complex", ";".join(fc), "-map", vcur, "-map", "[aout]",
             "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", keluar]
    hasil = subprocess.run(args)
    if hasil.returncode:
        sys.exit("GAGAL render (lihat pesan ffmpeg di atas)")

    # 4) cover + lembar cek frame (1 frame di tengah tiap shot)
    cover_t = float(r.get("cover_detik", 0.5))
    cover = keluar.replace(".mp4", "-cover.jpg")
    subprocess.run([ff, "-y", "-loglevel", "error", "-ss", str(cover_t), "-i", keluar, "-frames:v", "1", cover])
    titik, t0 = [], 0.0
    for s in r["shots"]:
        titik.append(t0 + float(s["durasi"]) / 2); t0 += float(s["durasi"])
    frames = []
    for i, tt in enumerate(titik):
        fp = os.path.join(tmp, f"f{i:02d}.jpg")
        subprocess.run([ff, "-y", "-loglevel", "error", "-ss", f"{tt:.2f}", "-i", keluar,
                        "-frames:v", "1", "-vf", "scale=270:480", fp])
        frames.append(fp)
    kol = min(len(frames), 6); bar = (len(frames) + kol - 1) // kol
    lembar = keluar.replace(".mp4", "-cek-frame.jpg")
    subprocess.run([ff, "-y", "-loglevel", "error", "-framerate", "1", "-i", os.path.join(tmp, "f%02d.jpg"),
                    "-vf", f"tile={kol}x{bar}:padding=6:color=white", "-frames:v", "1", lembar])
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"OK: {keluar}\n    cover: {cover}\n    cek frame: {lembar}")


if __name__ == "__main__":
    main()
