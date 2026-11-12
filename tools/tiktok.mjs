// tiktok.mjs — Analitik TikTok klinik tanpa pihak ketiga. HANYA BACA.
// Dua jalur:
//   (1) PUBLIK, tanpa token — angka yang tampil di halaman publik: views, like, komentar, share, simpan,
//       durasi, tanggal. Bisa dipakai SEKARANG. Tidak memuat % tonton habis, waktu tonton, follower per video.
//   (2) TikTok API for Business (Accounts API), butuh token — menambah reach, % tonton habis,
//       rata-rata/total waktu tonton, follower baru, sumber trafik. Akun harus akun Bisnis.
//
// Pemakaian (output JSON ke stdout):
//   node tools/tiktok.mjs public-profile [username]            follower, total like, jumlah video (default env TIKTOK_USERNAME)
//   node tools/tiktok.mjs public-videos [username] [--limit 30] daftar video terbaru + angka publik per video
//   node tools/tiktok.mjs biz-account [--days 7]                (token) ringkasan akun Bisnis
//   node tools/tiktok.mjs biz-videos [--limit 20]               (token) video + insight lengkap
//   node tools/tiktok.mjs tukar-kode <kode_otorisasi>           tukar kode otorisasi (10 menit, sekali pakai) jadi token,
//                                                               simpan di Vault Supabase Anvil; cetak open_id/scope/kedaluwarsa saja
//   node tools/tiktok.mjs token-status                          status token di Vault (tanpa mencetak token)
//   node tools/tiktok.mjs impor-vault                           pindahkan token yang Bapak tempel di Vault 'tiktok_token_masuk'
//                                                               (JSON hasil tukar kode / access token polos / alamat ?code=) ke 'tiktok_token'
//   Opsi: --fields f1,f2 untuk mengganti daftar field API (bila TikTok mengganti nama field).
//
// Kredensial jalur 2 (11 Nov 2026, panduan deliverables/PANDUAN-TOKEN-TIKTOK-11Nov.pdf):
//   Access token TikTok hanya berlaku 24 jam, refresh token 1 tahun dan BERGANTI tiap diperbarui (dok. resmi
//   Accounts API Authentication v1.3). Karena itu token tidak disimpan sebagai env, tapi di Vault Supabase Anvil
//   (proyek Supabase KLINIK di env TIKTOK_VAULT_PROJECT, lewat Management API dengan env SUPABASE_ACCESS_TOKEN):
//     tiktok_client_secret  (Secret app TikTok milik klinik; diisi Bapak sendiri lewat dashboard Supabase → Vault)
//     tiktok_token          (JSON {access_token, refresh_token, open_id, scope, kedaluwarsa…}; ditulis alat ini)
//   Alat memperbarui access token otomatis bila sisa < 1 jam, lalu menyimpan refresh token baru.
//   Cadangan lama tetap jalan: env TIKTOK_BUSINESS_TOKEN + TIKTOK_BUSINESS_ID (tanpa perpanjangan otomatis).
//   TIKTOK_USERNAME         (WAJIB; username akun TikTok klinik)
// Panduan: deliverables/PANDUAN-TOKEN-API-META-TIKTOK-30Sep.md
// CATATAN: nama field jalur 2 mengikuti dokumentasi Accounts API v1.3; cek ulang di panggilan pertama
// (`biz-videos --limit 1`). Kalau TikTok menolak satu field, pakai --fields untuk menguranginya.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
function loadEnv(file) {
  const out = {};
  try {
    for (const line of fs.readFileSync(file, "utf8").split(/\r?\n/)) {
      if (/^\s*#/.test(line)) continue;
      const m = line.match(/^\s*([A-Za-z0-9_]+)\s*=\s*(.*)$/);
      if (m) out[m[1]] = m[2].trim();
    }
  } catch { /* .env tak ada */ }
  return out;
}
const env = loadEnv(path.join(HERE, ".env"));
const get = (k) => (process.env[k] || env[k] || "").trim();
const USER = (get("TIKTOK_USERNAME") || "").replace(/^@/, "");
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const wib = (sec) => new Date(sec * 1000 + 7 * 3600e3).toISOString().replace("T", " ").slice(0, 16);
const out = (x) => console.log(JSON.stringify(x, null, 2));

function args() {
  const a = process.argv.slice(3), o = { _: [] };
  for (let i = 0; i < a.length; i++) {
    if (a[i].startsWith("--")) { const k = a[i].slice(2); const n = a[i + 1]; if (n === undefined || n.startsWith("--")) o[k] = true; else { o[k] = n; i++; } }
    else o._.push(a[i]);
  }
  return o;
}

// ---------- jalur 1: publik ----------
async function page(url) {
  await sleep(1200); // sopan: ±1 halaman per detik
  const res = await fetch(url, { headers: { "user-agent": UA, "accept-language": "id-ID,id;q=0.9" } });
  return res.text();
}
function rehydrate(html) {
  const m = html.match(/__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application\/json">(.*?)<\/script>/s);
  return m ? JSON.parse(m[1]).__DEFAULT_SCOPE__ : null;
}
async function publicProfile(user) {
  const s = rehydrate(await page(`https://www.tiktok.com/@${user}`));
  const d = s?.["webapp.user-detail"];
  if (!d || d.statusCode) return { username: user, error: `profil tidak terbaca (statusCode ${d?.statusCode ?? "?"})` };
  const u = d.userInfo.user, st = d.userInfo.statsV2 || d.userInfo.stats;
  return { username: u.uniqueId, nama: u.nickname, bio: u.signature, akun_bisnis: !!u.commerceUserInfo?.commerceUser,
    follower: +st.followerCount, total_like: +(st.heartCount ?? st.heart), jumlah_video: +st.videoCount };
}
async function publicVideoIds(user, limit) {
  const html = await page(`https://www.tiktok.com/embed/@${user}`);
  const m = html.match(/<script id="__FRONTITY_CONNECT_STATE__"[^>]*>(.*?)<\/script>/s);
  if (!m) return [];
  const data = JSON.parse(m[1]).source?.data || {};
  const key = Object.keys(data).find((k) => k.toLowerCase() === `/embed/@${user}`.toLowerCase());
  return (data[key]?.videoList || []).map((v) => v.id).slice(0, limit);
}
async function publicVideo(user, id) {
  const s = rehydrate(await page(`https://www.tiktok.com/@${user}/video/${id}`));
  const it = s?.["webapp.video-detail"]?.itemInfo?.itemStruct;
  if (!it) return { id, error: "halaman video tidak terbaca" };
  const st = it.statsV2 || it.stats;
  const views = +st.playCount, like = +st.diggCount, kom = +st.commentCount, share = +st.shareCount, simpan = +st.collectCount;
  const umur = Math.round((Date.now() / 1000 - it.createTime) / 3600);
  return { id, link: `https://www.tiktok.com/@${user}/video/${id}`, tayang_wib: wib(it.createTime), umur_jam: umur,
    durasi_dtk: it.video?.duration, caption_awal: (it.desc || "").slice(0, 80),
    views, like, komentar: kom, share, simpan,
    er_persen: views ? +((100 * (like + kom + share)) / views).toFixed(2) : null,
    simpan_persen: views ? +((100 * simpan) / views).toFixed(3) : null,
    label_ai: !!it.aigcLabelType || !!it.IsAigc, iklan: !!it.isAd };
}

// ---------- jalur 2: TikTok API for Business ----------
const BIZ = "https://business-api.tiktok.com/open_api/v1.3";
const APP_ID = get("TIKTOK_APP_ID") || ""; // App ID TikTok milik klinik (bukan rahasia)
const REDIRECT = get("TIKTOK_REDIRECT_URI") || "";
const REF = get("TIKTOK_VAULT_PROJECT") || "";

async function sql(q) {
  const tok = get("SUPABASE_ACCESS_TOKEN");
  if (!tok) throw new Error("SUPABASE_ACCESS_TOKEN tidak ada: Vault token TikTok tidak bisa dibaca/ditulis");
  const res = await fetch(`https://api.supabase.com/v1/projects/${REF}/database/query`, {
    method: "POST", headers: { Authorization: `Bearer ${tok}`, "content-type": "application/json" }, body: JSON.stringify({ query: q }) });
  const d = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`Vault ${res.status}: ${(d.message || "").slice(0, 200)}`);
  return d;
}
const dq = (v) => { const t = "$tt$"; if (String(v).includes(t)) throw new Error("nilai tidak sah"); return `${t}${v}${t}`; };
async function vaultGet(nama) {
  const r = await sql(`select decrypted_secret as v from vault.decrypted_secrets where name = ${dq(nama)} limit 1`);
  return r[0]?.v ?? null;
}
async function vaultSet(nama, nilai) {
  const r = await sql(`select id from vault.secrets where name = ${dq(nama)} limit 1`);
  if (r[0]?.id) await sql(`select vault.update_secret(${dq(r[0].id)}::uuid, ${dq(nilai)})`);
  else await sql(`select vault.create_secret(${dq(nilai)}, ${dq(nama)})`);
}
async function oauth(pathStr, body) {
  const secret = await vaultGet("tiktok_client_secret");
  if (!secret) throw new Error("Vault 'tiktok_client_secret' belum diisi (Bapak: dashboard Supabase Anvil → Vault). Lihat panduan.");
  const res = await fetch(BIZ + pathStr, { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ client_id: APP_ID, client_secret: secret, ...body }) });
  const d = await res.json().catch(() => ({}));
  if (d.code !== 0) throw new Error(`TikTok OAuth ${res.status} code ${d.code}: ${d.message || "?"}`);
  const x = d.data, now = Date.now();
  const simpan = { access_token: x.access_token, refresh_token: x.refresh_token, open_id: x.open_id, scope: x.scope,
    access_kedaluwarsa: new Date(now + x.expires_in * 1000).toISOString(),
    refresh_kedaluwarsa: new Date(now + x.refresh_token_expires_in * 1000).toISOString(), diperbarui: new Date(now).toISOString() };
  await vaultSet("tiktok_token", JSON.stringify(simpan));
  return simpan;
}
const ringkasToken = (t) => t && ({ open_id: t.open_id, scope: (t.scope || "").split(","), access_kedaluwarsa_wib: wib(Date.parse(t.access_kedaluwarsa) / 1000),
  refresh_kedaluwarsa_wib: wib(Date.parse(t.refresh_kedaluwarsa) / 1000), diperbarui_wib: wib(Date.parse(t.diperbarui) / 1000) });
async function tokenVault() {
  const raw = await vaultGet("tiktok_token");
  if (!raw) return null;
  let t = JSON.parse(raw);
  if (Date.parse(t.access_kedaluwarsa) - Date.now() < 3600e3) {
    if (Date.parse(t.refresh_kedaluwarsa) < Date.now()) throw new Error("Refresh token TikTok kedaluwarsa (1 tahun): ulangi otorisasi akun (panduan bagian B).");
    t = await oauth("/tt_user/oauth2/refresh_token/", { grant_type: "refresh_token", refresh_token: t.refresh_token });
  }
  return t;
}
async function biz(pathStr, params) {
  let token = get("TIKTOK_BUSINESS_TOKEN"), id = get("TIKTOK_BUSINESS_ID");
  if (!token || !id) { const t = await tokenVault(); if (t) { token = t.access_token; id = t.open_id; } }
  if (!token || !id) { console.error("Token TikTok belum ada (Vault 'tiktok_token' kosong; env TIKTOK_BUSINESS_TOKEN juga tidak ada). Jalur publik (public-*) tetap bisa dipakai. Lihat panduan."); process.exit(2); }
  const url = new URL(BIZ + pathStr);
  for (const [k, v] of Object.entries({ business_id: id, ...params })) if (v !== undefined) url.searchParams.set(k, typeof v === "object" ? JSON.stringify(v) : String(v));
  const res = await fetch(url, { headers: { "Access-Token": token } });
  const d = await res.json().catch(() => ({}));
  if (d.code !== 0) throw new Error(`TikTok API ${res.status} code ${d.code}: ${d.message || JSON.stringify(d).slice(0, 300)}`);
  return d.data;
}
const ACC_FIELDS = ["username", "display_name", "followers_count", "profile_views", "video_views", "likes", "comments", "shares", "audience_countries"];
const VID_FIELDS = ["item_id", "create_time", "caption", "share_url", "video_duration", "video_views", "likes", "comments", "shares", "favorites",
  "reach", "full_video_watched_rate", "total_time_watched", "average_time_watched", "new_followers", "impression_sources"];

const cmd = process.argv[2];
const o = args();
try {
  switch (cmd) {
    case "public-profile": out(await publicProfile((o._[0] || USER).replace(/^@/, ""))); break;
    case "public-videos": {
      const user = (o._[0] || USER).replace(/^@/, "");
      const ids = await publicVideoIds(user, +(o.limit || 30));
      const rows = [];
      for (const id of ids) rows.push(await publicVideo(user, id));
      out({ username: user, diambil_wib: wib(Date.now() / 1000), jumlah: rows.length,
        catatan: "Angka publik. Embed TikTok hanya memberi ±10–13 video terbaru/populer. % tonton habis & follower per video tidak ada di jalur publik. Jangan menilai video sebelum 48 jam.",
        rows });
      break;
    }
    case "biz-account": {
      const days = +(o.days || 7);
      // end_date harus sebelum hari ini (TikTok 40002): kemarin WIB, mundur `days` hari.
      const end = new Date(Date.now() + 7 * 3600e3 - 86400e3), start = new Date(end - (days - 1) * 86400e3);
      out(await biz("/business/get/", { fields: o.fields ? o.fields.split(",") : ACC_FIELDS,
        start_date: start.toISOString().slice(0, 10), end_date: end.toISOString().slice(0, 10) }));
      break;
    }
    case "biz-videos": {
      const fields = o.fields ? o.fields.split(",") : VID_FIELDS;
      const rows = []; let cursor;
      while (rows.length < +(o.limit || 20)) {
        const d = await biz("/business/video/list/", { fields, cursor, max_count: 20 });
        rows.push(...(d.videos || []));
        if (!d.has_more) break;
        cursor = d.cursor;
      }
      const pilih = rows.slice(0, +(o.limit || 20));
      out({ jumlah: pilih.length, rows: pilih });
      break;
    }
    case "tukar-kode": {
      const kode = (o._[0] || "").trim().replace(/^.*[?&](?:code|auth_code)=([^&#]+).*$/, "$1");
      if (!kode) throw new Error("tukar-kode: <kode_otorisasi> wajib (boleh juga seluruh alamat halaman sesudah persetujuan)");
      const t = await oauth("/tt_user/oauth2/token/", { grant_type: "authorization_code", auth_code: decodeURIComponent(kode), redirect_uri: REDIRECT });
      out({ ok: true, ...ringkasToken(t), catatan: "Token tersimpan di Vault 'tiktok_token'. Uji: node tools/tiktok.mjs biz-account" });
      break;
    }
    case "impor-vault": {
      const raw = (await vaultGet("tiktok_token_masuk") || "").trim();
      if (!raw) throw new Error("Vault 'tiktok_token_masuk' kosong. Tempel token di dashboard Supabase → Vault dengan nama itu.");
      let t, cara;
      const kode = raw.match(/[?&](?:code|auth_code)=([^&#\s]+)/);
      let j = null; try { j = JSON.parse(raw); } catch { /* bukan JSON */ }
      const x = j ? (j.data || j) : null;
      if (kode && !x) {
        t = await oauth("/tt_user/oauth2/token/", { grant_type: "authorization_code", auth_code: decodeURIComponent(kode[1]), redirect_uri: REDIRECT }); cara = "kode otorisasi ditukar";
      } else if (x && x.refresh_token) {
        const sec = await vaultGet("tiktok_client_secret");
        if (sec) { t = await oauth("/tt_user/oauth2/refresh_token/", { grant_type: "refresh_token", refresh_token: x.refresh_token }); cara = "refresh token dipakai (token baru, kedaluwarsa pasti)"; }
        else {
          const now = Date.now();
          t = { access_token: x.access_token, refresh_token: x.refresh_token, open_id: x.open_id, scope: x.scope,
            access_kedaluwarsa: new Date(now + (x.expires_in || 3600) * 1000).toISOString(),
            refresh_kedaluwarsa: new Date(now + (x.refresh_token_expires_in || 0) * 1000).toISOString(), diperbarui: new Date(now).toISOString() };
          await vaultSet("tiktok_token", JSON.stringify(t)); cara = "disimpan apa adanya; Secret belum di Vault, jadi belum bisa diperpanjang otomatis";
        }
      } else {
        const at = x ? x.access_token : raw;
        const oid = (x && x.open_id) || (await vaultGet("tiktok_open_id")) || get("TIKTOK_BUSINESS_ID");
        if (!at || !oid) throw new Error("Isi 'tiktok_token_masuk' tidak dikenali, atau access token polos tanpa open_id (tambahkan Vault 'tiktok_open_id').");
        const now = Date.now();
        t = { access_token: at, refresh_token: null, open_id: oid, scope: x?.scope || "", access_kedaluwarsa: new Date(now + ((x && x.expires_in) || 86400) * 1000).toISOString(),
          refresh_kedaluwarsa: new Date(now).toISOString(), diperbarui: new Date(now).toISOString() };
        await vaultSet("tiktok_token", JSON.stringify(t)); cara = "access token polos: berlaku <= 24 jam, sesudah itu perlu otorisasi (panduan C)";
      }
      await sql(`delete from vault.secrets where name = ${dq("tiktok_token_masuk")}`);
      out({ ok: true, cara, ...ringkasToken(t), catatan: "'tiktok_token_masuk' dihapus dari Vault. Uji: node tools/tiktok.mjs biz-account" });
      break;
    }
    case "token-status": {
      const raw = await vaultGet("tiktok_token");
      out({ client_secret_di_vault: !!(await vaultGet("tiktok_client_secret")), token: raw ? ringkasToken(JSON.parse(raw)) : null });
      break;
    }
    default:
      console.error("Perintah: public-profile | public-videos | biz-account | biz-videos | tukar-kode | token-status. Lihat kepala file.");
      process.exit(1);
  }
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
