#!/usr/bin/env python3
"""F4b-F7: the only safe way to run /benchmark/feed.

feed has no dry_run, cannot update or delete, and there is no test database. It is
also ATOMIC (a failed batch writes nothing), which is what makes this ladder work:
every rung can fail safely, be fixed, and be retried.

    python feed_ladder.py --id 390 --rows feed.json --backup-dir ./restore        # plan only
    python feed_ladder.py --id 390 --rows feed.json --backup-dir ./restore --apply

Rungs:
  F3/F4  validate_rows.py must pass first, or --apply refuses to run
  F4b    group rows by key signature — the server derives the bulk-INSERT column
         list from the FIRST row of a batch, so a mixed batch dies with
         "1136 Column count doesn't match value count"
  F5     snapshot the table before writing
  F6     one canary per signature (a canary must obey F4b too), read back, compare
  F7     feed the rest group by group, then compare every cell against the source
"""
from __future__ import annotations
import argparse, collections, datetime, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import api, validate_rows  # noqa: E402

SYS_COLS = {"id", "status", "created_at", "updated_at", "deleted_at", "data_version"}


def norm(v):
    if v is None:
        return None
    try:
        return round(float(v), 6)
    except (TypeError, ValueError):
        return str(v)


def canon(row, universe):
    return tuple(sorted((k, norm(row.get(k))) for k in universe))


def signature_groups(rows):
    g = collections.defaultdict(list)
    for r in rows:
        g[frozenset(k for k, v in r.items() if v is not None)].append(r)
    return sorted(g.values(), key=len, reverse=True)


def compare(sent, got, key=None):
    """Cell-level comparison. With --key, per-field diffs; without, a multiset check."""
    universe = sorted({k for r in sent for k in r})
    bad = []
    if key:
        idx = {tuple(str(r.get(k)) for k in key): r for r in got}
        if len(idx) != len(got):
            bad.append(f"geri dönende mükerrer anahtar ({len(got)} satır, {len(idx)} benzersiz)")
        for s in sent:
            kk = tuple(str(s.get(k)) for k in key)
            g = idx.get(kk)
            if g is None:
                bad.append(f"EKSİK: {kk}")
                continue
            for c in universe:
                sv, gv = norm(s.get(c)), norm(g.get(c))
                if sv != gv:
                    bad.append(f"{kk}.{c}: gönderilen={s.get(c)!r} okunan={g.get(c)!r}")
    else:
        cs = collections.Counter(canon(r, universe) for r in sent)
        cg = collections.Counter(canon(r, universe) for r in got)
        for t, n in (cs - cg).items():
            bad.append("geri dönende YOK (%dx): %s" % (n, dict(t)))
        for t, n in (cg - cs).items():
            bad.append("kaynakta YOK (%dx): %s" % (n, dict(t)))
    return bad


def fetch(bid, btype):
    d = api.call("get", {"id": str(bid), "type": btype, "limit": 10000})
    if isinstance(d, dict) and d.get("status") == "error":
        # an empty table answers "Table not found" before the first insert
        return []
    return api.rows(d)


def feed(bid, btype, batch, tag):
    d = api.call("feed", {"id": int(bid), "type": btype,
                          "autoCreateRelation": False, "data": batch})
    if not api.ok(d):
        print(f"  ✗ {tag} HATA: {json.dumps(d, ensure_ascii=False)[:600]}")
        return None
    n = d["data"]["insertCount"]
    print(f"  ✓ {tag}: {len(batch)} gönderildi → {n} eklendi")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--type", default="benchmark")
    ap.add_argument("--rows", required=True)
    ap.add_argument("--backup-dir", default=".")
    ap.add_argument("--key", help="karşılaştırma anahtarı, virgüllü (örn. 'ai_models.name,question_bucket')")
    ap.add_argument("--apply", action="store_true", help="olmadan hiçbir şey yazılmaz")
    a = ap.parse_args()
    key = [k.strip() for k in a.key.split(",")] if a.key else None

    src = [dict(sorted(r.items())) for r in json.load(open(a.rows))]
    groups = signature_groups(src)
    print(f"kaynak: {len(src)} satır · {len(groups)} anahtar-imzası grubu "
          f"→ {[len(g) for g in groups]}")

    print("\n— F3/F4 —")
    desc = api.call("describe", {"id": str(a.id), "type": a.type})
    if not api.ok(desc):
        sys.exit(f"describe başarısız: {json.dumps(desc, ensure_ascii=False)[:300]}")
    spec = validate_rows.parse_contract(desc["data"])
    shared = {t.split(".", 1)[0]: api.rows(api.call(
        "get", {"id": t.split(".", 1)[0], "type": "shared", "limit": 5000}))
        for t in spec if "." in t}
    errs, warns = validate_rows.validate(spec, src, shared)
    for w in warns:
        print("  ⚠", w)
    if errs:
        print(f"\n❌ {len(errs)} hata — feed çalıştırılmayacak:")
        for e in errs[:20]:
            print("   ", e)
        return 1
    print("  ✅ temiz")

    if not a.apply:
        print("\n— PLAN (hiçbir şey yazılmadı) —")
        for i, g in enumerate(groups, 1):
            c = g[0]
            print(f"  grup {i}: {len(g):4} satır · {len(c)} kolon · kanarya: "
                  + ", ".join(f"{c[k]}" for k in (key or list(c))[:2]))
        print(f"\n  --apply ile: yedek → {len(groups)} kanarya → {len(groups)} grup → tam doğrulama")
        return 0

    print("\n— F5 yedek —")
    before = fetch(a.id, a.type)
    Path(a.backup_dir).mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    bp = Path(a.backup_dir) / f"restore_b{a.id}_before_feed_{stamp}.json"
    bp.write_text(json.dumps(before, ensure_ascii=False, indent=1))
    print(f"  mevcut {len(before)} satır → {bp}")

    print("\n— F6 kanarya (imza başına bir satır) —")
    canaries = [g[0] for g in groups]
    for i, c in enumerate(canaries, 1):
        if feed(a.id, a.type, [c], f"kanarya {i} ({len(c)} kolon)") is None:
            return 1
    got = fetch(a.id, a.type)
    fresh = [r for r in got if r not in before]
    bad = compare(canaries, fresh if len(fresh) == len(canaries) else got, key)
    if bad:
        print(f"  ❌ kanarya uyuşmadı, DURULDU ({len(bad)}):")
        for b in bad[:10]:
            print("   ", b)
        return 1
    print(f"  ✅ {len(canaries)} kanarya birebir geri okundu")

    print("\n— F7 kalan satırlar —")
    total = len(canaries)
    for i, g in enumerate(groups, 1):
        rest = g[1:]
        if not rest:
            continue
        n = feed(a.id, a.type, rest, f"grup {i}")
        if n is None:
            print("  (feed atomik: bu grup yazılmadı, önceki gruplar yazıldı)")
            return 1
        total += n
    print(f"  toplam eklenen: {total}")

    print("\n— F7 tam doğrulama —")
    got = fetch(a.id, a.type)
    print(f"  geri okunan: {len(got)} · beklenen: {len(before) + len(src)}")
    new = [r for r in got if r.get("id") not in {x.get("id") for x in before}]
    bad = compare(src, new, key)
    if bad:
        print(f"  ❌ {len(bad)} fark:")
        for b in bad[:20]:
            print("   ", b)
        return 1
    filled = {k for r in new for k, v in r.items() if v is not None} - SYS_COLS
    empty = {k for k in spec if k not in filled and "." not in k}
    print(f"  ✅ {len(src)} satırın TÜM hücreleri kaynakla birebir")
    if empty:
        print(f"  boş bırakılan kolonlar gerçek NULL: {sorted(empty)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
