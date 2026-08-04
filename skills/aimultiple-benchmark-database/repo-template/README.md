# <benchmark name>

Bitbucket repo for AIMultiple benchmark `b_<id>`. Repo name equals the DB benchmark id.

## What this repo holds

- `start.sh` runs the benchmark and produces `output/runs/run-<UTC>/db-ready.csv` plus `nivo/<chart>.csv` files.
- `upload_to_db.py` pushes `db-ready.csv` into the AIMultiple research database via `/benchmark/feed`.
- `benchmark.toml` holds the DB id, type, article URL, and CSV path.

## Workflow

```bash
export AIMULTIPLE_BENCHMARK_API_KEY=...

./start.sh                              # produces output/runs/run-<UTC>/db-ready.csv
python upload_to_db.py describe         # show the DB schema
python upload_to_db.py validate         # check CSV headers and FK values
python upload_to_db.py upload --test    # dry-feed into the test DB
python upload_to_db.py get --test --limit 5
python upload_to_db.py upload           # prod feed
python upload_to_db.py get --limit 5
python upload_to_db.py assign           # attach article URL
```

Commit `output/runs/run-<UTC>/` so the run is reproducible.

## See also

The upload contract, schema convention, and failure modes are defined in
`skills/aimultiple-benchmark-database/SKILL.md` of the parent workspace.
