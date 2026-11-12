#!/usr/bin/env python3
"""Hook UserPromptSubmit: sisipkan pengingat alat repo bila pesan Hannes cocok dengan pemicu.

Kenapa (8 Nov 2026): agent berulang kali bilang "tidak bisa" (contoh: menonton reel IG) padahal alatnya
sudah ada di tools/. Catatan di log panjang (LOG-PAGAR/PELAJARAN) tidak terbaca pada saat dibutuhkan,
dan hilang saat konteks diringkas. Hook ini bekerja tanpa bergantung ingatan agent: setiap pesan dicek,
pengingat dicetak ke stdout (masuk konteks sebelum agent menjawab).

Peta pemicu: tools/pengingat-alat.json. Gagal apa pun -> diam (exit 0), tidak pernah memblokir pesan.

Tambahan 9 Nov 2026 (B24): baca memori/ANTREAN-KEPUTUSAN.md; bila ada keputusan berstatus TERBUKA, ingatkan agent
untuk menampilkannya ke Bapak sebagai pop-up AskUserQuestion.
"""
import json, os, re, sys


def keputusan_terbuka(root):
    """Baris antrean keputusan berstatus TERBUKA -> [(id, pertanyaan singkat)]."""
    try:
        teks = open(os.path.join(root, "memori", "ANTREAN-KEPUTUSAN.md"), encoding="utf-8").read()
    except Exception:
        return []
    hasil = []
    for baris in teks.splitlines():
        kol = [k.strip() for k in baris.strip().strip("|").split("|")]
        if len(kol) >= 7 and re.match(r"^K\d{6}-\d+$", kol[0]) and kol[-1].upper().startswith("TERBUKA"):
            hasil.append((kol[0], kol[3][:90]))
    return hasil


def main():
    try:
        data = json.load(sys.stdin)
        teks = data.get("prompt") or ""
        root = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        peta = json.load(open(os.path.join(root, "tools", "pengingat-alat.json"), encoding="utf-8"))
    except Exception:
        return
    buka = keputusan_terbuka(root)
    if buka:
        print(f"[ANTREAN KEPUTUSAN B24, otomatis dari hook] {len(buka)} keputusan Bapak TERBUKA di memori/ANTREAN-KEPUTUSAN.md:")
        for i, q in buka[:8]:
            print(f"- {i}: {q}")
        print("Aturan B24: tampilkan yang belum ditanyakan di sesi ini sebagai pop-up AskUserQuestion (maks 4 per pop-up, urut uang/batas waktu), "
              "sesudah menangani pesan Bapak; catat jawaban di antrean (DIPUTUS) + LOG-PAGAR, lalu eksekusi.")
    cocok = []
    for p in peta.get("pemicu", []):
        try:
            if re.search(p["pola"], teks, re.IGNORECASE) and p["pesan"] not in cocok:
                cocok.append(p["pesan"])
        except re.error:
            continue
    if cocok:
        print("[PENGINGAT ALAT RHJ, otomatis dari hook] Alat repo yang relevan dengan pesan ini:")
        for c in cocok[:4]:
            print("- " + c)
        print("Aturan: jangan bilang 'tidak bisa' sebelum alat di atas dicoba; kalau gagal, sebut perintah + errornya.")


if __name__ == "__main__":
    main()
