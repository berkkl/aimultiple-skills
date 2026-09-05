---
name: aimultiple-benchmark-database
description: |
  Defines how to push benchmark results into the AIMultiple research database via the /benchmark API and how to structure a Bitbucket repo per benchmark. Activates when uploading benchmark data, creating a new benchmark repo, or migrating an existing benchmark into the centralized DB. Without this skill, results stay in ad-hoc CSVs with no fixed schema and no link to the published article.
---

# AIMultiple Benchmark Database Upload

## Convention

One Bitbucket repo per benchmark. Repo name equals the benchmark id (integer in DB, prefixed `b_<id>` in URL-attaching contexts).

Articles that contain more than one benchmark get more than one repo. `agentic-llm/` currently holds two benchmarks under one folder; it will split into two repos when migrated.

Each repo emits one canonical DB-ready CSV plus a `nivo/` directory of chart CSVs. The chart CSVs feed the published article. The DB CSV feeds the new research DB.

## Who owns the id and the table (changed 2026-08-24)

**We take the benchmark id in Houston ourselves, register the benchmark there, and push the data
ourselves.** Berkk, 2026-08-24, on the move to the new system. The old flow, requesting an id and a
table from the tech team and waiting, no longer applies to new benchmarks.

Record fields and their rules are in [[aimultiple-benchmark-centralization]]. Two consequences here:

- `POST /benchmark/assign` writes `article_url` and `page_title`, but a **stale URL title cannot be
  fixed through the API**: it is corrected by emptying the field in Houston and saving, after which
  the system refills it. Do not assume `assign` repaired a title; check the record.
- **CONFIRMED 2026-09-05 (Confluence + OpenAPI):** the table is created by us, in three calls:
  `POST /benchmark/create` opens the record and returns the slug (`b_NNN`, server-allocated, cannot be
  chosen); `GET /benchmark/schema-prompt?format=raw` returns the prompt that turns a plain description
  into the table JSON (fetch it fresh every time, the type allowlist and relation targets are filled at
  request time); `POST /benchmark/table/create` with that JSON plus `benchmark_id`, first with
  `dry_run:true`, then for real. The API key needs schema-management permission (probe: a `table/create`
  dry run on a nonexistent slug must answer "not found", not "schema management not allowed").
  **The full procedure, the measured server traps and the feed safety ladder live in
  [[aimultiple-benchmark-push]]**; this skill keeps the contract and `upload_to_db.py` for the repos
  that already have tables. The preview-CSV handoff to the tech team is retired.

## API surface

Base URL: `https://research-api.test.v5.aimultiple.com` (test env). Override with `AIMULTIPLE_BENCHMARK_API_BASE`.

| Endpoint | Use |
|---|---|
| GET /benchmark/authorize       | Trade `Api-Key` header for `Authorization: Bearer <token>`. |
| POST /benchmark/describe       | Returns `table_structure` and `example_input_data`. Run before every feed. |
| POST /benchmark/feed           | Insert rows. `test:true` writes to a test DB. Returns `insertCount`. |
| POST /benchmark/get            | Read back to confirm a feed landed. |
| POST /benchmark/assign         | Attach `article_url` and `page_title` to a benchmark id (string form `b_<id>`). |
| POST /benchmark/shared-tables  | List shared relational tables. |
| POST /benchmark/list           | Benchmarks owned by `company_id`. |
| POST /benchmark/top-list       | Leaderboard projection. |
| POST /benchmark/create         | Register a benchmark (name, description, responsible, type, urls[]). Returns the slug. Record only, no table. |
| GET /benchmark/schema-prompt   | The table-design prompt (`?format=raw`). Re-fetch for every new table. |
| POST /benchmark/table/create   | Create `<slug>_results` (+ `_info`, aux tables) from the prompt's JSON. `dry_run:true` first. Needs schema-management on the key. |
| POST /benchmark/table/update   | Declarative: the payload is the whole table; a missing column is a drop request (blocked unless `allow_drop:true`); non-additive changes back up to `bak_<table>_<ts>` first. `indexes` omitted = untouched, `[]` = drop all. |
| POST /benchmark/all            | The registry itself (search over name/slug/responsible/url, `status: active|passive|all`). Use it to find existing records before taking a new id. |
| POST /benchmark/urls           | Pages a benchmark is published on. |
| POST /benchmark/unassign       | Remove a published URL (row kept, marked removed). |
| POST /benchmark/update         | Edit name/description/responsible/status/downloadble/list_query. `status:0` = outdated. Slug and id never change. |

Feed has two newer options: `data_version` per row (decimal, defaults to 1; the only way to supersede wrong rows, since there is no delete) and `autoCreateRelation` (auto-creates unknown lookup values as `status=2` rows in the shared table; **keep it false**, resolve names first). Feed is atomic per call: a failed batch writes nothing.

`type` is `benchmark` for measurements, `price` for price indexes, `data` for vendor lists and market maps. It fixes the slug prefix (`b_`, `p_`, `d_`) and can never be changed afterwards, so choose it at `create` time.

`id` is integer for `describe`, `feed`, `top-list`. It is a string for `get` (the integer as a string, or a shared table name like `"companies"`). It is `b_<int>` for `assign`. `upload_to_db.py` handles the casts.

## Schema convention

Columns of the form `<shared>.<field>` in the `describe` output (e.g. `companies.name`, `ai_models.name`, `gpu_interfaces.code`) are foreign keys. The value in the CSV must already exist in that shared table. Resolve by calling `POST /benchmark/get {id: "<shared>", type: "shared"}`.

If a company or model is missing from the shared table, ask the tech team to add it. Do not feed orphan rows.

Shared tables today: `companies, company_types, company_benchmarks, benchmark_urls, ai_models, ai_code_tools, gpus, gpu_interfaces, gpu_prices, mcp_servers, proxy_types, scraper_types`.

## Required inputs

1. A populated `benchmark.toml` in the repo:
   - `benchmark_id` (int)
   - `article_url`, `page_title`
   - `csv.path` (canonical DB-ready CSV path inside the repo)
2. The DB-ready CSV with column headers matching the `describe` output.
3. `AIMULTIPLE_BENCHMARK_API_KEY` set in env. Never commit the key.

## Pre-push transforms the CSV must already have applied

The `upload_to_db.py` client handles boolean and int coercion automatically, but the input CSV must be normalized in these ways first:

1. **Boolean columns.** Source CSVs often store `True`/`False` (Pandas, Python) or `true`/`false` (JSON). The client converts these to `1`/`0` for tinyint columns. If you bypass the client, do this transform manually — the server stores `0` for any unparseable string in a tinyint, silently corrupting `True` values.

2. **FK columns (`<shared>.<field>` format).** The CSV header must match the FK column name exactly (e.g. `ai_models.name`, not `model`). Use `[csv.rename]` in `benchmark.toml` if the source uses a different header. The cell values must already exist in the shared table — confirm with `python upload_to_db.py shared --id <table> --limit 10000` and grep for your values.

3. **Model name normalization** (for `ai_models.name` specifically):
   - Strip provider prefixes: `openrouter/anthropic/claude-sonnet-4.6` → `claude-sonnet-4.6`, `google/gemini-3-pro-preview` → `gemini-3-pro-preview`.
   - Strip snapshot suffixes: `claude-opus-4-5-20251101` → `claude-opus-4.5` (verify the unsuffixed name exists in `ai_models` first).
   - Resolve placeholder values like `default` by reading the benchmark's own agents/models config (e.g. `agents.yaml` declares `default_model` per agent).
   - If a model is genuinely missing from `ai_models`, ping Vedat to add it (Houston benchmarks → ai_models). Do not feed orphan rows.

4. **RFC 4180 CSV escaping.** If you write the source CSV by hand-concatenating strings, embedded `"`, `,`, or `\n` in text fields will misalign columns on read. Always use the language's CSV writer (Python `csv.writer`, PHP `fputcsv`, Node `csv-stringify`). Escape internal quotes by doubling (`""`), never with backslash (`\"`).

## Procedure (run from inside the repo)

Two cases. **A table already exists** (b_327, b_328, b_329 and every repo with a `benchmark.toml`): the
steps below with `upload_to_db.py`. **A new benchmark with no table yet:** run [[aimultiple-benchmark-push]]
instead (record, prompt, `table/create` dry run, feed ladder); come back here only for the contract.
Either way, before any feed: `get` first, feed has no idempotency.

```bash
export AIMULTIPLE_BENCHMARK_API_KEY=...

# 1. Pull the table contract from the DB.
python upload_to_db.py describe

# 2. Verify local CSV headers and that FK values resolve.
python upload_to_db.py validate

# 2b. MANDATORY before any feed: check the table is empty (or contains exactly
# what you expect). feed has no idempotency and no delete endpoint; tech team
# sometimes seeds the table with the CSV you sent them for schema review.
# If rows already exist, STOP and reconcile before feeding (b_238 got duplicated this way).
python upload_to_db.py get --limit 100

# 3. Dry-feed into the test DB and read it back.
python upload_to_db.py upload --test
python upload_to_db.py get --test --limit 5

# 4. Prod feed. Confirm insertCount matches CSV row count.
python upload_to_db.py upload
python upload_to_db.py get --limit 5

# 5. Attach the live article URL.
python upload_to_db.py assign
```

`upload_to_db.py` caches the bearer token to `~/.cache/aimultiple-benchmark-token` and re-authorizes automatically when the token is rejected.

## Failure modes & server gotchas

- **401 on any non-authorize call:** token expired. Re-run any subcommand; the client re-authorizes automatically.
- **`Invalid benchmark id or type`:** the id does not exist in the DB. Register it with `POST /benchmark/create` (see the ownership section); an id that exists in the registry but has no table still fails here until `table/create` has run.
- **`insertCount` less than CSV row count:** rows silently rejected. Re-describe and diff headers. FK mismatches are the usual cause.
- **522 or unexpected 301:** base URL is wrong. Confirm `AIMULTIPLE_BENCHMARK_API_BASE`.
- **DNS works but Cloudflare 522:** the test environment is down; check with tech team before retrying.
- **Cloudflare 403 "Request forbidden by administrative rules":** WAF rate-limit triggered by rapid API calls (~15 in a minute, e.g. during a wipe + reupload cycle). Wait several minutes or connect to VPN. Hits every endpoint including `/authorize`.
- **`--test` mode broken on server:** returns `Database connection [new_benchmarks_test] not configured`. Push directly without `--test`; the test env URL already targets the test DB. Skip steps 3 in the Procedure above and go straight to step 4.
- **`limit=100000` server bug:** `/benchmark/get` with `limit=100000` silently returns only 45 rows (likely integer overflow). The client uses `limit=10000` in `validate` to work around this. If you hand-call `/get` for shared tables, use `limit=10000` not `100000`.
- **No idempotency on `/benchmark/feed`:** a second push of the same rows creates duplicates. No delete endpoint exists. Recovery is `data_version`: push the corrected rows with a higher version and set `list_query` on the record so downloads only see the latest; wiping a table is still a tech-team request.
- **Freshly created tables may not be empty:** tech team can seed the table with the preview/schema CSV while creating it (happened on b_238, 2026-07-08: table pre-seeded with all 8 rows a day before the "official" push, result was 16 identical rows). Always run the step-2b `get` check before feeding.
- **Booleans stored as 0 by default:** see Pre-push transforms above. The patched `upload_to_db.py` in this skill's template handles `True`/`False` strings correctly; older copies of the script may not.

## Repo layout (from `repo-template/`)

```
<benchmark_id>/                 Bitbucket repo, name == benchmark_id (folder under team-benchmarks)
  benchmark.toml                id, type, article URL, csv path, optional rename map
  upload_to_db.py               self-contained client + CLI
  start.sh                      entry point for the benchmark harness (stub in template)
  README.md                     fill-in template
  .gitignore                    lean by default: excludes data/, charts/, raw-batches/, output*/
  output/runs/run-<UTC>/        produced by the user's benchmark harness (NOT committed)
    db-ready.csv                canonical DB feed
    nivo/<chart>.csv            chart CSVs for the article
```

The user's benchmark harness (orchestrator, scoring scripts) is not part of this skill. Each repo owns its own pipeline. The skill defines only the upload contract.

### What lives in the repo vs in the DB

- **In the repo (committed):** scripts, configs, task definitions, README, methodology docs, `benchmark.toml`, `upload_to_db.py`. Everything needed to RE-RUN the benchmark on a fresh machine.
- **Not in the repo (gitignored):** generated data CSVs, chart CSVs, raw-batch tarballs, per-run output dirs, workspaces, venvs, node_modules. The DB is the source of truth for results. Data lives there; the repo is just the harness.
- **Agentic context / planning markdown** (`PLAN.md`, `AGENTS.md`, `CLAUDE.md`, `AGENT.md`) is excluded by default. These are internal scaffolding, not part of the public benchmark.

### Commit convention

First commit for a benchmark uses `<benchmark-slug> init`. Example: `agentic-llm init`, `tabular-models init`, `agentic-cli init`. Subsequent commits use whatever shape fits the change (`fix:`, `feat:`, plain summary). No Claude attribution in any commit.

## Centralizing an existing benchmark into a new repo

When migrating an old benchmark folder into the `team-benchmarks/<b_id>/` shape, copy ONLY what's needed to re-run:

1. Source scripts (`scripts/`, `src/`, runners)
2. Configs (`config/`, `*.yaml`)
3. Task definitions (`TASKS/`, dataset specs)
4. `README.md` (rewrite to point at the article URL and DB benchmark id)
5. `.gitignore` (use the one in `repo-template/`)
6. Top-level entry points (`start.sh`, `health.sh`, etc.)

Do NOT copy:

- Output directories from past runs (`output/`, `output_*/`, `workspaces/`, `backup/`)
- Generated data CSVs (`data/`, `charts/`, `raw-batches/`)
- venv directories or `__pycache__`
- Planning markdown (`PLAN.md`) or agent context files

After copying, run `git add --dry-run <b_id>/` and verify no data/output/venv paths slipped in. Then commit as `<benchmark-slug> init` and push.

## Smoke test

Run from anywhere to confirm the token flow works without touching production data:

```bash
export AIMULTIPLE_BENCHMARK_API_KEY=...
python upload_to_db.py authorize          # prints token, caches to disk
python upload_to_db.py shared-tables      # lists shared relational tables
python upload_to_db.py shared --id companies --limit 3
```
