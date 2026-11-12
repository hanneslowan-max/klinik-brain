#!/usr/bin/env python3
"""Mix audio iklan animasi klinik: VO + musik (ducking) + efek suara sintetis -> -14 LUFS, lalu gabung ke video.

Pakai:  python3 tools/animasi/mix.py resep.json
resep.json:
{
  "video": "render/X-bisu.mp4",          # video tanpa suara (hasil hf.sh render)
  "keluar": "render/X-final.mp4",
  "durasi": 26.6,
  "vo": {"file": "vo1.mp3", "tempo": 1.12, "mulai": 0.3, "gain_db": 0},
  "musik": {"file": "mu1.mp3", "gain_db": -14, "tempo": 1.0, "fade_in": 0.3, "fade_out": 1.5, "duck": true},
  "sfx": [{"t": 4.9, "jenis": "dentum", "gain_db": -6}, ...]
}
Jenis sfx: klik, dentum, whoosh, kriet, ding, tik, alarm, gesek, rewind.
Efek suara dibuat dari rumus (aevalsrc/anoisesrc), bebas lisensi.
"""
import json, os, subprocess, sys, tempfile

SFX = {
    # (filter lavfi, durasi)
    "klik": ("aevalsrc='0.9*sin(2*PI*2400*t)*exp(-90*t)+0.5*sin(2*PI*900*t)*exp(-60*t)':d=0.12", 0.12),
    "dentum": ("aevalsrc='1.0*sin(2*PI*(70-30*t)*t)*exp(-7*t)':d=0.6", 0.6),
    "whoosh": ("anoisesrc=d=0.45:c=pink:a=0.9,bandpass=f=1400:w=1.2,afade=t=in:d=0.2,afade=t=out:st=0.2:d=0.25", 0.45),
    "kriet": ("aevalsrc='0.4*sin(2*PI*(1800+600*sin(2*PI*9*t))*t)*(t<0.5)':d=0.5,afade=t=out:st=0.35:d=0.15", 0.5),
    "ding": ("aevalsrc='0.6*sin(2*PI*1320*t)*exp(-4*t)+0.3*sin(2*PI*2640*t)*exp(-6*t)':d=1.0", 1.0),
    "tik": ("aevalsrc='0.7*sin(2*PI*3200*t)*exp(-200*t)':d=0.05", 0.05),
    "alarm": ("aevalsrc='0.35*sin(2*PI*880*t)*(mod(t,0.5)<0.25)+0.35*sin(2*PI*660*t)*(mod(t,0.5)>=0.25)':d=1.0", 1.0),
    "gesek": ("anoisesrc=d=0.5:c=brown:a=0.8,highpass=f=300,afade=t=out:st=0.2:d=0.3", 0.5),
    "rewind": ("aevalsrc='0.5*sin(2*PI*(300+1500*t*t)*t)':d=0.7,afade=t=out:st=0.5:d=0.2", 0.7),
}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg gagal:\n" + r.stderr[-1500:])


def main():
    resep = json.load(open(sys.argv[1], encoding="utf-8"))
    dasar = os.path.dirname(os.path.abspath(sys.argv[1]))
    p = lambda f: f if os.path.isabs(f) else os.path.join(dasar, f)
    D = float(resep["durasi"])
    kerja = tempfile.mkdtemp(prefix="mix-")
    masuk, graf, label = [], [], []
    # VO
    vo = resep["vo"]
    masuk += ["-i", p(vo["file"])]
    ms = int(round(vo.get("mulai", 0) * 1000))
    graf.append(f"[0:a]atempo={vo.get('tempo', 1.0)},adelay={ms}|{ms},volume={vo.get('gain_db', 0)}dB,apad,atrim=0:{D},asplit=2[vo][vosc]")
    # musik
    mu = resep.get("musik")
    idx = 1
    if mu:
        masuk += ["-stream_loop", "-1", "-i", p(mu["file"])]
        f_out = mu.get("fade_out", 1.5)
        graf.append(f"[{idx}:a]atempo={mu.get('tempo', 1.0)},atrim=0:{D},asetpts=N/SR/TB,volume={mu.get('gain_db', -14)}dB,afade=t=in:d={mu.get('fade_in', 0.3)},afade=t=out:st={D - f_out}:d={f_out}[mu0]")
        if mu.get("duck", True):
            graf.append("[mu0][vosc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[mu]")
        else:
            graf.append("[vosc]anullsink;[mu0]anull[mu]")
        label.append("[mu]")
        idx += 1
    else:
        graf.append("[vosc]anullsink")
    # sfx
    for i, s in enumerate(resep.get("sfx", [])):
        src, d = SFX[s["jenis"]]
        f = os.path.join(kerja, f"sfx{i}.wav")
        run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", src, "-ar", "48000", "-ac", "2", "-y", f])
        masuk += ["-i", f]
        t = int(round(s["t"] * 1000))
        graf.append(f"[{idx}:a]volume={s.get('gain_db', -6)}dB,adelay={t}|{t},apad,atrim=0:{D}[s{i}]")
        label.append(f"[s{i}]")
        idx += 1
    semua = "[vo]" + "".join(label)
    n = 1 + len(label)
    graf.append(f"{semua}amix=inputs={n}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.0:LRA=11[out]")
    wav = os.path.join(kerja, "campur.wav")
    run(["ffmpeg", "-v", "error"] + masuk + ["-filter_complex", ";".join(graf), "-map", "[out]", "-ar", "48000", "-ac", "2", "-t", str(D), "-y", wav])
    keluar = p(resep["keluar"])
    run(["ffmpeg", "-v", "error", "-i", p(resep["video"]), "-i", wav, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-y", keluar])
    print("ok", keluar)


if __name__ == "__main__":
    main()
