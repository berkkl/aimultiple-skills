# Open-ended judging: the process

For anyone at AIMultiple scoring a benchmark task that has no answer key. Tool-neutral:
the rules hold whether the panel is driven by a script, a CLI or by hand. `SKILL.md` in
this folder is the same standard written for an AI assistant; this file is the one a
person follows. If they ever disagree, this file is wrong and should be fixed.

## When this applies

The deliverable is a document, an analysis, a plan or a piece of work whose quality is
a judgement rather than a value. If a gold key, a regex or a script can decide it,
build that instead and stop reading.

Mixed tasks are normal: a task can have a checkable component (facts against a human
key) and a judged component. Score them separately and report them separately. Never
average a checked score into a judged one without saying so.

## Roles

| Role | Owns |
|---|---|
| Task author | The task, the rubric, and the human gold and trap key where facts are checkable |
| Scorer | The gate, the panel run, the aggregation, the retained artifacts |
| Reviewer | Sign-off before publication: reads the disagreement log and the disclosure block |

The scorer is never the task author for the same task. If the team is too small to
separate them, say so in the methodology note.

## The six phases

### 1. Freeze

Nothing is scored until the task text, the rubric, the arm list and the model versions
are frozen and committed. Record the commit. A rubric edited after the first judge call
invalidates every call before it.

Fill `templates/judging-plan.md`. It is one page and it is the contract for the run.

### 2. Gate

A deterministic check of format and completeness, run before any judge sees anything.
Output per arm and per task is one of:

- `DELIVERED` — goes to the panel
- `INVALID` — present but malformed; scores zero, stays in the average
- `NO_DELIVERABLE` — the arm produced nothing; a model behaviour, reported separately
- `BLOCKED` — the environment stopped it; an infrastructure fault, excluded and disclosed

The last two are different failures and must not be merged. Count all four in the
article.

### 3. Panel

Two judges minimum, from two different vendors. One judge is not a panel and its
numbers are not publishable: a lone vote can never be contested and scores higher for
that reason alone.

Each judge receives one item at a time, sees every arm's work for that item under
aliases, and returns a full forced ranking of those arms. No scores out of ten, no
ties, no partial orders. Use `templates/judge-prompt.md`.

Anonymization is mandatory, not a nicety. With names visible we measured one judge
placing its own vendor's rows 8.4 percentiles higher than the other judge placed them.

Reject any response that is not a clean full permutation. Retry within a stated bound,
then abort that item and log it. Never repair or parse a judge's prose into a ranking.

### 4. Resolve disagreement

Compute the share of items where the judges materially disagree. Log every one in
`templates/disagreement-log.md`.

If the disagreement is large enough that the resolution rule changes the published
order, do not pick a convention. Ask a third judge from a third vendor the contested
items only and take the majority. Record which judge the third sided with and each
judge's overall pass or agreement rate; that is what tells you whether one judge is an
outlier rather than the others being lax.

### 5. Aggregate

Borda across judges and items. The field mean is 50 by construction. Confidence comes
from a paired bootstrap over the task set with a recorded seed, never from rerunning
models. Report rank ranges next to ranks, and describe arms with overlapping intervals
as one unseparated block.

### 6. Report and sign off

Fill `templates/article-disclosures.md` and put its content in the article. The reviewer
reads the disagreement log and the disclosure block before publication, not after.

## Definition of done

- [ ] Frozen commit recorded in the judging plan
- [ ] Gate results counted in all four states
- [ ] Two vendors on every scored item, three on every contested one
- [ ] Anonymization on, verified by inspecting one real prompt
- [ ] Every judge request and response retained with its prompt hash, model id, effort and account
- [ ] Disagreement rate computed and logged
- [ ] Bootstrap seed recorded, rank ranges reported
- [ ] Disclosure block written and reviewed
- [ ] Any judge whose vendor is also a scored arm disclosed with a measured effect size

A run missing any of these is not publishable. The one time this suite published a
judged table without retained artifacts, the numbers had to be rebuilt from scratch
months later and the ranking changed.

## What gets stored, and where

```
output/<benchmark>/
  gate.csv                  arm x task -> DELIVERED | INVALID | NO_DELIVERABLE | BLOCKED
  judge/<judge-id>/<item>/  one file per call: prompt, raw response, metadata
  rankings.csv              judge x item x arm -> rank
  disagreement-log.md       every contested item and how it was resolved
  leaderboard.csv           arm -> score, rank, rank range, interval
  judging-plan.md           the frozen contract for this run
```

Judge folders are the audit trail. They are committed, not cleaned up.

## The two operational traps

Subscription CLIs carry weekly quotas that end a campaign mid-run. Past a few hundred
calls, use a billed API.

Always set an explicit maximum output length on judge calls. Without one, providers
reserve their full context window against the account balance, and calls worth cents
fail on a healthy account with a payment error.
