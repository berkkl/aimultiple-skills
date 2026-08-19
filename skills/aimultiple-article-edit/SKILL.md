---
name: aimultiple-article-edit
description: "Proposes edits to an AIMultiple article as strict OLD/NEW pairs the editor can apply by find-and-replace. Every change is OLD: [exact current text] / NEW: [replacement]. Direct, no preamble, no AI slop. Use when the user asks what to change in an article, wants article edits, says 'edit this', 'what should I change', 'update the article', 'fix the copy', 'makale duzenle', 'neyi degistirmeliyim', or pastes article text for revision."
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, AskUserQuestion
metadata:
  argument-hint: "[article-slug-or-path]"
---

Propose edits to an AIMultiple article as OLD/NEW pairs. The output is a list the editor applies by hand; it is not a rewrite of the article. Arguments: $ARGUMENTS

## The format (non-negotiable)

Every edit is exactly two labeled blocks, OLD then NEW:

```
OLD: the exact current text, verbatim, copy-pasteable and unique enough to locate
NEW: the replacement text
```

Rules:
- OLD must be a verbatim, contiguous span from the current article. Never paraphrase it. If it is not unique, extend it until it is.
- For an insertion (no text to replace), use `ADD AFTER:` instead of `OLD:` and anchor it to a verbatim span:
  ```
  ADD AFTER: the verbatim sentence the new text follows
  NEW: the text to insert
  ```
- For a deletion: `OLD: [verbatim span]` / `NEW: (remove)`.
- Group edits under the article's section heading (`## Cost & success comparison`). Order them top-to-bottom as they appear in the article.
- One short `Why:` line is allowed under a pair ONLY when the edit fixes a factual error or a chart/text contradiction. Otherwise no commentary.
- No preamble, no "Here are the edits", no summary paragraph. Lead with the first heading.

## AIMultiple house structure (chart-first)

Cem's rule: the chart comes first because it draws more attention than a wall of text. Results and numbers are stated AFTER the chart, not before it.

- Keep intros short. Do not extend an intro to add findings. An intro sets up the topic; it does not report results.
- Put the lead finding (the headline number, the ranking) in the copy that follows the chart, not in the intro.
- When a finding needs surfacing, anchor the new text after the chart or as the lead-in to the results section, never in the intro.
- Broader standing goal (not every task): replace walls of text with charts, tables, and tight result paragraphs. The agentic-cli and agentic-llm articles are the main targets. When editing them, prefer cutting prose over adding it.
- Bullets are not strict on count, but every key point must survive the conversion. Do not drop facts to shorten; drop only sub-mechanisms and connective prose.
- Not everything becomes bullets. Observation-driven sections (qualitative behavioral findings, the observatory benchmarks, per-agent deep-dives) stay as prose because takeaways flatten them. The bullet treatment is for data-chart and table sections.
- References/sources go in WordPress footnotes via the `[efn_note]source text and URL[/efn_note]` shortcode, placed inline at the citation point (Easy Footnotes plugin). Do not use inline markdown links for external sources in published copy.
- Watch the wording. State the point in plain, concrete words and lead with a concrete subject. Avoid abstract framings: no "X, not Y, decides Z" and no "it's not X, it's Y" (banned globally). Avoid vague labels like "wide spread," "token use," "figures are bounds, not exact." Name the concrete thing instead: a 22-point gap, an upper bound, a floor, no prompt caching, four tasks scored 0. If a phrase sounds clever but a non-native reader could misread it, rewrite it plainly.
- Takeaways surface findings, not the ranking the chart already shows. Do not write "X is second, Y is third" or "Z is last", that is readable off the bars. Call out the non-obvious: cross-tab divergences (high backend rank but weak frontend), surprises (a proxied agent's depressed score, with the caveat noted), inversions (cheapest tool also scores top), and independence (build rank doesn't predict compaction). If a bullet restates the visible order, cut it.
- Per-chart analysis pass (run BEFORE writing any takeaway; do not skim). For each data chart ask, in order:
  1. What decision does a reader make from this chart? Write the finding that informs it, not a description of the bars.
  2. Where does the result contradict a model's known positioning? Cross-reference tier (flagship vs mid vs small), price, specialization (a `codex`/`code` variant, a `flash`/`mini`/`nano` speed-or-size tier, a `thinking` variant), and vendor claims. Inversions are the highest-value takeaway: a mid-tier beating the flagship, a code-specialist losing a coding benchmark, the "cheap/fast" tier turning out most expensive, newer scoring below older. Ground positioning in official naming/tier/marketing (safe: `Opus` = Anthropic flagship, `codex` = code-tuned, `Flash` = fast tier, `Haiku` = small tier). Do NOT invent a model's public benchmark numbers; verify any external claim before citing it.
  3. State the honest ceiling and diminishing returns, not just who won. If the best score still fails a third of the checks, say so. If the last few points cost most of the money or time, say so. Cem's rule: the story is whether the winner conquers the hard, business-relevant part, not that it ranked first.
- **Budget the block under a chart: six items and about 190 words, whichever comes first.** Cem, 2026-08-19, cut the agentic-enterprise results section from seven paragraphs. When an edit pass finds a block over budget, the OLD/NEW pair replaces the whole block, it does not trim a sentence out of each paragraph.
- **Method sentences move to Methodology, they are not shortened in place.** How the scale works, how many judges scored it, how a resampling ran, why a task was excluded: none of it belongs under the chart. The exception is a one-sentence disclosure about what the chart itself shows or omits, and the reasoning effort it ran at.
- **Answer the reader's obvious question about the chart in the first line under it.** If two well-known models are absent from a cost chart, the first sentence says they are absent and why. Cem asked "Burada neden Fable ve Opus yok?" of a chart whose text buried the answer in the phrase "five setups, including both leaders".
- Depth over count. 2-3 findings that each change the reader's decision beat 6-7 that restate the chart, so never pad to a number. But run the pass above so you do not miss the strong ones (a low ceiling, a positioning inversion, steep diminishing returns are easy to skim past).
- Repetition audit (mandatory, before delivering, every time). List the distinct facts in the section. If two bullets carry the same fact in different words, keep one. If deleting a bullet loses no fact, delete it. Three sentences that all say "Sonnet beats Opus" is AI slop. This restates the global rule (no repeating a point in different words); apply it here without being reminded.

## Reference rewrites (real before → after)

Wording, name the concrete thing:
- "Same model, wide spread" → "All nine clean agents use the same Sonnet 4.6, yet backend ranges from 77.3% to 55.4%. That 22-point gap comes entirely from the orchestration."
- "Caching, not workload, decides token use" → "The token numbers are mostly about caching. Six agents cache 86–98% of input, so Claude Code's 4.18M gross shrinks to 115k effective; five don't cache and pay for everything they re-send."
- "the depressed backend" (a non-native reader reads it as sad) → "this is likely a floor rather than the agent's true backend."
- "A few figures are bounds, not exact" → "Three caveats on the numbers: ... read it as a ceiling; ... is a floor; ... each scored 0."

Findings, not the chart's visible ranking:
- BAD (restates the bars): "Grok is second (75.4%), Claude Code third (74.9%)." / "Aider is last at 32.7%."
- GOOD (non-obvious): "Cline (4th on backend) and Forge (5th) trail on frontend, so they slip down the combined board." / "Codex ranks 10th on backend despite a perfect 100% frontend, a proxy floor, not the agent."

References as footnotes:
- BAD: an inline link, "our [OpenRouter setup](url)".
- GOOD: "...likely a floor.[efn_note]We ran Codex CLI against the common model through OpenRouter, following <url>[/efn_note]"

Check the data before you label:
- "Junie's 2.36M is a caching bug" → after checking `db-ready.csv` cache% (junie ~0; six agents 86–98%): "Junie has no prompt caching, so it pays for everything it re-sends." Derive the why from the data; do not hedge with a vague label or guess a cause.

## Activation

The user wants to know what to change in an article, or pastes article text for revision. If no article is given, ask for the slug or path.

## Required inputs

- The article text (pasted, or read from `drafts/<slug>.md`).
- The data behind any number you touch: benchmark leaderboard/merged CSVs, chart CSVs, the handoff. Never quote a figure from memory.

## Workflow

1. Get the article text and identify the slug.
2. Read it against the current data. Flag two classes of change first: (a) numbers or claims the data/charts now contradict, (b) missing content the data now supports.
3. For every change, locate the verbatim OLD span and write the NEW span.
4. **Verify every number in a NEW block against the source data before writing it.** Recompute from the CSV; do not trust memory or the article's own prior text.
5. Write the NEW text under anti-slop rules: short, direct, fact then implication, varied structure. No em dash, no "not X but Y", no italics for emphasis, no emoji, no padding. Load `skills/aimultiple-anti-slop-writing`.
6. Output the OLD/NEW list grouped by heading. Offer to apply the edits to `drafts/<slug>.md` if it is a local file.

## Failure cases

- **OLD not verbatim.** The pair is useless if find-and-replace cannot match it. Copy the span exactly, including punctuation and spacing.
- **OLD not unique.** Extend the span until it matches one place only.
- **Unverified number in NEW.** Stop and compute it from the data, or drop the claim. Never approximate.
- **Editorializing in NEW.** A NEW block is publishable copy, not a note to the editor. Caveats go in the copy; reasons go in the one optional `Why:` line.
- **Rewriting untouched text.** Only emit pairs for spans that actually change. Do not restate the article.

## Integration points

- Anti-slop on every NEW block: `skills/aimultiple-anti-slop-writing/SKILL.md`.
- Number and claim verification: `skills/aimultiple-source-validation/SKILL.md`, `skills/aimultiple-fact-check-workflow/SKILL.md`.
- Before anything ships externally: `skills/aimultiple-publication-quality-gate/SKILL.md`.
- Shareable findings from the same data: `skills/aimultiple-social-sharing/SKILL.md`.
- Benchmark numbers live in the relevant handoff and `new-models-*/**/leaderboard.csv` / chart CSVs.
