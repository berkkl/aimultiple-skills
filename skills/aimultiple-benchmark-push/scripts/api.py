#!/usr/bin/env python3
"""research-api client for the benchmark-push skill. Stdlib only, no deps.

Nothing here is hardcoded. Key: $AIMULTIPLE_BENCHMARK_API_KEY (AIMultiple convention, same env
var upload_to_db.py uses), falling back to $BENCHMARK_API_KEY or $DATABASES/benchmark_cent/.env
(Ekrem's layout). Base URL: $AIMULTIPLE_BENCHMARK_API_BASE, then $RESEARCH_API_BASE.

CLI:
    python api.py preflight                 # K1-K4, including the schema-management probe
    python api.py prompt [-o prompt.md]     # fresh schema-design prompt
    python api.py describe <num> <type>     # table contract for feed
    python api.py get <num> <type> [limit]  # rows
    python api.py shared <table> [limit]    # a shared lookup table
    python api.py all [search]              # registry
    python api.py urls <slug>               # a record's published urls
    python api.py post <endpoint> <file>    # raw POST of a JSON file (writes!)
"""
from __future__ import annotations
import json, os, sys, urllib.request, urllib.error
from pathlib import Path

DEFAULT_BASE = "https://research-api.test.v5.aimultiple.com"


def base_url() -> str:
    # K3: a trailing slash produces "//benchmark/x" which 404s. Always strip it.
    return (os.environ.get("AIMULTIPLE_BENCHMARK_API_BASE")
            or os.environ.get("RESEARCH_API_BASE", DEFAULT_BASE)).rstrip("/")


def api_key() -> str:
    for var in ("AIMULTIPLE_BENCHMARK_API_KEY", "BENCHMARK_API_KEY"):
        if os.environ.get(var):
            return os.environ[var].strip()
    root = Path(os.environ.get("DATABASES", str(Path.home() / "Developer" / "databases")))
    env = root / "benchmark_cent" / ".env"
    if not env.exists():
        sys.exit("API anahtarı bulunamadı: AIMULTIPLE_BENCHMARK_API_KEY (veya BENCHMARK_API_KEY) "
                 f"env'de yok ve {env} de yok")
    for line in env.read_text().splitlines():
        if line.startswith("BENCHMARK_API_KEY="):
            return line.split("=", 1)[1].strip().strip("\"'")
    sys.exit(f"{env} içinde BENCHMARK_API_KEY yok")


_token = None


def token(refresh: bool = False) -> str:
    global _token
    if _token and not refresh:
        return _token
    req = urllib.request.Request(f"{base_url()}/benchmark/authorize",
                                 headers={"Api-Key": api_key()})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    if not d.get("token"):
        sys.exit(f"authorize başarısız: {d}")
    _token = d["token"]
    return _token


def call(endpoint: str, payload: dict | None = None, method: str = "POST", raw: bool = False):
    """POST (or GET) a benchmark endpoint. Returns the parsed body, error bodies included."""
    url = f"{base_url()}/benchmark/{endpoint.lstrip('/')}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token()}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            body = r.read()
    except urllib.error.HTTPError as e:          # error bodies carry the real message
        body = e.read()
    if raw:
        return body.decode("utf-8", "replace")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"status": "error", "errors": [body.decode("utf-8", "replace")[:2000]]}


def rows(payload_result):
    """/benchmark/get returns {status,data,pagination}; older shapes return a bare list."""
    if isinstance(payload_result, list):
        return payload_result
    return payload_result.get("data", [])


def ok(d) -> bool:
    return isinstance(d, dict) and d.get("status") == "success"


def preflight() -> bool:
    """K1-K4. Writes nothing. Returns True when the key may create tables."""
    print(f"K3 base URL      : {base_url()}")
    try:
        t = token()
    except Exception as e:
        print(f"K1/K4 authorize  : ✗ {e}"); return False
    print(f"K1/K4 token      : ✓ ({t[:12]}...)")
    # K2: valid-format but nonexistent slug. Nothing is written either way.
    d = call("table/create", {"benchmark_id": "b_999", "dry_run": True,
             "table": {"comment": "probe", "columns": [
                 {"name": "probe_value", "type": "int", "nullable": True}]}})
    errs = " ".join(d.get("errors", [])) if isinstance(d, dict) else str(d)
    if "schema management not allowed" in errs:
        print("K2 şema yetkisi  : ✗ KAPALI — 'schema management not allowed for this api key'")
        print("                   DUR. Yetkiyi iste; anahtarın kendisini mesaja yapıştırma.")
        return False
    if "not found" in errs:
        print("K2 şema yetkisi  : ✓ AÇIK (probe 'benchmark b_999 not found' ile döndü)")
        return True
    print(f"K2 şema yetkisi  : ? beklenmedik cevap: {json.dumps(d, ensure_ascii=False)[:300]}")
    return False


def _main(argv):
    if not argv:
        print(__doc__); return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "preflight":
        return 0 if preflight() else 1
    if cmd == "prompt":
        out = rest[1] if len(rest) > 1 and rest[0] == "-o" else None
        url = f"{base_url()}/benchmark/schema-prompt?format=raw"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token()}"})
        with urllib.request.urlopen(req, timeout=60) as r:
            text = r.read().decode()
        (Path(out).write_text(text) if out else sys.stdout.write(text))
        if out: print(f"{len(text.encode())} bayt ({len(text)} karakter) -> {out}")
        return 0
    if cmd == "describe":
        print(json.dumps(call("describe", {"id": rest[0], "type": rest[1]}), ensure_ascii=False, indent=1)); return 0
    if cmd == "get":
        lim = int(rest[2]) if len(rest) > 2 else 10000
        print(json.dumps(call("get", {"id": rest[0], "type": rest[1], "limit": lim}), ensure_ascii=False, indent=1)); return 0
    if cmd == "shared":
        lim = int(rest[1]) if len(rest) > 1 else 5000
        print(json.dumps(call("get", {"id": rest[0], "type": "shared", "limit": lim}), ensure_ascii=False, indent=1)); return 0
    if cmd == "all":
        p = {"status": "all", "limit": 200}
        if rest: p["search"] = rest[0]
        print(json.dumps(call("all", p), ensure_ascii=False, indent=1)); return 0
    if cmd == "urls":
        print(json.dumps(call("urls", {"benchmark_id": rest[0]}), ensure_ascii=False, indent=1)); return 0
    if cmd == "post":
        print(json.dumps(call(rest[0], json.load(open(rest[1]))), ensure_ascii=False, indent=1)); return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
