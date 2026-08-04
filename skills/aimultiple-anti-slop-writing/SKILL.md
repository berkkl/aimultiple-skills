---
name: aimultiple-anti-slop-writing
description: |
  Enforces AIMultiple writing style for article drafts, benchmark writeups, summaries, and rewrites. Use when drafting, editing, summarizing, or making text publishable. Without this skill, copy becomes templated, low-density, and easy to flag as AI-generated.
---

# Anti-Slop Writing

## Activation

Use this skill for every sentence intended for publication.

## Core Rules

1. Do not use em dash characters.
2. Avoid "it is not X, it is Y" rhetorical templates.
3. Avoid italic emphasis unless quoting or showing prompt text.
4. Do not use emojis.
5. Keep idea density high. Remove filler and repeated paraphrases.
6. Prefer concrete facts and direct implications.
7. Keep bullet lists short and necessary.
8. Do not invent terminology just to label simple ideas.
9. Each paragraph must contribute one new point.
10. Prefer specific numbers and named entities over vague descriptors.
11. Distinguish facts from interpretations clearly.
12. Keep sentence rhythm varied to avoid template feel.
13. Flag sections that are accurate but structurally redundant.
14. Flag taxonomy-heavy passages that add classification but little decision value.
15. Prefer one-line clarifications over full headers when a distinction is not central to the argument.
16. Avoid clever-but-vague framings. A phrase like "wide spread," "decides token use," or "the depressed backend" sounds like a point but names nothing concrete. State the actual thing: a 22-point gap, no prompt caching, a likely floor.
17. Write for a global audience. If a non-native English reader could read a phrase literally and be confused (e.g. "depressed backend"), rewrite it plainly.
18. In data writeups, a takeaway must say something the chart does not already show. Do not restate the visible ranking ("X is second, Y is last"); surface the non-obvious finding (a cross-axis divergence, an inversion, an independence). Derive any causal claim from the source data, not a guess.

## Mandatory cut pass (run before delivering anything, every time)

Repeated feedback, 2026-07-29: "whatever you share comes at 2x the text" and "the structure is good, the rest is word salad." Drafting is not the problem. Not cutting is. So the cut is a separate pass, not a mindset.

Write the draft, then delete from it. A document that was not shortened after drafting was not edited.

Delete on sight:
- Any sentence justifying a choice the reader already accepted. State the decision; drop the defence.
- Any restatement of a heading in the first sentence under it.
- Any sentence a reader can skip without losing information. Test: cover it and reread. If nothing breaks, it was slop.
- Specification the reader did not ask for. Column lists, field semantics and status vocabularies belong in the code or the schema, not in a proposal. Clear file names are usually the whole ask.
- Any "why this matters" paragraph. If it matters, the fact shows it.
- Numbered rationale under a decision that is already agreed.

Keep: the structure, the decision, the number, the concrete failure it prevents.

Target: cut the first draft by half. If the cut version loses a fact, put that fact back, not the sentence around it.

## Editing Pass Order

1. Factual correctness
2. **Cut pass (above). Non-optional.**
3. Density and redundancy cuts
4. Tone and natural phrasing
5. Structural usefulness check
6. Final anti-slop sweep

## Error Scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Template-like repetition | Multiple sentences use the same structure | Merge and keep the strongest one |
| Fluffy paragraph | No measurable fact inside the paragraph | Rewrite around one concrete fact |
| Artificial transitions | Generic connectors appear everywhere | Use direct transitions or split the section |
| Taxonomy overload | Section mainly defines labels readers do not need | Compress to one sentence or move later |
| Accurate but redundant section | Repeats a prior point with new labels | Cut instead of rewriting |

## Integration Points

- Depends on `aimultiple-source-validation` for fact safety.
- Final gate is `aimultiple-publication-quality-gate`.
