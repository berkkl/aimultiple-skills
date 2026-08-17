---
name: aimultiple-session-pm
description: |
  Session-level project management against the weekly plan. checkin (default) reads
  weekly-plan/<week>.md + YouTrack and reports where this session sits in the week:
  which card, what stage, what is stalled, what to do next. checkout updates the plan
  row and posts the card's durum comment. Use at session start, or when the user says
  checkin, checkout, pm, neredeyiz, durum, haftalık plan, hangi taskteyiz.
---

# Session PM

Single source: `weekly-plan/<YYYY-Www>.md` (current ISO week; `date +%Y-W%V`). Rows: iş | kart | hedef gün | durum | kalan. Weekly Cem summaries are generated from this file, not reconstructed.

## checkin (default)

1. Read the current week's plan file. Missing → say so, offer to create it from the user's list. Do not invent rows.
2. One YouTrack query: `project: AIM #Unresolved for: me sort by: updated desc` (limit 20). Cross-check the states of the cards named in the plan. File and YouTrack disagree → report the disagreement, do not silently pick one.
3. Output, 10 lines max, no essay:
   - This session maps to row N / card AIM-XX (unclear → ask in one line).
   - Weekly counter: X done / Y in-progress / Z not-started (of M).
   - Nudges: every row past its hedef gün or unchanged 2+ days, by name ("6 numara iki gündür kımıldamıyor").
   - One-sentence recommendation: what this session should produce for its row to move.

## checkout (session end, or on request)

1. Update the touched rows: Durum, Kalan, date in parentheses. A row moves only on concrete evidence (file written, run finished, live check, card comment). No evidence, no move.
2. Post the durum comment to the card (existing convention: Yapılan / Sıradaki / Blocker). Row fully done → mark done in the file and move the card state with user confirmation.
3. Friday checkout → offer to generate the Cem weekly from this file (aimultiple-cem-report summary format, flat bullets).

## Failure cases

- Plan file missing mid-week: create the skeleton table, populate only from the user's own list.
- YouTrack unreachable: run from the file alone and say so.
- Session works on something not in the plan: add a row tagged "plansız giriş" instead of losing the work; flag it at checkout so the week's story stays honest.

## Integration

- Weekly summary: `aimultiple-cem-report` (summary mode reads this file first, dailies second).
- Card conventions: `aimultiple-youtrack-tasks`.
- The nudge rule is the point of the skill. A checkin that lists no nudge when a row is stalled is a failed checkin.
