"""Lembar tokoh: gambar acuan kanon + frame tengah tiap shot (hasil bedah.py) dalam satu lembar besar,
untuk cek konsistensi wajah/kostum antar-shot dan cacat AI (tangan, teks rusak, benda melebur).

Pakai:
  python3 lembar_tokoh.py <folder_bedah> <acuan.jpg> [acuan2.jpg ...]
  → <folder_bedah>/TOKOH.jpg (acuan diberi bingkai merah, lalu shot_001.jpg dst., 4 per baris)

Acuan Bu Lastri: deliverables/aset-lastri/KANON-01-master-24Sep.jpg (+ deskripsi kanon di
deliverables/CHARACTER-SHEET-LASTRI-24Sep.md bagian 3). Ini identitas tokoh, BUKAN brief.
"""
import glob, os, sys
from PIL import Image, ImageDraw


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    folder, acuan = sys.argv[1], sys.argv[2:]
    shots = sorted(glob.glob(os.path.join(folder, "shot_*.jpg")))
    if not shots:
        sys.exit(f"GAGAL: tidak ada shot_*.jpg di {folder} (jalankan bedah.py dulu)")
    w = 400
    ims = []
    for p in acuan:
        if not os.path.exists(p):
            sys.exit(f"GAGAL: acuan tidak ada: {p}")
        im = Image.open(p).convert("RGB")
        im = im.resize((w, int(im.height * w / im.width)))
        ImageDraw.Draw(im).rectangle([0, 0, im.width - 1, im.height - 1], outline="red", width=6)
        ims.append(im)
    for p in shots:
        im = Image.open(p).convert("RGB")
        ims.append(im.resize((w, int(im.height * w / im.width))))
    kol, pad = 4, 6
    h = max(i.height for i in ims)
    bar = (len(ims) + kol - 1) // kol
    sheet = Image.new("RGB", (kol * (w + pad) + pad, bar * (h + pad) + pad), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (pad + (i % kol) * (w + pad), pad + (i // kol) * (h + pad)))
    out = os.path.join(folder, "TOKOH.jpg")
    sheet.save(out, quality=85)
    print(f"OK: {len(acuan)} acuan + {len(shots)} shot → {out}")


if __name__ == "__main__":
    main()
