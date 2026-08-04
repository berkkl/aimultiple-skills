---
name: aimultiple-social-sharing
description: "Drafts an AIMultiple social-sharing 'interesting facts' block for a benchmark or research article, in the format Cem lifts onto LinkedIn. Produces a 3-paragraph block led by the most counterintuitive head-to-head fact with hard numbers, a cost/speed angle, and brief honest caveats. Use when the user says social share, social sharing, interesting facts, Cem'e paylasim, LinkedIn post, social post, paylasim metni, share metni, or asks for shareable findings from a benchmark."
allowed-tools: Read, Edit, Write, Grep, Glob, Bash, AskUserQuestion
metadata:
  argument-hint: "[article-url-or-slug]"
---

Draft a social-sharing "interesting facts" block for an AIMultiple article. The output is the shareable hooks Cem posts to LinkedIn, not the article itself. Arguments: $ARGUMENTS

Base path: `/Users/berkk/Library/Mobile Documents/com~apple~CloudDocs/AIM Articles/`. Save drafts under `social-share/<article-slug>-YYYY-MM-DD.md` (create the folder with `mkdir -p` if missing). Always show the block inline for copy; saving the file is secondary.

Read `reference_social_sharing_style` from memory before drafting. It is the source of truth for voice; this skill is the procedure.

## Activation

The user wants shareable findings for an article or benchmark, or names the social-sharing format. If no article is identified, ask which one (slug or URL).

## Required inputs

- The article slug or URL (e.g. `agentic-llm`, `tabular-models`).
- The underlying numbers. Pull from the benchmark's leaderboard/merged CSVs, the article draft, or the handoff. Never invent or round-guess a figure; if a number is not in front of you, compute it from the data or ask.

## Format (non-negotiable)

Three short paragraphs, each 2-3 sentences:

1. **Lead with whatever pulls the most readers right now.** Audience pull beats clean comparability for the lead. If a just-released, controversial, or heavily-searched model is in the set (a new flagship like Fable), lead with it even when its result is caveated; keep the caveat in the lead, honest and brief. Absent such a draw, lead with the most counterintuitive head-to-head fact. Either way, hard numbers and a comparison, stated directly. No "the surprise of our benchmark"-style framing.
2. **Context plus the catch.** Who still wins, where this result places, and its weakness (cost, speed, iteration count, weak axis), with numbers.
3. **A secondary finding or a practical/cost takeaway** ("for one-shot prototyping, X wins at half the price").

Voice:
- Precise model descriptors ("Anthropic's first Mythos-class model", not "newest flagship").
- Every claim pairs with a number and a comparison ($0.70 vs $3.08; 0.611 vs 0.61; ~20 min vs ~10 min).
- Counterintuitive hooks land best ("a non-Anthropic model now matches an Anthropic flagship").
- Caveats stay brief and honest: disclose a harness exception; keep methodology internals (latency, reruns) out.
- Anti-slop applies. No em dash, no "not X but Y", no italics for emphasis, no emoji. Load [[feedback_anti_slop_strict]] / `skills/aimultiple-anti-slop-writing`.

## Workflow

1. Resolve the article slug from `$ARGUMENTS` or ask.
2. Gather the numbers from the benchmark data and article draft. List the candidate facts.
3. Pick the lead by reader pull first: the most controversial / most-searched model in the set (a new flagship), even if caveated. Only when there is no such draw, lead with the most counterintuitive clean head-to-head fact.
4. Draft the three paragraphs.
5. **Verify every number against the data before presenting.** Recompute averages and costs from the source CSV; do not quote from memory.
6. Flag any claim you could not verify (e.g. "open-weight", "slowest") and either drop it or mark it for the user to confirm. Do not overclaim.
7. Show the block inline. Offer to save to `social-share/<slug>-YYYY-MM-DD.md` and to adjust the lead.

## Failure cases

- **Number not in the data.** Compute it from the merged/leaderboard CSV or ask. Never approximate from memory.
- **Superlative not supported** ("slowest", "cheapest", "first to clear X"). Check the full field before using it; downgrade to a true comparison ("about double Sonnet") if the superlative is false.
- **Burying the draw.** Do not push a high-interest model (a just-released, controversial flagship) down for the sake of comparability. It leads for reach; the caveat rides with it in the lead.

## Integration points

- Voice and structure: `reference_social_sharing_style` memory.
- Numbers: the benchmark handoff (e.g. `handoffs/agentic-llm.md`) and `new-models-2026-06/**/leaderboard.csv` / `*-merged.csv`.
- Anti-slop pass: `skills/aimultiple-anti-slop-writing/SKILL.md`.
- The article itself: `skills/aimultiple-publication-quality-gate` before anything ships externally.
