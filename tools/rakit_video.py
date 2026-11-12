#!/usr/bin/env python3
"""Rakit video iklan dari klip AI + EDL JSON (FFmpeg + Pillow).

Pakai:
  python3 tools/rakit_video.py <edl.json> --akar <folder media> [--kerja DIR] [--hanya 9x16|4x5]

Path media di EDL (klip, sfx, out_dir) relatif ke --akar (default: folder EDL);
font relatif ke root repo. Hasil:
  <out_dir>/<nama>_9x16.mp4, <nama>_4x5.mp4, <nama>_cek-frame.jpg

Teks, penghitung, dan "?" digambar di sini (bukan AI). Klip AI hanya gambar.
Struktur EDL: lihat deliverables/produksi/PM-06/edl-pm06.json; opsi tambahan (scrim di tata_letak,
teks_naik, grade per shot berisi hflip/crop bergerak) dipakai di edl-pm06-v2.json.
"""
import argparse, json, math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920          # master 9:16
W45, H45 = 1080, 1350      # 4:5


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg gagal:\n" + " ".join(cmd) + "\n" + r.stderr[-2000:])


def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------- 1. klip per shot -> segmen 1080x1920, fps tetap, tanpa audio ----------

def render_shots(edl, base, kerja):
    fps = edl.get('fps', 30)
    grade = edl.get('grade', '')
    segs = []
    for i, s in enumerate(edl['shots']):
        src = path(base, s['clip'])
        dur = float(s['dur'])
        z0, z1 = s.get('zoom', [1.0, 1.0])
        # skala ke tinggi 1920 (atau lebar 1080) lalu push-in digital linear z0->z1 sepanjang durasi
        z = f"({z0}+({z1}-{z0})*t/{dur})"
        vf = [
            f"scale={W}:{H}:force_original_aspect_ratio=increase",
            f"crop={W}:{H}",
            f"scale=w='trunc({W}*{z}/2)*2':h='trunc({H}*{z}/2)*2':eval=frame",
            f"crop={W}:{H}",
            f"fps={fps}",
        ]
        if s.get('speed'):
            vf.insert(0, f"setpts=PTS/{float(s['speed'])}")
        g = s.get('grade', grade)          # grade per shot (opsional) menimpa grade global
        if g:
            vf.append(g)
        vf.append("format=yuv420p")
        out = os.path.join(kerja, f"seg{i:02d}.mp4")
        inp = ['-loop', '1', '-framerate', str(fps), '-i', src] if src.lower().endswith(('.jpg', '.jpeg', '.png')) \
            else (['-stream_loop', '-1'] if s.get('loop') else []) + ['-ss', str(s.get('in', 0)), '-i', src]
        run(['ffmpeg', '-v', 'error', '-y', *inp, '-t', str(dur), '-an', '-vf', ",".join(vf),
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-r', str(fps), out])
        segs.append(out)
    lst = os.path.join(kerja, 'segs.txt')
    with open(lst, 'w') as f:
        f.writelines(f"file '{p}'\n" for p in segs)
    master = os.path.join(kerja, 'master_9x16.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', master])
    return master


def crop_45(edl, master, kerja):
    """Reframe 4:5 per shot: crop 1080x1350 dari master dengan offset y per shot (0..1, 0.5 = tengah)."""
    t, parts = 0.0, []
    for s in edl['shots']:
        y = int((H - H45) * float(s.get('y45', 0.5)))
        d = float(s['dur'])
        parts.append(f"between(t,{t:.4f},{t + d:.4f})*{y}")
        t += d
    yexpr = "+".join(parts) if parts else str((H - H45) // 2)
    out = os.path.join(kerja, 'master_4x5.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-i', master, '-vf', f"crop={W45}:{H45}:0:'min({H - H45},{yexpr})'",
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', out])
    return out


# ---------- 2. lapisan grafis (teks + penghitung) per frame ----------

class Gambar:
    def __init__(self, edl, base):
        self.edl = edl
        self.font_path = path(REPO, edl['font'])
        self._cache = {}

    def font(self, size):
        if size not in self._cache:
            f = ImageFont.truetype(self.font_path, size)
            try:
                f.set_variation_by_axes([self.edl.get('font_bobot', 700)])   # font variabel (Montserrat) -> Bold
            except Exception:
                pass                                                         # font statis (mis. Jost-SemiBold)
            self._cache[size] = f
        return self._cache[size]

    def lebar(self, d, s, f, size):
        """Lebar baris; dengan `tracking` (em) huruf digambar satu per satu."""
        tr = self.edl.get('tracking', 0) * size
        if not tr:
            return d.textlength(s, font=f)
        return sum(d.textlength(c, font=f) for c in s) + tr * max(0, len(s) - 1)

    def tulis(self, d, xy, s, f, size, **kw):
        tr = self.edl.get('tracking', 0) * size
        if not tr:
            d.text(xy, s, font=f, **kw)
            return
        x, y = xy
        for c in s:
            d.text((x, y), c, font=f, **kw)
            x += d.textlength(c, font=f) + tr

    def teks(self, img, tx, lay, alpha, naik=0):
        d = ImageDraw.Draw(img)
        size = int(tx.get('size', 48) * lay.get('skala_teks', 1.0))
        kapital = self.edl.get('kapital', False)                 # huruf besar semua (tampilan saja)
        lines = (tx['text'].upper() if kapital else tx['text']).split('\n')
        f = self.font(size)
        while max(self.lebar(d, l, f, size) for l in lines) > lay['lebar_teks'] and size > 24:
            size -= 2
            f = self.font(size)
        fmt = '4x5' if img.height == H45 else '9x16'
        if 'y_px' in tx:                              # posisi y per format: {"9x16": 1050, "4x5": 760} (dipakai PM-07 punch di atas lantai)
            y = int(tx['y_px'][fmt])
        else:
            y = int(img.height * tx['y_frac']) if 'y_frac' in tx else lay['y_teks']
        if 'y_frac' not in tx and tx.get('baris'):   # baris ke-n di bawah y_teks: teks bertumpuk mengikuti VO
            y += int(tx['baris'] * int(tx.get('size', 48) * lay.get('skala_teks', 1.0)) * 1.22)
        y += int(naik)
        gap = int(size * self.edl.get('jarak_baris', 0.22))
        a = int(255 * alpha)
        warna = hex_rgb(tx.get('warna', self.edl.get('warna_teks', '#FFFFFF')))   # per teks > global > putih
        garis = max(2, size // 22) if self.edl.get('garis_teks', True) else 0    # garis tepi gelap (bawaan ada)
        for l in lines:
            w = self.lebar(d, l, f, size)
            x = (img.width - w) / 2 + lay.get('x_geser', 0)     # geser tengah (px), mis. -38 = ruang teks x 54-950 (kanan 130 px kosong)
            sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
            self.tulis(ImageDraw.Draw(sh), (x + 3, y + 4), l, f, size,
                       fill=(0, 0, 0, int(a * self.edl.get('bayangan', 0.55))))
            img.alpha_composite(sh)
            self.tulis(d, (x, y), l, f, size, fill=warna + (a,),
                       stroke_width=garis, stroke_fill=(20, 20, 20, int(a * 0.8)))
            gb = tx.get('garis_bawah')     # {"kata": "foto", "warna": "#B51B1B"}: garis bawah satu kata
            kata = gb['kata'].upper() if (gb and kapital) else (gb['kata'] if gb else None)
            if gb and kata in l:
                xk = x + self.lebar(d, l[:l.index(kata)], f, size) + (self.edl.get('tracking', 0) * size if l.index(kata) else 0)
                wk = self.lebar(d, kata, f, size)
                yk = d.textbbox((xk, y), kata, font=f)[3] + max(4, size // 10)   # di bawah garis dasar huruf
                d.rounded_rectangle([xk, yk, xk + wk, yk + max(5, size // 9)], radius=2,
                                    fill=hex_rgb(gb.get('warna', '#B51B1B')) + (a,))
            y += size + gap

    def penghitung(self, img, c, lay, t, fps):
        d = ImageDraw.Draw(img)
        n, cw, ch, g = c['sel'], c.get('w', 56), c.get('h', 14), c.get('jarak', 20)
        sk = lay.get('skala_penghitung', 1.0)
        cw, ch, g = int(cw * sk), int(ch * sk), int(g * sk)
        total = n * cw + (n - 1) * g
        x0, y0 = (img.width - total) // 2, lay['y_penghitung']
        merah = hex_rgb(c.get('merah', '#B51B1B'))
        warna = hex_rgb(c.get('warna', '#FFFFFF'))      # sel terisi, garis sel, dan "?" (bawaan putih)
        for k in range(n):
            x = x0 + k * (cw + g)
            box = [x, y0, x + cw, y0 + ch]
            terakhir = k == n - 1
            if not terakhir:
                isi = t >= c['isi_pada'][k]
                d.rounded_rectangle(box, radius=3, outline=warna + (230,), width=2,
                                    fill=warna + (240,) if isi else (0, 0, 0, 70))
                continue
            if t >= c['merah_pada']:
                p = min(1.0, (t - c['merah_pada']) * fps / 6)          # pop 6 frame
                s = 1 + 0.25 * math.sin(math.pi * p)
                cx, cy = x + cw / 2, y0 + ch / 2
                d.rounded_rectangle([cx - cw * s / 2, cy - ch * s / 2, cx + cw * s / 2, cy + ch * s / 2],
                                    radius=3, fill=merah + (255,))
            else:
                a = 1.0
                p0, p1 = c['denyut']
                if p0 <= t < p1:
                    a = 0.55 + 0.45 * (0.5 + 0.5 * math.cos(2 * math.pi * (t - p0) / c.get('periode', 1.0)))
                f = self.font(int(ch * 2.3))
                q = '?'
                w = d.textlength(q, font=f)
                bb = d.textbbox((0, 0), q, font=f)
                qy = y0 + ch / 2 - (bb[1] + bb[3]) / 2
                d.text((x + (cw - w) / 2, qy), q, font=f, fill=warna + (int(255 * a),),
                       stroke_width=2, stroke_fill=(20, 20, 20, int(200 * a)))

    def scrim(self, size, s):
        """Gradasi gelap di belakang pita teks (opsional, tata_letak.scrim = {y0, y1, alpha}):
        naik 0 -> alpha di 35% pertama pita, datar, lalu turun ke 0 di 35% terakhir."""
        key = ('scrim', size, int(s['y0']), int(s['y1']), float(s.get('alpha', 0.4)))
        if key not in self._cache:
            im = Image.new('RGBA', size, (0, 0, 0, 0))
            y0, y1, am = int(s['y0']), int(s['y1']), float(s.get('alpha', 0.4))
            tepi = max(1, int((y1 - y0) * 0.35))
            d = ImageDraw.Draw(im)
            for y in range(max(0, y0), min(size[1], y1)):
                k = min(1.0, (y - y0) / tepi, (y1 - y) / tepi)
                k = k * k * (3 - 2 * k)                       # smoothstep
                d.line([(0, y), (size[0], y)], fill=(0, 0, 0, int(255 * am * k)))
            self._cache[key] = im
        return self._cache[key]

    def frame(self, size, lay, t, fps):
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        if lay.get('scrim'):
            img.alpha_composite(self.scrim(size, lay['scrim']))
        c = self.edl.get('penghitung')
        if c and c.get('mulai', 0) <= t:
            self.penghitung(img, c, lay, t, fps)
        fade = self.edl.get('fade_teks', 0.12)
        naik_px = self.edl.get('teks_naik', 0)          # animasi masuk: teks naik N px selama fade-in
        for tx in self.edl['teks']:
            if tx['t0'] <= t < tx['t1']:
                if tx.get('scrim_px'):                 # gradasi gelap hanya selama teks ini tampil: {"9x16": [y0, y1, alpha], "4x5": [...]}
                    y0, y1, am = tx['scrim_px']['4x5' if size[1] == H45 else '9x16']
                    img.alpha_composite(self.scrim(size, {'y0': y0, 'y1': y1, 'alpha': am}))
                a = min(1.0, (t - tx['t0']) / fade) if fade else 1.0
                p = 1 - (1 - a) ** 3                                 # ease-out
                a = min(a, (tx['t1'] - t) / fade) if (fade and tx.get('fade_keluar', True)) else a
                self.teks(img, tx, lay, max(0.0, a), naik=(1 - p) * naik_px * lay.get('skala_teks', 1.0))
        return img


def render_lapisan(edl, base, kerja, size, lay, tag):
    fps = edl.get('fps', 30)
    total = sum(float(s['dur']) for s in edl['shots'])
    n = int(round(total * fps))
    d = os.path.join(kerja, f'lapisan_{tag}')
    os.makedirs(d, exist_ok=True)
    g = Gambar(edl, base)
    prev = None
    for i in range(n):
        im = g.frame(size, lay, i / fps, fps)
        b = im.tobytes()
        p = os.path.join(d, f'{i:05d}.png')
        if b == prev:                        # frame sama -> salin, hemat waktu
            shutil.copyfile(os.path.join(d, f'{i - 1:05d}.png'), p)
        else:
            im.save(p, compress_level=1)
        prev = b
    return os.path.join(d, '%05d.png'), n


# ---------- 3. audio ----------

def mix_audio(edl, base, kerja, total):
    items = []
    for a in edl.get('audio', []):
        if os.path.exists(path(base, a['file'])):
            items.append(a)
        else:
            print(f"PERINGATAN: audio {a['file']} tidak ada, dilewati", file=sys.stderr)
    out = os.path.join(kerja, 'audio.wav')
    if not items:
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', str(total), out])
        return out
    args, fl = [], []
    for k, a in enumerate(items):
        args += ['-i', path(base, a['file'])]
        ms = int(float(a['pada']) * 1000)
        f = f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo"
        if a.get('in') or a.get('dur'):
            f += f",atrim=start={a.get('in', 0)}" + (f":duration={a['dur']}" if a.get('dur') else '') + ",asetpts=PTS-STARTPTS"
        f += f",volume={a.get('gain_db', 0)}dB,adelay={ms}|{ms}[a{k}]"
        fl.append(f)
    fo = edl.get('fade_akhir', 0.5)
    fl.append("".join(f"[a{k}]" for k in range(len(items))) +
              f"amix=inputs={len(items)}:normalize=0,apad,atrim=0:{total},"
              f"afade=t=out:st={total - fo}:d={fo},loudnorm=I={edl.get('lufs', -14)}:TP=-1.5:LRA=11[aout]")
    run(['ffmpeg', '-v', 'error', '-y', *args, '-filter_complex', ";".join(fl), '-map', '[aout]',
         '-ar', '48000', out])
    return out


# ---------- 4. gabung + ekspor ----------

def gabung(master, lapisan, n, audio, fps, out):
    run(['ffmpeg', '-v', 'error', '-y', '-i', master, '-framerate', str(fps), '-i', lapisan, '-i', audio,
         '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]',
         '-map', '[v]', '-map', '2:a', '-frames:v', str(n),
         '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', '18', '-r', str(fps),
         '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest', out])


def cek_frame(edl, files, out):
    """Lembar cek: frame di tengah tiap jendela teks + awal tiap shot, untuk QC tanpa menonton."""
    ts = sorted({round((tx['t0'] + tx['t1']) / 2, 2) for tx in edl['teks']} |
                {round(sum(float(s['dur']) for s in edl['shots'][:i]) + 0.1, 2) for i in range(len(edl['shots']))})
    rows = []
    for f in files:
        ims = []
        for t in ts:
            p = f + f'.{t}.jpg'
            run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', f, '-frames:v', '1', '-vf', 'scale=270:-2', p])
            im = Image.open(p).convert('RGB'); os.remove(p)
            ims.append((t, im))
        rows.append(ims)
    cw = 270
    rh = [max(im.height for _, im in r) + 26 for r in rows]
    sheet = Image.new('RGB', (cw * len(ts), sum(rh)), 'white')
    d = ImageDraw.Draw(sheet)
    y = 0
    for r, h in zip(rows, rh):
        for k, (t, im) in enumerate(r):
            sheet.paste(im, (k * cw, y + 26)); d.text((k * cw + 4, y + 6), f'{t:.2f} dtk', fill='black')
        y += h
    sheet.save(out, quality=85)


def path(base, p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(base, p))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('edl')
    ap.add_argument('--akar', help='folder media (klip/, sfx/, hasil/)')
    ap.add_argument('--kerja', help='folder kerja sementara (default: <out_dir>/_kerja)')
    ap.add_argument('--hanya', choices=['9x16', '4x5'])
    a = ap.parse_args()
    edl = json.load(open(a.edl))
    base = os.path.abspath(a.akar) if a.akar else os.path.dirname(os.path.abspath(a.edl))
    out_dir = path(base, edl.get('out_dir', 'hasil'))
    kerja = a.kerja or os.path.join(out_dir, '_kerja')
    os.makedirs(kerja, exist_ok=True)
    fps = edl.get('fps', 30)
    total = sum(float(s['dur']) for s in edl['shots'])
    nama = edl['nama']

    master = render_shots(edl, base, kerja)
    audio = mix_audio(edl, base, kerja, total)
    hasil = []
    if a.hanya in (None, '9x16'):
        lap, n = render_lapisan(edl, base, kerja, (W, H), edl['tata_letak']['9x16'], '9x16')
        o = os.path.join(out_dir, f'{nama}_9x16.mp4'); gabung(master, lap, n, audio, fps, o); hasil.append(o)
    if a.hanya in (None, '4x5'):
        m45 = crop_45(edl, master, kerja)
        lap, n = render_lapisan(edl, base, kerja, (W45, H45), edl['tata_letak']['4x5'], '4x5')
        o = os.path.join(out_dir, f'{nama}_4x5.mp4'); gabung(m45, lap, n, audio, fps, o); hasil.append(o)
    cek_frame(edl, hasil, os.path.join(out_dir, f'{nama}_cek-frame.jpg'))
    if not edl.get('simpan_kerja'):
        shutil.rmtree(kerja, ignore_errors=True)
    for o in hasil:
        print(o)


if __name__ == '__main__':
    main()
