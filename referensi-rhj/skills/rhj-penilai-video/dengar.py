"""Dengar video: transkrip per kata + ukuran suara per baris dialog, untuk menilai humor & naskah kaku.

Pakai:
  export FFMPEG=$(bash .claude/skills/rhj-pic-produksi-video/pasang_ffmpeg.sh)
  export PYTHONPATH=$(bash .claude/skills/rhj-penilai-video/pasang_dengar.sh)
  python3 dengar.py <video.mp4> <folder_keluar> [--model small] [--bahasa id]

Keluaran di folder:
  dengar.json  per baris (kalimat; putus di . ? ! atau jeda >= 0.25 dtk): mulai/selesai, teks, kata per detik, jeda sebelum & sesudah,
               rentang nada (semiton p10-p90), keras suara (dB), selisih suara vs latar (dB), tanda
  DENGAR.txt   ringkasan yang enak dibaca (tabel baris + tanda)
  BICARA.jpg   1 frame di tengah tiap baris, berlabel teks: cek siapa yang bicara & bibir bergerak/tidak

Batas (sebut di laporan): ini UKURAN, bukan mendengar. Nada dihitung dari autokorelasi sederhana;
musik latar/SFX bisa mengacaukan nada. "Latar" = keras suara di celah tanpa dialog (biasanya musik/ambience).
Ambang tanda di bawah = titik awal, dikalibrasi lewat memori/PENILAIAN-VIDEO-LOG.md.
"""
import json, os, subprocess, sys, wave
import numpy as np


def _pastikan_pil():
    # PIL bawaan sistem di container cloud bisa rusak (ImportError _imaging, 8 Nov 2026).
    try:
        from PIL import Image  # noqa: F401
        return
    except ImportError:
        pass
    cache = os.path.expanduser("~/.cache/rhj-pil")
    if not os.path.isdir(os.path.join(cache, "PIL")):
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--target", cache, "pillow"], check=True)
    for m in [m for m in sys.modules if m == "PIL" or m.startswith("PIL.")]:
        del sys.modules[m]
    sys.path.insert(0, cache)


_pastikan_pil()

SR = 16000
AMBANG_DATAR_ST = 4.0      # rentang nada p10-p90 <= ini → indikasi suara datar
AMBANG_CEPAT_KPS = 4.0     # kata per detik > ini → terburu-buru
AMBANG_JEDA_PUNCH = 0.3    # jeda sebelum kalimat pendek terakhir/punchline < ini → tanpa ancang-ancang
AMBANG_TIMPA_DB = 6.0      # suara dialog hanya <= ini dB di atas latar → rawan ketimpa musik
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def ffmpeg():
    ff = os.environ.get("FFMPEG")
    if ff and os.path.exists(ff):
        return ff
    sk = os.path.join(os.path.dirname(__file__), "..", "rhj-pic-produksi-video", "pasang_ffmpeg.sh")
    return subprocess.run(["bash", sk], capture_output=True, text=True, check=True).stdout.strip()


def audio(ff, src, out):
    wav = os.path.join(out, "_audio.wav")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-vn", wav], check=True)
    with wave.open(wav) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return wav, x


def db(x):
    return float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)) if len(x) else None


def nada(x):
    """F0 per 10 ms (autokorelasi, 75-400 Hz). Kembalikan array Hz untuk frame bersuara."""
    n, hop = int(0.04 * SR), int(0.01 * SR)
    lo, hi = int(SR / 400), int(SR / 75)
    if len(x) < n:
        return np.array([])
    batas = 0.1 * np.sqrt(np.mean(x ** 2)) * 3 + 1e-4
    f0 = []
    for i in range(0, len(x) - n, hop):
        fr = x[i:i + n] - np.mean(x[i:i + n])
        if np.sqrt(np.mean(fr ** 2)) < batas:
            continue
        ac = np.correlate(fr, fr, "full")[n - 1:]
        if ac[0] <= 0:
            continue
        ac = ac / ac[0]
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.5:
            f0.append(SR / k)
    return np.array(f0)


def rentang_st(f0):
    if len(f0) < 30:  # < 0,3 dtk bersuara → terlalu pendek untuk menilai nada
        return None
    st = 12 * np.log2(f0 / np.median(f0))
    return round(float(np.percentile(st, 90) - np.percentile(st, 10)), 1)


def transkrip(wav, model, bahasa):
    from faster_whisper import WhisperModel
    m = WhisperModel(model, device="cpu", compute_type="int8")
    segs, inf = m.transcribe(wav, language=bahasa, vad_filter=True, word_timestamps=True)
    # Pecah jadi baris per kalimat: putus di tanda . ? ! atau jeda antar-kata >= 0.25 dtk
    kata = [w for s in segs for w in (s.words or [])]
    baris, cur = [], []
    for i, w in enumerate(kata):
        cur.append(w)
        nxt = kata[i + 1] if i + 1 < len(kata) else None
        if nxt is None or w.word.strip()[-1:] in ".?!" or nxt.start - w.end >= 0.25:
            baris.append({"teks": "".join(k.word for k in cur).strip(), "kata": len(cur),
                          "bicara_mulai": round(cur[0].start, 2), "bicara_selesai": round(cur[-1].end, 2)})
            cur = []
    return inf.language, baris


def frame(ff, src, t, out, label):
    from PIL import Image, ImageDraw, ImageFont
    subprocess.run([ff, "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1",
                    "-vf", "scale=300:-2", out])
    if not os.path.exists(out):
        return
    im = Image.open(out).convert("RGB")
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, 15) if os.path.exists(FONT) else ImageFont.load_default()
    d.text((6, 4), label[:38], font=f, fill="yellow", stroke_width=2, stroke_fill="black")
    im.save(out, quality=88)


def lembar(files, out, kol=5):
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


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], os.path.abspath(sys.argv[2])
    opt = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    if not os.path.isfile(src):
        sys.exit(f"GAGAL: file tidak ada: {src}")
    os.makedirs(out, exist_ok=True)
    ff = ffmpeg()
    wav, x = audio(ff, src, out)
    dur = len(x) / SR
    try:
        bhs, baris = transkrip(wav, opt("--model", "small"), opt("--bahasa", "id"))
    except ImportError:
        # Pasang otomatis (8 Nov 2026: dulu berhenti dan agent menyerah "tidak bisa transkrip").
        import subprocess
        d = subprocess.run(["bash", os.path.join(os.path.dirname(os.path.abspath(__file__)), "pasang_dengar.sh")],
                           capture_output=True, text=True, check=True).stdout.strip().splitlines()[-1]
        sys.path.insert(0, d)
        bhs, baris = transkrip(wav, opt("--model", "small"), opt("--bahasa", "id"))

    # latar = celah tanpa dialog (>= 0.3 dtk)
    celah, t = [], 0.0
    for b in baris + [{"bicara_mulai": dur, "bicara_selesai": dur}]:
        if b["bicara_mulai"] - t >= 0.3:
            celah.append((t, b["bicara_mulai"]))
        t = max(t, b["bicara_selesai"])
    lat = np.concatenate([x[int(a * SR):int(b * SR)] for a, b in celah]) if celah else np.array([])
    latar_db = db(lat) if len(lat) > SR * 0.3 else None

    tmp = os.path.join(out, "_b"); os.makedirs(tmp, exist_ok=True)
    for i, b in enumerate(baris):
        seg = x[int(b["bicara_mulai"] * SR):int(b["bicara_selesai"] * SR)]
        lama = max(b["bicara_selesai"] - b["bicara_mulai"], 0.01)
        b["kata_per_dtk"] = round(b["kata"] / lama, 1)
        b["jeda_sebelum"] = round(b["bicara_mulai"] - (baris[i - 1]["bicara_selesai"] if i else 0.0), 2)
        b["jeda_sesudah"] = round((baris[i + 1]["bicara_mulai"] if i + 1 < len(baris) else dur) - b["bicara_selesai"], 2)
        b["nada_rentang_st"] = rentang_st(nada(seg))
        b["keras_db"] = round(db(seg), 1) if len(seg) else None
        b["di_atas_latar_db"] = round(b["keras_db"] - latar_db, 1) if latar_db is not None and b["keras_db"] is not None else None
        tanda = []
        if b["nada_rentang_st"] is not None and b["nada_rentang_st"] <= AMBANG_DATAR_ST:
            tanda.append("NADA DATAR")
        if b["kata"] >= 4 and b["kata_per_dtk"] > AMBANG_CEPAT_KPS:
            tanda.append("CEPAT")
        if b["di_atas_latar_db"] is not None and b["di_atas_latar_db"] <= AMBANG_TIMPA_DB:
            tanda.append("RAWAN KETIMPA LATAR")
        if b["kata"] <= 6 and b["jeda_sebelum"] < AMBANG_JEDA_PUNCH and i:
            tanda.append("KALIMAT PENDEK TANPA JEDA (cek bila punchline)")
        b["tanda"] = tanda
        frame(ff, src, (b["bicara_mulai"] + b["bicara_selesai"]) / 2, os.path.join(tmp, f"b{i:03d}.jpg"),
              f"#{i + 1} {b['bicara_mulai']:.1f}s {b['teks']}")
    lembar([os.path.join(tmp, f"b{i:03d}.jpg") for i in range(len(baris))], os.path.join(out, "BICARA.jpg"))
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp); os.remove(wav)

    f0_all = nada(np.concatenate([x[int(b["bicara_mulai"] * SR):int(b["bicara_selesai"] * SR)] for b in baris])) if baris else np.array([])
    data = {"sumber": os.path.basename(src), "durasi": round(dur, 2), "bahasa": bhs,
            "latar_db": round(latar_db, 1) if latar_db is not None else None,
            "persen_waktu_bicara": round(100 * sum(b["bicara_selesai"] - b["bicara_mulai"] for b in baris) / dur, 1) if dur else None,
            "nada_rentang_st_seluruh": rentang_st(f0_all),
            "ambang": {"datar_st": AMBANG_DATAR_ST, "cepat_kps": AMBANG_CEPAT_KPS,
                       "jeda_punch_dtk": AMBANG_JEDA_PUNCH, "timpa_db": AMBANG_TIMPA_DB},
            "baris": baris}
    json.dump(data, open(os.path.join(out, "dengar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(out, "DENGAR.txt"), "w", encoding="utf-8") as f:
        f.write(f"{data['sumber']} · {data['durasi']} dtk · bahasa {bhs} · bicara {data['persen_waktu_bicara']}% · "
                f"latar {data['latar_db']} dB · rentang nada seluruh {data['nada_rentang_st_seluruh']} st\n\n")
        for i, b in enumerate(baris):
            f.write(f"#{i + 1} {b['bicara_mulai']:.1f}-{b['bicara_selesai']:.1f}s | jeda {b['jeda_sebelum']:.2f}/{b['jeda_sesudah']:.2f} | "
                    f"{b['kata_per_dtk']} kps | nada {b['nada_rentang_st']} st | +{b['di_atas_latar_db']} dB | "
                    f"{', '.join(b['tanda']) or '-'}\n    {b['teks']}\n")
    print(f"OK: {len(baris)} baris dialog · latar {data['latar_db']} dB · nada seluruh {data['nada_rentang_st_seluruh']} st → {out}")


if __name__ == "__main__":
    main()
