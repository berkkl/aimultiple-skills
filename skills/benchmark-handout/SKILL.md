---
name: benchmark-handout
description: Write or audit a benchmark write-up as input for the AIMultiple article agent, the benchmark-mode article pipeline that turns a handout into a published article. Use ONLY when the user explicitly names that pipeline, for example "prepare this for the AIMultiple article agent", "write a handout for the article agent", "is this benchmark doc ready for the article pipeline", "audit this against the article agent's requirements". Do NOT use for general benchmark documentation, evaluation write-ups, research reports, results summaries, internal handoff documents, or any request that does not name the AIMultiple article agent or its article pipeline. Those belong to other skills, and this one encodes requirements specific to one pipeline that would be wrong elsewhere.
---

# Benchmark handout

## Scope check first

This skill encodes the input requirements of one specific system: AIMultiple's
benchmark-mode article pipeline. If the user did not name that pipeline, stop
and say so rather than applying these rules.

The requirements here are not general good practice for writing up a benchmark.
They exist because of how this particular pipeline parses a document, and
several would be actively unhelpful elsewhere: a research paper does not need a
`Commercial products: yes` line, and an internal results memo does not need
`[CHART C1: ...]` placeholders carrying their own data.

If a teammate asks for help documenting a benchmark without mentioning the
article agent, they probably want a different skill or no skill at all. Say
something like: "I have a skill for preparing benchmark handouts specifically
for the AIMultiple article agent. Is that what this is for, or do you want a
general write-up?"

## What this is for

A benchmark write-up gets read by an article agent, not only by people. The agent
extracts a fixed set of facts from it, researches the products on the web, and
assembles an article. It does that well when the document states things plainly
and badly when it has to infer them.

This skill is about the difference. Most of what goes wrong downstream is not the
agent reasoning poorly. It is the agent reasoning correctly from a document that
left something out.

## Two modes

**Writing a new handout**: work through the sections below with the author,
then produce the document. `assets/TEMPLATE.md` is a fill-in skeleton.

**Auditing an existing draft**: read it against the checklist at the end, report
what is missing, and offer to fix each gap. Do not rewrite the author's prose.
The hedges and qualifications in a benchmark write-up are usually load-bearing
and were argued over.

## Never invent a name, with one exception

This applies to you while you write or audit, and it is the rule the document
should make unnecessary downstream.

If something has an official name, use it exactly as it is officially written.
If it has no official name, describe it. Do not coin one.

**The exception is the name of our own benchmark.** We ran it, so we are the
ones entitled to name it, and "official" already means the owner's naming. When
the benchmarker has given the work a name, that name wins and you use it exactly.
When they have not, the house convention applies:

> AIM &lt;Topic&gt; Benchmark

built from the article topic: `tabular-models` gives "AIM Tabular Models
Benchmark", `agentic-it` gives "AIM Agentic IT Benchmark". Write it into the
`Benchmark name:` line rather than leaving the line to say "none". A name in the
document is a name the author can see and object to; a name supplied later is
one nobody reviewed.

The exception stops at our own benchmark. Everything the benchmark touches, and
everything anyone else owns, still falls under the rule below.

Official means published or otherwise established by whoever owns the thing: the
product's own site for a product, the paper or repository for a method, the
team's own naming for internal work. "GitHub Copilot Code Review", not "Copilot".
"HIVE-COTE 2", not "HC2", unless the source itself uses the short form.

Coining a name is tempting because a named thing reads better than a described
one, and because a name fills a field that would otherwise sit empty. Both are
bad reasons. A benchmark name that appears for the first time in the write-up
will propagate into a published article, into how colleagues refer to the work,
and into anything that cites it. Nobody chose it, and by the time someone
notices, it is the name.

The same holds for datasets, panels, metrics, scoring scales, phases, chart
identifiers, and internal tooling. "The 15-dataset univariate panel" is a
description and is fine. "UniPanel-15" is a name, and inventing it is not yours
to do.

Where a name for one of those is genuinely missing and would help, ask the
author rather than supplying one:

> The write-up calls this "the 15-dataset univariate panel" throughout. Does
> that panel have an official name, or should the article keep describing it?

For the benchmark's own name, ask the narrower question instead:

> Has this benchmark been given a name? If not, the handout will call it
> "AIM &lt;Topic&gt; Benchmark", which is our house convention for our own work.

**If the benchmarker deliberately wants no name at all**, that is a real
position and it needs to be stated as a rule, not as a blank. A replication
study may avoid a name precisely because naming it implies a contribution it
does not claim. Put it under `## Writing rules` as a constraint with its reason:

> - Never give this benchmark a name. It replicates published work and a name
>   would imply an original contribution. Refer to it as "the benchmark".

Stated there, it reaches the writer as a hard constraint and outranks the house
convention. Written as "Benchmark name: none", it does not: the pipeline reads
that as an empty field and fills it.

The same restraint applies to numbers, and for the same reason. If the document
does not state a figure, do not supply a plausible one. Ask, or leave it out.

## What the agent extracts

Read `references/pipeline-contract.md` for the exact field list and how each one
is used. The short version: the agent pulls the benchmark's name, dataset size,
the roster of what was tested, the results table, the winner, chart specs,
per-item findings, methodology, caveats, writing constraints, and mandatory
disclosures. Anything not in the document cannot be recovered.

## The rules that matter most

These are ordered by how much damage their absence causes, measured across real
runs of the pipeline.

### 1. Name every item you benchmarked, in one place

This is the single most common failure. A write-up mentions a model where it
makes a specific point and never lists the full roster, so the agent finds four
names in a document about eleven models. It then pads the article with products
it discovered on the web, and a heading claims eleven while the section shows
ten, six of which were never benchmarked.

Nothing downstream can fix this. The agent cannot invent names it was not given.

Put an explicit list near the top:

```
Benchmarked: GPT 5.6 Sol, MiniMax M3, Claude Sonnet 5, GLM 5.2, Claude Opus 5,
Gemini 3.1 Pro, Grok 4.3, DeepSeek V4, Qwen 3.6 Plus, Kimi K3, Mistral Large 3.
```

If a benchmarked unit is a combination rather than a plain product, write the
combination: "Claude Opus 5 under Claude Code", not "Claude Opus 5". The agent
preserves that pairing and it matters for the results section.

Name the benchmark itself in the same place, or say plainly that it has no name:

```
Benchmark name: RevEval (AI Code Review Eval).
```

```
Benchmark name: none. Refer to it as "the benchmark".
```

Leaving this blank is where invented names come from. With nothing to read, the
extractor takes whatever looks like a name: it has produced "Can" from a title
beginning "Can AI agents...", and article slugs like "agentic-it" and "ai-vc"
used as if they were the benchmark's name. Those then appear in the published
article. One line prevents it, and "none" is a perfectly good answer.

### 2. State the topic in the document's own words

The agent takes its research topic from the article slug. Short SEO slugs are
often ambiguous: `ai-vc` was read as "AI venture capital research tooling", so
the agent researched PitchBook and CB Insights for an article that benchmarked
language models. That run cost real money and was thrown away.

Add one line stating what category the benchmarked items belong to, and what
they are not:

```
Category: large language models with live web access. Not research platforms,
data vendors, or market intelligence tools.
```

### 3. Describe every chart, with its numbers

A chart placeholder like `[nivo_charts id="" /]` carries no information. The
agent will invent a chart description from whatever numbers it can find nearby,
which may not be the figure you intend to build.

Write the figure as a sentence with the data in it:

```
[CHART C1: horizontal bar chart. Share of pull requests where each tool scored
highest, across 309 pull requests. CodeRabbit 51%, Greptile 24%, GitHub Copilot
Code Review 15%, Cursor BugBot 10%]
```

Chart IDs may carry a letter suffix (C7, C7b). Keep the numbers inside the
brackets: a reader who cannot see the figure still gets the data, and the agent
carries the placeholder through unchanged for a designer to build from.

### 4. Say whether there is a winner, in one explicit sentence

The agent guesses this from tone, and it guesses wrong in both directions. A
write-up saying "scores sit close together" and "no model shows much judgment"
was read as declining to name a winner, when it plainly stated one. A write-up
that genuinely refuses to crown one needs that refusal stated, or the agent may
crown one anyway.

Write one of:

```
Winner: Claude Opus 5, at 89.1 against 85.0 for the next arm.
```

```
No single winner. HC2 and RocketPFN split first place 47.8% to 44.2% under a
5,000-draw bootstrap and are not separated by this evidence.
```

### 5. State your writing rules as rules

This is where the largest quality difference appears. The same benchmark yielded
27 extractable writing constraints when its rules were written as an explicit
list, and 9 when the same constraints were only implied by careful phrasing in
prose. The agent cannot reliably infer a rule from an author writing carefully.

Write them under a heading, one per line, with the reason:

```
## Writing rules

- Never name a single winner. HC2 and RocketPFN split first place and the top
  four share a clique. Allowed: "HC2 ranked first on mean rank, RocketPFN first
  on mean accuracy, and the two are not separated." Banned: any sentence with
  one name and the word best.
- Never write "statistically indistinguishable" or "equivalent". No equivalence
  margin was prespecified, so a non-significant result means no difference was
  detected, not that none exists.
- Never attribute the SleepEDF result to leakage. The data cannot separate
  subject-identity leakage from genuine variation in subject difficulty. Write
  "split-associated gap".
```

The reason matters as much as the rule. A rule with its reason attached survives
paraphrase; a bare ban only catches the exact string.

### 6. Say what the rule does not ban

A ban gets over-applied, and an over-applied ban does its own damage. The agent
reads "never rank A against B" and stops distinguishing A from B at all, which
can make the article less accurate than the error the rule was written to
prevent.

This is a real case. A handout carried:

```
- Never write that the Bright Data command-line interface beat the Bright Data
  MCP server. They split the five runs 3-1 with one tie. Allowed: "a Bright Data
  interface led every run". Banned: any sentence ranking the two against each
  other.
```

The rule is correct and the agent obeyed it. It then wrote:

> A Bright Data interface completed at least 44.6 tasks out of 100 on average.

44.6 is the command-line interface's mean. The MCP server's is 42.2. So the
sentence is false for one of the two things it covers. The agent took the
Allowed phrasing, which was written for the claim about who led each run, and
reused it for a claim about one interface's own average, where it does not hold.

The rule banned a **comparison**. The agent applied it to **attribution**.

Write the boundary into the rule:

```
- Never write that the Bright Data command-line interface beat the Bright Data
  MCP server. They split the five runs 3-1 with one tie. Allowed: "a Bright Data
  interface led every run", and reporting each interface's own figures under its
  own name, for example "the command-line interface averaged 44.6 and the MCP
  server 42.2". Banned: any sentence ranking the two against each other. This
  rule bans the comparison, not the attribution: every figure still belongs to
  the interface that produced it.
```

The test to apply to each of your rules: **what would obeying this too
enthusiastically cost?** If the answer is a number losing its owner, a product
losing its name, or a finding becoming vague, say so in the rule. One sentence
naming what stays allowed is usually enough.

Watch for it especially on rules that ban naming, ranking, or comparing. Those
are the ones an agent generalises from "do not compare these two" into "do not
mention these two separately".

### 7. Name the wrong conclusion, not just the wrong words

A ban list catches phrasings. It does not catch scope errors. "RocketPFN
outperformed the foundation models" breaks no ban and is still a category error
if RocketPFN is not a foundation model in your taxonomy.

For each significant finding, add what it does **not** support:

```
**Finding.** TimEE's prediction depends on which other test instances share the
inference call.
**Holds on.** All TimEE cells.
**Required qualifier.** Both machines differ in hardware in both strata. Only
the contrast between strata is evidence.
**Does not support.** That TimEE's scores are inflated in either direction, or
that its published rank changes.
```

That "does not support" line is the highest-value sentence in a handout. It is
the failure a ban list cannot prevent.

### 8. List anything that must appear in the article

If a caveat has to reach the reader, say so explicitly. The agent treats these
as required and places them in the body.

```
## Must appear in the article

- The primary table is univariate-only. Two methods have no multivariate support
  and pin the complete-case intersection.
- ROC-AUC was the declared primary metric and is unavailable for 5 of 7 models.
  Accuracy became the comparison metric without a recorded decision.
```

### 9. Say whether the benchmarked items are commercial

The agent builds a pricing section for commercial products and skips it for
research methods and open-source algorithms. Getting this wrong either wastes a
research call producing "not enough data", or drops a pricing table you wanted.

One line: `Commercial products: yes` or `Commercial products: no, these are
research methods with no pricing.`

### 10. Mark anything that must not be published

Sign-off gates, reviewer names, internal links, open questions, and TODOs get
stripped only if they are marked. Put them under a heading containing "not for
publication", "draft notes", or "internal only", at the end of the document.
Everything from that heading to the next top-level heading is removed.

## Structure

Order is flexible; the agent reads by meaning. This order works well:

1. Title and a one-paragraph summary with the headline number
2. Topic and category line, roster, commercial flag
3. Results, with the table, the winner statement, and chart placeholders
4. Findings, each with its qualifier and its "does not support" line
5. Writing rules
6. Must appear in the article
7. Methodology: approach, dataset construction, environment, evaluation
8. Limitations and caveats
9. Not-for-publication notes, last

## Folder handouts

For a benchmark with data files, a folder works and is often better than one
file: narrative documents plus a `data/` directory. Add a `MANIFEST.json` at the
root to control what the agent reads.

```json
{
  "drafting_context": ["README.md", "01-design.md", "03-findings.md", "data/"],
  "excluded_from_drafting_context": ["annex-audit/", "raw/"],
  "post_draft_checker": "06-lint-checks.md",
  "valid_as_of": "2026-07-31T09:00:00Z",
  "data_frozen_at": "2026-07-29T03:00:00Z"
}
```

`drafting_context` is an ordered allow-list. Files present but unlisted are
excluded and reported, so nothing vanishes silently. Data files under 32 KB are
read whole; larger CSVs are sampled, so put the numbers the article quotes in a
small summary table rather than expecting the agent to aggregate a large one.

## Audit checklist

When reviewing an existing draft, check each and report what is missing:

- [ ] Every benchmarked item named in one explicit list
- [ ] Count in the list matches the count claimed in the title and summary
- [ ] Benchmark named, or explicitly marked as having no name
- [ ] No name in the document was invented during this pass. Anything you named
      rather than described should be flagged to the author, not left in silently
- [ ] Category line saying what these items are and are not
- [ ] Results table with the comparable numbers
- [ ] Winner stated, or no-winner stated, in one sentence
- [ ] Every chart described with its real numbers
- [ ] Each finding has a qualifier and a "does not support" line
- [ ] Writing rules stated as a list, each with its reason
- [ ] Mandatory disclosures listed
- [ ] Commercial flag present
- [ ] Methodology covers approach, dataset, environment, evaluation
- [ ] Caveats stated, not softened
- [ ] Internal notes marked not for publication

Report gaps in order of cost. A missing roster is expensive; a missing
commercial flag is cheap. Say which is which so the author can triage.
