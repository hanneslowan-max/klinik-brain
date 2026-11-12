#!/usr/bin/env python3
"""SFX & beat sintetis untuk iklan (numpy, tanpa sampel luar → tanpa urusan lisensi musik).

Pakai:
  python3 tools/sfx_sintetis.py <folder_keluar> [--bpm 120] [--bar 16] [--seed 7]

Keluaran WAV 48 kHz stereo 16-bit, puncak -1 dBFS per berkas:
  beat.wav      loop drum industrial (kick ketukan 1 & 3, "clank" logam 2 & 4, hi-hat 1/8), mulai tepat di downbeat
  drone.wav     dengung rendah 55 Hz + kuint, untuk isi jeda
  roomtone.wav  derau ruang pabrik sangat pelan (pengganti hening total)
  whoosh.wav    sapuan derau 0,5 dtk, puncak di 0,30 dtk (taruh ~0,3 dtk sebelum potongan)
  impact.wav    hentakan rendah 1,2 dtk (transien di 0)
  riser.wav     naik 1,0 dtk, berakhir tepat di potongan
  tick.wav      klik pendek (penghitung terisi / denyut "?")
  pop.wav       "ding" pendek (sel "?" jadi merah)
Ditempatkan di EDL `audio` rakit_video.py (field pada / in / dur / gain_db). Agent tidak mendengar
audio: hasil wajib didengar manusia sebelum tayang.
"""
import argparse, os, wave
import numpy as np

SR = 48000


def tulis(path, x):
    x = np.asarray(x, dtype=np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    pk = np.max(np.abs(x)) or 1.0
    x = x / pk * 10 ** (-1 / 20)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())


def t_(dur):
    return np.arange(int(SR * dur)) / SR


def lowpass(x, fc):
    """One-pole low-pass; fc boleh array (cutoff berubah per sampel)."""
    fc = np.broadcast_to(np.asarray(fc, dtype=np.float64), x.shape)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def highpass(x, fc):
    return x - lowpass(x, fc)


def kick(rng):
    t = t_(0.45)
    f = 46 + 120 * np.exp(-t / 0.032)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.24)
    klik = highpass(rng.standard_normal(len(t)), 2500) * np.exp(-t / 0.004) * 0.35
    return body + klik


def clank(rng):
    t = t_(0.4)
    n = highpass(lowpass(rng.standard_normal(len(t)), 6500), 1400) * np.exp(-t / 0.075)
    metal = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / d)
                for f, d in [(523, .20), (811, .16), (1187, .13), (1693, .10), (2417, .07)]) / 5
    return 0.65 * n / (np.max(np.abs(n)) or 1) + 0.45 * metal


def hat(rng):
    t = t_(0.09)
    return highpass(rng.standard_normal(len(t)), 7000) * np.exp(-t / 0.022)


def beat(rng, bpm, bars):
    step = 60 / bpm / 2                     # 1/8 not
    total = bars * 8 * step
    out = np.zeros(int(SR * total) + SR)
    k, c, h = kick(rng), clank(rng), hat(rng)
    k /= np.max(np.abs(k)); c /= np.max(np.abs(c)); h /= np.max(np.abs(h))

    def taruh(sig, t0, g):
        i = int(round(t0 * SR)); out[i:i + len(sig)] += g * sig[:len(out) - i]
    for b in range(bars):
        t0 = b * 8 * step
        for s in range(8):
            taruh(h, t0 + s * step, 0.16 if s % 2 else 0.24)
        taruh(k, t0, 0.95); taruh(k, t0 + 4 * step, 0.85)
        if b % 2:
            taruh(k, t0 + 7 * step, 0.55)     # sinkop di akhir bar genap
        taruh(c, t0 + 2 * step, 0.55); taruh(c, t0 + 6 * step, 0.6)
    out = out[:int(SR * total)]
    # sedikit lebar stereo: hi-hat & clank sudah sama; tambah delay pendek kanan
    d = int(0.011 * SR)
    kanan = np.concatenate([np.zeros(d), out[:-d]]) * 0.25 + out * 0.85
    return np.stack([out, kanan], axis=1)


def drone(rng, dur=20.0):
    t = t_(dur)
    x = 0.6 * np.sin(2 * np.pi * 55 * t) + 0.3 * np.sin(2 * np.pi * 82.5 * t) + 0.12 * np.sin(2 * np.pi * 110 * t)
    x += 0.15 * lowpass(rng.standard_normal(len(t)), 180)
    x *= 0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t)
    f = np.minimum(1, np.minimum(t / 0.4, (dur - t) / 0.4))
    return x * f


def roomtone(rng, dur=20.0):
    b = np.cumsum(rng.standard_normal(int(SR * dur)))
    b = highpass(b, 30)
    b = lowpass(b, 900)
    return b / (np.max(np.abs(b)) or 1)


def whoosh(rng):
    t = t_(0.5)
    env = np.where(t < 0.30, (t / 0.30) ** 2, np.exp(-(t - 0.30) / 0.07))
    fc = 250 + 5500 * env
    n = lowpass(rng.standard_normal(len(t)), fc) * env
    pan = np.clip(t / 0.5, 0, 1)
    return np.stack([n * (1 - 0.6 * pan), n * (0.4 + 0.6 * pan)], axis=1)


def impact(rng):
    t = t_(1.2)
    f = 34 + 50 * np.exp(-t / 0.06)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45)
    hit = lowpass(rng.standard_normal(len(t)), 1800) * np.exp(-t / 0.05)
    return boom + 0.5 * hit / (np.max(np.abs(hit)) or 1)


def riser(rng):
    t = t_(1.0)
    env = (t / 1.0) ** 2
    n = highpass(rng.standard_normal(len(t)), 300 + 5000 * env) * env
    s = np.sin(2 * np.pi * np.cumsum(180 + 620 * env) / SR) * env * 0.25
    return n / (np.max(np.abs(n)) or 1) * 0.8 + s


def tick(rng):
    t = t_(0.06)
    return np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.006) + \
        highpass(rng.standard_normal(len(t)), 4000) * np.exp(-t / 0.002) * 0.4


def pop(rng):
    t = t_(0.35)
    f = 880 + 440 * np.minimum(1, t / 0.03)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)
    return x + 0.35 * np.sin(2 * np.pi * 2640 * t) * np.exp(-t / 0.05)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--bpm', type=float, default=120)
    ap.add_argument('--bar', type=int, default=16)
    ap.add_argument('--seed', type=int, default=7)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rng = np.random.default_rng(a.seed)
    for nama, sig in [('beat', beat(rng, a.bpm, a.bar)), ('drone', drone(rng)), ('roomtone', roomtone(rng)),
                      ('whoosh', whoosh(rng)), ('impact', impact(rng)), ('riser', riser(rng)),
                      ('tick', tick(rng)), ('pop', pop(rng))]:
        p = os.path.join(a.out, f'{nama}.wav'); tulis(p, sig); print(p)


if __name__ == '__main__':
    main()
