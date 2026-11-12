#!/usr/bin/env python3
"""Cek bahasa dialog naskah Bu Lastri (pic-scriptwriter).

Definisi kata, kalimat, partikel, sapaan, kalimat tanya, dan pembuka
penanda wacana SAMA dengan skrip korpus pic-data (KORPUS-DIALOG-SHORTMOVIE-01Okt),
jadi angkanya bisa dibandingkan langsung dengan korpus.

Format masukan (UTF-8, satu baris dialog per baris):
    ## Eps 1                      <- judul kelompok (episode/video), opsional
    Selo | 3 | Mas, kepala pabrik barunya mana, sih?
    Lastri VO | 4 | Saya Lastri. Kepala pabrik. Jarang senyum.
    # komentar diabaikan
Kolom: tokoh (tambahkan "VO" bila narasi/luar frame tanpa lip-sync) | durasi baris
dalam detik (boleh kosong, koma atau titik; "+" = masih di shot baris sebelumnya,
tempo dihitung gabungan per shot seperti di brief) | teks yang diucapkan.

Pakai:
    python3 cek_dialog.py naskah.txt                 # ringkasan per tokoh + per baris
    python3 cek_dialog.py sebelum.txt sesudah.txt    # bandingkan dua versi
"""
import re, sys, collections

BATAS_TEMPO = 2.6        # kata/dtk, batas keras brief (per baris)
BATAS_LASTRI = 2.0       # kata/dtk, tempo tenang Lastri (brief CC1 "batas Lastri ±2"); lewat = cek uji suara
BATAS_KLIP = 5.0         # dtk, klip lip-sync maks (VO dikecualikan)

PART = {'ya': ['ya', 'yah'], 'kan': ['kan'], 'kok': ['kok'], 'sih': ['sih'], 'nih': ['nih'],
        'tuh': ['tuh'], 'deh': ['deh'], 'dong': ['dong'], 'lho': ['lho', 'loh'], 'mah': ['mah'],
        'to': ['toh', 'to'], 'kali': ['kali']}
NUM = {'satu', 'se', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan',
       'sepuluh', 'seratus', 'berapa', 'beberapa', 'puluh', 'ratus', 'ribu', 'banyak', 'sekian'}
SAP = {'pak', 'bu', 'mas', 'mbak', 'mba'}
NAMA = {'yaqin', 'selo', 'lastri'}          # "Pak Yaqin" = rujukan nama, bukan sapaan vokatif
DM = {'ya', 'oh', 'eh', 'wah', 'iya', 'lho', 'loh', 'nah', 'hah', 'aduh', 'astaga', 'ih', 'lah',
      'tuh', 'yah', 'duh', 'waduh', 'hmm', 'hm', 'ah', 'wih', 'yaudah', 'oke', 'ok'}
TAK_BAKU = {'udah': 'sudah', 'aja': 'saja', 'nggak': 'tidak', 'gak': 'tidak', 'enggak': 'tidak', 'ngga': 'tidak'}
BAKU_KAKU = ['tersebut', 'apakah', 'merupakan', 'bagaimana', 'sangat', 'mari kita',
             'oleh karena itu', 'dengan demikian', 'sudah', 'saja', 'tidak']
PAGAR = ['rp', 'harga', 'promo', 'diskon', 'kw', 'galvanis', 'stocky', 'kisah nyata', 'beli sekarang']
# Makian/hinaan (BAHASA-DIALOG bagian G, 6 Okt): dipakai sebagai punch di akun referensi @agunkperkasa, terlarang di naskah RHJ.
MAKIAN = ['tolol', 'goblok', 'bego', 'anjing', 'anjir', 'anjay', 'asu', 'wasu', 'bangsat', 'bajingan', 'sialan', 'kampret', 'bodoh']


def toks(t):
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", t.lower().replace('’', "'"))


def sents(text):
    parts = re.split(r'(?<=[.?!…])\s+|(?<=\.\.\.)\s*', text)
    return [p.strip() for p in parts if p and toks(p)]


def baca(path):
    rows, grp = [], '-'
    for raw in open(path, encoding='utf-8'):
        l = raw.strip()
        if not l or l.startswith('#') and not l.startswith('##'):
            continue
        if l.startswith('##'):
            grp = l.lstrip('#').strip(); continue
        c = [x.strip() for x in l.split('|')]
        if len(c) < 3:
            continue
        tokoh, dur, teks = c[0], c[1].replace(',', '.'), '|'.join(c[2:]).strip()
        vo = bool(re.search(r'\bVO\b', tokoh)); nama = re.sub(r'\bVO\b', '', tokoh).strip()
        ikut = dur == '+'
        rows.append(dict(grp=grp, tokoh=nama, vo=vo, ikut=ikut,
                         dur=float(dur) if dur and not ikut else None, teks=teks))
    return rows


def hitung_partikel(T):
    c = collections.Counter(T); n = 0; per = {}
    for k, ws in PART.items():
        if k == 'kali':
            v = sum(1 for i, t in enumerate(T) if t == 'kali'
                    and not (i > 0 and (T[i-1] in NUM or T[i-1].isdigit()))
                    and not (i + 1 < len(T) and T[i+1] in ('ini', 'itu', 'lipat', 'pertama', 'kedua')))
        else:
            v = sum(c[w] for w in ws)
        if v: per[k] = v
        n += v
    return n, per


def metrik(rows):
    units = [r['teks'] for r in rows]
    S = [s for u in units for s in sents(u)]
    T = [t for u in units for t in toks(u)]
    N = len(T)
    if not N:
        return None
    sl = [len(toks(s)) for s in S]
    np_, per = hitung_partikel(T)
    sap_all = sum(1 for t in T if t in SAP)
    sap_vok = sum(1 for i, t in enumerate(T) if t in SAP and not (i + 1 < len(T) and T[i+1] in NAMA))
    low = ' '.join(T)
    kaku = {w: len(re.findall(r'\b' + w + r'\b', low)) for w in BAKU_KAKU}
    kaku = {k: v for k, v in kaku.items() if v}
    tb = sum(1 for t in T if t in TAK_BAKU); bk = sum(T.count(v) for v in ('sudah', 'saja', 'tidak'))
    return dict(
        baris=len(rows), kata=N, kalimat=len(S),
        kata_per_kalimat=round(N / len(S), 2),
        pct_le5=round(100 * sum(1 for x in sl if x <= 5) / len(sl), 1),
        partikel_100=round(100 * np_ / N, 2), partikel_n=np_, partikel_rinci=per,
        sapaan_100=round(100 * sap_all / N, 2), sapaan_n=sap_all, sapaan_vokatif_n=sap_vok,
        pct_kal_sapaan=round(100 * sum(1 for s in S if SAP & set(toks(s))) / len(S), 1),
        pct_tanya=round(100 * sum(1 for s in S if s.rstrip().endswith('?')) / len(S), 1),
        pct_buka_penanda=round(100 * sum(1 for s in S if toks(s)[0] in DM) / len(S), 1),
        tak_baku_share=(round(tb / (tb + bk), 2) if tb + bk else None),
        baku_kaku=kaku)


def grup_tokoh(t):
    return 'Yaqin+Selo' if t in ('Yaqin', 'Selo') else t


def laporan(rows, judul):
    print(f'\n===== {judul} =====')
    by = collections.defaultdict(list)
    for r in rows:
        by[r['tokoh']].append(r); by[grup_tokoh(r['tokoh'])].append(r) if r['tokoh'] in ('Yaqin', 'Selo') else None
    by['SEMUA'] = rows
    hasil = {}
    for k in sorted(by, key=lambda x: (x == 'SEMUA', x)):
        m = metrik(by[k])
        if not m: continue
        hasil[k] = m
        print(f"{k:11s} baris {m['baris']:2d} kata {m['kata']:3d} kal {m['kalimat']:3d} | kata/kal {m['kata_per_kalimat']:.2f} "
              f"≤5kata {m['pct_le5']:5.1f}% | partikel/100 {m['partikel_100']:5.2f} ({m['partikel_n']}) "
              f"| sapaan/100 {m['sapaan_100']:5.2f} ({m['sapaan_n']}; vokatif {m['sapaan_vokatif_n']}) kal-bersapaan {m['pct_kal_sapaan']:4.1f}% "
              f"| tanya {m['pct_tanya']:4.1f}% | buka-penanda {m['pct_buka_penanda']:4.1f}% | tak-baku {m['tak_baku_share']} "
              f"| kaku {m['baku_kaku'] or '-'}")
    # jatah per kelompok (episode/video)
    print('\nSapaan per tokoh per kelompok (vokatif) + jatah kalimat khas:')
    for g in dict.fromkeys(r['grp'] for r in rows):
        rr = [r for r in rows if r['grp'] == g]
        sap = collections.Counter()
        for r in rr:
            T = toks(r['teks'])
            sap[r['tokoh']] += sum(1 for i, t in enumerate(T) if t in SAP and not (i + 1 < len(T) and T[i+1] in NAMA))
        low = ' '.join(' '.join(toks(r['teks'])) for r in rr)
        jatah = {'yaqin pak': low.count('yaqin pak'), 'selow': len(re.findall(r'\bselow\b', low))}
        warn = [k for k, v in jatah.items() if v > 1]
        print(f"  {g}: {dict(sap)} · khas {jatah}{'  <-- LEBIH DARI 1x' if warn else ''}")
    # per baris
    print('\nPer baris (kata/dtk):')
    for i, r in enumerate(rows):
        n = len(toks(r['teks']))
        if r['ikut']:
            print(f"  {r['grp']:6s} {r['tokoh']:6s}{' VO' if r['vo'] else '   '} {n:2d} kata (satu shot dengan baris di atas) | {r['teks']}")
            continue
        if r['dur']:
            j = i + 1
            while j < len(rows) and rows[j]['ikut']:
                n += len(toks(rows[j]['teks'])); j += 1
            kd = n / r['dur']
            flag = ''
            if kd > BATAS_TEMPO: flag = '  <-- MELANGGAR tempo >2,6'
            elif r['tokoh'] == 'Lastri' and kd > BATAS_LASTRI: flag = '  <-- Lastri >2,0: cek di uji suara'
            if not r['vo'] and r['dur'] > BATAS_KLIP: flag += '  <-- klip lip-sync >5 dtk'
            print(f"  {r['grp']:6s} {r['tokoh']:6s}{' VO' if r['vo'] else '   '} {n:2d} kata / {r['dur']:>4} dtk = {kd:4.2f}{flag} | {r['teks']}")
        else:
            print(f"  {r['grp']:6s} {r['tokoh']:6s} {n:2d} kata / (durasi kosong) | {r['teks']}")
    # pagar
    allt = ' '.join(' '.join(toks(r['teks'])) for r in rows)
    hit = [p for p in PAGAR if re.search(r'\b' + p + r'\b', allt)]
    print('\nPagar kata:', hit or 'bersih')
    mk = [p for p in MAKIAN if re.search(r'\b' + p + r'\b', allt)]
    print('Makian/hinaan:', (str(mk) + '  <-- tinjau manual; kata harfiah (mis. anjing = hewan) boleh bila dicatat [pic-data 6/10]') if mk else 'bersih')
    return hasil


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    H = [laporan(baca(p), p) for p in sys.argv[1:3]]
    if len(H) == 2:
        print('\n===== SEBELUM → SESUDAH =====')
        for k in H[0]:
            if k in H[1]:
                a, b = H[0][k], H[1][k]
                print(f"{k:11s} kata/kal {a['kata_per_kalimat']:.2f}→{b['kata_per_kalimat']:.2f} · partikel/100 {a['partikel_100']:.2f}→{b['partikel_100']:.2f} "
                      f"· sapaan/100 {a['sapaan_100']:.2f}→{b['sapaan_100']:.2f} · kal-bersapaan {a['pct_kal_sapaan']}→{b['pct_kal_sapaan']}% "
                      f"· tanya {a['pct_tanya']}→{b['pct_tanya']}% · buka-penanda {a['pct_buka_penanda']}→{b['pct_buka_penanda']}%")
