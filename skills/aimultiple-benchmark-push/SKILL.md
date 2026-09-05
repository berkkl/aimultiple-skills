---
name: aimultiple-benchmark-push
description: |
  Pushes a measured benchmark into the AIMultiple registry (Houston /benchmarks/list, research-api)
  under the self-service flow: opens the record, designs the results table from the server's own
  schema prompt, creates it with dry_run, feeds the rows through a safety ladder. Parses the
  benchmark folder's own result files, never transcribes numbers. Use when a benchmark has produced
  its output/db-ready.csv and needs a Houston record + table + feed, or when the user says push the
  benchmark, DB'ye bas, tablo aç, Houston kaydı aç, benchmark verisini yükle. Not for producing CSVs
  (centralization skill), for repos that already have a table (upload_to_db.py in the database
  skill), or for writing the article. Adapted from Ekrem Sarı's benchmark-push (2026-09-05).
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, AskUserQuestion
metadata:
  argument-hint: "[benchmark-folder-path]"
---

Push a benchmark into the registry. Arguments: $ARGUMENTS

**Read `reference/playbook.md` (next to this file) before the first write.** It carries the numbered
rules (K1-K4, R2.x, R3.x, R4.x, R5.x, F1-F7, R7.x) this file refers to and every measured server trap.
**Read `reference/naming.md`** before writing the record name, description, or any column name.
Paths below are relative to `skills/aimultiple-benchmark-push/`.

## Ownership (Berkk, 2026-08-24 and 2026-09-05)

We take the id, open the table and push the data ourselves; the tech team is no longer asked for an
id or a table. **Berkk executes the two irreversible writes himself** (`create` and the real
`table/create`); the session prepares and checks everything around them and runs the feed ladder with
his go. Missing rows in shared tables (`ai_models`, `companies`) still go to the tech team.

## What this skill guarantees, and what it does not

**Deterministic, always enforced:** permission probe, base-URL normalisation, the two id forms
(prefixed slug for `table/create`, bare number for `describe`/`feed`/`get`), `dry_run` before every
DDL, system-column filter, type allowlist, apostrophe scan, relation pre-resolution against LIVE rows,
key-signature grouping, backup, canary, full cell-level verify.

**Semantic, always a checkpoint (`AskUserQuestion`):** the table grain (what one row is), what each
column measures, whether an `is_total` guard is needed, the record name / description / type, new
record vs updating an existing one. Never guess these. `feed` cannot be undone.

## Step 0: preflight (writes nothing)

```bash
export AIMULTIPLE_BENCHMARK_API_KEY=...   # Berkk supplies it per session; never written to disk or chat
python3 scripts/api.py preflight
```
K2 fails ("schema management not allowed") → STOP and tell Berkk to request schema management on the
key. No workaround.

## Step 1: reconnaissance (writes nothing)

1. `python3 scripts/api.py all "<topic>"` with status all: does a record already exist for this
   article? What does it hold (`describe` + `get`)? Old-generation data, or empty?
2. Live article: `curl -sI https://aimultiple.com/<slug>` must be 200. `page_title` stays empty
   unless Berkk wants it set; the server fills it from the post (R2.4).
3. Data in the folder: `output/db-ready.csv` (our centralization contract: one row per provider or
   model, empty cell = NULL) is the starting point for the table design; `results/`, `data/`, raw JSON
   are the sources the extractor parses. Orçun's `/benchmark-csv` output, if present, is discovery only
   (playbook § "Veri girdisi").
4. **Checkpoint:** new record or existing? One record or several (an article split into two
   measurements is two records)? Show what you found.

## Step 2: open the record

Write `push/create_<tag>.json` in the benchmark folder per playbook § 2 and naming.md
(`responsible: Berk Kalelioğlu`, `url: https://aimultiple.com/<slug>`, no apostrophes, `type` chosen
once). **Checkpoint, then Berkk posts it** (`python3 scripts/api.py post create push/create_<tag>.json`
or curl from the Confluence page). Record the returned `benchmark_id`.

## Step 3: fresh prompt

```bash
python3 scripts/api.py prompt -o push/schema-prompt-$(date +%Y%m%d).md
```
Always re-fetch (R3.1). The type allowlist and relation-target list are filled at request time and
override anything remembered. Where the prompt and `/benchmark/shared-tables` disagree, shared-tables
wins (R3.2).

## Step 4: design the table

Follow the fetched prompt plus playbook § 4 (R4.1-R4.9) and naming.md. Write `push/schema_<tag>.json`.
**Checkpoint: show the column list with types, nullability and comments.**

## Step 5: build the rows

Write `scripts/build_push_rows.py` into the benchmark folder so it can be re-run when numbers change.
It must parse, never transcribe (F1); omit a missing cell entirely (SQL NULL, never 0, never "NULL");
cross-validate two sources of the same quantity and exit 1 on disagreement (F2); assert structural
claims the table relies on; round every number to its column scale read from `schema_<tag>.json`;
keep text free of `'`, `"`, newlines and backslashes (server-side addslashes bug); strip markdown
markers from parsed markdown. Build rows BEFORE creating the table: afterwards every schema change
costs a `table/update` with `allow_drop` and a backup.

## Step 6: create the table

```bash
python3 -c "import json,sys;d=json.load(open('push/schema_<tag>.json'));d['benchmark_id']='b_XXX';d['dry_run']=True;json.dump(d,sys.stdout)" \
  | python3 scripts/api.py post table/create /dev/stdin
```
**Show the plan; Berkk approves and runs the real call** (same command without `dry_run`). The plan
lists column names only, so run `describe` afterwards and show the real structure (R6.2).

## Step 7: feed (the irreversible one)

```bash
python3 scripts/feed_ladder.py --id <num> --rows push/feed_<tag>.json \
        --backup-dir <folder>/push/restore --key '<lookup>,<discriminator>'
```
Plan mode: validates, groups, prints, writes nothing. **Checkpoint, then re-run with `--apply`.** The
ladder does backup, one canary per key signature, read-back compare, the rest group by group, full
cell-level verification. A failed batch writes nothing (feed is atomic). Never `autoCreateRelation`.

## Step 8: close out

- `python3 scripts/api.py urls <slug>`: URL and title landed.
- `python3 scripts/api.py all "<topic>"`: the record as the registry shows it.
- More than one `data_version` in the table → write a one-line `list_query` via `/benchmark/update`
  so downloads only carry the latest; read it back and compare byte for byte.
- An older record for the same article → ask whether to set `status:0`.
- Write what changed, evidence and rollback into `handoffs/benchmark-centralization.md`; keep the
  ladder's backups; mark the plan row and the YouTrack card (session-pm checkout, DB gate).
