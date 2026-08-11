---
name: aimultiple-open-ended-judging
description: |
  The standard for scoring open-ended benchmark tasks, where no answer key exists and the deliverable is a document, an analysis or a piece of work rather than a checkable value. Use when designing or running any model-as-judge evaluation, choosing a judge panel, or reporting a judged leaderboard. Without this skill, judged scores drift into single-judge opinion, absolute numbers that mean nothing across benchmarks, and rankings that move when the resolution convention changes.
---

# Open-Ended Judging

The canonical text is `docs/JUDGING.md` in the agentic-enterprise-benchmark repo. It
is self-contained and carries the four templates a run produces (judging plan, judge
prompt, disagreement log, article disclosures) as appendices, so a teammate without
this skills repo can still run a panel. Point people there. This file is the same
standard in short form for routing an assistant; if the two ever disagree, JUDGING.md
is right and this one gets fixed.

## Activation

Any task whose output cannot be scored against a key: written deliverables, research
outputs, plans, analyses, designs. If a gold key or a programmatic check can exist,
build that instead. Judging is what you do when checking is impossible, not when it is
inconvenient.

Applies to every benchmark in the suite, not to one task set.

## The rules

**1. Deterministic gate first.** Format, required sections, required columns. A file
that fails the gate is INVALID and scores zero; it is not dropped from the average.
The gate runs before any judge sees anything. A missing deliverable and a malformed
one are different states and are reported separately.

**2. Judges rank, they do not grade.** Ask for a full forced permutation of all arms
on one item. No ties, no absolute quality points, no partial rankings. A judge asked
"how good is this, out of 10" is answering a different question each time it is asked;
a judge asked "order these six" is answering the same one.

**3. Malformed output is rejected, never repaired.** Strict JSON, exact permutation, no
extraction from prose, bounded retries, then abort. Repairing a judge's output silently
invents a judgement.

**4. Two vendors minimum, three when they disagree.** Never one judge: a single vote
can never be contested, so it is both unverifiable and mechanically more generous than
a panel that resolves disagreement strictly. Two judges from different vendors is the
floor. When they split on enough of the material to move the ranking, a third vendor
breaks those ties by majority. Do not settle a ranking-moving disagreement with a
convention such as "take the stricter reading"; measure which judge is the outlier.

Evidence: on the meta benchmark two judges split on 29% of criteria, and strict versus
lenient resolution moved cells up to 23 points and reordered most of the table. A third
vendor sided with the lenient judge on 149 of 200, and pass rates were 53.6% / 80.7% /
76.0%. The convention had amounted to the harshest judge deciding alone.

**5. Anonymize, always.** Judges see aliases, never vendor or model identity, and never
the arm's own directory or file names. Measured on agentic-enterprise with names
visible: Sol placed GPT rows 8.4 percentiles above where Opus placed them, Opus placed
Anthropic rows 4.9 percentiles above where Sol placed them.

**6. Disclose and measure judge-vendor conflicts.** When a judge's vendor also appears
as a scored arm, report the effect. Measure it by difference-in-differences: the gap
between two judges on the conflicted arms, against the gap the same two show on arms
neither vendor produced. Do not measure it by dropping the conflicted judge and
comparing to the panel, which measures the single-judge artifact in rule 4 instead.

**7. The scale is relative and must be labelled as such.** Aggregate by Borda across
judges and items. The field mean is 50 by construction. A 66 means the arm's work sits
above the middle of this field, not that 66% of it was right. Never compare a judged
score to a judged score from another benchmark, another field of arms, or another task
set. State this in the article, next to the first number.

**8. Length is not quality.** The rubric must penalize padding and unsupported claims
explicitly, or judges reward volume. Where facts in the deliverable are checkable,
carry a human-written gold and trap key and score those separately from the judged
component.

**9. Confidence comes from resampling tasks, not from rerunning models.** Paired
bootstrap over the task set, fixed seed recorded. Report rank ranges alongside ranks.
Arms whose intervals overlap are one block and must be described as unseparated, not
ordered.

**10. A winner claim needs the hardest subset.** Leading the overall average is not a
win. The winner leads on the hardest business-relevant tasks with a gap the bootstrap
separates. If the data does not support that, report the field as unseparated and give
the vendor feedback instead of manufacturing a headline.

**11. Everything is retained.** Per item and per judge: the exact prompt, the raw
response, the prompt hash, the judge's resolved model id and effort setting, and the
account or profile it ran under. A judged number without its request and response is
the defect this suite has already had to rebuild once.

## Transport

Prefer a billed API over a subscription CLI for any panel over a few hundred calls: a
weekly quota has already ended one campaign mid-run. Set `max_tokens` explicitly on
every call; without it providers reserve the full context against the account balance
and cheap calls fail on a healthy balance. Bind judge accounts through an explicit
profile and verify the expected account before the run, never inherit the shell's.

Give the judge panel an account nothing else uses. OAuth refresh tokens are
single-owner, so an account shared with a run box means the two cannot run at the same
time, and a fresh login on one silently kills the other. Where a fallback order exists,
write it down and move down it only on exhaustion, recording which account scored which
items: a campaign split across accounts is still one panel, but the audit trail has to
say where each call was billed.

Detect exhaustion on both streams. Codex reports a weekly cap on stderr; Claude Code
reports it on **stdout** with an empty stderr and exit code 1, so a wrapper that reads
only stderr logs an empty error and the campaign looks like it merely crashed. After a
cap, a short probe succeeding proves one small call fit, not that the cap cleared.

## Reporting checklist

Before publishing a judged leaderboard, the article states: the gate and how many arms
failed it, the panel and its vendors, that anonymization was on, any judge-vendor
conflict and its measured size, the resolution rule for disagreement, that the scale is
relative with mean 50, the bootstrap seed and the rank ranges, and which arms are
statistically unseparated.

## Failure scenarios

| Scenario | Recovery |
|---|---|
| One judge unavailable mid-campaign | Stop. Do not publish a mixed one-judge / two-judge table; single-judge items score higher for structural reasons. Fill the gap, then recompute. |
| Judges split on a large share of items | Third vendor on the contested items only, majority decides. Report the split rate and which judge the third sided with. |
| A judge's vendor is also an arm | Keep it, disclose it, measure it per rule 6. Removing the judge costs more than it fixes. |
| Judge returns prose instead of the permutation | Retry within bounds, then abort the item and record it. Never parse it. |
| Ranking changes under a different resolution rule | The rule is doing the work, not the evidence. Resolve with a third opinion before publishing. |
| Someone asks to compare this score to another benchmark's | Refuse the comparison and restate rule 7. |

## Integration points

- Design decisions and fairness rules: `aimultiple-benchmark-methodology-design`
- Before implementation: `aimultiple-benchmark-preflight-check`
- Publishing the table and charts: `aimultiple-benchmark-centralization`
- Article wording of the disclosures: `aimultiple-article-checklist`
