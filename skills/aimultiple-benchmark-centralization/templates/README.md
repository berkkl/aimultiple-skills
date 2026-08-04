# <benchmark name>

`b_<id>` in the AIMultiple research DB. Article: https://aimultiple.com/<slug>.

## What It Is

One paragraph on what is being tested. Include the providers / models, the
dataset(s), and the metric being optimized for. State the question this
benchmark answers in one sentence.

## How It Works

- Dataset(s): <files / sources / sample counts>
- Scoring: <metric definitions, primary vs secondary>
- Code layout: `src/` holds the runner, `config/` holds the dataset and model lists, `scripts/` holds the aggregation + audit helpers.
- Output: per-fold raws under `output_<run>/`, aggregated `output/db-ready.csv` produced by `scripts/build_db_csv.py`.

## How to Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1. run the benchmark (writes output_<run>/results_*.csv)
python main.py

# 2. aggregate into the canonical DB-ready CSV
python scripts/build_db_csv.py

# 3. generate the preview pair for tech team
python scripts/build_preview.py

# 4. local preflight
python scripts/audit.py

# 5. push to the research DB (requires AIMULTIPLE_BENCHMARK_API_KEY)
export AIMULTIPLE_BENCHMARK_API_KEY=...
python upload_to_db.py describe
python upload_to_db.py validate
python upload_to_db.py upload
python upload_to_db.py get --limit 5
python upload_to_db.py assign
```

## DB benchmark id

- benchmark_id: <int>
- tables: `b_<id>_results`, optionally `b_<id>_info`
- article_url: https://aimultiple.com/<slug>

## See also

- Upload contract: `skills/aimultiple-benchmark-database/SKILL.md`
- Centralization standard: `skills/aimultiple-benchmark-centralization/SKILL.md`
