---
name: aimultiple-deep-research-question-gen
description: |
  Generates and refreshes the task set for the AI Deep Research Benchmark: 40 short verifiable
  questions and 10 open-ended research tasks. Source-first pipeline run via the Workflow tool:
  harvest fresh primary sources, derive questions from documents (never from model memory),
  adversarially verify with evidence, dedup, and hand a candidate pool to human curation and a
  manifest-based freeze. Use when creating the benchmark's question set, refreshing decayed
  questions, or auditing pool health. Without this skill, questions leak from the generator
  model's priors (contamination), answer keys go unverifiable, and frozen sets mutate silently.
---

# Deep Research Benchmark question generation

## Activation

Creating or refreshing the task set for `specs/ai-deep-research-benchmark-spec.md`. Also for pool health audits (which questions' answers changed or died).

## Required inputs

- The spec and `ai-deep-research/refresh-2026-08-25/framework-v2.md`
- Contestant model training cutoffs (latest one governs)
- Target run week (freshness window measured against it)
- Integer domain/type quotas for the frozen 40+10, written down before harvest
- Existing pool file if refreshing (merge, never regenerate from scratch)

## Contamination defense

The generator model (Fable) is also a contestant. Three layers, all mandatory:

1. **Source-first.** Every short question is derived from a primary-source document fetched during generation. The answer key is a value or quote in that document, with evidence locator. Record both the source's publication date and the fact's first-public date; both must be after the latest contestant cutoff (a fresh document restating an old fact fails). Target facts/events from the ~60 days before the run week (Berkk rule 2026-08-28: ideally the last two months; older post-cutoff facts are fallback only, marked in the freeze manifest). Research-task scenario anchor events follow the same recency rule.
2. **Cue lint.** A prompt is rejected if it contains the answer, the source's title or navigation phrasing, or distinctive non-entity phrase overlap with the source. Questions must be findable through the fact, not through the document's own words.
3. **Non-contestant audit + human curation.** Before freeze, the near-final pool passes an audit by a model from a non-contestant vendor (the independent judge vendor), and a human selects the final set. Question authorship assistance is disclosed in the methodology.

These rules apply at full strength to the 40 short questions. Research tasks use sources for scenario realism and freshness; their quality answer is not contained in the source basis and their gates are structural (see below).

## Record schemas

Short question:
`id, type (factual|comparative|multi-hop|calculation|structured-json|categorical-listing), domain, question (contains an explicit as-of date when volatile), answer_type, canonical_answer, accepted_variants, units, tolerance_rule, derivation (for calculation/multi-hop), sources[] {url, published_at, retrieved_at, archived_copy_path, sha256, evidence_quote}, fact_first_public_at, stability (stable|volatile), notes`

Comparative and multi-hop questions carry one source entry per hop; a single URL is not sufficient.

Research task (one file per task):
`id, domain, prompt, deliverable, gate_elements[] {id, public_text, check_type (presence|section|format), predicate}, source_basis[], notes`

Gate elements are printed in the published task and check structure and presence only. Factual quality, padding, and unsupported claims belong to the blinded judge panel and the claim-support audit, never to the gate.

## Workflow pipeline

Run via the Workflow tool, phases in order. Targets: 60 short-question candidates for 40 slots, 15 research-task candidates for 10 slots. Loop phases 1-3 until quotas met (stop after 2 rounds with no accepted candidates).

1. **Source harvest.** Per-domain agents (software releases/patch notes, earnings, funding/M&A, regulation, developer ecosystems) fetch primary sources published inside the freshness window (default: last 90 days before run week, after cutoffs). Output: source list with URL, date, one-line summary.
2. **Drafting.** Per-source agents write candidates from the fetched document only, filling the full schema including archived copy and evidence quote.
3. **Verification.** An independent agent per candidate emits PASS/FAIL with evidence for each check: unauthenticated clean-session fetch succeeds; archived copy matches (hash); publication and first-public dates post-cutoff; evidence quote present at locator; exactly one canonical answer derivable; a second retrieval-only agent reproduces the answer from the source; cue lint passes; as-of date present if volatile. Missing evidence or reproduction mismatch kills the candidate with a recorded reason.
4. **Dedup and balance.** Kill near-duplicates; enforce the pre-registered quotas (all six types; integer domain quotas; traps present: version trap, recency trap, and conflict traps only where the prompt fixes source authority and as-of date so the canonical answer stays unique).
5. **Curation handoff.** Write the pool with per-candidate verification evidence to `ai-deep-research/question-pool/`. Non-contestant audit pass, then human curation selects the final 40+10.

## Freeze

**No-web probe (mandatory, before the manifest).** The benchmark must measure live research, not the model's knowledge base; products like structured-lookup APIs have no parametric fallback, so a memory-answerable task breaks comparability. Run the full selected set against a model with web access disabled. Any short question the no-web model answers correctly is killed and replaced from surplus. For research tasks, the no-web output goes through the claim audit; if it passes the gates with mostly supported claims, the task is not research-forcing and must be hardened (add post-cutoff factual requirements) before freeze. Record probe results in the manifest.

Freezing writes an immutable manifest: set version ID, the exact 40+10 IDs, pilot question IDs (pilot items are members of the 40), the saturation formula, numeric threshold and its single pre-registered consequence, referenced product-config manifest, per-item artifact hashes, freeze timestamp. The manifest is the only input scoring accepts.

- Volatile items: the capture frozen before the first product receives the item is the scoring key. Anchor volatile prompts to an absolute as-of date; exclude unanchored "most recent X" items from the pilot subset.
- Replacement from candidate surplus is allowed only before an item is exposed to any product.
- A defect found after exposure never mutates the key in place: it creates a new set version and triggers the pre-registered all-product rerun-or-abort rule.

## Failure cases

| Failure | Rule |
|---|---|
| Source paywalled or login-gated | Drop; contestants must be able to reach the source class |
| Drafting agent cites a URL that does not resolve or lacks the answer | Verification kills it; repeated offenses discard that agent's whole batch |
| Fresh document, old fact | `fact_first_public_at` check kills it |
| Answer changes before exposure | Re-verify, update key or replace from surplus; log it |
| Answer changes after exposure | New set version + pre-registered rerun/abort rule; never edit the scored key |
| Pool misses a quota | Balance phase blocks handoff until another harvest round fills it |
| Refresh regenerates instead of merging | Wrong: load existing pool, replace only dead/decayed entries |

## Integration points

- Spec: `aimultiple-benchmark-spec-template` (the spec this set implements)
- Research-task gates and judging: `aimultiple-open-ended-judging`
- Before implementation/run: `aimultiple-benchmark-preflight-check`
- Methodology internals: `aimultiple-benchmark-methodology-design`
