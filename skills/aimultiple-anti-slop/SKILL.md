---
name: aimultiple-anti-slop
description: |
  Enforces AIMultiple writing style on every sentence destined for humans. Use when drafting Discord replies, reviewing an article draft, rewriting a paragraph, summarizing research, or converting notes into publishable text. Without this skill, output becomes templated, low-density, and easy to flag as AI-generated slop.
---

# Anti-Slop Writing

## When to use

Every time prose is produced for a human reader. This includes Discord replies, article drafts, review comments, and summaries. This skill runs as a background check on all writing output.

## Banned patterns

1. **Em dash character (`—`).** Split into two sentences.
2. **"It is not X, it is Y" framing.** It is a slop tell. Rewrite directly.
3. **Italic for emphasis.** Only italicize when quoting someone or showing prompt text.
4. **Emojis in prose output.** Exception: reactions on Discord and similar platforms, which are not prose.
5. **Paraphrase repetition.** If deleting a sentence changes nothing, it was slop.
6. **Templated structure.** If every section or paragraph follows the same shape, vary it.
7. **Inventing terminology.** Do not coin a label for an idea that already has a plain-language description.
8. **Embellished facts.** State the fact, then the implication. No hedging, no adjective stacking.
9. **Excessive bullet points.** Use bullets only when the information is a genuine list. Prose by default.
10. **Filler words and phrases.** basically, simply, just, very, more and more, these days, in fact, over time, for a long time, this article, our article. Drop them.
11. **Salesy adjectives.** intuitive, amazing, awesome, huge, enormous. Drop unless quoting.
12. **Passive voice beyond ~5%.** Default to active.
13. **Time-relative claims that will rot.** "Interest grew X% this month", "as of December 2025", "recently announced". Why: outdated next cycle. Use absolute dates and avoid growth-in-current-period claims unless they are the point of the article.
14. **Superficial marketing distinctions.** "AI-powered vs AI-native", "next-generation vs traditional". These are sales vocabulary presented as taxonomy. Cut or name the real difference.
15. **Section-link descriptions that do not carry the claim.** A hashtag link that just names the section wastes the reader's scan. Include the point. Example: `#agents-vs-deep-research` should read "Agents vs Deep Research Models demonstrates agents are cheaper than deep research models while providing comparable accuracy", not just "Agents vs Deep Research Models".
16. **Embellished repetition of a single point across sentences.** The same fact restated with new adjectives counts as two slop hits, not one. Cem flags this explicitly.

## What to do instead

- Short, direct sentences.
- State fact, then implication, then stop.
- Vary sentence structure across paragraphs.
- Concrete nouns and named entities over generic descriptors.
- Verify facts against sources before writing them.
- Use absolute dates, not relative ones.
- One new point per paragraph.
- Every paragraph under ~430 characters.

## Density test

Read every paragraph twice. If there is no measurable fact inside, rewrite around one.

Read every sentence. Ask: does this sentence say something a generic article on any topic could not? If not, cut or sharpen.

## Error table

| Symptom | Fix |
|---|---|
| Several sentences with same structure | Merge to the strongest; cut the rest |
| Paragraph with no facts | Rewrite around one concrete fact |
| Generic transitions everywhere | Use direct transitions or split the section |
| Taxonomy-heavy passage | Compress to one sentence or move lower |
| Accurate but redundant paragraph | Cut it |
| Time-relative hook ("this month", "recently") | Replace with an absolute date or cut |
| Marketing distinction with no real difference | Cut or rewrite to name the actual difference |
| Section link with no claim | Add the claim inline with the link |

## Integration

- Gates output from `aimultiple-article-checklist` phase 2.
- Paired with `aimultiple-source-validation` for fact safety.
- Final check by `aimultiple-publication-quality-gate` before publishing.
