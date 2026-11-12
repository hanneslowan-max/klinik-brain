#!/usr/bin/env python3
"""md2pdf.py — render brief/laporan Markdown jadi PDF (Chromium headless, tanpa layanan luar).

Pakai:
  python3 tools/md2pdf.py <masuk.md> <keluar.pdf> [--landscape]

--landscape dipakai untuk brief per scene (tabel 5 kolom). Kotak "> **Ringkasan episode …**" dirender
sebagai kotak kuning. Butuh modul `markdown` dan Chromium Playwright (/opt/pw-browsers) — sudah ada di cloud.
"""
import glob, os, subprocess, sys
import markdown

def main():
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if len(a) != 2:
        sys.exit(__doc__)
    src, out = a
    land = '--landscape' in sys.argv
    md = open(src, encoding='utf-8').read()
    body = markdown.markdown(md, extensions=['tables', 'fenced_code', 'sane_lists'])
    css = f"""
@page {{ size: A4{' landscape' if land else ''}; margin: 16mm 14mm; }}
body {{ font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }}
h1 {{ font-size: 17pt; border-bottom: 2px solid #333; padding-bottom: 4px; }}
h2 {{ font-size: 13.5pt; margin-top: 18px; border-bottom: 1px solid #bbb; padding-bottom: 2px; page-break-after: avoid; }}
h3 {{ font-size: 11.5pt; margin-top: 14px; page-break-after: avoid; }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9pt; }}
th, td {{ border: 1px solid #999; padding: 4px 6px; vertical-align: top; word-break: break-word; }}
th {{ background: #eee; }}
th:nth-child(2), td:nth-child(2) {{ white-space: nowrap; }}
tr {{ page-break-inside: avoid; }}
code {{ background: #f3f3f3; padding: 1px 3px; font-size: 9pt; }}
pre {{ background: #f3f3f3; padding: 6px; white-space: pre-wrap; word-break: break-word; font-size: 8.5pt; }}
blockquote {{ border-left: 4px solid #c9a227; background: #fbf8ec; margin: 8px 0; padding: 6px 12px; color: #222; }}
blockquote ul {{ margin: 4px 0; padding-left: 18px; }} blockquote li {{ margin: 2px 0; }}
"""
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>"
    tmp = os.path.splitext(out)[0] + '.tmp.html'
    open(tmp, 'w', encoding='utf-8').write(html)
    cands = glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome') or glob.glob('/opt/pw-browsers/chromium')
    if not cands:
        sys.exit('Chromium tidak ditemukan di /opt/pw-browsers')
    subprocess.run([cands[0], '--headless', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={os.path.abspath(out)}', 'file://' + os.path.abspath(tmp)], check=True, capture_output=True)
    os.remove(tmp)
    print(out)

if __name__ == '__main__':
    main()
