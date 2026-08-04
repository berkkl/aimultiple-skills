# Structure — detail

## Header hierarchy

- Always start with H2. Never open a section with H3 or H4.
- H2s contain H3s when there is material to split. A section without H3s is suspect if it is longer than ~150 words.
- No H2 may eat more than ~40% of the body without H3 subdivisions.
- Two H2s must not appear back to back with no content between them.
- Articles over 500 words need more than two H2s.
- No two H2s may share identical text. It breaks the table of contents.
- Do not put the year in any header (H2, H3, H4). Headers are expensive to update and rot.
- Lowercase common nouns in H2 and H3. Only proper nouns capitalized. Title-case-everywhere is an AI slop signal.

## Opening the article

- Open with the most interesting element: a key list, a benchmark chart, or the main comparison table. Not taxonomy, not intro boilerplate, not a definition paragraph.
- The first scroll is the reader's attention budget. Spend it on the finding, not on setup.
- Put the main comparison table above the fold.
- Do not duplicate the table of contents inside the intro. It is a cheap time-on-page trick that hurts reader satisfaction.

## Intro

The intro is the single most important section. Readers decide in the first view whether to stay.

Rules:
- A few sentences. Not a block of text.
- Check above-the-fold on a 390x844 mobile viewport. If the first screen looks like a wall, shorten.
- Pick one of: SCIQA (Situation, Complication, Implication, Question, Answer), SCQA (drop Implication), or SCR (Situation, Complication, Resolution).
- The intro must beat the intros of the top 3 Google results for the keyword on at least one of: clarity or insight density.
- Write for a working professional who will skim, not a student who will read top to bottom. Mr. Beast pacing.

The second paragraph should explain the concept and foreshadow what the article will dive into.

## Elements

Every article should carry at least one AIMultiple element. Top performers by traffic uplift:
- TablePress
- AIM List

Top combinations:
- AIM Chart + TablePress
- AIM List + TablePress
- MaxButton + Use Cases

Replace wall-of-text explanations with AIMList whenever the content is actually a list. A bulleted list rendered as AIMList gets read; a prose paragraph of the same content does not.

## Charts

- Chart first, prose second. The highlighted takeaway goes below the chart, not above.
- For price-vs-accuracy comparisons, open with an XY scatter chart. The trade-off must be visible in one glance.
- When multiple metrics point the same direction, consider a single composite metric (events/sec/$, ops per watt, or similar). One composite chart beats three separate charts when the story is the same.
- Charts built on averaged values must show the data point count per bucket. Averages of two points and averages of twenty points should not look visually identical.
- Do not reuse the same graphic across different articles. Readers notice.
- Consolidate a vendor's multiple product charts into one labeled chart when possible. One chart with labels beats three tabbed buttons.
- Never invent data points to complete a chart. If the data is not real, do not display it.
- Benchmark charts should include the number of runs and, where applicable, confidence intervals. Single-run benchmarks are not statistically significant.

## Tables

- Follow AIMultiple table best practices.
- Short column names only. Use asterisks and a glossary below the table for long definitions.
- Feature markers should be neutral present/absent. Do not mix emoji and text in the same cell. Put context in the vendor write-up, not inside the cell.
- If every vendor has a feature, do not put it in the comparison table. Note it in prose.
- If every cell in a column is "no" (all red), drop the column and move the differentiator into prose. An all-red column is punitive without being informative.
- Benchmark details are not the lead. The benchmark result is the lead. Open with the chart or table; explain the method below.
- Exception: on Discord or WhatsApp delivery, use bullet lists instead. Markdown tables render poorly.

## Images

- Follow AIMultiple image guidelines.
- Add alt text.
- Try to include a featured image.

## Bold text

Keep bold text under 5% of body text. Category labels at the start of a list item are a common acceptable use. Sentence-level bold should be rare.

## Further reading section

Optional. If present:
- A few links only. This is not a link dump.
- Do not copy-paste titles. If you use titles as anchor text, strip years.
