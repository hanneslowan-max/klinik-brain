// meta.mjs — Analitik Instagram klinik + Meta Ads langsung dari Graph API / Marketing API resmi Meta.
// Kenapa: tanpa pihak ketiga (Windsor/Metricool). HANYA BACA — skrip ini tidak pernah membuat/mengubah
// posting, iklan, budget, atau setelan apa pun.
//
// Pemakaian (output JSON ke stdout):
//   node tools/meta.mjs whoami                               cek token: nama + izin (scope) yang diberikan
//   node tools/meta.mjs ig-account                           profil IG: username, follower, jumlah media
//   node tools/meta.mjs ig-media [--limit 30]                daftar posting/Reels + like & komentar
//   node tools/meta.mjs ig-insights <media_id>               insight 1 posting (views, reach, share, simpan, watch time)
//   node tools/meta.mjs ig-report [--limit 30]               ig-media + insight tiap posting (tabel siap untuk SOSMED-MEMORI)
//   node tools/meta.mjs ig-account-insights [--days 7]       insight akun: views, reach, follow/unfollow, klik link bio, interaksi
//   node tools/meta.mjs ads-list                             daftar iklan + status
//   node tools/meta.mjs ads-insights [--level ad|adset|campaign|account] [--since YYYY-MM-DD --until YYYY-MM-DD | --preset last_7d] [--daily]
//        spend, reach, klik, chat WA dimulai, biaya per chat WA, retensi video 25/50/75/100%
//
// Kredensial dari ENV (di cloud: pengaturan environment) — JANGAN commit, JANGAN tempel di chat:
//   META_ACCESS_TOKEN    (wajib; token system user Business Manager, izin baca saja:
//                         instagram_basic, instagram_manage_insights, pages_show_list,
//                         pages_read_engagement, ads_read, read_insights, business_management)
//   META_IG_USER_ID      (ID akun IG Bisnis klinik — BUKAN username)
//   META_AD_ACCOUNT_ID   (ID akun iklan Meta KLINIK, angka saja atau "act_...")
//   META_PAGE_ID         (opsional; ID Page Facebook klinik, dipakai `whoami` untuk cek sambungan IG)
//   META_GRAPH_VERSION   (opsional; default v23.0)
// Panduan pembuatan token: deliverables/PANDUAN-TOKEN-API-META-TIKTOK-30Sep.md

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
  } catch { /* .env tak ada -> pakai process.env */ }
  return out;
}
const env = loadEnv(path.join(HERE, ".env"));
const get = (k) => (process.env[k] || env[k] || "").trim();
const TOKEN = get("META_ACCESS_TOKEN");
const IG = get("META_IG_USER_ID");
const PAGE = get("META_PAGE_ID");
const ACT = get("META_AD_ACCOUNT_ID").replace(/^act_/, "");
const BASE = `https://graph.facebook.com/${get("META_GRAPH_VERSION") || "v23.0"}`;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let lastCall = 0;
async function api(pathOrUrl, params = {}) {
  const url = new URL(pathOrUrl.startsWith("https://") ? pathOrUrl : BASE + pathOrUrl);
  for (const [k, v] of Object.entries(params)) if (v !== undefined) url.searchParams.set(k, typeof v === "object" ? JSON.stringify(v) : String(v));
  if (!url.searchParams.has("access_token")) url.searchParams.set("access_token", TOKEN);
  for (let attempt = 0; attempt < 4; attempt++) {
    const wait = lastCall + 350 - Date.now();
    if (wait > 0) await sleep(wait);
    lastCall = Date.now();
    const res = await fetch(url, { method: "GET" });
    const data = await res.json().catch(() => ({}));
    if (res.ok) return data;
    const e = data.error || {};
    // 4/17/32/613 = batas panggilan -> tunggu & ulang
    if ([4, 17, 32, 613].includes(e.code) && attempt < 3) { await sleep(60000 * (attempt + 1)); continue; }
    const err = new Error(`Graph API ${res.status}: ${e.message || JSON.stringify(data).slice(0, 300)}`);
    err.meta = e;
    throw err;
  }
}
async function allPages(pathStr, params, max = 1000) {
  const out = [];
  let data = await api(pathStr, params);
  while (true) {
    out.push(...(data.data || []));
    if (out.length >= max || !data.paging?.next) break;
    data = await api(data.paging.next);
  }
  return out.slice(0, max);
}

function args() {
  const a = process.argv.slice(3), o = { _: [] };
  for (let i = 0; i < a.length; i++) {
    if (a[i].startsWith("--")) { const k = a[i].slice(2); const n = a[i + 1]; if (n === undefined || n.startsWith("--")) o[k] = true; else { o[k] = n; i++; } }
    else o._.push(a[i]);
  }
  return o;
}
function need(v, name) { if (!v) { console.error(`${name} belum di-set di environment. Lihat deliverables/PANDUAN-TOKEN-API-META-TIKTOK-30Sep.md`); process.exit(2); } }
const ymd = (d) => new Date(d.getTime() + 7 * 3600e3).toISOString().slice(0, 10); // tanggal WIB

// Metrik insight per posting. Reels & video/foto punya set berbeda; kalau satu set ditolak, coba set berikutnya.
const MEDIA_METRICS = [
  "views,reach,likes,comments,shares,saved,total_interactions,ig_reels_avg_watch_time,ig_reels_video_view_total_time",
  "views,reach,likes,comments,shares,saved,total_interactions",
  "reach,likes,comments,shares,saved,total_interactions",
];
async function mediaInsights(id) {
  let lastErr;
  for (const metric of MEDIA_METRICS) {
    try {
      const d = await api(`/${id}/insights`, { metric });
      const o = {};
      for (const m of d.data || []) o[m.name] = m.values?.[0]?.value ?? m.total_value?.value ?? null;
      // ms -> detik supaya mudah dibaca
      if (o.ig_reels_avg_watch_time != null) o.avg_watch_time_dtk = +(o.ig_reels_avg_watch_time / 1000).toFixed(2);
      if (o.ig_reels_video_view_total_time != null) o.total_watch_time_dtk = Math.round(o.ig_reels_video_view_total_time / 1000);
      return o;
    } catch (e) { lastErr = e; }
  }
  return { error: lastErr?.message };
}
const MEDIA_FIELDS = "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count";

// Aksi WA / pesan di Marketing API (click-to-WhatsApp)
const WA_ACTIONS = ["onsite_conversion.messaging_conversation_started_7d", "onsite_conversion.total_messaging_connection"];
function pickAction(list, types) {
  for (const t of types) { const f = (list || []).find((a) => a.action_type === t); if (f) return +f.value; }
  return 0;
}

const cmd = process.argv[2];
const o = args();
const out = (x) => console.log(JSON.stringify(x, null, 2));

try {
  need(TOKEN, "META_ACCESS_TOKEN");
  switch (cmd) {
    case "whoami": {
      const me = await api("/me", { fields: "id,name" });
      const perms = await api("/me/permissions").catch((e) => ({ error: e.message }));
      const res = { me, izin: (perms.data || []).filter((p) => p.status === "granted").map((p) => p.permission) };
      if (PAGE) res.page = await api(`/${PAGE}`, { fields: "name,instagram_business_account{id,username}" }).catch((e) => ({ error: e.message }));
      res.env = { META_IG_USER_ID: !!IG, META_AD_ACCOUNT_ID: !!ACT, META_PAGE_ID: !!PAGE };
      out(res); break;
    }
    case "ig-account": {
      need(IG, "META_IG_USER_ID");
      out(await api(`/${IG}`, { fields: "id,username,name,followers_count,follows_count,media_count,biography,website" })); break;
    }
    case "ig-media": {
      need(IG, "META_IG_USER_ID");
      out(await allPages(`/${IG}/media`, { fields: MEDIA_FIELDS, limit: 50 }, +(o.limit || 30))); break;
    }
    case "ig-insights": {
      need(o._[0], "media_id");
      out({ id: o._[0], ...(await mediaInsights(o._[0])) }); break;
    }
    case "ig-report": {
      need(IG, "META_IG_USER_ID");
      const media = await allPages(`/${IG}/media`, { fields: MEDIA_FIELDS, limit: 50 }, +(o.limit || 30));
      const rows = [];
      for (const m of media) {
        const ins = await mediaInsights(m.id);
        const umurJam = Math.round((Date.now() - new Date(m.timestamp)) / 3600e3);
        rows.push({ id: m.id, tgl_wib: ymd(new Date(m.timestamp)), umur_jam: umurJam, jenis: m.media_product_type || m.media_type,
          link: m.permalink, caption_awal: (m.caption || "").split("\n")[0].slice(0, 80), ...ins });
      }
      out({ diambil_wib: new Date(Date.now() + 7 * 3600e3).toISOString().replace("T", " ").slice(0, 16), jumlah: rows.length,
        catatan: "Jangan menilai video sebelum 48 jam (umur_jam < 48).", rows }); break;
    }
    case "ig-account-insights": {
      need(IG, "META_IG_USER_ID");
      const days = +(o.days || 7);
      const until = Math.floor(Date.now() / 1000), since = until - days * 86400;
      const res = {};
      for (const metric of ["views", "reach", "follows_and_unfollows", "profile_links_taps", "total_interactions", "accounts_engaged"]) {
        try {
          const d = await api(`/${IG}/insights`, { metric, period: "day", metric_type: "total_value", since, until });
          res[metric] = d.data?.[0]?.total_value ?? null;
        } catch (e) { res[metric] = { error: e.message }; }
      }
      try {
        const d = await api(`/${IG}/insights`, { metric: "follower_count", period: "day", since, until });
        res.follower_bertambah_per_hari = (d.data?.[0]?.values || []).map((v) => ({ tgl: v.end_time?.slice(0, 10), nilai: v.value }));
      } catch (e) { res.follower_bertambah_per_hari = { error: e.message }; }
      out({ rentang_hari: days, ...res }); break;
    }
    case "ads-list": {
      need(ACT, "META_AD_ACCOUNT_ID");
      out(await allPages(`/act_${ACT}/ads`, { fields: "id,name,status,effective_status,adset{name},campaign{name,objective},created_time", limit: 100 })); break;
    }
    case "ads-insights": {
      need(ACT, "META_AD_ACCOUNT_ID");
      const level = o.level || "ad";
      const params = {
        level, limit: 200,
        fields: "campaign_name,adset_name,ad_name,ad_id,spend,impressions,reach,frequency,clicks,inline_link_clicks,ctr,cpc,actions,cost_per_action_type,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p100_watched_actions,video_thruplay_watched_actions",
      };
      if (o.since) params.time_range = { since: o.since, until: o.until || ymd(new Date()) };
      else params.date_preset = o.preset || "last_7d";
      if (o.daily) params.time_increment = 1;
      const rows = (await allPages(`/act_${ACT}/insights`, params)).map((r) => {
        const v = (k) => +(r[k]?.[0]?.value || 0);
        const wa = pickAction(r.actions, WA_ACTIONS);
        return {
          tgl: r.date_start === r.date_stop ? r.date_start : `${r.date_start}..${r.date_stop}`,
          campaign: r.campaign_name, adset: r.adset_name, iklan: r.ad_name, ad_id: r.ad_id,
          spend: +r.spend || 0, impresi: +r.impressions || 0, reach: +r.reach || 0, frekuensi: +r.frequency || 0,
          klik: +r.clicks || 0, klik_link: +r.inline_link_clicks || 0, ctr_persen: +r.ctr || 0, cpc: +r.cpc || 0,
          chat_wa_dimulai: wa, biaya_per_chat_wa: wa ? +((+r.spend || 0) / wa).toFixed(0) : null,
          video_25: v("video_p25_watched_actions"), video_50: v("video_p50_watched_actions"), video_75: v("video_p75_watched_actions"),
          video_100: v("video_p100_watched_actions"), thruplay: v("video_thruplay_watched_actions"),
          actions_mentah: r.actions,
        };
      });
      out({ level, rentang: params.time_range || params.date_preset, catatan: "Mata uang = mata uang akun iklan (IDR). Aksi WA diambil dari messaging_conversation_started_7d.", rows }); break;
    }
    default:
      console.error("Perintah: whoami | ig-account | ig-media | ig-insights <id> | ig-report | ig-account-insights | ads-list | ads-insights. Lihat kepala file.");
      process.exit(1);
  }
} catch (e) {
  console.error(e.message);
  process.exit(1);
}
