#!/usr/bin/env python3
"""Local preflight audit for a benchmark repo.

Run before pushing the init commit. Covers items 1-9 and 13 from the
aimultiple-benchmark-centralization checklist. Items 10 (DB describe)
and 11 (FK validate) need the API key and live in upload_to_db.py.

Exit 0 if all checks pass, 1 otherwise. Prints one line per check.
"""
from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_README_SECTIONS = [
    r"What\s+It\s+Is",
    r"How\s+It\s+Works",
    r"How\s+to\s+Run",
]
REQUIRED_GITIGNORE_ENTRIES = [
    "output/",
    "output_*/",
    "data/",
    "venv/",
    ".venv/",
    "__pycache__/",
    ".env",
    ".DS_Store",
]
NUMERIC_BOOL_STRINGS = {"True", "False", "true", "false"}
NUMERIC_NULL_STRINGS = {"N/A", "n/a", "NA", "null", "None", "NaN", "nan"}

DB_CSV = ROOT / "output" / "db-ready.csv"
PREVIEW_CSV = ROOT / "output" / "preview.csv"
TYPES_CSV = ROOT / "output" / "db-types-proposal.csv"

results: list[tuple[bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    results.append((ok, label))
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label}" + (f" — {detail}" if detail else ""))


def check_folder_id() -> None:
    folder = ROOT.name
    cfg_path = ROOT / "benchmark.toml"
    if not cfg_path.exists():
        check("benchmark.toml present", False, f"missing at {cfg_path}")
        return
    cfg = tomllib.loads(cfg_path.read_text())
    bid = cfg.get("benchmark_id")
    ok = bool(re.fullmatch(r"b_\d+", folder)) and folder == f"b_{bid}"
    check(
        "folder name matches benchmark.toml id",
        ok,
        f"folder={folder} benchmark_id={bid}",
    )


def check_readme_sections() -> None:
    readme = ROOT / "README.md"
    if not readme.exists():
        check("README.md exists", False)
        return
    body = readme.read_text()
    missing = [
        s for s in REQUIRED_README_SECTIONS
        if not re.search(s, body, re.IGNORECASE)
    ]
    check("README has required sections", not missing, f"missing: {missing}")


def check_methodology() -> None:
    p = ROOT / "methodology.md"
    check("methodology.md exists", p.exists() and p.stat().st_size > 0)


def check_gitignore() -> None:
    p = ROOT / ".gitignore"
    if not p.exists():
        check(".gitignore exists", False)
        return
    body = p.read_text()
    missing = [e for e in REQUIRED_GITIGNORE_ENTRIES if e not in body]
    check(".gitignore has required entries", not missing, f"missing: {missing}")


def check_upload_client() -> None:
    p = ROOT / "upload_to_db.py"
    check("upload_to_db.py present", p.exists())


def check_db_csv_idempotent() -> None:
    builder = ROOT / "scripts" / "build_db_csv.py"
    if not builder.exists():
        check("scripts/build_db_csv.py exists", False)
        return
    if not DB_CSV.exists():
        check(
            "output/db-ready.csv exists",
            False,
            "run scripts/build_db_csv.py",
        )
        return
    h1 = hashlib.md5(DB_CSV.read_bytes()).hexdigest()
    res = subprocess.run(
        [sys.executable, str(builder)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    if res.returncode != 0:
        check("build_db_csv.py runs cleanly", False, res.stderr.strip()[:200])
        return
    h2 = hashlib.md5(DB_CSV.read_bytes()).hexdigest()
    check("db-ready.csv is idempotent", h1 == h2, f"md5 before={h1} after={h2}")


def check_preview() -> None:
    builder = ROOT / "scripts" / "build_preview.py"
    if not builder.exists():
        check("scripts/build_preview.py exists", False)
        return
    if not PREVIEW_CSV.exists() or not TYPES_CSV.exists():
        check(
            "preview.csv + db-types-proposal.csv present",
            False,
            "run scripts/build_preview.py",
        )
        return
    check("preview.csv + db-types-proposal.csv present", True)


def check_csv_lint() -> None:
    if not DB_CSV.exists() or not TYPES_CSV.exists():
        check("CSV boolean / null lint", False, "missing inputs")
        return
    with TYPES_CSV.open() as f:
        types = {row["column_name"]: row["proposed_type"] for row in csv.DictReader(f)}
    numeric_types = ("tinyint", "smallint", "int", "bigint", "decimal", "float", "double")
    bad: list[str] = []
    with DB_CSV.open() as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=2):
            for col, val in row.items():
                t = types.get(col, "")
                if not any(t.lower().startswith(x) for x in numeric_types):
                    continue
                if val in NUMERIC_BOOL_STRINGS:
                    bad.append(f"L{i} {col}={val!r} (boolean string in numeric col)")
                if val in NUMERIC_NULL_STRINGS:
                    bad.append(f"L{i} {col}={val!r} (null-sentinel in numeric col; use empty)")
                if len(bad) > 5:
                    break
            if len(bad) > 5:
                break
    check("CSV boolean / null lint", not bad, "; ".join(bad[:5]))


def check_git_add_dryrun() -> None:
    try:
        res = subprocess.run(
            ["git", "add", "--dry-run", str(ROOT)],
            capture_output=True,
            text=True,
            cwd=str(ROOT.parent),
        )
    except FileNotFoundError:
        check("git add --dry-run is clean", False, "git not available")
        return
    leaks = [
        line for line in res.stdout.splitlines()
        if re.search(r"(output/|output_|/data/|/data_cache/|/venv|/\.venv|__pycache__|/charts/|PLAN\.md|AGENTS?\.md|CLAUDE\.md)", line)
    ]
    check("git add --dry-run is clean", not leaks, f"leaks: {leaks[:3]}")


def main() -> int:
    check_folder_id()
    check_readme_sections()
    check_methodology()
    check_gitignore()
    check_upload_client()
    check_db_csv_idempotent()
    check_preview()
    check_csv_lint()
    check_git_add_dryrun()

    failed = sum(1 for ok, _ in results if not ok)
    total = len(results)
    print(f"\n{total - failed}/{total} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
