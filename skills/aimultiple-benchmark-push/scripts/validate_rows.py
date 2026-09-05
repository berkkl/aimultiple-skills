#!/usr/bin/env python3
"""F3 + F4: local dry-run for /benchmark/feed. Writes NOTHING.

/benchmark/feed has no dry_run and is insert-only, so this is the only chance to
catch a bad payload. Fetches the live contract (describe) and the live lookup
tables, then checks every row against them.

    python validate_rows.py --id 390 --type benchmark --rows feed.json
    python validate_rows.py --describe desc.json --rows feed.json --shared ai_models.json

Exit 0 = feed may run. Exit 1 = it must not.
"""
from __future__ import annotations
import argparse, collections, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import api  # noqa: E402

SYSTEM = {"id", "status", "created_at", "updated_at", "deleted_at", "data_version",
          "insert_api_key_id"}
AUTO = {"data_version"}                      # optional on feed, server defaults it to 1
INT_T = {"tinyint", "smallint", "mediumint", "int", "bigint"}
LINE = re.compile(r"^(\S+)\s+(\S+?)(?:\((\d+)(?:,(\d+))?\))?\s+(not null|nullable)$")


def parse_contract(desc_data: dict) -> dict:
    spec = {}
    for line in desc_data["table_structure"]:
        m = LINE.match(line.strip())
        if not m:
            sys.exit(f"describe satırı ayrıştırılamadı: {line}")
        name, typ, p, s, null = m.groups()
        spec[name] = dict(type=typ, p=int(p) if p else None, s=int(s) if s else None,
                          nullable=(null == "nullable"))
    return spec


def is_live(row: dict) -> bool:
    """The server resolves relations only against live rows. /benchmark/get returns
    soft-deleted ones too, so a validator that skips this check gives a false green."""
    return not row.get("deleted_at") and row.get("status") in (1, "1", "active")


def validate(spec: dict, rows: list, shared: dict[str, list] | None):
    errs, warns = [], []
    required = {k for k, v in spec.items() if not v["nullable"] and k not in AUTO}

    for i, r in enumerate(rows):
        for k in r:
            if k not in spec:
                errs.append(f"satır {i}: bilinmeyen kolon {k!r}")
            elif k in SYSTEM and k not in AUTO:
                errs.append(f"satır {i}: sistem kolonu gönderiliyor {k!r}")
        for k in sorted(required - set(r)):
            errs.append(f"satır {i}: NOT NULL kolon eksik {k!r}")
        for k, v in r.items():
            c = spec.get(k)
            if not c:
                continue
            if v is None:
                if not c["nullable"]:
                    errs.append(f"satır {i}: {k} NOT NULL ama null gönderiliyor")
                continue
            t = c["type"]
            if t in INT_T:
                if not isinstance(v, int) or isinstance(v, bool):
                    errs.append(f"satır {i}: {k} tam sayı değil ({v!r})")
                elif t == "tinyint" and not -128 <= v <= 127:
                    errs.append(f"satır {i}: {k} tinyint aralığı dışında ({v})")
            elif t in ("decimal", "numeric", "float", "double"):
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    errs.append(f"satır {i}: {k} sayı değil ({v!r})")
                elif c["p"]:
                    if abs(v) >= 10 ** (c["p"] - c["s"]):
                        errs.append(f"satır {i}: {k}={v} decimal({c['p']},{c['s']}) tam kısmına sığmıyor")
                    frac = str(abs(v)).split(".")
                    if len(frac) > 1 and len(frac[1].rstrip("0")) > c["s"]:
                        errs.append(f"satır {i}: {k}={v} {c['s']} ondalık basamağı aşıyor")
            elif t in ("varchar", "char", "string", "text", "tinytext", "mediumtext", "longtext"):
                if not isinstance(v, str):
                    errs.append(f"satır {i}: {k} metin değil ({v!r})")
                elif c["p"] and len(v) > c["p"]:
                    errs.append(f"satır {i}: {k} {c['p']} karakteri aşıyor ({len(v)})")
            # HARD error, not a warning: the server escapes ' " and newlines with a naive
            # addslashes() and leaves the backslash in the stored text. A value carrying any
            # of them CANNOT be stored correctly, and feed cannot be undone.
            if isinstance(v, str):
                for ch, name, fix in (("'", "apostrof", "tipografik ’ (U+2019) kullan"),
                                      ('"', "cift tirnak", "tirnaksiz yaz: M=64, ef=128"),
                                      ("\n", "satir sonu", "tek satira indir"),
                                      ("\\", "ters bolu", "kaldir")):
                    if ch in v:
                        errs.append(f"satır {i}: {k} {name} içeriyor — sunucu bozar "
                                    f"(addslashes bug, 2026-09-04 ölçüldü). Çözüm: {fix}")

    # ---- F4: relations resolve against LIVE rows only ----
    for rc in [k for k in spec if "." in k]:
        field = rc.split(".", 1)[1]
        pool = (shared or {}).get(rc.split(".", 1)[0])
        if pool is None:
            warns.append(f"F4 ATLANDI: {rc} için paylaşılan tablo çekilemedi")
            continue
        live = collections.Counter((x.get(field) or "").lower() for x in pool if is_live(x))
        dead = collections.Counter((x.get(field) or "").lower() for x in pool if not is_live(x))
        want = collections.Counter(r[rc] for r in rows if r.get(rc) is not None)
        miss = 0
        for val, n in sorted(want.items()):
            hits = live.get(val.lower(), 0)
            if hits == 0:
                why = (f" — o adla {dead[val.lower()]} satır var ama SİLİNMİŞ/pasif, sunucu görmüyor"
                       if dead.get(val.lower()) else " — hedef tabloda yok")
                errs.append(f"ilişki ÇÖZÜLEMEDİ: {rc}={val!r} ({n} satır){why}")
                miss += 1
            elif hits > 1:
                warns.append(f"ilişki BELİRSİZ: {rc}={val!r} için {hits} AKTİF satır var")
        print(f"F4 {rc}: {len(want)} farklı değer, {len(want)-miss} çözüldü"
              + (f", {miss} ÇÖZÜLEMEDİ" if miss else ""))

    # ---- F4b: the server derives the bulk-INSERT column list from the FIRST row ----
    groups = collections.defaultdict(int)
    for r in rows:
        groups[frozenset(k for k, v in r.items() if v is not None)] += 1
    print(f"F3 {len(rows)} satır · sözleşmede {len(spec)} kolon · NOT NULL {len(required)}")
    print(f"F4b anahtar-imzası: {len(groups)} grup → {sorted(groups.values(), reverse=True)}")
    if len(groups) > 1:
        print("    (feed batch'i imza başına bölünmeli — bkz. feed_ladder.py)")
    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--id"); ap.add_argument("--type", default="benchmark")
    ap.add_argument("--describe"); ap.add_argument("--shared", action="append", default=[])
    a = ap.parse_args()

    rows = json.load(open(a.rows))
    if a.describe:
        desc = json.load(open(a.describe))
    else:
        if not a.id:
            sys.exit("--id ya da --describe gerekli")
        desc = api.call("describe", {"id": str(a.id), "type": a.type})
        if not api.ok(desc):
            sys.exit(f"describe başarısız: {json.dumps(desc, ensure_ascii=False)[:300]}")
    spec = parse_contract(desc["data"] if "data" in desc else desc)

    shared = {}
    for f in a.shared:                       # --shared ai_models=file.json
        name, _, path = f.partition("=")
        shared[name] = api.rows(json.load(open(path)))
    for rc in [k for k in spec if "." in k]:
        tbl = rc.split(".", 1)[0]
        if tbl not in shared:
            shared[tbl] = api.rows(api.call("get", {"id": tbl, "type": "shared", "limit": 5000}))

    errs, warns = validate(spec, rows, shared)
    for w in warns:
        print("  ⚠", w)
    if errs:
        print(f"\n❌ {len(errs)} HATA — feed ÇALIŞTIRILMAMALI:")
        for e in errs[:30]:
            print("   ", e)
        if len(errs) > 30:
            print(f"    ... {len(errs)-30} hata daha")
        return 1
    print("\n✅ F3 + F4 temiz — feed edilebilir")
    return 0


if __name__ == "__main__":
    sys.exit(main())
