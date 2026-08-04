#!/usr/bin/env python3
"""
upload_to_db.py - push a benchmark CSV to the AIMultiple research DB.

Subcommands:
  authorize       print and cache a bearer token
  describe        fetch table_structure and example rows for benchmark.toml id
  validate        check local CSV headers and resolve FK values against shared tables
  upload          feed rows. --test writes to the test DB.
  get             read N rows back from the DB
  assign          attach benchmark.toml's article_url and page_title
  shared          read rows from a shared table (companies, ai_models, ...)
  shared-tables   list shared relational tables
  list            list benchmarks for a company_id
  top-list        leaderboard projection

Env:
  AIMULTIPLE_BENCHMARK_API_KEY     required
  AIMULTIPLE_BENCHMARK_API_BASE    default: https://research-api.test.v5.aimultiple.com
  AIMULTIPLE_BENCHMARK_TOKEN_PATH  default: ~/.cache/aimultiple-benchmark-token
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE = "https://research-api.test.v5.aimultiple.com"
TOKEN_PATH = Path(os.environ.get(
    "AIMULTIPLE_BENCHMARK_TOKEN_PATH",
    str(Path.home() / ".cache" / "aimultiple-benchmark-token"),
))


def api_base() -> str:
    return os.environ.get("AIMULTIPLE_BENCHMARK_API_BASE", DEFAULT_BASE).rstrip("/")


def api_key() -> str:
    key = os.environ.get("AIMULTIPLE_BENCHMARK_API_KEY")
    if not key:
        sys.exit("error: AIMULTIPLE_BENCHMARK_API_KEY is not set")
    return key


def http(method: str, path: str, headers: dict | None = None, body: dict | None = None) -> dict:
    url = f"{api_base()}{path}"
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace") if e.fp else ""
        return {"status": "error", "_http": e.code, "errors": [msg or e.reason]}


def authorize(force: bool = False) -> str:
    if not force and TOKEN_PATH.exists():
        tok = TOKEN_PATH.read_text().strip()
        if tok:
            return tok
    res = http("GET", "/benchmark/authorize", headers={"Api-Key": api_key()})
    if res.get("status") != "success":
        sys.exit(f"error: authorize failed: {res}")
    tok = res["token"]
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(tok)
    TOKEN_PATH.chmod(0o600)
    return tok


def call(path: str, body: dict, retry_401: bool = True) -> dict:
    tok = authorize()
    headers = {"Authorization": f"Bearer {tok}"}
    res = http("POST", path, headers=headers, body=body)
    if retry_401 and isinstance(res, dict):
        looks_unauth = res.get("_http") == 401 or any(
            "token" in str(e).lower() or "unauthor" in str(e).lower()
            for e in res.get("errors", [])
        )
        if res.get("status") == "error" and looks_unauth:
            authorize(force=True)
            return call(path, body, retry_401=False)
    return res


def load_config(path: Path = Path("benchmark.toml")) -> dict:
    if not path.exists():
        sys.exit(f"error: {path} not found in {Path.cwd()}")
    return tomllib.loads(path.read_text())


def load_csv(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def rename_columns(rows: list[dict], rename: dict) -> list[dict]:
    if not rename:
        return rows
    return [{rename.get(k, k): v for k, v in r.items()} for r in rows]


def coerce_types(rows: list[dict], structure: list[str]) -> list[dict]:
    types = {}
    for spec in structure:
        parts = spec.split()
        if len(parts) >= 2:
            types[parts[0]] = parts[1].lower()
    out = []
    for r in rows:
        new = {}
        for k, v in r.items():
            t = types.get(k, "")
            is_numeric = t.startswith(("decimal", "float", "double", "int", "bigint", "smallint", "tinyint"))
            if v is None:
                new[k] = None
                continue
            if v == "":
                # Numeric empty becomes NULL; string-typed empty stays as "" so
                # PK constraints relying on empty-string values (e.g. reasoning_effort)
                # do not collapse to NULL.
                new[k] = None if is_numeric else ""
                continue
            if t.startswith(("decimal", "float", "double")):
                try:
                    new[k] = float(v)
                except ValueError:
                    new[k] = v
            elif t.startswith(("int", "bigint", "smallint", "tinyint")):
                # Coerce boolean strings to 1/0 before int parsing so tinyint
                # columns ("True"/"False"/"true"/"false" in CSV) land correctly.
                # Without this, int("True") raises ValueError, the raw string is
                # sent, and the server stores 0 for every boolean, including True.
                if isinstance(v, str) and v.strip().lower() in ("true", "false"):
                    new[k] = 1 if v.strip().lower() == "true" else 0
                    continue
                try:
                    new[k] = int(v)
                except ValueError:
                    new[k] = v
            else:
                new[k] = v
        out.append(new)
    return out


def string_id(cfg: dict) -> str:
    return cfg.get("benchmark_string_id") or f"b_{cfg['benchmark_id']}"


def cmd_authorize(args, cfg):
    print(authorize(force=args.force))


def cmd_describe(args, cfg):
    body = {"id": cfg["benchmark_id"], "type": cfg["type"]}
    res = call("/benchmark/describe", body)
    print(json.dumps(res, indent=2))


def cmd_validate(args, cfg):
    desc = call("/benchmark/describe", {"id": cfg["benchmark_id"], "type": cfg["type"]})
    if desc.get("status") != "success":
        sys.exit(f"error: describe failed: {desc}")
    structure = desc["data"]["table_structure"]
    cols = [s.split()[0] for s in structure]
    csv_path = Path(cfg["csv"]["path"])
    rows = load_csv(csv_path)
    rows = rename_columns(rows, cfg.get("csv", {}).get("rename", {}))
    if not rows:
        sys.exit(f"error: {csv_path} has no rows")
    local_cols = set(rows[0].keys())
    expected = set(cols)
    missing = expected - local_cols
    extra = local_cols - expected
    if missing:
        print(f"missing local columns: {sorted(missing)}", file=sys.stderr)
    if extra:
        print(f"extra local columns (will be dropped on upload): {sorted(extra)}", file=sys.stderr)
    if missing:
        sys.exit("header mismatch. Fix CSV headers or add [csv.rename] in benchmark.toml.")
    fk_cols = [c for c in cols if "." in c]
    bad = 0
    for col in fk_cols:
        table, field = col.split(".", 1)
        # Server bug: limit=100000 returns only 45 rows (silent overflow).
        # limit=10000 returns all rows for every shared table we have today.
        shared = call("/benchmark/get", {"id": table, "type": "shared", "limit": 10000})
        if shared.get("status") != "success":
            print(f"warn: could not load shared table {table}: {shared}", file=sys.stderr)
            continue
        known = {row.get(field) for row in shared.get("data", []) if row.get(field) is not None}
        local_vals = {r[col] for r in rows if r.get(col)}
        unknown = local_vals - known
        if unknown:
            print(f"unknown {col} ({len(unknown)}): {sorted(unknown)[:10]}", file=sys.stderr)
            bad += 1
    if bad:
        sys.exit(f"{bad} FK column(s) have unresolved values. Ask tech team to add the missing entries.")
    print(f"ok: {len(rows)} rows match the {len(cols)}-column schema; all FK values resolve")


def cmd_upload(args, cfg):
    desc = call("/benchmark/describe", {"id": cfg["benchmark_id"], "type": cfg["type"]})
    if desc.get("status") != "success":
        sys.exit(f"error: describe failed: {desc}")
    structure = desc["data"]["table_structure"]
    expected_cols = {s.split()[0] for s in structure}
    csv_path = Path(cfg["csv"]["path"])
    rows = load_csv(csv_path)
    rows = rename_columns(rows, cfg.get("csv", {}).get("rename", {}))
    rows = coerce_types(rows, structure)
    # Drop any local columns the DB schema does not expect. Forward-looking
    # CSV columns (e.g. cost_usd) should not break the feed.
    if rows and not set(rows[0].keys()).issubset(expected_cols):
        dropped = sorted(set(rows[0].keys()) - expected_cols)
        print(f"dropping {len(dropped)} extra column(s) from payload: {dropped}", file=sys.stderr)
        rows = [{k: v for k, v in r.items() if k in expected_cols} for r in rows]
    body = {
        "id": cfg["benchmark_id"],
        "type": cfg["type"],
        "data": rows,
        "test": bool(args.test),
    }
    res = call("/benchmark/feed", body)
    print(json.dumps(res, indent=2))
    if res.get("status") != "success":
        sys.exit(1)
    inserted = res.get("data", {}).get("insertCount")
    if inserted is not None and inserted != len(rows):
        sys.exit(f"warn: insertCount={inserted} but CSV had {len(rows)} rows")


def cmd_get(args, cfg):
    body = {
        "id": str(cfg["benchmark_id"]),
        "type": cfg["type"],
        "limit": args.limit,
        "test": bool(args.test),
    }
    res = call("/benchmark/get", body)
    print(json.dumps(res, indent=2))


def cmd_assign(args, cfg):
    title = cfg.get("page_title") or ""
    if not title:
        desc = call("/benchmark/describe", {"id": cfg["benchmark_id"], "type": cfg["type"]})
        if desc.get("status") == "success":
            title = desc["data"].get("benchmark_name") or ""
    body = {
        "benchmark_id": string_id(cfg),
        "url": cfg["article_url"],
        "page_title": title,
    }
    res = call("/benchmark/assign", body)
    print(json.dumps(res, indent=2))


def cmd_shared(args, cfg):
    body = {"id": args.id, "type": "shared", "limit": args.limit}
    res = call("/benchmark/get", body)
    print(json.dumps(res, indent=2))


def cmd_shared_tables(args, cfg):
    print(json.dumps(call("/benchmark/shared-tables", {}), indent=2))


def cmd_list(args, cfg):
    print(json.dumps(call("/benchmark/list", {"company_id": args.company_id}), indent=2))


def cmd_top_list(args, cfg):
    body = {"id": cfg["benchmark_id"], "type": cfg["type"]}
    print(json.dumps(call("/benchmark/top-list", body), indent=2))


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("authorize"); sp.add_argument("--force", action="store_true"); sp.set_defaults(func=cmd_authorize, _need_cfg=False)
    sp = sub.add_parser("describe"); sp.set_defaults(func=cmd_describe, _need_cfg=True)
    sp = sub.add_parser("validate"); sp.set_defaults(func=cmd_validate, _need_cfg=True)
    sp = sub.add_parser("upload"); sp.add_argument("--test", action="store_true"); sp.set_defaults(func=cmd_upload, _need_cfg=True)
    sp = sub.add_parser("get"); sp.add_argument("--limit", type=int, default=10); sp.add_argument("--test", action="store_true"); sp.set_defaults(func=cmd_get, _need_cfg=True)
    sp = sub.add_parser("assign"); sp.set_defaults(func=cmd_assign, _need_cfg=True)
    sp = sub.add_parser("shared"); sp.add_argument("--id", required=True); sp.add_argument("--limit", type=int, default=50); sp.set_defaults(func=cmd_shared, _need_cfg=False)
    sp = sub.add_parser("shared-tables"); sp.set_defaults(func=cmd_shared_tables, _need_cfg=False)
    sp = sub.add_parser("list"); sp.add_argument("--company-id", dest="company_id", type=int, required=True); sp.set_defaults(func=cmd_list, _need_cfg=False)
    sp = sub.add_parser("top-list"); sp.set_defaults(func=cmd_top_list, _need_cfg=True)

    args = p.parse_args()
    cfg = load_config() if args._need_cfg else {}
    args.func(args, cfg)


if __name__ == "__main__":
    main()
