# Article disclosures: <benchmark slug>

The sentences a judged leaderboard has to carry. Written as prose the article can use
after substitution, not as a checklist to summarize. Cut anything that does not apply
to this run; do not cut anything that does.

## Next to the first number

The scale is relative. Judges rank every submission against every other in the field,
so 50 is the average by construction and the average here is `<x>`. A `<y>` means this
arm's work sits above the middle of this field, not that `<y>`% of it was right. Scores
from this benchmark are not comparable to scores from any other.

## In the methodology section

Two judges scored every submission: `<J1 model>` and `<J2 model>`, at `<effort>`,
each seeing all submissions for one task at a time under aliases and returning a full
ranking. Model and vendor identity were hidden. `<Where a third judge was used:>` The
two judges disagreed on `<n>`% of items; `<J3 model>`, from a third vendor, was asked
those items and a majority decided, siding with `<judge>` on `<n>` of `<m>`.

`<Where a judge's vendor is also an arm:>` `<Judge>` is also a scored arm in this
table. Measured against items neither judge's vendor produced, the effect is `<x>`
points in its own vendor's favour. `<If measured with anonymization off:>` With names
visible the effect was `<x>` percentiles.

Confidence intervals come from resampling the task set, `<n>` draws at seed `<n>`, not
from rerunning models. Arms whose intervals overlap are not separated by this data.

## Where the gate is described

`<n>` of `<m>` deliverables failed the deterministic format gate and score zero rather
than being dropped, because a file that cannot be parsed is a result. `<n>` arms
produced nothing at all, which is a model behaviour and counted separately from `<n>`
runs stopped by the environment.

## Where a winner is claimed

`<Only if true:>` `<Arm>` leads on the hardest tasks in the set with a gap the
bootstrap separates. `<If not true:>` The top `<n>` arms are not separated by this
data and are reported as one block.

## What is not claimed

`<n>`% of row-level judgements are unreviewed by a human. `<Any other limitation from
the judging plan.>`
