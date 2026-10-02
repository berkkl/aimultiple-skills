---
name: aimultiple-internal-writing
description: Writing rules for internal communication, based on ASD-STE100 Simplified Technical English. Covers YouTrack cards and comments, Slack and e-mail messages to the team or Cem, weekly summaries, internal reports and briefings, handoff prose, and Claude's chat replies to Berkk. Turkish and English. Never for articles, social posts or other published text (those use aimultiple-anti-slop-writing). Use when writing or checking any internal text, or when the user says "iç yazım", "STE", "kart dili", "mesajı sadeleştir".
---

Codex: read [the runtime adaptations](../../codex-migration/RUNTIME.md) before
following this skill. They replace Claude-specific tool and session behavior.

# Internal writing

Internal text has one job: the reader acts on it correctly after one read. This skill sets the words (Part 1) and the order of a message (Part 2). The cut pass in CLAUDE.md still applies: write, then cut toward half.

## Scope

| Text | Part 1 words | Part 2 shape |
|---|---|---|
| YouTrack card, comment | yes | yes |
| Slack or e-mail message to the team or Cem | yes | yes |
| Weekly summary, internal report, briefing | yes | yes |
| Claude's chat reply to Berkk | yes | yes |
| Handoff document | yes | no (structure comes from the handoff skill) |
| Article, social post, vendor-facing copy | no | no |
| Code, commands, log output, quoted errors | no | no |

Published text keeps its voice and follows `aimultiple-anti-slop-writing` and `aimultiple-article-checklist`. Do not carry these rules into articles.

## Part 1: words

Source: ASD-STE100 Issue 9 (2025), applied at about 80%. Use the writing rules. Do not use the approved-word dictionary, because it bans the technical nouns we need. Rule numbers in parentheses.

**Sentences**
- One instruction per sentence (5.2). An instruction has max 20 words (5.1). Any other sentence has max 25 words (6.3).
- Put a condition before its command, with a comma (5.4): "If the run fails, rerun the cell once." / "Koşu düşerse hücreyi bir kez tekrar koş."
- Do not drop words to compress (4.2). Write "Remove the rows from the table", not "Remove rows from table". Telegraph style is fine only in a list label ("GLiDE row in b_426").
- One topic per paragraph, max six sentences (6.5, 6.6). Steps go in a numbered list, one action per item.
- No semicolons (8.1). Write two sentences.

**Verbs**
- Active voice when the actor is known (3.6). "The judge scored 69 tasks", not "69 tasks were scored".
- Simple tenses only (3.2). English: no present perfect ("we ran", not "we have run"), no stacked modals ("this may help to improve" becomes "this improves"). Turkish: "-dı" for your own observed work, "-mış" only for something you did not see; no "-mektedir/-maktadır" endings.
- A verb for an action (3.7). "Analyze the log", not "perform an analysis of the log". "Logu incele", not "logun incelenmesi yapılmalıdır".
- English: no phrasal verbs (9.3) such as spin up, kick off, roll out, dive into. Use start, run, release, read.

**Words**
- One name for one thing (1.11). Use the name the repo, card or article uses, every time.
- The short common word: use (not utilize, leverage), start (not commence, initiate), help (not facilitate), make sure (not ensure), before (not prior to), about (not regarding), get (not obtain).
- Turkish: the word a person says, not a literal translation of English jargon. "klasik modellerin koşusu", not "klasik kol".
- Multi-word nouns: max three words (2.1). Unpack longer ones.
- Define an abbreviation at first use.
- No "not X, but Y" framing ("X değil, Y"). State Y.
- No marketing adjectives, hedges that carry no fact ("perhaps", "aslında", "bir nevi"), or idioms.

## Part 2: shape

The reader reads the message on a screen and acts on it. Anything below the first screen may be lost.

1. **First line = the answer or the next action.** Not context, not a plan, not a restatement of the question.
2. **No preamble, no recap, no closer.** Cut "Let me...", "Harika soru", "Özetle...", "Let me know if...", "Umarım işine yarar".
3. **Action lists have max five items.** If there are more, split into "şimdi" and "sonra", or "must" and "nice to have". A reference table or file list has no cap.
4. **Estimates in units.** Minutes, hours, days. Not "biraz zaman", "some work", "yakında".
5. **State multi-step work in every message.** "Adım 3/5 bitti: şema güncel. Sıradaki: kolonu doldur."
6. **Errors: cause, then fix.** No "Uh oh", no "bir sorun var gibi görünüyor".
7. **One issue per message.** Finish it. Put a side issue at the end as a separate question.

Break Part 2 in four cases:
- The reader asks for an explanation. Write it in full, but keep rule 2.
- A destructive action comes next. Confirm first.
- Three fix attempts failed. Stop and name the assumption that may be wrong.
- The request is truly ambiguous. Ask one question.

## Guards

- Never cut a fact, number, condition or scope qualifier to meet a length cap. "n=6", "on macOS only", "measured once" stay. A cut qualifier turns a bounded claim into an overclaim. Keep the longer sentence.
- Keep identifiers, file paths, model names, numbers and quoted error strings exactly.
- When you rewrite someone's text, change the smallest span that fixes a rule.

## Check

For any internal text over 60 words that goes into a file, a card or a message:

```
python3 skills/aimultiple-internal-writing/lint_internal.py <file>             # language auto-detected
python3 skills/aimultiple-internal-writing/lint_internal.py --lang tr <file>
```

The score is rule hits per 100 words. Target: under 2.5. Fix the reported lines, run it once more, then send. The linter checks form only. It cannot tell whether the content is true or useful.

English checks: sentence length, semicolons, em dashes, italic emphasis, contractions, present perfect, phrasal verbs, long words, openers and closers, hedges, vague estimates. Turkish checks: sentence length, semicolons, em dashes, italic emphasis, "-mektedir" endings, nominal "yapılması" forms, openers and closers, hedges, vague estimates. Long lists and possible Turkish passive forms ("-ıldı", "-ndi", "edildi") are reported as info but not scored. For each passive hit, ask: is the actor known? If yes, write it active.

## Integration

- `aimultiple-youtrack-tasks`: card text follows this skill. The card format, the no-names rule and engineer hours live there.
- `aimultiple-cem-report` and `aimultiple-internal-briefing`: their register rules stay. This skill adds the sentence and shape rules.
- `aimultiple-anti-slop-writing`: articles only. The two skills do not share rules on purpose.

Rules adapted from the MIT-licensed asd-ste100 skill by Ege Chelebi (github.com/woosal1337/blog, 2026-07-25). ASD-STE100 is a registered trademark of ASD. This skill is not affiliated with ASD.
