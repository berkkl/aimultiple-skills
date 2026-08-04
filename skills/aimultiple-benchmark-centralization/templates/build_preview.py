#!/usr/bin/env python3
"""Generate output/preview.csv and output/db-types-proposal.csv.

Forward both files to the tech team when asking them to create the
b_<id>_results table. preview.csv shows the data shape; db-types-proposal.csv
declares the column types and FK relationships you want.

Fill TYPE_MAP with one entry per CSV column before running. Unmapped columns
default to (decimal(10,5), nullable=true, is_fk=false). The default is wrong
for varchar / int / boolean columns, so map them explicitly.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "output" / "db-ready.csv"
PREVIEW = ROOT / "output" / "preview.csv"
TYPES = ROOT / "output" / "db-types-proposal.csv"

PREVIEW_ROW_COUNT = 3

# Edit this per benchmark. Format:
#   column_name: (proposed_type, nullable, is_fk, notes)
# Example entries:
#   "ai_models.name": ("varchar(64)", False, True, "FK to shared ai_models"),
#   "dataset": ("varchar(64)", False, False, ""),
#   "fold": ("tinyint", False, False, "0-4"),
#   "primary_value": ("decimal(10,5)", True, False, "NULL when status != ok"),
#   "is_fallback": ("tinyint", False, False, "boolean 0/1"),
TYPE_MAP: dict[str, tuple[str, bool, bool, str]] = {
    # fill in
}

DEFAULT_SPEC = ("decimal(10,5)", True, False, "")


def main() -> int:
    if not SRC.exists():
        print(f"error: {SRC} missing. Run scripts/build_db_csv.py first.", file=sys.stderr)
        return 1

    with SRC.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        sample: list[list[str]] = []
        for _ in range(PREVIEW_ROW_COUNT):
            try:
                sample.append(next(reader))
            except StopIteration:
                break

    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    with PREVIEW.open("w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(header)
        w.writerows(sample)

    with TYPES.open("w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(["column_name", "proposed_type", "nullable", "is_fk", "notes"])
        for col in header:
            spec = TYPE_MAP.get(col, DEFAULT_SPEC)
            t, nullable, is_fk, notes = spec
            w.writerow([col, t, str(nullable).lower(), str(is_fk).lower(), notes])

    unmapped = [c for c in header if c not in TYPE_MAP]
    print(f"wrote {len(sample)} preview rows to {PREVIEW.relative_to(ROOT)}")
    print(f"wrote {len(header)} type entries to {TYPES.relative_to(ROOT)}")
    if unmapped:
        print(
            f"warn: {len(unmapped)} columns used default spec {DEFAULT_SPEC}. "
            f"Fill TYPE_MAP for: {unmapped[:10]}{'...' if len(unmapped) > 10 else ''}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
