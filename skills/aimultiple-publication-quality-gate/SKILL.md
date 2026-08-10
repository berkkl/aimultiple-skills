---
name: aimultiple-publication-quality-gate
description: |
  Final pre-publish quality gate for AIMultiple outputs: articles, benchmark writeups, scorecards, vendor recommendation memos. Use at the end of every draft cycle, after writing and research are complete, before anything is shared externally or posted. Without this skill, factual, methodology, and decision-quality defects survive into publication and damage AIMultiple's rankings and customer trust.
---

# Publication Quality Gate

## When to use

At the end of every draft cycle, right before publishing or sharing externally. This is the last checkpoint.

## Pass criteria

All of the following must be true:

1. Every non-trivial claim has a source identifier and a confidence tag.
2. Segment and vendor taxonomy is consistent across the document.
3. Vendor recommendations include explicit trade-offs, not absolutes.
4. Pricing references include their as-of date.
5. Budget feasibility is present when a recommendation implies spend.
6. Anti-slop checks (`aimultiple-anti-slop`) pass.
7. Inference statements are labeled as inference, separate from observed facts.
8. Open questions are listed as open questions, not buried in prose.
9. Every major recommendation has a risk-and-limit note.
10. No unresolved placeholders, TODOs, or `{TK}` markers.
11. Methodology sections are reproducible enough for a skeptical reader to audit.
12. For articles specifically: the `aimultiple-article-checklist` publishing phase has passed (category, permalink, tags, featured image, plagiarism check, link audit).

## Cross-model review (mandatory before any article is finalized)

Cem, 2026-08-09: "LLM'le de bi review lazim finalize edince." The time-series-classification article was drafted and cut by Claude, read by Berkk, iterated, and still shipped with fragments, four-decimal numbers and a lede that claimed more than the corrected statistics supported. An Anthropic model does not hear its own register, so the finalize review runs on a different vendor.

```bash
codex exec -s read-only -o review-out.md - < skills/aimultiple-publication-quality-gate/review-prompt.md
```

Append the draft to that prompt file, or pass the draft path inside it. `-c model_reasoning_effort=xhigh` for a long article. Use the default `~/.codex` profile: this is not judge work and it does not burn the judge quota.

The reviewer brief is a reader brief, not an editor brief. Three questions only:
1. Does every sentence parse, and does any of them need a second read?
2. Does the headline claim match what the statistics in the body actually support?
3. Is any term used before it is defined, or any characterization of a named method contradicted by that method's own source?

Findings are triaged, not applied wholesale. A cross-model reviewer will also propose rewrites that restore the padding the cut pass removed; reject those.

## Release decision

- **Pass.** All criteria met. Ship.
- **Conditional pass.** Only minor style gaps remain. Ship with the note that a style pass is outstanding.
- **Fail.** Any factual, sourcing, methodology, or taxonomy gap. Do not ship until fixed.

## Error table

| Symptom | Recovery |
|---|---|
| Unsupported claim discovered during gate | Add evidence or remove the claim. Do not ship pending. |
| No clear recommendation | Add a shortlist and name the reasoning |
| Methodology not reproducible | Add a protocol appendix or methodology note |
| Open question presented as an answer | Move to an open-questions section |
| Vendor recommendation with absolute language | Rewrite with named scope, audience, and reason |

## Integration

- Consumes outputs from `aimultiple-anti-slop`, `aimultiple-source-validation`, and `aimultiple-article-checklist`.
- This is the last skill in the chain. Nothing runs after it.
