# Judging plan: <benchmark slug>

Filled before the first judge call. One page. This is the contract for the run; if
something here changes afterwards, every call made before the change is void.

## Frozen state

| | |
|---|---|
| Repo commit | `<sha>` |
| Task set | `<n>` tasks, listed in `<path>` |
| Rubric | `<path>`, version `<v>` |
| Arms | `<n>`, listed in `<path>` |
| Model versions / slugs | `<path>` |
| Frozen on | `<YYYY-MM-DD>` |

## Scored components

| Component | Method | Weight | Owner |
|---|---|---|---|
| Judged quality | panel ranking, Borda | | |
| Checkable facts | human gold and trap key | | |
| Format gate | deterministic, INVALID = 0 | pass/fail | |

If a component is not used, delete the row rather than leaving it blank.

## Panel

| Judge | Vendor | Model id | Effort | Transport | Account / profile |
|---|---|---|---|---|---|
| J1 | | | | | |
| J2 | | | | | |
| J3 (tie-break only) | | | | | |

- Anonymization: on. Alias scheme: `<describe>`
- Retries per item before abort: `<n>`
- Maximum output length per call: `<n>` tokens
- Judge vendors that also appear as scored arms: `<list, or none>`

## Disagreement rule

Third vendor decides contested items by majority. Threshold for calling the panel
contested: `<state it, e.g. any item where the two judges' orders differ>`.

## Statistics

- Bootstrap: paired over tasks, `<n>` draws, seed `<n>`
- Reported: score, rank, rank range, 95% interval

## Known limitations to disclose

- `<e.g. N=1 per task, no rerun variance>`
- `<e.g. one judge's vendor is also an arm>`

## Sign-off

| | Name | Date |
|---|---|---|
| Task author | | |
| Scorer | | |
| Reviewer | | |
