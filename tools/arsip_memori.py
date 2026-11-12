#!/usr/bin/env python3
"""Pindahkan entri lama memori/*.md ke memori/arsip/ (tidak ada yang dihapus).

Pakai:
  python3 tools/arsip_memori.py --cek          # hanya laporan, tidak menulis
  python3 tools/arsip_memori.py                # jalankan

Aturan per berkas ada di ATURAN di bawah. Blok = judul markdown + isi sampai judul
setingkat/lebih tinggi berikutnya. Tanggal dibaca dari judul (2026-09-17 / 17 Sep / 1 Okt).
Blok bertanggal < batas dipindah ke memori/arsip/<NAMA>-<bulan>.md (append, berurutan seperti asal).
Sesudah pindah dicek: semua baris lama tetap ada (aktif + arsip) — kalau tidak, batal.
"""
import argparse, datetime as dt, os, re, sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEM = os.path.join(REPO, 'memori')
ARSIP = os.path.join(MEM, 'arsip')
BULAN = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'mei': 5, 'may': 5, 'jun': 6, 'jul': 7,
         'agu': 8, 'aug': 8, 'sep': 9, 'okt': 10, 'oct': 10, 'nov': 11, 'des': 12, 'dec': 12}


def tanggal(teks, tahun=2026):
    m = re.search(r'\b(20\d\d)-(\d\d)-(\d\d)\b', teks)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.search(r'\b(\d{1,2})\s+(jan|feb|mar|apr|mei|may|jun|jul|agu|aug|sep|okt|oct|nov|des|dec)[a-z]*\b', teks, re.I)
    if m:
        try:
            return dt.date(tahun, BULAN[m[2].lower()], int(m[1]))
        except ValueError:
            return None
    return None


BARIS_TGL = re.compile(r'^\s*[-*|]?\s*\**\[?\s*(\d{1,2} (?:jan|feb|mar|apr|mei|jun|jul|agu|sep|okt|oct|nov|des)[a-z]*|20\d\d-\d\d-\d\d)', re.I)


def ada_baris_baru(isi, batas):
    for l in isi:
        if BARIS_TGL.match(l):
            t = tanggal(l[:60])
            if t and t >= batas:
                return True
    return False


def level(baris):
    m = re.match(r'^(#{1,6}) ', baris)
    return len(m[1]) if m else 0


def blok(lines, a, b, lv):
    """Pecah lines[a:b] menjadi (preambul, [(mulai, akhir)]) untuk judul level lv."""
    starts = [i for i in range(a, b) if level(lines[i]) == lv]
    out = []
    for k, s in enumerate(starts):
        e = b
        for j in range(s + 1, b):
            if 0 < level(lines[j]) <= lv:
                e = j
                break
        out.append((s, e))
    return out


def anak(lines, s, e, lv):
    """Blok level lv+1 di dalam blok level lv [s,e)."""
    return blok(lines, s + 1, e, lv + 1)


# ---- aturan per berkas: fungsi yang mengembalikan daftar (mulai, akhir, kelompok) yang dipindah ----

def r_pelajaran(lines, batas):
    pindah = []
    for s, e in blok(lines, 0, len(lines), 2):
        t = tanggal(lines[s])
        if t:
            if t < batas:
                pindah.append((s, e, None))
        else:  # bagian topik: periksa entri ### di dalamnya
            for cs, ce in anak(lines, s, e, 2):
                ct = tanggal(lines[cs])
                if ct and ct < batas:
                    pindah.append((cs, ce, lines[s].rstrip()))
    return pindah


def r_otak(lines, batas):
    pindah = []
    for s, e in blok(lines, 0, len(lines), 2):
        judul = lines[s]
        if ('PERTANYAAN UNTUK HANNES' in judul or 'PERTANYAAN UNTUK BAPAK' in judul) or 'LOG SINKRON' in judul:
            for cs, ce in anak(lines, s, e, 2):
                h = lines[cs]
                if 'LOG SINKRON' not in judul and not re.search(r'STATUS|RIWAYAT|RESOLVED', h, re.I):
                    continue  # blok UPDATE (keputusan/fakta) tetap di berkas aktif
                ct = tanggal(h)
                if ct and ct < batas:
                    pindah.append((cs, ce, judul.rstrip()))
    return pindah


def r_ads(lines, batas):
    pindah = []
    for s, e in blok(lines, 0, len(lines), 2):
        for cs, ce in anak(lines, s, e, 2):
            h = lines[cs]
            ct = tanggal(h)
            if re.search(r'\brun\b', h, re.I) and ct and ct < batas:
                pindah.append((cs, ce, lines[s].rstrip()))
    return pindah


def r_seo(lines, batas):
    pindah, ttl = [], None
    for s, e in blok(lines, 0, len(lines), 2):
        h = lines[s]
        if re.match(r'^## RUN ', h):
            ttl = tanggal(h)
        elif not h.startswith('## USUL'):
            ttl = None
            continue
        if ttl and ttl < batas:
            pindah.append((s, e, None))
    return pindah


def r_tanggal_l2(lines, batas):
    return [(s, e, None) for s, e in blok(lines, 0, len(lines), 2)
            if tanggal(lines[s]) and tanggal(lines[s]) < batas]


def r_mmeks(lines, batas):
    return [(s, e, None) for s, e in blok(lines, 0, len(lines), 2)
            if re.search(r'DELTA|RIWAYAT', lines[s]) and tanggal(lines[s]) and tanggal(lines[s]) < batas]


def r_agen(lines, batas):
    pindah = []
    for s, e in blok(lines, 0, len(lines), 2):
        if 'LOG RUN AGEN' not in lines[s]:
            continue
        for i in range(s + 1, e):
            l = lines[i]
            if (l.startswith('| **') or l.startswith('- **')):
                t = tanggal(l[:80])
                if t and t < batas:
                    pindah.append((i, i + 1, lines[s].rstrip()))
    return pindah


H7 = dt.date(2026, 10, 3)
ATURAN = [
    # berkas, fungsi, batas, keterangan
    ('PELAJARAN-PIC.md', r_pelajaran, dt.date(2026, 10, 1), 'entri bertanggal September'),
    ('OTAK-MM.md', r_otak, H7, 'blok STATUS/RIWAYAT/RESOLVED + LOG SINKRON < 3 Okt (blok UPDATE tetap)'),
    ('ANALISA-ADS-MENDALAM.md', r_ads, H7, 'detail/ringkas run < 3 Okt'),
    ('ANALISA-SEO-MENDALAM.md', r_seo, H7, 'RUN + USUL < 3 Okt'),
    ('ARAHAN-PIPELINE-MEMORI.md', r_tanggal_l2, H7, 'entri harian < 3 Okt'),
    ('MM-EKSEKUSI-MEMORI.md', r_mmeks, H7, 'blok DELTA/RIWAYAT < 3 Okt'),
    ('AGEN-HARIAN-MEMORI.md', r_agen, H7, 'baris LOG RUN AGEN < 3 Okt'),
]


def jalankan(cek):
    os.makedirs(ARSIP, exist_ok=True)
    total0 = total1 = 0
    for nama, fn, batas, ket in ATURAN:
        p = os.path.join(MEM, nama)
        if not os.path.exists(p):
            continue
        lines = open(p, encoding='utf-8').read().split('\n')
        pindah = sorted(fn(lines, batas))
        # jangan arsipkan blok yang di dalamnya masih ada baris bertanggal >= batas
        # (entri baru sering ditambahkan di bawah judul lama; bug 10 Okt)
        pindah = [(s, e, g) for s, e, g in pindah if not ada_baris_baru(lines[s + 1:e], batas)]
        # buang tumpang tindih (blok anak di dalam blok yang sudah dipindah)
        bersih, akhir = [], -1
        for s, e, g in pindah:
            if s >= akhir:
                bersih.append((s, e, g))
                akhir = e
        ambil = set()
        for s, e, _ in bersih:
            ambil.update(range(s, e))
        aktif = [l for i, l in enumerate(lines) if i not in ambil]
        b0 = len('\n'.join(lines).encode())
        b1 = len('\n'.join(aktif).encode())
        total0 += b0
        total1 += b1
        print(f'{nama}: {len(bersih)} blok dipindah, {b0/1024:.0f} KB -> {b1/1024:.0f} KB ({ket})')
        if cek or not bersih:
            continue
        # tulis arsip per bulan
        per_bulan = {}
        for s, e, g in bersih:
            t = tanggal(lines[s][:120]) or batas
            per_bulan.setdefault(t.strftime('%Y-%m'), []).append((s, e, g))
        arsip_baru = []
        for bln, bs in sorted(per_bulan.items()):
            ap = os.path.join(ARSIP, f'{nama[:-3]}-{bln}.md')
            baru = not os.path.exists(ap)
            with open(ap, 'a', encoding='utf-8') as f:
                if baru:
                    f.write(f'# ARSIP {nama} — {bln}\n\nDipindah dari `memori/{nama}` oleh `tools/arsip_memori.py` '
                            f'(aturan: {ket}). Isi asli, tidak diubah. Berkas aktif tetap di `memori/{nama}`.\n')
                f.write(f'\n<!-- dipindah {dt.date.today().isoformat()} -->\n')
                kel = object()
                for s, e, g in bs:
                    if g and g != kel:
                        f.write(f'\n{g}\n')
                        kel = g
                    f.write('\n'.join(lines[s:e]).rstrip('\n') + '\n')
            arsip_baru.append(ap)
        # cek tidak ada baris hilang
        sisa = Counter(lines) - Counter(aktif)
        dipindah = Counter()
        for s, e, _ in bersih:
            dipindah.update(lines[s:e])
        if sisa != dipindah:
            sys.exit(f'BATAL {nama}: hitungan baris tidak cocok')
        catatan = (f'> Entri lama dipindah ke `memori/arsip/{nama[:-3]}-<bulan>.md` '
                   f'({ket}). Lihat `memori/INDEKS-MEMORI.md`.')
        if catatan not in aktif:
            # sisipkan catatan sesudah judul utama
            idx = next((i for i, l in enumerate(aktif) if l.startswith('# ')), 0)
            aktif.insert(idx + 1, '')
            aktif.insert(idx + 2, catatan)
        open(p, 'w', encoding='utf-8').write('\n'.join(aktif))
    print(f'TOTAL {total0/1024:.0f} KB -> {total1/1024:.0f} KB')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cek', action='store_true')
    jalankan(ap.parse_args().cek)
