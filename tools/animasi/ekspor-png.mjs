// Skrip: ekspor elemen grafis proyek HyperFrames sebagai PNG transparan (Playwright, tanpa CLI HyperFrames).
// Pakai: node tools/animasi/ekspor-png.mjs <folder-kerja> <folder-keluar> <daftar.json>; folder-kerja = salinan proyek + fonts/ (woff2 dari ~/.cache/hyperframes/fonts: archivo.woff2, inter-600..900.woff2, jbm-700.woff2).
// daftar.json = [{"nama","sel","t","adegan","sembunyi":[selector...]}]. Contoh: deliverables/animasi/*/paket-edit.
import { createRequire } from "node:module"; const { chromium } = createRequire(process.env.PW_ROOT || "/opt/node22/lib/node_modules/")("playwright");
import fs from "node:fs";
import path from "node:path";
const [kerja, keluar] = process.argv.slice(2, 4);
let html = fs.readFileSync(path.join(kerja, "index.html"), "utf8");
const ff = `@font-face{font-family:"Archivo Black";src:url(fonts/archivo.woff2)}
${[600,700,800,900].map(w=>`@font-face{font-family:"Inter";font-weight:${w};src:url(fonts/inter-${w}.woff2)}`).join("\n")}
@font-face{font-family:"JetBrains Mono";font-weight:700;src:url(fonts/jbm-700.woff2)}
html,body{background:transparent!important}`;
html = html.replace("<style>", "<style>" + ff).replace('<script src="assets/gsap.min.js"></script>', '<script>window.__timelines={}</script><script src="assets/gsap.min.js"></script>');
fs.writeFileSync(path.join(kerja, "aset.html"), html);
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 2 });
await p.goto("file://" + path.join(kerja, "aset.html"));
await p.evaluate(() => document.fonts.ready);
const ambil = JSON.parse(fs.readFileSync(process.argv[4], "utf8"));
for (const a of ambil) {
  const kotak = await p.evaluate(({ a }) => {
    document.querySelectorAll(".adegan").forEach(e => e.style.display = e.id === a.adegan ? "" : "none");
    document.querySelectorAll("[data-sembunyi]").forEach(e => { e.style.visibility = ""; e.removeAttribute("data-sembunyi"); });
    (a.sembunyi||[]).forEach(q => document.querySelectorAll(q).forEach(e => { e.style.visibility = "hidden"; e.setAttribute("data-sembunyi", "1"); }));
    window.__timelines.main.seek(a.t);
    const el = document.querySelector(a.sel);
    let r = el.getBoundingClientRect(); let x0=r.left,y0=r.top,x1=r.right,y1=r.bottom;
    el.querySelectorAll("*").forEach(c => { if (c.matches(".slot, .slot span, #d-kilau, [data-ekspor-abaikan]")) return; const q = c.getBoundingClientRect(); if (q.width&&q.height){x0=Math.min(x0,q.left);y0=Math.min(y0,q.top);x1=Math.max(x1,q.right);y1=Math.max(y1,q.bottom);} });
    const m = 24; return { x: Math.max(0,x0-m), y: Math.max(0,y0-m), width: Math.min(1080,x1+m)-Math.max(0,x0-m), height: Math.min(1920,y1+m)-Math.max(0,y0-m) };
  }, { a });
  await p.waitForTimeout(100);
  await p.screenshot({ path: path.join(keluar, a.nama + ".png"), clip: kotak, omitBackground: true });
  console.log(a.nama, JSON.stringify(kotak));
}
await b.close();
