---
name: aimultiple-article-checklist
description: |
  End-to-end quality protocol for AIMultiple research articles. Covers topic research, sentence-level writing, structure, linking, Surfer SEO optimization, sponsorship handling, and WordPress publishing. Use when drafting a new article, reviewing a draft, scoring a draft against the AIMultiple standard, or deciding whether a draft is publish-ready. Without this skill, drafts drift toward paraphrase, weak sourcing, templated structure, and publishing mistakes that damage rankings or customer trust.
---

# AIMultiple Article Checklist

## When to use

Triggered by any of:
- "review this draft"
- "is this article ready to publish"
- "score this article"
- "check this against our checklist"
- "what is missing from this draft"
- Any draft posted in chat with >300 words and a clear AIMultiple topic

## Step zero: read the reference article

**Before drafting or restructuring anything, read `drafts/agentic-llm-article-2026-06.md`.** It is the canonical shape for a benchmark article and the team has invested the most effort in it. The rules below describe that shape; the file demonstrates it, which is faster and less ambiguous.

What to copy from it: a two-sentence intro with no header; `## <direct noun-phrase H2>` then the chart embed, then a one-line note on sample size, then three to six standalone takeaway paragraphs; H3s for sub-results; methodology after the results, not before.

`drafts/agentic-it-final.md` is a counter-example on structure: a claim-sentence H2 and a 168-word intro. Do not use it as a model.

## Guiding principle

The article must be better than every other Google result for its keyword. If it is not, it should not be published. Everything below serves that one test.

## Mechanical lint

Run before delivering any draft:

```
python3 skills/aimultiple-article-checklist/lint_article.py <draft.md>
```

It checks the rules in this file that are mechanical: claim-sentence H2s, intro length, paragraphs over 430 characters, bold budget, year in a header, title-cased headers, chart description blocks, empty or oversized H2 sections, banned characters, filler. FAIL blocks delivery; WARN is the author's call. Everything it cannot check, research depth, source quality, Surfer score, and whether a takeaway is actually non-obvious, still needs a human read. **A rule enforced nowhere is not a rule: if a new structural rule lands in this file and is mechanical, add it to the script in the same edit.**

## Four-phase review

The skill runs in four phases. For each, the high-level rules live here and the granular rules live in `references/`. Load the reference file only when drilling into that phase.

### Phase 1. Research depth (pre-writing)

Before writing begins, the author must:
1. Understand the topic deeply. No sentence is allowed that the author cannot explain unaided.
2. Read the top 3 US Google results for the keyword.
3. Check whether AIMultiple already published on the topic and reference prior articles.
4. Read recent (<2 years) reports from McKinsey, BCG, Bain, IBM, Google, Deloitte, EY, KPMG, PwC, Gartner, Forrester, IDC, G2, plus AIMultiple's great reports folder.
5. Use Surfer SERP Analyzer for the keyword. Study competitor articles with content score >66. Take notes on titles, H2s, H3s, images, tables.
6. Decide actionable recommendations the article will give readers. Explain trade-offs. Do not give vague advice.
7. Kill the article if it adds no original thinking. A single-source article is not worth writing.
8. Identify subtopics via Surfer Questions, answerthepublic, AlsoAsked.
9. Choose the archetype and follow its structure.
10. For vendor-feature articles, open a Sedat card via Vedat before writing.

Detail: see `references/research.md`.

### Phase 2. Sentence-level quality

Every sentence must be:
- Relevant.
- Data-driven.
- Specific.
- Succinct (Hemingway style).
- Original. No paraphrased competitor text. Paraphrasing is machine work, not analyst work.

Banned patterns:
- Em dash character.
- Filler words (already, basically, simply, just, very, more and more, these days, over time, in fact, etc.). Full list in `references/writing.md`.
- Unprofessional, salesy, or hurtful expressions.
- Sarcasm and double negatives.
- Capitalized generic tech terms (big data, machine learning).
- Precision theater (never "20.37% CAGR" on a market prediction; round to "20% p.a.").
- Passive voice beyond ~5% of sentences.
- "Top 3 in industry X" without a sourced citation.
- Time-relative hooks that will rot ("interest grew X% this month"). Use absolute dates.
- Superficial marketing distinctions ("AI-powered vs AI-native"). Cut or name the real difference.
- Embellished facts. State the fact, then the implication.

Numerical formatting:
- Consistent decimal precision across all numbers in a table. If some cells show two decimals, `1` becomes `1.00`.
- If trailing decimals are all zero across all rows, drop them entirely. `97.000` becomes `97`.
- Never undersell effort. If a benchmark scored 200 deliverables, do not frame it as "10 tasks".

Paragraph rules:
- Open with a summary that promises the value to come.
- Max 6 lines or 430 characters.
- One idea per paragraph.

Originality test: if deleting a sentence changes nothing, delete it. If it could appear in any article on any topic, rewrite it around a concrete fact.

Detail: see `references/writing.md`. Generic anti-slop rules live in the `aimultiple-anti-slop` skill and should be loaded in parallel.

### Phase 3. Structure, linking, SEO, sponsorship

**Structure**
- Always start with H2. Never open with H3 or H4.
- H2 sections must have H3s if there is material to split.
- No section over ~40% of the article without H3s.
- No two H2s back to back with no content between.
- Articles >500 words need more than two H2s.
- Two H2s must not share identical text (breaks the table of contents).
- No year in headers. Headers rot otherwise.
- Lowercase common nouns in H2/H3 headers. Only proper nouns capitalized. Title-case-everywhere is an AI slop signal.
- **H2s are direct noun phrases naming a section, never claim sentences.** "TSC benchmark results", "Cost & success comparison", "Tool calls per task". Not "A broad-panel shortlist does not carry to multivariate data", not "Split design changes the reported result on subject-structured data". The finding belongs in the takeaways under the chart, where it can carry its numbers and its caveats. Questions are the one exception: "What are agentic LLM systems?" is house style.
- **A finding that reads as a sentence is an H3 at most, and usually a takeaway instead.** If a section needs a claim in its header to make sense, the claim is not yet stated clearly enough in the body.
- Open the article with the most interesting element (key list, chart, or comparison), not taxonomy or intro boilerplate. The first scroll is the reader's attention budget.
- Include at least one element per article. Top performers: TablePress, AIM List. Top combinations: AIM Chart + TablePress; AIM List + TablePress; MaxButton + Use Cases.
- Put the main comparison table above the fold.
- Do not duplicate the table of contents inside the intro. It is a cheap time-on-page trick that hurts reader satisfaction.
- Replace wall-of-text explanations with AIMList format whenever the content is listy.

**Intro**
- Single most important section. Readers decide to stay in the first view.
- A few sentences only. On a 390x844 mobile viewport, the above-the-fold should not look like a wall.
- Pick a structure: SCIQA, SCQA, or SCR.
- Must be better than the intros of the top 3 Google results on at least one of: communication clarity or insight density.

**Charts, tables, and data presentation**
- Chart first, prose second. The highlighted takeaway goes below the chart. Readers scan visuals before text.
- **Never embed a description block on a chart.** The article carries the embed shortcode and nothing else: `[nivo_charts id="177006" /]`. What the chart means, what it excludes, what it does not license the reader to conclude, all of that is body text under the chart. A caption block inside the article is not the house format and does not render.
- **Takeaways under a chart: three to six standalone paragraphs, one claim each.** Lead with the claim, carry the number in the same sentence, and stop. No bold lead-ins: bolding every opener is the templated-structure pattern. No bullet list. If a takeaway only restates what the chart axis already says, cut it.
- **Takeaways must be non-obvious.** "Model A scored highest" is the chart, not a takeaway. What belongs there: where two metrics disagree, where a cheap method matches an expensive one, where the ranking is unstable, where the winner's margin does not survive correction, where a result reverses inside the aggregate. If the section has no non-obvious reading, it may not need prose at all.
- **Any disclosure the methodology requires travels with the chart into the body text.** When a statistical caveat is mandatory (interval type, panel size, what did not survive correction, which rows are excluded), it is a requirement on the section's prose, not on a caption. Verify each one landed after any restructure.
- For price-vs-accuracy comparisons (benchmark scatter, cost vs quality), open with an XY scatter chart. The trade-off needs to be visible in one glance.
- When multiple metrics point the same direction, consider combining them into a single composite metric (events/sec/$, or similar). One composite chart beats three separate charts.
- If every vendor has a feature, do not put it in a comparison table. Note it in prose. A column of yes/yes/yes/yes adds nothing.
- If every cell in a comparison column is "no" (all red), drop the column and move the differentiator into prose. An all-red column is punitive without being informative.
- Feature markers should be neutral present/absent. Do not mix emoji and text in the same cell. Put context in the vendor write-up, not inside the cell.
- Short column names only. Use asterisks and a glossary below the table for long definitions.
- Charts built on averaged values must show the data point count per bucket. A two-point average and a twenty-point average should not look identical.
- Never reuse the same graphic across different articles. Readers notice.
- Consolidate a vendor's multiple product charts into one chart with labeled categories when possible. One labeled chart beats three tabbed buttons.
- Never invent data points to fill a chart. Show only real data.
- Benchmark details are not the lead. The benchmark result is the lead. Open with a chart, a table, or a verbal summary of the finding, then explain how it was measured.

**Benchmark review** (applies when the article is a benchmark or includes benchmark results)
- If a good model scores 90% or higher on the benchmark, the benchmark has no information value. Design a harder one before publishing.
- Benchmark rankings need confidence intervals. Single-run numbers are not statistically significant. Run each task multiple times.
- Define technical terms the first time they appear.
- Drop subjective criteria from the benchmark if outputs do not differ meaningfully on them. Subjective plus no-differentiation equals noise.
- Do not undersell the effort. Frame the benchmark by the real number of deliverables, not the headline task count.
- New benchmarks go to the social sharing channel as soon as they are live.

**Linking**
- Anchor text must describe the destination accurately. Do not link entire sentences. Link the anchor phrase only.
- "Based on X reviews" is not useful anchor text. Drop it.
- Every article has a CTA: at minimum, a link to a relevant AIMultiple vendor list (e.g. `/synthetic-data-generator`).
- Link to relevant AIMultiple articles (internal links drive growth).
- Internal links: no "open in new tab". Verify they point to `research.aimultiple.com` or `aimultiple.com`, not `research-headless.aimultiple.com` (WordPress auto-rewrite bug).
- External links: "open in new tab" enabled.
- External sources: check domain authority and spam risk with websiteseochecker.com. DA <40 or spam risk >1 is a red flag unless the source is clearly trustworthy (official site, dataset, named research).
- Do not link to non-customer B2B vendors for free. Exceptions: top-solutions lists, articles about a sponsor competitor, industry-analyst reports. When the exception applies, minimize anchor text and link visibility for non-sponsors.
- Customer URLs must carry the customer tracking tag.
- Section-link descriptions should carry the claim, not just the section name. "Agents vs Deep Research Models demonstrates agents are cheaper while providing comparable accuracy" beats "Agents vs Deep Research Models".
- When contradictory statements appear in the same section, delete both rather than reconcile.
- Broken internal links must be fixed at every article update. Links that loop back to the same article count as broken.

**Surfer SEO**
- Write inside Surfer Content Editor against the target keyword.
- Target a content score above 66 AND above the average of the page-1 competitors. Ideally above the highest-scoring competitor.
- Use "Insert terms" carefully. Read every suggestion; many do not make sense.
- Never accept keyword stuffing. If Surfer demands more keywords than the main body can absorb, create an FAQ by RankMath section at the bottom for the leftover coverage.

**Sponsorship**
- TOFU articles carry no sponsored sections.
- BoFU articles concentrate sponsored content.
- Each article has one primary sponsor per topic space. Job scheduler articles link only Run My Jobs. Winshuttle mentions link only Run My Jobs. Three sponsors in one article dilutes both the sponsor relationship and the reader experience.
- Every sponsored section contains a link to a page with a conversion form (contact / demo request). Bare vendor content URLs with no form are not acceptable.
- Do not click sponsor links. It looks like fraud to the sponsor and AIMultiple.
- Avoid mentioning non-sponsors. Named exceptions only.
- No absolute claims like "X is the best solution for Y". Stick to facts and trade-offs.

Detail: see `references/structure.md`, `references/linking.md`, `references/surfer.md`, `references/sponsorship.md`.

### Phase 4. Publishing checklist

Before hitting publish, confirm:
1. Title: carries the current year until June if applicable; includes a specific number when it can be justified; never has the year baked into an H2.
2. Permalink: matches the target keyword, not the title. WordPress rewrites permalinks the first time you save, so verify manually.
3. Meta description / snippet: includes all relevant terms, excludes filler like "this article".
4. Category: single, leaf-level. Exception: tech+industry articles (e.g. `chatgpt-use-cases-fashion`) get two.
5. Archetype tag set.
6. Featured image set.
7. Every internal link resolves to `research.aimultiple.com` or `aimultiple.com`.
8. Every external link passes the domain authority / spam risk check.
9. `NewArticleTag` present on new articles. `EditTag` present on articles the analyst wrote or substantively edited, one per article, old editors removed.
10. Plagiarism check via smallseotools plagiarism checker returns clean.
11. Bold text is under 5% of body text.
12. CTA exists at or near the end.
13. Intro passes the top-3 Google comparison test.
14. Cache-busted verification: after editing, append `?cachebuster` to the URL and confirm your edits are live. WordPress and Cloudflare caching both bite.
15. For new benchmarks, posted to the social sharing channel.

Detail: see `references/publishing.md`.

## Red flags that fail the article immediately

Return FAIL (not conditional pass) if any of the following are present:
- A claim without a source.
- A copy-paste paragraph of more than a few words from another site.
- Passive voice over ~10%.
- A single H2 that eats >50% of the body with no H3 split.
- A sponsored section with no conversion-form link.
- A non-sponsor vendor named with absolute language ("the best", "the top").
- Year embedded in an H2 or H3.
- Permalink not matching the target keyword.
- Missing `EditTag`.
- Benchmark with a best-model score of 90% or above (benchmark has no information value).
- Benchmark rankings without confidence intervals or multi-run evidence.
- Invented data points in a chart.
- Double-precision market sizing numbers.
- Time-relative hooks in the intro ("this month", "recently").

## Review output format

When reviewing a draft, return:

```
Article: <slug or title>
Target keyword: <keyword>
Phase 1 — Research depth:   <PASS / CONDITIONAL / FAIL>   <one-line reason>
Phase 2 — Writing quality:  <PASS / CONDITIONAL / FAIL>   <one-line reason>
Phase 3 — Structure/SEO:    <PASS / CONDITIONAL / FAIL>   <one-line reason>
Phase 4 — Publishing ready: <PASS / CONDITIONAL / FAIL>   <one-line reason>

Overall: <PUBLISH / FIX AND RESUBMIT / REWRITE>

Blocking issues:
1. <specific fix, with paragraph or H2 reference>
2. ...

Non-blocking nits:
1. <minor style fix>
2. ...
```

Be specific. "Fix the intro" is not actionable. "Rewrite sentence 2 of the intro to drop the filler word 'basically'" is.

## Integration

- Load `aimultiple-anti-slop` for sentence-level enforcement.
- Load `aimultiple-source-validation` when checking claim evidence.
- Load `aimultiple-publication-quality-gate` for the final pre-share sign-off (this skill covers AIMultiple-specific publishing mechanics; the quality gate covers generic research-output standards).
