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

## Sentences must parse before they are cut

Cem, 2026-08-09, on the published time-series-classification article: "Devrik cumleleri duzeltirsen biraz AI-slop'umsulugu azalir." The article had already been through a Claude cut pass. The cut is what broke it.

1. **Every sentence carries a subject and a finite main verb.** An appositive followed by a relative clause is a fragment, not a sentence. "Twenty-seven datasets, 18 univariate and 9 multivariate, where all four models and both baselines produced a result." has no main verb. Write "Twenty-seven datasets produced a result from all four models and both baselines: 18 univariate and 9 multivariate."
2. **Plain word order: subject, verb, object.** Fronted adverbials, inverted clauses and stacked qualifiers before the subject are the single biggest source of the translated-prose feel. One fronted phrase in a paragraph is fine, one per sentence is the pattern to kill.
3. **The cut pass removes words, not information.** Cem on the same article: "Gereksiz kelimeleri cikartmisiz ama ben bile anlamiyorum simdi de. Gerekli kelimeler de cikmis." Shortening that drops the article, the antecedent, or the noun a verb belongs to produces a shorter sentence that says less. If the compressed version needs a reread, it failed.
4. **Comprehension bar: an intelligent reader outside the field, making an effort, understands it on one read.** Cem's own test: "Ben her gun time series analizi yapmiyorum ama Claude Code'la yapabilirim. Yaziyi ben efor gosterip anlayamiyorsam olmamis." A term of art is defined at first use or replaced. "One of these comparisons was inspected as a corrected contrast and it survives" and "those three carry no test" are unreadable outside the project. Write what was done: "We ran a significance test on only one of these comparisons. MiniRocket beat MOMENT on 24 datasets to 4, and the result holds after correcting for multiple tests. The other three comparisons were never tested."
5. **Round to three decimals.** Cem: "3 decimal digitte kalirdim." 0.8584 becomes 0.858. Four-digit precision on a benchmark score is precision theater, and it makes the number harder to hold in the head. Exceptions: p-values in scientific notation, and identities where the extra digits are the point.

## Use the word a person would use, not the word the source used

Berkk, 2026-08-17, on "invent a domain" in the agentic-it methodology: the phrase was lifted straight from the task prompt. Precise for the engineer who wrote the prompt, jargon for the reader, and on a site that publishes about SEO, "domain" reads as a domain name first. Being faithful to the source text is not the same as being right for the reader.

Our own words leak in from prompts, rubrics, configs, chart titles and code. The same session had to strip `arm`, `cell`, `harness`, `deliverable`, `field`, `Borda count`, `Kendall tau`, `rank range` and `format gate` out of two drafts, all of them correct internally and all unreadable outside the project.

1. **Every term of art is defined at first use or replaced.** Replacing is the default; define only when the term is the subject of the article.
2. **Check words that carry a second, more common meaning.** `domain`, `cell`, `field`, `arm`. The reader picks the everyday reading, so a technically correct sentence can still be read wrong.
3. **Translate at the point of writing, not at review.** The lint catches known words; it cannot catch a new one invented this week.
4. **A word from an artifact is a draft, not a decision.** Chart titles and axis legends count as published prose: the enterprise score chart said "by model and harness" while the article said "agent program".

Known replacements are in `JARGON` in `skills/aimultiple-article-checklist/lint_article.py` and fire as a WARN. Add the word when a new one leaks.

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
3. **Parse pass. Reread every sentence the cut touched.** Subject, finite verb, plain word order, no orphaned pronoun. This pass exists because the cut pass creates fragments.
4. Density and redundancy cuts
5. Tone and natural phrasing
6. Structural usefulness check
7. Final anti-slop sweep
8. **Cross-model review before finalizing.** Anthropic models do not catch their own register. Run the finished draft past a different vendor (Codex / GPT 5.6 Sol) with a reader brief, not an editor brief: does each sentence parse, does the headline claim match the statistics, is any term undefined. Procedure in `aimultiple-publication-quality-gate`.

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
