#!/usr/bin/env python3
"""Cek koneksi API ElevenLabs & Higgsfield TANPA memakai kredit.

Pakai: python3 cek_api.py            # cek keduanya
       python3 cek_api.py --suara    # + daftar suara ElevenLabs (nama + voice_id) untuk voices.json
Env: ELEVENLABS_API_KEY · HF_API_KEY + HF_API_SECRET. Nilai kunci tidak pernah dicetak.
"""
import json, os, sys, urllib.request, urllib.error


def get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:  # jaringan
        return None, str(e).encode()


def eleven():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        print("ElevenLabs: env ELEVENLABS_API_KEY KOSONG"); return
    st, body = get("https://api.elevenlabs.io/v1/user/subscription", {"xi-api-key": key})
    if st == 200:
        d = json.loads(body)
        print(f"ElevenLabs: OK · paket {d.get('tier')} · karakter terpakai "
              f"{d.get('character_count')}/{d.get('character_limit')}")
    elif st in (401, 403):
        # kunci yang dibatasi bisa tidak punya izin baca langganan; coba endpoint suara
        st2, _ = get("https://api.elevenlabs.io/v1/voices", {"xi-api-key": key})
        print(f"ElevenLabs: langganan HTTP {st} · daftar suara HTTP {st2}"
              + (" → kunci DITERIMA (izin terbatas)" if st2 == 200 else " → kunci DITOLAK/izin kurang"))
    else:
        print(f"ElevenLabs: HTTP {st} {body[:200]!r}")
    if "--suara" in sys.argv:
        st, body = get("https://api.elevenlabs.io/v1/voices", {"xi-api-key": key})
        if st == 200:
            for v in json.loads(body).get("voices", []):
                print(f"  - {v.get('name')} · voice_id {v.get('voice_id')} · {v.get('category')}")
        else:
            print(f"  daftar suara: HTTP {st}")


def higgs():
    kid, sec = os.environ.get("HF_API_KEY"), os.environ.get("HF_API_SECRET")
    if not kid or not sec:
        print("Higgsfield: env HF_API_KEY / HF_API_SECRET KOSONG"); return
    # status request fiktif: 401 = kunci ditolak; 404/422/400 = kunci diterima (request memang tidak ada)
    st, body = get("https://platform.higgsfield.ai/requests/00000000-0000-0000-0000-000000000000/status",
                   {"Authorization": f"Key {kid}:{sec}"})
    if st == 401:
        print("Higgsfield: kunci DITOLAK (401)")
    elif st in (400, 404, 422):
        print(f"Higgsfield: kunci DITERIMA (HTTP {st} untuk request fiktif, sesuai harapan)")
    else:
        print(f"Higgsfield: HTTP {st} {body[:200]!r} → periksa manual")


if __name__ == "__main__":
    eleven(); higgs()
