#!/usr/bin/env bash
set -euo pipefail

# start.sh - entry point for this benchmark.
#
# Replace the body with your benchmark harness call. The output contract is:
#
#   output/runs/run-<UTC>/db-ready.csv     canonical DB feed
#   output/runs/run-<UTC>/nivo/<chart>.csv chart CSVs for the article
#
# Example (adapted from agentic-llm):
#   ROOT="$(cd "$(dirname "$0")" && pwd)"
#   exec python3 "$ROOT/scripts/orchestrate/main.py" --root "$ROOT" "$@"

echo "start.sh stub. Edit me to call your benchmark harness." >&2
exit 1
