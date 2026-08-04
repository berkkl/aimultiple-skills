---
name: aimultiple-benchmark-centralization
description: |
  Standard project structure, README sections, .gitignore, DB-ready CSV shape, preview CSV for tech-team review, boolean lint, and the Nivo chart pipeline for benchmarks under team-benchmarks/. Activates when creating, migrating, or auditing a benchmark folder. Without this skill, repos drift in folder layout, CSVs ship with True/False strings, charts get hand-edited, and tech team gets ambiguous schema specs.
---

# AIMultiple Benchmark Centralization Standard

## Scope vs other skills

This skill covers project structure, audit checklist, preview generation, and the chart pipeline. For the API contract (describe / feed / get / assign, token caching, `upload_to_db.py`), use [[aimultiple-benchmark-database]]. For spec validation before a benchmark is implemented, use [[aimultiple-benchmark-preflight-check]].

The three skills layer:

1. Preflight check validates the design before code.
2. Centralization (this skill) validates the repo + CSV + charts before push.
3. Database skill handles the API push itself.

## Folder layout

Every benchmark lives at `team-benchmarks/b_<id>/`. The id starts at 100, must be unique across all benchmarks, and matches the DB table names. The prefix is one of `b_` (benchmark results), `p_` (price), `d_` (general data).

```
b_<id>/
├── README.md                 # required, see "README" below
├── methodology.md            # what is tested, scoring, caveats
├── .gitignore                # verbatim from aimultiple-benchmark-database/repo-template/
├── benchmark.toml            # id, type, article_url, csv path
├── main.py | main.js         # standard entry point
├── requirements.txt | package.json
├── upload_to_db.py           # copy from repo-template/, do not fork
├── src/                      # benchmark logic
├── config/                   # dataset specs, model lists, prompts
├── scripts/
│   ├── build_db_csv.py       # produces output/db-ready.csv
│   ├── build_preview.py      # produces output/preview.csv + output/db-types-proposal.csv
│   └── audit.py              # runs the local preflight checklist below
├── nivo/
│   ├── base-<chart-id>.json  # visualization structure, no data
│   └── prepare-<chart-id>.py # fills base with values from the DB
└── output/                   # gitignored
    ├── db-ready.csv
    ├── preview.csv
    ├── db-types-proposal.csv
    └── results-<chart-id>.json
```

`chart-id` matches the Nivo Chart ID used by the Management Panel.

## DB table naming

Per data engineering convention, each benchmark id maps to one or two tables:

- `b_<id>_results` — actual data. Required for every benchmark. Schema varies per benchmark.
- `b_<id>_info` — metadata: field-level relations, lookup fields, validation rules. Optional. Used when FK behavior needs explicit declaration.

`_info` fields when present: `field_name`, `relation_table`, `relation_field`, `relation_lookup`, `relation_lookup_type`.

Tech team creates both tables. The benchmark repo does not own the table definitions, only the row data.

## README required sections

Per Confluence Code Development Standards, every README has:

1. **What It Is** — one paragraph on what is being tested.
2. **How It Works** — files, dataset/task definitions, scoring.
3. **How to Run** — install steps, run command, expected outputs.
4. **DB benchmark id and article URL** — `b_<id>`, link to the published article.

Skip generic project descriptions. The README is for someone reproducing the run on a fresh machine.

## Standard entry file

- Python benchmarks: `main.py`.
- Node.js benchmarks: `main.js`.

This lets automation tools run every benchmark with the same command. If the benchmark needs orchestration across multiple steps, `main.py` is the dispatcher that calls into `src/`.

## DB-ready CSV shape

One row per provider/model. Row key is `ai_models.name` or `companies.name`. Per-fold detail collapses into mean/std columns, not extra rows. See [[feedback-benchmark-db-row-shape]] for the rule and why.

Long per-event rows are acceptable only when the cell itself is the natural unit (one inference call per row in a latency benchmark, one URL per row in a web-scraping benchmark).

Use the language's CSV writer with RFC 4180 escaping. Python `csv.writer`, Node `csv-stringify`, PHP `fputcsv`. Never hand-concatenate strings.

## Preview CSV for tech-team review

Before asking tech team to create the `_results` table, produce two sidecar files:

- `output/preview.csv` — first 3 rows of `db-ready.csv`. Shows what the data looks like.
- `output/db-types-proposal.csv` — one row per CSV column with proposed type, nullability, and FK status. Columns: `column_name`, `proposed_type`, `nullable`, `is_fk`, `notes`.

Forward both to the tech team in one message. They use the types proposal to define the `_results` schema and the `_info` relations.

Template `scripts/build_preview.py` lives at `templates/build_preview.py` in this skill. Copy it into the benchmark repo, fill in the `TYPE_MAP`, and run.

## Boolean lint

CSVs that ship `True`, `False`, `true`, `false` in numeric columns get stored as 0 by the DB. The patched `upload_to_db.py` coerces strings to 1/0, but the source CSV should already be clean so the file itself is correct on disk and in git history.

The lint catches:

- Any cell that is exactly `True`, `False`, `true`, or `false` in a column whose proposed type is `tinyint`, `int`, or `decimal`.
- Any cell that is `N/A`, `null`, `None`, or `nan` in a numeric column. Use empty string for NULL.
- Any header that mismatches the DB schema after the `csv.rename` map is applied (caught by `upload_to_db.py validate`, included here so the repo stays clean offline).

`scripts/audit.py` runs the lint. Template at `templates/audit.py`.

## .gitignore

Use the template from `aimultiple-benchmark-database/repo-template/.gitignore` verbatim. Required exclusions:

- `output/`, `output_*/`, `workspaces/`, `backup/`, `data/`, `data_cache/`, `charts/`, `raw-batches/`
- `venv/`, `venv*/`, `.venv/`, `__pycache__/`, `node_modules/`, `*/node_modules/`
- `*.parquet`, `*.pickle`, `*.pkl`
- `PLAN.md`, `AGENTS.md`, `AGENT.md`, `CLAUDE.md` (agentic context, not part of the runnable harness)
- `.env`, `.env.*`, `*.log`
- `.DS_Store`

Sanity-check before commit:

```
git add --dry-run b_<id>/
```

If any path under `output*/`, `data/`, `venv/`, `__pycache__/` shows up, the gitignore is wrong.

## Nivo chart pipeline

The Management Panel renders charts from `results-<chart-id>.json`. That file is the combination of a design-only template and live DB data.

Three files per chart:

- `nivo/base-<chart-id>.json` — visualization structure: axes, labels, series shapes. No benchmark values. `chart-id` is the Nivo Chart ID used by the panel.
- `nivo/prepare-<chart-id>.py` — reads `base-<chart-id>.json`, fetches benchmark data from `/benchmark/get`, fills in series values, writes `output/results-<chart-id>.json`. Does NOT mutate the structure.
- `output/results-<chart-id>.json` — gitignored. Uploaded to the Management Panel.

Design rule: `base-<chart-id>.json` stays strict-structure so new providers or new datasets fold in without breaking the rendered chart. When a benchmark adds a model, `prepare` re-pulls the DB and the new series appears without anyone editing `base`. When a benchmark adds a dataset column, `base` may need a new axis tick — that is the only time the design changes.

Multiple chart-ids per benchmark are fine. One base + one prepare + one results per chart-id.

## Preflight checklist

Run before pushing the init commit. `scripts/audit.py` automates items 1-9 and 13.

1. Repo folder name is `b_<id>` and matches `benchmark.toml`'s `benchmark_id`.
2. `README.md` has the four required sections.
3. `methodology.md` exists and explains what is being tested.
4. `.gitignore` is the template verbatim.
5. `benchmark.toml` has `benchmark_id`, `type`, `article_url`, `csv.path`.
6. `upload_to_db.py` matches the current copy from the skill template (check `md5` against `aimultiple-benchmark-database/repo-template/upload_to_db.py`).
7. `scripts/build_db_csv.py` produces `output/db-ready.csv` and is idempotent (md5 stable on rerun).
8. `scripts/build_preview.py` produces `output/preview.csv` + `output/db-types-proposal.csv`.
9. Boolean lint passes (no `True`/`False` strings in numeric columns, no `N/A` in numeric columns).
10. `python upload_to_db.py describe` succeeds (table exists), OR `preview.csv` + `db-types-proposal.csv` are ready to forward to tech team.
11. All FK values in the CSV resolve in the shared table (`python upload_to_db.py validate`).
12. Every model/provider used in the CSV exists in the relevant shared table. If not, list the missing entries for the tech team to add.
13. `git add --dry-run b_<id>/` shows no data, output, venv, cache, or agentic-md paths.
14. For every chart in the published article: `nivo/base-<chart-id>.json` and `nivo/prepare-<chart-id>.py` exist. `prepare` runs end-to-end and writes `output/results-<chart-id>.json`.

## Procedure

1. Build the source data with the benchmark harness. Save fold-level raws under `output_<run>/`.
2. Aggregate into `output/db-ready.csv` via `scripts/build_db_csv.py`.
3. Generate `output/preview.csv` + `output/db-types-proposal.csv` via `scripts/build_preview.py`.
4. Run `python scripts/audit.py`. Fix anything it flags.
5. If the DB table for this id does not exist: forward `preview.csv` + `db-types-proposal.csv` to tech team. Wait for table creation. Forward any missing shared-table entries (models, companies) at the same time.
6. Once the table exists: `validate → upload → get → assign` via `upload_to_db.py`. See [[aimultiple-benchmark-database]].
7. Build `output/results-<chart-id>.json` for every chart via `nivo/prepare-<chart-id>.py`. Upload to Management Panel.
8. Commit as `<benchmark-slug> init`. No Claude attribution. Push to `aimultiplev4/team-benchmarks` main.

## Migrating an existing benchmark folder

Copy ONLY what is needed to reproduce the run:

1. Source scripts (`src/`, `scripts/` except `__pycache__/`)
2. Configs (`config/`, `*.yaml`)
3. Task definitions (`TASKS/`, dataset specs)
4. `README.md` (rewrite to point at the article URL and DB benchmark id)
5. `.gitignore` (template version)
6. `methodology.md`
7. Top-level entry points (`main.py`, `start.sh`, `health.sh`)

Do NOT copy:

- Past run outputs (`output/`, `output_*/`, `workspaces/`, `backup/`)
- Generated data CSVs (`data/`, `charts/`, `raw-batches/`)
- venv directories or `__pycache__`
- Planning markdown (`PLAN.md`) or agent context files

After copying, run `git add --dry-run b_<id>/` and verify no data, output, or venv paths slipped in. Then commit as `<benchmark-slug> init`.

## Templates

- `templates/build_preview.py` — preview CSV + types proposal generator.
- `templates/audit.py` — local preflight runner.
- `templates/README.md` — README skeleton with the four required sections.
- `templates/prepare-chart.py` — Nivo prepare-script skeleton.

Copy into the benchmark repo, do not symlink.

## Integration with existing skills

- [[aimultiple-benchmark-database]] — API contract, upload procedure, repo-template gitignore + benchmark.toml + upload_to_db.py.
- [[aimultiple-benchmark-preflight-check]] — pre-implementation spec validation.
- [[feedback-benchmark-db-row-shape]] — why one row per provider with mean/std columns.
- [[project-benchmark-centralization]] — overall centralization context.
