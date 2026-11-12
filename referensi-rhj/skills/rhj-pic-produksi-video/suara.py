#!/usr/bin/env python3
"""Buat audio dialog/VO dari daftar baris memakai API ElevenLabs (text-to-speech).

Pakai:
  python3 suara.py baris.json            # buat semua file audio yang belum ada
  python3 suara.py baris.json --dry-run  # tampilkan rencana + jumlah karakter, tanpa memanggil API

baris.json: {"keluar": "audio", "baris": [{"file": "d01-lastri.mp3", "preset": "Lastri-dialog",
             "teks": "Yang ngelas juga saya."}, ...]}
Preset (voice_id + setelan) dibaca dari voices.json di folder skill ini.
Kunci API: env ELEVENLABS_API_KEY (JANGAN ditulis ke file/repo).
"""
import json, os, sys, urllib.request, urllib.error

DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    jalur = os.path.abspath(sys.argv[1]); basis = os.path.dirname(jalur)
    cfg = json.load(open(jalur, encoding="utf-8"))
    presets = json.load(open(os.path.join(DIR, "voices.json"), encoding="utf-8"))["preset"]
    keluar = os.path.join(basis, cfg.get("keluar", "audio")); os.makedirs(keluar, exist_ok=True)
    dry = "--dry-run" in sys.argv
    total = 0
    for b in cfg["baris"]:
        p = presets.get(b["preset"])
        if not p or not p.get("voice_id") or p["voice_id"].startswith("ISI"):
            sys.exit(f"GAGAL: preset '{b['preset']}' belum punya voice_id di voices.json")
        total += len(b["teks"])
    print(f"{len(cfg['baris'])} baris, {total} karakter")
    if dry:
        for b in cfg["baris"]:
            print(f"- {b['file']} [{b['preset']}] {b['teks']}")
        return
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("GAGAL: env ELEVENLABS_API_KEY kosong (isi di pengaturan environment cloud, bukan di chat)")
    for b in cfg["baris"]:
        out = os.path.join(keluar, b["file"])
        if os.path.exists(out) and "--timpa" not in sys.argv:
            print(f"lewati (sudah ada): {b['file']}"); continue
        p = presets[b["preset"]]
        body = {"text": b["teks"], "model_id": p.get("model_id", "eleven_multilingual_v2")}
        if p.get("voice_settings"):
            body["voice_settings"] = p["voice_settings"]
        url = (f"https://api.elevenlabs.io/v1/text-to-speech/{p['voice_id']}"
               f"?output_format={p.get('output_format', 'mp3_44100_128')}")
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                     headers={"xi-api-key": key, "Content-Type": "application/json",
                                              "Accept": "audio/mpeg"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                open(out, "wb").write(r.read())
        except urllib.error.HTTPError as e:
            sys.exit(f"GAGAL {b['file']}: HTTP {e.code} {e.read()[:300].decode(errors='replace')}")
        print(f"OK: {b['file']}")


if __name__ == "__main__":
    main()
