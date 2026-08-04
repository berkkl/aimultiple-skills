---
name: aimultiple-python-research-standards
description: |
  Enforces Python standards for AIMultiple analysis and benchmarking code. Use for scripts, parsers, benchmark runners, cost models, and research pipelines. Without this skill, experiments become non-reproducible and vendor comparisons lose credibility.
---

# Python Research Standards

## Activation

Use this skill for any Python implementation in this workspace.

## Verified Tool Baseline

- Python: 3.14.3
- `uv`: 0.10.9
- `pytest`: 9.0.2
- `ruff`: 0.15.5
- `pandas`: 3.0.1
- `pydantic`: 2.12.5
- `duckdb`: 1.5.0

## Core Rules

1. Use Python 3.14 syntax and typing features.
2. Manage environments and dependency locking with `uv`.
3. Type annotate all public functions.
4. Parse structured data with Pydantic models before analysis.
5. Keep raw vendor payloads immutable and write normalized tables separately.
6. Every benchmark run must emit deterministic metadata: timestamp, seed, and source set.
7. Use `pytest` for scoring and parser logic.
8. Run `ruff check` and `ruff format` before finalizing changes.
9. Never hide parse failures. Raise explicit exceptions with vendor and field context.
10. Time-sensitive metrics must include explicit timezone.
11. No network calls inside scoring functions. Inputs must be local artifacts.
12. Keep scripts idempotent. Re-running should not duplicate rows.

## Performance Budgets

- Parse 100 vendor rows in under 2 seconds on a local laptop.
- Build one scorecard table in under 5 seconds.
- Keep routine analyses under 512 MB of memory.

## Error Scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Schema drift in vendor data | Pydantic validation error | Version the schema and add a transformer |
| Non-deterministic ranking | Repeated run hash mismatch | Fix seed and sort keys |
| Hidden null inflation | Null rate jumps more than 10% | Fail the run and inspect the parser |

## Integration Points

- Uses `aimultiple-source-validation` for upstream evidence quality.
- Implements designs from `aimultiple-benchmark-methodology-design`.
