#!/usr/bin/env bash
# Pagar ERP baca-saja (perintah Bapak 29 Sep 2026; diperkuat 10 Nov 2026 sesudah Bapak tanya "ada kemungkinan data
# bisa tidak sengaja terhapus?").
# Di klinik: konektor MCP Supabase akun ini bisa tersambung ke project RHJ. Agent klinik hanya BACA lewat MCP; perubahan Anvil klinik lewat CLI/migrasi dengan ACC Bapak.
# PreToolUse untuk mcp__Supabase__execute_sql. Dua lapis:
#  1. Tolak query kosong / berisi kata kunci penulis ATAU pengendali transaksi (commit, rollback, begin, set, ...).
#     Kata kunci di komentar SQL juga ditolak (sengaja: lebih baik salah tolak daripada lolos).
#  2. Query yang lolos DIBUNGKUS `set transaction read only;` (updatedInput): seluruh permintaan berjalan dalam transaksi
#     baca-saja, jadi penulisan apa pun (termasuk lewat fungsi di dalam SELECT) ditolak database sendiri
#     ("cannot execute UPDATE in a read-only transaction", diuji 10 Nov). Lapis 1 mencegah transaksi itu diakhiri
#     (commit) atau dibalik (set transaction read write) dari dalam query; satu pernyataan per panggilan (titik koma hanya
#     di akhir).
masuk=$(cat)
q=$(printf '%s' "$masuk" | jq -r '.tool_input.query // empty' 2>/dev/null)
pola='\b(insert|update|delete|merge|upsert|alter|create|drop|truncate|grant|revoke|vacuum|reindex|cluster|copy|call|refresh|lock|comment[[:space:]]+on|security[[:space:]]+label|nextval|setval|set_config|pg_terminate_backend|pg_cancel_backend|lo_import|lo_unlink|dblink|commit|rollback|abort|begin|savepoint|release|prepare|discard|listen|notify|set|reset|start[[:space:]]+transaction|read[[:space:]]+write|transaction_read_only|pg_read_file|pg_ls_dir)\b|\bdo[[:space:]]*\$'
tolak() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}
[ -z "$q" ] && tolak "Pagar klinik: query kosong."
# Satu pernyataan saja: titik koma hanya boleh di akhir (juga di komentar/teks tidak boleh), supaya query tidak bisa
# mengakhiri transaksi baca-saja (commit/end) lalu menjalankan pernyataan lain.
if printf '%s' "$q" | sed -e 's/[[:space:]]*$//' -e '$ s/;$//' | grep -q ';'; then
  tolak "Pagar klinik: hanya SATU pernyataan SQL per panggilan (titik koma hanya di akhir, termasuk di komentar). Pecah jadi beberapa panggilan."
fi
if printf '%s' "$q" | grep -qiE "$pola"; then
  tolak "Pagar klinik: MCP Supabase = ERP, BACA-SAJA. Query berisi kata kunci penulis / pengendali transaksi (insert, update, delete, commit, begin, set, ...) ditolak. Tulis ulang sebagai SELECT murni. Anvil memakai berkas migrasi + alat/sql-proyek.sh, bukan MCP."
fi
printf '%s' "$masuk" | jq -c '.tool_input | .query = ("set transaction read only;\n" + .query) | {hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"allow",permissionDecisionReason:"Pagar klinik: dijalankan dalam transaksi baca-saja",updatedInput:.}}'
exit 0
