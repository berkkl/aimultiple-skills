---
name: aimultiple-publication-quality-gate
description: |
  Final pre-publish quality gate for AIMultiple outputs: articles, benchmark writeups, scorecards, vendor recommendation memos. Use at the end of every draft cycle, after writing and research are complete, before anything is shared externally or posted. Also the home of the cross-model Codex review: invoke this skill whenever the user asks for a codex review, a second-model review, an AI-slop or language check on a draft, or says the copy "sounds like AI". Carries both review briefs and the `codex exec` recipe, including the foreground-only rule. Without this skill, factual, methodology, and decision-quality defects survive into publication and damage AIMultiple's rankings and customer trust.
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

Two passes, different briefs, both required. They contradict each other on purpose: the
reader pass forbids wording suggestions, the register pass is entirely about wording.

| Pass | Brief | Finds |
|---|---|---|
| Reader | `review-prompt.md` | fragments, claims that outrun the statistics, undefined terms |
| Register | `slop-prompt.md` | colon reveals, meta-statements, aphorisms, personification, invented labels, deletable sentences |

```bash
codex exec --skip-git-repo-check "$(cat skills/aimultiple-publication-quality-gate/slop-prompt.md)
<path/to/draft.md>" 2>&1 | tee /tmp/codex-out.txt
```

Let Codex READ the draft from its path rather than pasting the text in. On 2026-08-24 that is
what let it cross-check figures against the repo's chart JSONs and findings files and catch a
product count, a mislabelled standard deviation and two internal contradictions.

`--skip-git-repo-check` is required: the AIM Articles workspace is not a git repository, and
without it `codex exec` prints "Not inside a trusted directory" and exits 0 with no output.
Use `-c model_reasoning_effort=xhigh` for a long article. Use the default `~/.codex` profile:
this is not judge work and it does not burn the judge quota.

### Running it, and the failure that wastes an hour

**Run it in the foreground.** Backgrounded `codex exec` returned exit 0 with the prompt echoed
and no answer, three times in a row on 2026-08-24, which reads exactly like a broken CLI. The
same command in the foreground with a long timeout produced a 51-finding audit. Before
concluding Codex is broken, smoke-test it: `codex exec --skip-git-repo-check 'Reply with
exactly: PONG'`.

**Extract the answer.** Codex echoes its whole tool trace, so the output can be hundreds of
kilobytes. The answer is the last block:

```bash
last=$(grep -n '^codex$' /tmp/codex-out.txt | tail -1 | cut -d: -f1)
sed -n "$((last+1)),\$p" /tmp/codex-out.txt | sed '/^tokens used$/,$d'
```

**A models-cache error is noise, not the cause.** `failed to load models cache: missing field
base_instructions` appears even on successful runs. If answers genuinely stop, move the file
aside and it regenerates: `mv ~/.codex/models_cache.json{,.corrupt}`.

The reviewer brief is a reader brief, not an editor brief. Three questions only:
1. Does every sentence parse, and does any of them need a second read?
2. Does the headline claim match what the statistics in the body actually support?
3. Is any term used before it is defined, or any characterization of a named method contradicted by that method's own source?

Findings are triaged, not applied wholesale. A cross-model reviewer will also propose rewrites
that restore the padding the cut pass removed; reject those.

### Triage, with real examples

Verify every finding against the draft and the data before applying it. From the 51 findings on
the MCP gateway article, 2026-08-24:

Accepted, all real defects the author missed:
- `**Products (7):**` followed by six product names.
- "Cortx is the only product that states the true reason" while the table two sections up says
  TrueFoundry also names the restriction.
- "authorization ... do not depend on the caller" in a benchmark whose authorization probe is
  defined by the caller's credential.
- A between-repetition standard deviation called a "spread".
- "the product's entire history" where the evidence was 40 records over one month.

Rejected:
- A claimed cross-section repetition that occurs exactly once in the draft.
- A claim that a finding rested only on a screenshot, when it had been verified through the
  product's API earlier in the session.

**Re-run `lint_article.py` after applying the fixes.** The fixes themselves introduced a filler
word and a relative-clause fragment on 2026-08-24. A review pass that ends without a clean lint
is not finished.

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
