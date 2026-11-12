#!/usr/bin/env python3
"""Peluang SEO dari GSC API (baca saja) — dua peran dari reel @mrraoai yang belum ada di routine (20 Okt):

  analyst    halaman "satu dorongan lagi ke halaman 1": kueri posisi 4-20, dikelompokkan per halaman.
  researcher (a) kueri GSC yang dicari orang tapi belum punya halaman kuat (posisi terbaik > 15), per topik;
             (b) --saran: kueri dari Google Autocomplete (publik, gratis) untuk benih produk tiap domain, dicocokkan
             dengan GSC -> "belum ada impresi" = celah konten. Kueri milik domain lain & produk TIDAK dijual ditandai.

Pakai:
  python3 -I tools/seo-peluang.py analyst klinik [--days 28] [--min-impr 20] [--top 10] [--json]
  python3 -I tools/seo-peluang.py researcher klinik [--days 28] [--min-impr 5] [--top 15] [--saran] [--json]
Sumber angka: `node tools/gsc.mjs query klinik --dims page,query --csv` (GSC API resmi). Kueri anonim tidak ikut.
Angka hanya yang dihitung dari GSC; tidak ada perkiraan klik tambahan (ATURAN NOL).
"""
import argparse, csv, io, json, os, re, subprocess, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CFG = json.load(open(os.path.join(ROOT, "tools", "seo-klinik.json"), encoding="utf-8"))
NOL = r"(?!x)x"  # pola yang tidak pernah cocok
MEREK = {"klinik": _CFG.get("merek") or NOL}
# Klinik hanya punya satu domain: penanda "milik domain lain" dimatikan.
MILIK_PM = NOL
TIDAK_DIJUAL = _CFG.get("tidak_dilayani") or NOL  # layanan yang TIDAK dibuka klinik (isi dari profil klinik)
BENIH = {"klinik": _CFG.get("benih", [])}
MODIF = ["", "harga ", "jual ", "ukuran ", "jenis ", "cara ", "untuk "]
MILIK_RH = NOL


def tarik(dom, days):
    out = subprocess.run(["node", os.path.join(ROOT, "tools", "gsc.mjs"), "query", dom, "--dims", "page,query",
                          "--days", str(days), "--limit", "25000", "--csv"], capture_output=True, text=True, cwd=ROOT)
    if out.returncode != 0 or not out.stdout.startswith("page,"):
        sys.exit(f"GSC gagal: {out.stderr.strip() or out.stdout[:300]}")
    rows = []
    for r in csv.DictReader(io.StringIO(out.stdout)):
        rows.append({"page": r["page"], "query": r["query"].strip().lower(), "clicks": int(float(r["clicks"])),
                     "impr": int(float(r["impressions"])), "pos": float(r["position"])})
    return rows


def wavg(items, key, w):
    t = sum(i[w] for i in items)
    return round(sum(i[key] * i[w] for i in items) / t, 1) if t else None


def analyst(rows, dom, a):
    brand = re.compile(MEREK[dom])
    hal = defaultdict(list)
    for r in rows:
        if brand.search(r["query"]) or r["impr"] < a.min_impr or not (4 <= r["pos"] <= 20):
            continue
        hal[r["page"]].append(r)
    hasil = []
    for p, qs in hal.items():
        qs.sort(key=lambda x: -x["impr"])
        hasil.append({"halaman": p, "kueri_4_20": len(qs), "impresi": sum(q["impr"] for q in qs),
                      "klik": sum(q["clicks"] for q in qs), "posisi_rata2_tertimbang": wavg(qs, "pos", "impr"),
                      "kueri_teratas": [f'{q["query"]} (pos {q["pos"]}, {q["impr"]} impr, {q["clicks"]} klik)' for q in qs[:3]]})
    hasil.sort(key=lambda x: -x["impresi"])
    return hasil[:a.top]


def researcher(rows, dom, a):
    brand = re.compile(MEREK[dom])
    lain = re.compile(MILIK_PM if dom == "rh" else MILIK_RH)
    per_q = defaultdict(list)
    for r in rows:
        if not brand.search(r["query"]):
            per_q[r["query"]].append(r)
    kand = []
    for q, rs in per_q.items():
        impr = sum(r["impr"] for r in rs)
        best = min(rs, key=lambda r: r["pos"])
        if impr < a.min_impr or best["pos"] <= 15:
            continue
        kand.append({"kueri": q, "impresi": impr, "klik": sum(r["clicks"] for r in rs), "posisi_terbaik": best["pos"],
                     "halaman_terbaik": best["page"], "milik_domain_lain": bool(lain.search(q))})
    # Kelompokkan per topik: dua kata pertama yang bukan kata umum.
    umum = {"harga", "jual", "beli", "toko", "di", "yang", "untuk", "dan", "murah", "terdekat", "jakarta", "cara", "apa", "itu"}
    topik = defaultdict(list)
    for k in kand:
        kata = [w for w in re.findall(r"[a-z0-9]+", k["kueri"]) if w not in umum]
        topik[" ".join(kata[:2]) or k["kueri"]].append(k)
    hasil = []
    for t, ks in topik.items():
        ks.sort(key=lambda x: -x["impresi"])
        hasil.append({"topik": t, "kueri": len(ks), "impresi": sum(k["impresi"] for k in ks), "klik": sum(k["klik"] for k in ks),
                      "milik_domain_lain": all(k["milik_domain_lain"] for k in ks),
                      "contoh": [f'{k["kueri"]} ({k["impresi"]} impr, pos terbaik {k["posisi_terbaik"]})' for k in ks[:3]],
                      "halaman_sekarang": ks[0]["halaman_terbaik"]})
    hasil.sort(key=lambda x: -x["impresi"])
    return hasil[:a.top]


def saran(dom, rows):
    import urllib.parse, urllib.request, time
    lain, tdj = re.compile(MILIK_PM if dom == "rh" else MILIK_RH), re.compile(TIDAK_DIJUAL)
    gsc = defaultdict(lambda: {"impr": 0, "pos": 999.0})
    for r in rows:
        g = gsc[r["query"]]; g["impr"] += r["impr"]; g["pos"] = min(g["pos"], r["pos"])
    hasil, lihat = [], set()
    for b in BENIH[dom]:
        for m in MODIF:
            q = (m + b) if m in ("harga ", "jual ", "jenis ", "cara ") else (b + " " + m.strip() if m else b)
            url = "https://suggestqueries.google.com/complete/search?client=firefox&hl=id&gl=id&q=" + urllib.parse.quote(q + " ")
            try:
                sug = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"}), timeout=20).read().decode("utf-8", "ignore"))[1]
            except Exception as e:
                print(f"saran gagal {q}: {e}", file=sys.stderr); continue
            time.sleep(0.4)
            for s_ in sug:
                s_ = s_.strip().lower()
                if s_ in lihat: continue
                lihat.add(s_)
                g = gsc.get(s_)
                hasil.append({"kueri": s_, "benih": b, "impresi_gsc": g["impr"] if g else 0,
                              "posisi_terbaik_gsc": g["pos"] if g else None,
                              "milik_domain_lain": bool(lain.search(s_)), "produk_tidak_dijual": bool(tdj.search(s_))})
    celah = [h for h in hasil if h["impresi_gsc"] == 0 and not h["milik_domain_lain"] and not h["produk_tidak_dijual"]]
    return {"saran_total": len(hasil), "celah_tanpa_impresi": celah, "sudah_ada_impresi": [h for h in hasil if h["impresi_gsc"] > 0]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["analyst", "researcher"])
    ap.add_argument("dom", choices=["klinik"])
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--min-impr", type=int, default=None)
    ap.add_argument("--top", type=int, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--saran", action="store_true", help="researcher: tambah Google Autocomplete")
    a = ap.parse_args()
    a.min_impr = a.min_impr if a.min_impr is not None else (20 if a.mode == "analyst" else 5)
    a.top = a.top or (10 if a.mode == "analyst" else 15)
    rows = tarik(a.dom, a.days)
    hasil = analyst(rows, a.dom, a) if a.mode == "analyst" else researcher(rows, a.dom, a)
    sr = saran(a.dom, rows) if (a.mode == "researcher" and a.saran) else None
    if a.json:
        print(json.dumps({"mode": a.mode, "domain": a.dom, "hari": a.days, "min_impr": a.min_impr,
                          "baris_gsc": len(rows), "hasil": hasil, "saran": sr}, ensure_ascii=False, indent=1))
        return
    print(f"{a.mode.upper()} {a.dom} · {a.days} hari · {len(rows)} baris page+query GSC · min {a.min_impr} impr")
    for i, h in enumerate(hasil, 1):
        if a.mode == "analyst":
            print(f'{i}. {h["halaman"]} · {h["kueri_4_20"]} kueri pos 4-20 · {h["impresi"]} impr · {h["klik"]} klik · pos {h["posisi_rata2_tertimbang"]}')
        else:
            tanda = " [MILIK DOMAIN LAIN]" if h["milik_domain_lain"] else ""
            print(f'{i}. {h["topik"]}{tanda} · {h["kueri"]} kueri · {h["impresi"]} impr · {h["klik"]} klik · sekarang: {h["halaman_sekarang"]}')
        for c in h.get("kueri_teratas") or h.get("contoh"):
            print(f"     - {c}")
    if sr:
        print(f"\nSARAN GOOGLE AUTOCOMPLETE · {sr['saran_total']} kueri · celah (0 impresi GSC, milik domain ini, produk dijual): {len(sr['celah_tanpa_impresi'])}")
        for h in sr["celah_tanpa_impresi"][:40]:
            print(f"  - {h['kueri']}  (benih: {h['benih']})")


if __name__ == "__main__":
    main()
