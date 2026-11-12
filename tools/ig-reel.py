#!/usr/bin/env python3
"""Unduh video reel/post Instagram PUBLIK tanpa login, lewat halaman embed publik.

Kenapa cara ini (dicatat 20 Okt 2026 atas permintaan Bapak, "jangan sampe lupa lagi"):
- instagram.com/reel/<kode>/ dan yt-dlp dari server cloud kena 429 (IP diblokir).
- Graph API Business Discovery memberi caption/like/komentar, TAPI tidak memberi media_url video reel akun lain.
- Halaman embed instagram.com/reel/<kode>/embed/ MEMUAT "video_url" (mp4) asal diminta dengan User-Agent
  sederhana (curl / HP / facebookexternalhit). Dengan User-Agent Chrome desktop, IG mengirim halaman SPA
  tanpa data video -> itu jebakan yang membuat sesi 20 Okt sempat mengira "tidak bisa".
- (27 Okt) Reel yang memakai MUSIK BERLISENSI (clips_music_attribution_info.uses_original_audio=false,
  should_mute_audio=true) tetap publik, tapi IG TIDAK menaruh video_url di embed (musik tak boleh diputar
  di luar IG). Data lain tetap ada: sampul, caption, durasi, pemilik. Alat ini lalu menyimpan sampul + caption
  (<kode>-sampul.jpg, <kode>.json, "video": false) dan keluar dengan kode 3 -> minta file video ke Andrew/Bapak
  (unduh/rekam layar). Embed berisi "may be broken / removed" = post dihapus/dibatasi (kode 2).

Pakai:
  python3 -I tools/ig-reel.py <link_atau_kode> <folder_keluar>
Keluaran: <folder>/<kode>.mp4 + <kode>.json (caption, durasi, views, like, pemilik bila ada di embed).
Lanjut bedah: bedah.py (frame) dan tools/video/dengar.py (transkrip).
Video/frame JANGAN masuk repo; simpan di scratchpad.
"""
import json, os, re, sys, urllib.request

UA = ["curl/8.5.0",
      "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
      "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)"]


def kode_dari(s):
    m = re.search(r"instagram\.com/(?:[^/]+/)?(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)", s)
    return m.group(1) if m else s.strip().strip("/")


def ambil(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    return urllib.request.urlopen(req, timeout=60).read()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    kode, out = kode_dari(sys.argv[1]), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    sebagian = None
    for ua in UA:
        for jalur in (f"reel/{kode}/embed/", f"p/{kode}/embed/captioned/"):
            try:
                h = ambil(f"https://www.instagram.com/{jalur}", ua).decode("utf-8", "ignore")
            except Exception as e:  # coba kombinasi berikutnya
                print(f"gagal {jalur} [{ua[:12]}]: {e}", file=sys.stderr)
                continue
            u = h.replace('\\"', '"').replace('\\\\/', '/').replace('\\/', '/')
            m = re.search(r'"video_url":"([^"]+)"', u)
            g = lambda p: (re.search(p, u).group(1) if re.search(p, u) else None)
            if not m:
                if '"shortcode_media"' in u and '"is_video":true' in u and sebagian is None:
                    sebagian = (u, jalur, ua)
                continue
            cap = g(r'"edge_media_to_caption":\{"edges":\[\{"node":\{"text":"((?:[^"\\]|\\.)*)"')
            meta = {"kode": kode, "url": f"https://www.instagram.com/reel/{kode}/",
                    "pemilik": g(r'"owner":\{[^}]*?"username":"([^"]+)"'),
                    "durasi_dtk": float(g(r'"video_duration":([\d.]+)') or 0) or None,
                    "views": int(g(r'"video_view_count":(\d+)') or 0) or None,
                    "like": int(g(r'"edge_liked_by":\{"count":(\d+)') or 0) or None,
                    "caption": json.loads('"' + cap + '"') if cap else None,
                    "sumber": f"embed publik {jalur} UA={ua[:20]}"}
            video = m.group(1).replace("\\u0025", "%").replace("&amp;", "&")
            data = ambil(video, ua)
            open(os.path.join(out, f"{kode}.mp4"), "wb").write(data)
            json.dump(meta, open(os.path.join(out, f"{kode}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"OK {kode}.mp4 {len(data)} byte · durasi {meta['durasi_dtk']} dtk · views {meta['views']} · {meta['sumber']}")
            return
    if sebagian:
        u, jalur, ua = sebagian
        g = lambda p: (re.search(p, u).group(1) if re.search(p, u) else None)
        cap = g(r'"edge_media_to_caption":\{"edges":\[\{"node":\{"text":"((?:[^"\\]|\\.)*)"')
        meta = {"kode": kode, "url": f"https://www.instagram.com/reel/{kode}/", "video": False,
                "alasan": ("musik berlisensi (should_mute_audio=true): IG tidak memberi video di embed"
                           if '"should_mute_audio":true' in u else "video_url tidak ada di embed"),
                "pemilik": g(r'"owner":\{[^}]*?"username":"([^"]+)"'),
                "durasi_dtk": float(g(r'"video_duration":([\d.]+)') or 0) or None,
                "views": int(g(r'"video_view_count":(\d+)') or 0) or None,
                "caption": json.loads('"' + cap.replace('\\\\', '\\') + '"') if cap else None,
                "sumber": f"embed publik {jalur} UA={ua[:20]}"}
        sampul = g(r'"display_url":"([^"]+)"')
        if sampul:
            try:
                sampul = sampul.replace("\\u0026", "&").replace("\\", "").replace("&amp;", "&")
                open(os.path.join(out, f"{kode}-sampul.jpg"), "wb").write(ambil(sampul, ua))
                meta["sampul"] = f"{kode}-sampul.jpg"
            except Exception as e:
                print(f"sampul gagal: {e}", file=sys.stderr)
        json.dump(meta, open(os.path.join(out, f"{kode}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"SEBAGIAN {kode}: {meta['alasan']} · durasi {meta['durasi_dtk']} dtk · pemilik {meta['pemilik']} · "
              f"sampul+caption disimpan. Minta file video ke Andrew/Bapak (unduh/rekam layar).")
        sys.exit(3)
    sys.exit("TIDAK ADA video_url di embed (post dihapus/dibatasi, privat, atau gambar/carousel). "
             "Carousel/gambar: pakai Graph API Business Discovery (media_url) bila akun bisnis/kreator.")


if __name__ == "__main__":
    main()
