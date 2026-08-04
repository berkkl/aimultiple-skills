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
