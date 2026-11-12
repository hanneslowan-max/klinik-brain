"""Cek tag tracking yang BENAR-BENAR aktif di halaman (browser sungguhan, bukan HTML mentah).

Pakai lewat `bash tools/cek-tag-browser.sh <url> [url ...]` (menyiapkan venv Scrapling di /tmp).
Output JSON per URL: mentah vs browser (JSON-LD, ID GA4/GTM di HTML, H1) + runtime
(GA4/GTM yang terdaftar di window.google_tag_manager, Meta Pixel, event dataLayer).
READ-ONLY: hanya membuka halaman, tidak mengklik/mengisi apa pun.
"""
import base64, hashlib, json, os, re, subprocess, sys, urllib.request

from scrapling.fetchers import DynamicFetcher

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
CHROMIUM = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
PROXY_CA = "/root/.ccr/agent-proxy-ca.crt"


def flag_ca_proxy():
    """Cloud: TLS di-terminasi ulang oleh proxy sesi. Percayai HANYA CA proxy itu (bukan matikan verifikasi)."""
    if not os.path.exists(PROXY_CA):
        return []
    der = subprocess.run(
        f"openssl x509 -in {PROXY_CA} -pubkey -noout | openssl pkey -pubin -outform der",
        shell=True, capture_output=True, check=True).stdout
    spki = base64.b64encode(hashlib.sha256(der).digest()).decode()
    return [f"--ignore-certificate-errors-spki-list={spki}"]


def metrik(html):
    ld = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I)
    tipe = []
    for b in ld:
        try:
            d = json.loads(b)
            items = d.get("@graph", [d]) if isinstance(d, dict) else d
            tipe += [str(i.get("@type")) for i in items if isinstance(i, dict)]
        except Exception:
            tipe.append("JSON-rusak")
    return {
        "jsonld_blok": len(ld),
        "jsonld_tipe": sorted(set(tipe)),
        "ga4_di_html": sorted(set(re.findall(r"G-[A-Z0-9]{8,12}", html))),
        "gtm_di_html": sorted(set(re.findall(r"GTM-[A-Z0-9]{5,9}", html))),
        "h1": [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip()[:80]
               for h in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)][:3],
    }


hasil_js = {}


def aksi(page):
    page.wait_for_timeout(4000)
    hasil_js["js"] = page.evaluate("""() => ({
      ga4_aktif: Object.keys(window.google_tag_manager || {}).filter(k => k.startsWith('G-')),
      gtm_aktif: Object.keys(window.google_tag_manager || {}).filter(k => k.startsWith('GTM-')),
      meta_pixel: typeof window.fbq === 'function',
      dataLayer_event: [...new Set((window.dataLayer || []).map(e => e && (e.event || (e[0] ? String(e[0]) + ':' + String(e[1]) : null))).filter(Boolean))].slice(0, 15)
    })""")


def main(urls):
    flags = flag_ca_proxy()
    for url in urls:
        out = {"url": url}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            out["mentah"] = metrik(urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace"))
        except Exception as e:
            out["mentah"] = {"error": str(e)[:150]}
        try:
            hasil_js.clear()
            p = DynamicFetcher.fetch(url, headless=True, network_idle=True, executable_path=CHROMIUM,
                                     page_action=aksi, timeout=60000, extra_flags=flags)
            out["browser"] = metrik(p.html_content) | {"status": p.status}
            out["runtime"] = hasil_js.get("js")
        except Exception as e:
            out["browser"] = {"error": str(e)[:300]}
        print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("pakai: cek-tag-browser.py <url> [url ...]")
    main(sys.argv[1:])
