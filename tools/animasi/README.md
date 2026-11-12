# tools/animasi — animasi iklan berbasis kode (HyperFrames)

Dipasang 3 Nov 2026, ACC Andrew/Bapak "ACC pasang hyperframes". Audit: `deliverables/kreatif-keunggulan-3Nov/AUDIT-HYPERFRAMES-3Nov.md`.
Skill: `.claude/skills/hyperframes` + `.claude/skills/hyperframes-cli` (heygen-com/hyperframes @ 47ddded).

## Cara pakai (WAJIB lewat pembungkus)
```
bash tools/animasi/hf.sh init <folder> --example blank --resolution portrait --non-interactive --skip-skills
bash tools/animasi/hf.sh check <folder> --json
bash tools/animasi/hf.sh snapshot <folder> --at 0,2,5 --no-end -o <scratch>
bash tools/animasi/hf.sh render <folder> -q delivery -o <folder>/render/<nama>.mp4
```
- Jangan `npx hyperframes` (tidak terkunci versi, telemetri/auto-update tidak dimatikan).
- CLI 0.9.8 terkunci di `package-lock.json`; `node_modules` tidak di repo, dipasang otomatis oleh hf.sh (`npm ci --ignore-scripts`).
- hf.sh mematikan telemetri, cek/auto update, pemasangan skill oleh `init`, memakai chrome-headless-shell container, dan MENOLAK: publish, feedback, cloud, lambda, cloudrun, auth, login, usage, upgrade, skills, events, billing, `--file-issue`, `--describe`.
- Sesudah `init`: hapus `CLAUDE.md`/`AGENTS.md` hasil scaffold (menyuruh `npx skills update`), buang skrip `publish`/npx di package.json proyek, salin GSAP lokal (`node_modules/hyperframes/dist/vendor/npm/gsap@3.15.0/dist/gsap.min.js` → `assets/`).
- Abaikan saran skill membuka desktop app / Framey / HeyGen / media-use berbayar.
- Hasil render untuk iklan tetap lewat ACC Andrew/Bapak sebelum tayang. Fitur opsional yang memasang paket saat dipakai (transkripsi, TTS, MusicGen, @google/genai) tidak dipakai tanpa audit.

## Ukuran nyata

## Paket edit untuk manusia (CapCut/Premiere)
- Versi tanpa teks: salin proyek ke scratch, sembunyikan id teks baca dengan `visibility:hidden` di `<style>`, render lewat hf.sh.
- Klip per adegan: potong MP4 dengan ffmpeg di batas `data-start` tiap adegan.
- PNG transparan: `node tools/animasi/ekspor-png.mjs <kerja> <keluar> <daftar.json>` (Playwright, latar transparan, sembunyikan elemen lain per tangkapan; `.slot` dan `#d-kilau` dikecualikan dari kotak potong).
