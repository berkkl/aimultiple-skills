---
name: aimultiple-publication-quality-gate
description: |
  Review AIMultiple prose before publication or external sharing: articles, benchmark
  writeups, scorecards, and vendor memos. Use for Codex or Claude review of a draft, second-model
  review, AI-slop, reader, language or register checks, and final publication review.
  Turkish triggers: codexe review ettir, codexten geçir, Claude'a incelet, slop kontrolü, dil kontrolü,
  üslup kontrolü, AI gibi duruyor, yapay zeka yazmış gibi, yayına hazır mı, canlıya hazır mı,
  son kontrol. Includes reader and register briefs and runtime-specific CLI procedures. Source-code
  reviews belong to the code-review workflow; this prose gate does not require a git repo.
---

Codex: read [the runtime adaptations](../../codex-migration/RUNTIME.md) before
following this skill. They replace Claude-specific tool and session behavior.

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
6. Anti-slop checks (`aimultiple-anti-slop-writing`) pass.
7. Inference statements are labeled as inference, separate from observed facts.
8. Open questions are listed as open questions, not buried in prose.
9. Every major recommendation has a risk-and-limit note.
10. No unresolved placeholders, TODOs, or `{TK}` markers.
11. Methodology sections are reproducible enough for a skeptical reader to audit.
12. For articles specifically: the `aimultiple-article-checklist` publishing phase has passed (category, permalink, tags, featured image, plagiarism check, link audit).

## Cross-model review (mandatory before any article is finalized)

Cem, 2026-08-09: "LLM'le de bi review lazim finalize edince." The time-series-classification article was drafted and cut by Claude, read by Berkk, iterated, and still shipped with fragments, four-decimal numbers and a lede that claimed more than the corrected statistics supported. The author can miss its own register, so the finalize review runs on a different vendor.

Two passes, different briefs, both required. They contradict each other on purpose: the
reader pass forbids wording suggestions, the register pass is entirely about wording.

| Pass | Brief | Finds |
|---|---|---|
| Reader | `review-prompt.md` | fragments, claims that outrun the statistics, undefined terms |
| Register | `slop-prompt.md` | colon reveals, meta-statements, aphorisms, personification, invented labels, deletable sentences |

### Codex-led work: ask Claude

Run both passes through Claude Code, separately, using the same briefs above.
Follow [the Claude consultation procedure](../../codex-migration/CLAUDE-SECOND-OPINION.md)
for the command, read-only scope, model recording, and result checks. Do not run
the Sol command below from Codex as a substitute for independent-vendor review.
If Claude is unavailable, the required review remains pending. An explicit user
reviewer choice is preserved, with any authorship/independence gap disclosed.

### Claude-led work: ask Codex

The following Sol command, profile, model, and troubleshooting notes apply only
when Claude is the primary worker. Codex uses the Claude procedure above.

```bash
codex exec --skip-git-repo-check -m gpt-6.1-sol -c model_reasoning_effort=xhigh "$(cat skills/aimultiple-publication-quality-gate/slop-prompt.md)
<path/to/draft.md>" < /dev/null > /tmp/codex-out.txt 2>&1
```

**Always pass `-m gpt-6.1-sol`.** Berkk moved the gate from `gpt-5.6-sol` to `gpt-6.1-sol` on
2026-09-30. Naming the model keeps the run reproducible when the account default moves: on
2026-09-06 the default switched server-side to `gpt-6-astra`, and a bare `codex exec` on an
older CLI failed with `400 The 'gpt-6-astra' model requires a newer version of Codex`.

**6.1 Sol needs codex-cli 0.159.2 or newer.** On 2026-09-30 the Mac's `codex` (0.156.1) failed
with `400 The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account`,
which reads like an account problem but is a client-version gate. Check `codex --version`
before a gate run and upgrade if it is older. The judge install at
`~/.local/share/judge-cli-0930/node_modules/.bin/codex` (0.159.2) runs it on the default profile
if the PATH `codex` is behind.

Let Codex READ the draft from its path rather than pasting the text in. On 2026-08-24 that is
what let it cross-check figures against the repo's chart JSONs and findings files and catch a
product count, a mislabelled standard deviation and two internal contradictions.

`--skip-git-repo-check` is required: the AIM Articles workspace is not a git repository, and
without it `codex exec` prints "Not inside a trusted directory" and exits 0 with no output.
Use `-c model_reasoning_effort=xhigh` for a long article. Use the default `~/.codex` profile. It is the same agentbench@ account as the judge profile and the
benchmark VPS, so the gate draws on the judge quota: on 2026-09-06 both passes died on the usage
limit right after a 16-hour judging campaign. Do not run the gate while a campaign is live, and
expect to wait for the window to reset after one.

#### Running Codex, and the failure that wastes an hour

**Redirect stdin from `/dev/null`.** When stdin is a pipe that never closes, `codex exec`
prints `Reading additional input from stdin...` and blocks there forever, producing a 39-byte
output file and no answer. Both gate passes hung this way on 2026-08-27 until `< /dev/null`
was added. This is the real cause of the 2026-08-24 "backgrounded Codex returns nothing"
report, which was wrongly written up here as a foreground-versus-background rule; with stdin
closed, background works and is the better choice, because a long pass does not fit the 600s
foreground Bash ceiling. Before concluding Codex is broken, smoke-test it:
`codex exec --skip-git-repo-check 'Reply with exactly: PONG'`.

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

- Consumes outputs from `aimultiple-anti-slop-writing`, `aimultiple-source-validation`, and `aimultiple-article-checklist`.
- This is the last skill in the chain. Nothing runs after it.
