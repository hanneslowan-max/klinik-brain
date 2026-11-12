# SOURCE · motionmaxxing (terpasang sebagian)

- Sumber: https://github.com/Tejashmakwana/motionmaxxing
- Commit terkunci: 8c8ec0f2a6f6c9a0da15cd24f7b1298ab298368c
- Lisensi: Apache-2.0 (LICENSE + NOTICE ikut disalin). GSAP yang dipakai motion.js = lisensi Standard No-Charge (sama dengan HyperFrames).
- Audit: 9 Nov 2026, tools/audit-skill.py + baca manual seluruh kode (agent audit batch B); vonis AMAN DENGAN CATATAN. Uji pembanding di scratch 9 Nov (R7 detik 0–12 + gerbang pada R7).
- ACC Andrew/Bapak 9 Nov 2026: "ACC pasang sebagian motionmaxxing"
- Cara pasang: git archive dari commit terkunci, HANYA berkas di bawah (bukan audit-skill.py pasang, karena paket penuh tidak di-ACC). Bit executable dibuang.
- Perubahan RHJ pada salinan: (1) description di frontmatter dipersempit (cegah tabrakan dengan hyperframes/video/rhj-pic-produksi-video); (2) catatan > [KLINIK] di awal SKILL.md; (3) folder klinik/ ditulis RHJ (CARA-PAKAI.md, hf-shim.html, chrome-nosandbox.sh). Berkas upstream lain tidak diubah.
- Tidak dipasang: scripts/voice.py, imagegen.py, brand.mjs, fetch_logo.mjs, providers.sh, render.mjs, sync.mjs, mix.py, precedent.py, blind_review.py, install.sh; runtime/hero3d, native-ui, vendor, fonts; library/, taste/, templates/, docs/, studies/, examples/.
- Pembaruan: tidak otomatis. Versi baru = audit ulang + ACC.

## Berkas (sha256)
```
cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  ./LICENSE
82f5bde893626d09be6e024cfd8b6a07cbc59c859c2bba9a47ba45d66c5b3ac5  ./NOTICE
bd1c8205d1ef74fcc134034d23bc91909e3b8b2545895816f063cd9a1e306155  ./SKILL.md
172a1e4e2ac3c846ed5a4acfd212ec8e8b087cb499b51abd2c1bd759364802a8  ./references/brand.md
314a276380c2bc8bf6b0733a8ea99c5ac92fc97e8f3ec52d0d8a304e6f7461e5  ./references/close.md
de2901bc19126e6566b545b10e1d27709590655ad41f97ddd36e46b247b84796  ./references/director.md
60f1beb3fe5cfb97bc5834dfa8a573b310c3a4f63ac8366da19dd3063a702cd8  ./references/idea.md
6916778e8c3d622b8006a34099a933c069a671ee4b30589462846789abdca822  ./references/judgment.md
d0d1b37f1c2ba9254354294f7f143bc87503edc1dcf4b1a422a6a7f004e7608d  ./references/layout.md
3d9418623860308f34cafd3b816debc2644060270af78670d07fd0c53e434a90  ./references/motion.md
f469e124991b2b88941c3e1cd65fb62363273ad8b6443685481fc565925c7d6a  ./references/slop.md
4aa2d775fbf9f697e632b4c9dd37d0576de2c09720e4352d520586d670d99f69  ./references/sound-sync.md
c6212d87a3488f2424ed96c8653dcfe2925fb4d910a95e27c7b5521f3d2c36a9  ./references/tools.md
fd62bbb81002d4dc4d09150244b2c3a34e642adece42a51176e69b3a6cb3e9ec  ./references/transitions.md
4d52846795c5ea53ff7df11c152096c9145b625cf25dbed3c1aa6b4f37b91787  ./references/type.md
41d21a95c28b57cac5173c1de10ebebaff771b19374e31796fd5faa24bd7baf2  ./references/ui-demo.md
b6f6593ae470b20c7c1709e1afc8edb50fb27a747f767a7b3d5ac9845dba5cd3  ./references/world.md
3c48911bb63f20fb2304dbaeaf6f5fdacb98678ea11d8858ec0d7029663d14f0  ./rhj/CARA-PAKAI.md
ecfa9c48ea87b78a30e95bab3ead69b5f539990def49a9b4bdaf414b67c523bc  ./rhj/chrome-nosandbox.sh
c16e1a6ec4d4f2b37755640846b90f64e31147c2df8d61c069a971b574957942  ./rhj/hf-shim.html
f813765e2ba584d1502b34d0fd49744a8090766f3fbb618c82e1b8b00862737b  ./runtime/README.md
2cfc1494d084823958f4cf7a88b3d4412ddf35da06826b6ea4d788108de23409  ./runtime/motion.js
1ff2a601c7c4a62fb2c5d6876595e4eb1807d375399fce61c3efa56fecb1fe4b  ./scripts/_cdp.mjs
c6abcb2a50fb2dfc1fbdb209ee60c2bec1e358d6e078416c3d55275a0e8b98cf  ./scripts/lint.mjs
70f984b4baf024a6036dedc4efc317d4d48e41b790d2830821323d1204aa7811  ./scripts/look.py
```

- 12 Nov 2026: disalin ke klinik-brain dari rhj-brain (ACC Bapak, pop-up). Folder `rhj/` diganti nama `klinik/`; hash di atas merujuk nama lama. Catatan [RHJ] diganti [KLINIK].
