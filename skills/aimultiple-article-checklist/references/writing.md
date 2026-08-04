# Writing quality — detail

The generic anti-slop rules live in the `aimultiple-anti-slop` skill. Load that in parallel. This file covers AIMultiple-specific additions.

## Sentence test

Every sentence must satisfy all four:
1. Relevant to the reader's decision.
2. Data-driven (named number, named source, named case).
3. Specific (not "fast", but "20 days for 100-participant projects").
4. Succinct (Hemingway style, no filler).

## Banned filler words

Cut these unless they carry real meaning:

already, apparently, basically, by its very nature, day by day, ever, for a long time, generally, in actuality, in reality, in fact, just, more and more, much, only, our article, over time, simply, this article, these days, very.

Replacements:
- "for a long time" → state the duration.
- "this article" / "our article" → drop entirely and lead with the content.
- "very" → drop or replace with a specific intensifier.

## Unprofessional vocabulary

Cut:
- Swearwords.
- Words that can be hurtful to groups.
- Overused colloquials: huge, awesome, enormous, gigantic.
- Salesy expressions: "intuitive interface", "amazing solution". Exception: source-attributed quotes.
- Rarely used words readers cannot parse.

## Machine tells

- Em dash (`—`). Use a period and two sentences instead.
- "It is not X, it is Y" framing.
- Italic for emphasis (only italicize direct quotes).
- Templated paragraph patterns where every paragraph shares the same structure.
- Time-relative claims ("recently", "this month", "as of December 2025"). Use absolute dates or cut.
- Superficial marketing distinctions ("AI-powered vs AI-native"). Cut or name the real difference.

## Style guide

Use AP Style Guide for grammar, punctuation, numbers, capitalization, and abbreviations.

Exception: AIMultiple bullet list conventions override AP.

Do not capitalize: big data, machine learning, artificial intelligence (and similar generic tech terms).

H2 and H3 headers: lowercase common nouns. Only proper nouns capitalized. Title-case-every-word headers are an AI slop signal.

## Voice

Default to active voice. Passive voice allowed in roughly 5% of sentences or less, when it genuinely reads better (e.g. emphasizing the object).

## Precision

Never quote predictions to more than 2 significant figures. "Gartner predicts 5.67% CAGR reaching $6.87 Bn in 2025" becomes "Gartner predicts 6% per annum, reaching $7 Bn in 2025". Precision implies certainty that predictions do not have.

Never publish double-precision market-sizing figures. The underlying data does not support it and it damages credibility.

## Numerical formatting

- Consistent decimal precision across all numbers inside a single table or chart. If some cells show two decimals, every cell shows two decimals. `1` becomes `1.00`.
- If trailing decimals are all zero across every row in a column, drop them entirely. `97.000` becomes `97`, or `97.0` if the column is mostly integers with one exception.
- Numbers in prose follow AP Style: spell out one through nine, numerals for ten and above. Exceptions: percentages, units, and measurements always use numerals.

## Do not undersell the work

If a benchmark processed 200 deliverables, do not frame the intro as "we scored 10 tasks". The analyst-effort number is the honest number. Underselling is as misleading as overselling and it damages the reader's ability to weigh the result.

## Data-driven sourcing

Every factual claim carries a source. Use the `[efn_note]` format for citations. Example:

> The market is expected to grow at 20% per annum.[efn_note]McKinsey research on XXX. McKinsey. Retrieved on January 22, 2024[/efn_note]

Use the latest available version of any third-party report. A 2023 Goldman Sachs report where a 2025 version exists is a quality red flag.

## Paragraph rules

- Open with a summary that promises the value to come.
- Max 6 lines or 430 characters. Readers skip longer paragraphs.
- One new idea per paragraph.

## Vocabulary diversity

Repeating "tool", "platform", "solution" throughout an article is a slop tell. Use synonyms:
- "provide" → empower, allow, offer, facilitate, equip, streamline, enhance, accommodate
- "this tool" → this application, this platform, this library (as fits)

Vary sentence structures across the article:
- Active ("X provides Y") alternating with cause-effect ("Because X, Y becomes possible") alternating with passive when natural ("Y is enabled by X").

## Originality test

Paraphrasing is not analysis. Example:
- Original source: "RPA is a technology that accelerates the growth of manufacturing businesses."
- Plagiarism (exact or near-exact): both of the above and "Robotic Process Automation is a technology that speeds up the growth of manufacturing firms."
- Acceptable: "Manufacturers rely on legacy systems for machine configuration. They leverage RPA to increase automation rate in their factories, which helps them grow faster."

The acceptable version adds specificity the source did not.

## Grammar tools

Grammarly and Toastbot are allowed, but do not accept every suggestion blindly. They are machine learning tools and get things wrong.

## Final check

Run smallseotools plagiarism checker before publishing. Any hit is a blocker.
