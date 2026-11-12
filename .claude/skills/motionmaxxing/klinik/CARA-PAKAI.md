# motionmaxxing di klinik: cara pakai (terpasang sebagian 9 Nov 2026)

Dipakai pic-kreatif dan pic-produksi-video untuk menyutradarai dan mengkritik gerak iklan animasi HyperFrames. Produksi tetap mengikuti skill `hyperframes` + `tools/animasi/hf.sh`.

## 1. Bacaan
`references/motion.md` (easing terukur), `transitions.md`, `type.md`, `slop.md` (daftar pola murahan), `judgment.md`, `world.md`, `layout.md`, `director.md`. Abaikan bagian suara/VO/brand capture (alatnya tidak terpasang).

## 2. Easing di komposisi HyperFrames
Salin `runtime/motion.js` ke `assets/` proyek, muat sesudah gsap, dan pastikan ada baris registrasi `window.__timelines["main"] = tl;` sebaris di index.html (static guard HyperFrames membutuhkannya). Terbukti jalan di hf.sh 9 Nov (render identik dengan render.mjs).

## 3. Peringatan mutu sesudah render
- Gerak/beku/frame kosong dari MP4 (tanpa shim):
  `python3 -I .claude/skills/motionmaxxing/scripts/look.py <video.mp4> --out <scratch>/look`
  Baca: stretch beku >1,5 dtk di tengah film, energi gerak (band film profesional 4,4–9,8/255), frame nyaris kosong. Penutup logo+WA yang diam ≥2 dtk = disengaja, bukan cacat.
- Tata letak/label (perlu shim):
  1. salin proyek ke scratch, sisipkan `klinik/hf-shim.html` ke salinan index.html;
  2. `CHROME_PATH=.claude/skills/motionmaxxing/klinik/chrome-nosandbox.sh node .claude/skills/motionmaxxing/scripts/lint.mjs <scratch>/index.html`
     (jalankan wrapper lewat bash bila bit executable hilang: buat salinan di scratch lalu `chmod +x`).
  Temuan C1/C2 (label kecil kapital/HUD) dan D1 (judul gaya deck) = pertimbangkan; V4 warna abu sering salah alarm.
- Cek HyperFrames (`hf.sh check`) tetap wajib: ia menangkap hal yang luput dari motionmaxxing (teks terlalu cepat dibaca, kontras, teks <28 px).

## 4. Yang TIDAK dipakai
Lihat catatan [KLINIK] di SKILL.md. Uji pembanding 9 Nov (R7 detik 0–12): gerak lebih halus, tapi hook frame 0 dan perbandingan berdampingan versi lama lebih jelas untuk feed tanpa suara. Ambil mekanik geraknya, bukan aturan tata letaknya.
