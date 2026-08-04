#!/usr/bin/env python3
"""Fill base-<chart-id>.json with live DB data and write results-<chart-id>.json.

Skeleton: copy as `nivo/prepare-<chart-id>.py`, then fill in CHART_ID, the
benchmark id, and the field mapping. Do NOT modify the structure of base.json.
Only inject series data into the predefined slots.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NIVO_DIR = ROOT / "nivo"
OUT_DIR = ROOT / "output"

CHART_ID = "<nivo-chart-id>"           # must match the Nivo Chart ID in the Management Panel
BENCHMARK_ID = 0                        # set to the b_<id> integer
API_BASE = os.environ.get(
    "AIMULTIPLE_BENCHMARK_API_BASE",
    "https://research-api.test.v5.aimultiple.com",
)
TOKEN_PATH = Path.home() / ".cache" / "aimultiple-benchmark-token"


def fetch_rows() -> list[dict]:
    token = TOKEN_PATH.read_text().strip()
    body = json.dumps({
        "id": str(BENCHMARK_ID),
        "type": "benchmark",
        "limit": 10000,
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE.rstrip('/')}/benchmark/get",
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.loads(r.read().decode())
    if res.get("status") != "success":
        sys.exit(f"error: /benchmark/get failed: {res}")
    return res.get("data", [])


def inject(base: dict, rows: list[dict]) -> dict:
    """Fill base series with rows. Replace this body per chart."""
    # Example for a bar chart with series keyed by model name:
    #
    # for series in base.get("data", []):
    #     model = series.get("id")
    #     match = next((r for r in rows if r["ai_models.name"] == model), None)
    #     if match:
    #         series["value"] = float(match["primary_value"])
    raise NotImplementedError(
        "Replace this body with the field mapping for this chart."
    )


def main() -> int:
    base_path = NIVO_DIR / f"base-{CHART_ID}.json"
    out_path = OUT_DIR / f"results-{CHART_ID}.json"
    if not base_path.exists():
        sys.exit(f"error: {base_path} missing. Create the design template first.")
    base = json.loads(base_path.read_text())
    rows = fetch_rows()
    results = inject(base, rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2))
    print(f"wrote {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
