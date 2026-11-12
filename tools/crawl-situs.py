#!/usr/bin/env python3
"""Crawl teknis satu domain (baca saja) — peran "Auditor" yang belum rutin (20 Okt).

Mulai dari beranda + sitemap.xml, ikuti tautan internal (maks --max halaman, jeda --jeda dtk).
Per halaman: status, rantai redirect, title, meta description, jumlah H1, canonical, robots noindex.
Laporan: tautan internal rusak (4xx/5xx/timeout) + halaman sumbernya, redirect berantai, URL sitemap yang
non-200 / noindex / canonical ke URL lain, title/description kosong atau dobel, H1 0 atau >1,
gambar internal rusak (opsional --gambar).

Pakai:
  python3 -I tools/crawl-situs.py <rh|pm|https://domain> [--max 400] [--jeda 0.5] [--gambar] [--out <folder>]
Keluaran: ringkasan di stdout + <out>/crawl-<domain>-<tgl>.json (default folder: /tmp). Bukan untuk repo.
User-Agent "Klinik-SEO-Crawler" (situs sendiri). Hanya GET/HEAD, tidak mengisi form.
"""
import argparse, datetime, gzip, html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from collections import defaultdict, deque

DOM = {"klinik": os.environ.get("KLINIK_SITUS", "").strip()}  # mis. https://namaklinik.com
UA = "Mozilla/5.0 (compatible; Klinik-SEO-Crawler/1.0)"
LEWATI = re.compile(r"\.(pdf|zip|jpe?g|png|gif|webp|svg|ico|css|js|mp4|webm|woff2?|ttf|xml|txt)(\?|$)", re.I)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def minta(url, metode="GET", maks_hop=6):
    """Ikuti redirect manual supaya rantainya tercatat. Hasil: (status, url_akhir, rantai, body_teks|None)."""
    rantai, u = [], url
    for _ in range(maks_hop):
        req = urllib.request.Request(u, method=metode, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
        try:
            r = OPENER.open(req, timeout=25)
            st, hdr, body = r.status, r.headers, r.read() if metode == "GET" else b""
        except urllib.error.HTTPError as e:
            st, hdr, body = e.code, e.headers, b""
            if st in (301, 302, 303, 307, 308) and hdr.get("Location"):
                nxt = urllib.parse.urljoin(u, hdr["Location"])
                rantai.append((st, u)); u = nxt; continue
            return st, u, rantai, None
        except Exception as e:
            return f"ERR {type(e).__name__}", u, rantai, None
        if hdr.get("Content-Encoding") == "gzip" and body:
            body = gzip.decompress(body)
        teks = body.decode("utf-8", "ignore") if body and "html" in (hdr.get("Content-Type") or "") else None
        return st, u, rantai, teks
    return "ERR redirect>6", u, rantai, None


def norm(base, href, host):
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "#", "whatsapp:", "data:")):
        return None
    u = urllib.parse.urljoin(base, html.unescape(href.strip()))
    p = urllib.parse.urlsplit(u)
    if p.scheme not in ("http", "https") or p.netloc.replace("www.", "") != host:
        return None
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path or "/", p.query, ""))


def isi(teks):
    g = lambda pat: re.search(pat, teks, re.I | re.S)
    t = g(r"<title[^>]*>(.*?)</title>")
    d = g(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']*)') or g(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]*name=["\']description')
    c = g(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)') or g(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']canonical')
    rb = g(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']*)')
    return {"title": html.unescape(" ".join(t.group(1).split())) if t else "",
            "desc": html.unescape(d.group(1).strip()) if d else "",
            "canonical": c.group(1).strip() if c else "",
            "noindex": bool(rb and "noindex" in rb.group(1).lower()),
            "h1": len(re.findall(r"<h1[\s>]", teks, re.I)),
            "links": re.findall(r'<a[^>]+href=["\']([^"\']+)', teks, re.I),
            "imgs": re.findall(r'<img[^>]+src=["\']([^"\']+)', teks, re.I)}


def sitemap(root):
    urls, antre, lihat = [], [root + "/sitemap.xml"], set()
    while antre and len(urls) < 5000:
        sm = antre.pop()
        if sm in lihat: continue
        lihat.add(sm)
        st, _, _, _ = minta(sm, "HEAD")
        try:
            raw = urllib.request.urlopen(urllib.request.Request(sm, headers={"User-Agent": UA}), timeout=25).read()
            if raw[:2] == b"\x1f\x8b": raw = gzip.decompress(raw)
            x = raw.decode("utf-8", "ignore")
        except Exception:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", x)
        if "<sitemapindex" in x: antre += locs
        else: urls += [html.unescape(u) for u in locs]
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("situs")
    ap.add_argument("--max", type=int, default=400)
    ap.add_argument("--jeda", type=float, default=0.5)
    ap.add_argument("--gambar", action="store_true")
    ap.add_argument("--out", default="/tmp")
    a = ap.parse_args()
    root = DOM.get(a.situs, a.situs).rstrip("/")
    host = urllib.parse.urlsplit(root).netloc.replace("www.", "")
    sm = sitemap(root)
    antre, lihat = deque([root + "/"] + sm), set()
    hal, sumber, gambar = {}, defaultdict(set), defaultdict(set)
    while antre and len(hal) < a.max:
        u = antre.popleft()
        if u in lihat or LEWATI.search(u): continue
        lihat.add(u)
        st, akhir, rantai, teks = minta(u)
        h = {"status": st, "akhir": akhir, "rantai": [f"{s} {x}" for s, x in rantai]}
        if teks:
            i = isi(teks); h.update({k: i[k] for k in ("title", "desc", "canonical", "noindex", "h1")})
            for l in i["links"]:
                n = norm(akhir, l, host)
                if n:
                    sumber[n].add(u)
                    if n not in lihat: antre.append(n)
            if a.gambar:
                for s in i["imgs"]:
                    n = norm(akhir, s, host)
                    if n: gambar[n].add(u)
        hal[u] = h
        time.sleep(a.jeda)
    # Tautan internal yang ditemukan tapi belum sempat dicrawl: cek status saja (HEAD) bila kuota habis.
    rusak = []
    for t, srcs in sumber.items():
        if LEWATI.search(t): continue
        st = hal[t]["status"] if t in hal else minta(t, "HEAD")[0]
        if not (isinstance(st, int) and st < 400):
            rusak.append({"url": t, "status": st, "dari": sorted(srcs)[:5], "jumlah_sumber": len(srcs)})
    img_rusak = []
    for g_, srcs in list(gambar.items())[:800]:
        st = minta(g_, "HEAD")[0]
        if not (isinstance(st, int) and st < 400):
            img_rusak.append({"url": g_, "status": st, "dari": sorted(srcs)[:3]})
    ok = {u: h for u, h in hal.items() if h["status"] == 200 and "title" in h and not h["rantai"]}
    dobel = defaultdict(list)
    for u, h in ok.items():  # hanya halaman yang kanonik ke dirinya sendiri (varian ?query ber-canonical induk bukan masalah)
        if h["title"] and not h["noindex"] and (not h["canonical"] or h["canonical"].rstrip("/") == u.rstrip("/")):
            dobel[h["title"]].append(u)
    smset = set(sm)
    lap = {
        "situs": root, "tanggal": datetime.date.today().isoformat(), "halaman_dicrawl": len(hal), "url_sitemap": len(sm),
        "tautan_rusak": sorted(rusak, key=lambda r: -r["jumlah_sumber"]),
        "gambar_rusak": img_rusak,
        "redirect_berantai": [{"url": u, "rantai": h["rantai"], "akhir": h["akhir"]} for u, h in hal.items() if len(h["rantai"]) >= 2],
        "sitemap_bukan_200": [{"url": u, "status": hal[u]["status"], "akhir": hal[u]["akhir"]} for u in sm if u in hal and (hal[u]["status"] != 200 or hal[u]["rantai"])],
        "sitemap_noindex": [u for u in sm if u in ok and ok[u]["noindex"]],
        "sitemap_canonical_lain": [{"url": u, "canonical": ok[u]["canonical"]} for u in sm if u in ok and ok[u]["canonical"]
                                   and ok[u]["canonical"].rstrip("/") != u.rstrip("/")],
        "title_kosong": [u for u, h in ok.items() if not h["title"]],
        "desc_kosong": [u for u, h in ok.items() if not h["desc"] and not h["noindex"]],
        "title_dobel": {t: us for t, us in dobel.items() if len(us) > 1},
        "h1_bukan_1": [{"url": u, "h1": h["h1"]} for u, h in ok.items() if h["h1"] != 1 and not h["noindex"]],
        "terindeks_tapi_tidak_di_sitemap": [u for u, h in ok.items() if not h["noindex"] and u not in smset
                                            and (not h["canonical"] or h["canonical"].rstrip("/") == u.rstrip("/"))][:50],
    }
    os.makedirs(a.out, exist_ok=True)
    f = os.path.join(a.out, f"crawl-{host}-{lap['tanggal']}.json")
    json.dump(lap, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"CRAWL {root} · {lap['tanggal']} · {len(hal)} halaman · sitemap {len(sm)} URL → {f}")
    for k in ("tautan_rusak", "gambar_rusak", "redirect_berantai", "sitemap_bukan_200", "sitemap_noindex", "sitemap_canonical_lain",
              "title_kosong", "desc_kosong", "title_dobel", "h1_bukan_1", "terindeks_tapi_tidak_di_sitemap"):
        v = lap[k]; n = len(v)
        print(f"- {k}: {n}")
        for x in (list(v.items())[:3] if isinstance(v, dict) else v[:3]):
            print(f"    {json.dumps(x, ensure_ascii=False)[:220]}")


if __name__ == "__main__":
    main()
