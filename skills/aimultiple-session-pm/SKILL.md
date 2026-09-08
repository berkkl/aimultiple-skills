---
name: aimultiple-session-pm
description: |
  Session-level project management against the weekly plan. checkin (default) reads
  the current weekly-plan file + YouTrack and reports where this session sits in the week:
  which card, what stage, what is stalled, what to do next. checkout updates the plan
  row and posts the card's durum comment. Use at session start, or when the user says
  checkin, checkout, pm, neredeyiz, durum, haftalık plan, hangi taskteyiz.
---

# Session PM

Single source: `weekly-plan/<YYYY-Www>.md` (current ISO week; `date +%Y-W%V`). Rows: iş | kart | hedef gün | durum | kalan. Weekly Cem summaries are generated from this file, not reconstructed.

## checkin (default)

1. Read the current week's plan file. Missing → say so, offer to create it from the user's list. Do not invent rows.
2. One YouTrack query: `project: AIM #Unresolved for: me sort by: updated desc` (limit 20). Cross-check the states of the cards named in the plan. File and YouTrack disagree → report the disagreement, do not silently pick one.
3. Gelen kutusu: `project: INBOX #Unresolved sort by: created desc`. These are requests submitted through berkkalelioglu.com/aim-pm and never triaged. Each one is unfinished business: it has no AIM card, no plan row, and nobody has decided whether it is work. Name every one of them in the checkin and say what it needs. Empty result → say nothing about it.
4. Output, 10 lines max plus one line per untriaged INBOX card, no essay:
   - This session maps to row N / card AIM-XX (unclear → ask in one line).
   - Weekly counter: X done / Y in-progress / Z not-started (of M).
   - Nudges: every row past its hedef gün or unchanged 2+ days, by name ("6 numara iki gündür kımıldamıyor").
   - Untriaged incoming work: `INBOX-x, kimden, tek cümle özet -> incele ve AIM kartını aç`. Do not open the card yourself in this step; say it needs opening and let the user decide when.
   - One-sentence recommendation: what this session should produce for its row to move.

## Triaging an INBOX card

Requests arrive from the /aim-pm form as `INBOX-x` cards in the "Gelen İşler" project, assigned to Berk. They are raw: the description holds the sender, urgency, deadline, link, and the pasted message, nothing more. Triage means deciding what the work is, not copying the request.

1. Read the INBOX card. Decide with the user: real work, already covered by an existing AIM card, or not work at all.
2. Real work → open the AIM card per `skills/aimultiple-youtrack-tasks/SKILL.md` (full description format, subsystem, priority), then add a plan row if it belongs to this week.
3. Mark it handled on https://berkkalelioglu.com/aim-pm (the "işlendi" button takes the AIM id), which closes the INBOX card with a comment. Not work → "sil" there instead; the card is closed, not deleted.
4. Never leave an INBOX card open after deciding. An open INBOX card means undecided, and every checkin will name it again.

## checkout (session end, or on request)

1. Update the touched rows: Durum, Kalan, date in parentheses. A row moves only on concrete evidence (file written, run finished, live check, card comment). No evidence, no move.
2. Post the durum comment to the card (existing convention: Yapılan / Sıradaki / Blocker). Row fully done → mark done in the file and move the card state with user confirmation.
2b. **Benchmark rows carry a DB gate.** If the row is a benchmark that produced `output/db-ready.csv` (or published its results), it cannot be marked done until the Houston record exists, the table exists, and the rows are fed (`skills/aimultiple-benchmark-centralization/SKILL.md`, Procedure 5-6). Otherwise write "DB push bekliyor: kayıt/tablo/feed" into Kalan and remind Berkk to open the record and table; the next checkin repeats the reminder until the push lands.
3. **Push the plan to the board.** `cd ~/Projects/berkkalelioglu.com && npm run pm:push` (add a week label to push another week; `--dry` to check parsing first). berkkalelioglu.com/aim-pm renders a KV copy of the plan, not the file, and the plan is the whitelist: YouTrack is queried only for the cards the plan names, so a row that was never pushed is invisible there and its card shows only inside the "open cards not in the plan" count. Editing the markdown alone changes nothing on the site. On 2026-08-25 a new row (AIM-78) was written to the file and not pushed, and Berkk found it missing from the board.
4. Friday checkout → offer to generate the Cem weekly from this file (aimultiple-cem-report summary format, flat bullets).

## Failure cases

- **Codex / missing YouTrack MCP:** The weekly plan and board push are agent-independent. Read the plan locally and use the existing site's `npm run pm:inbox` for board intake when available. This does not replace a direct YouTrack query: disclose that card states and the YouTrack INBOX were not independently checked. For an authorized board update, run `npm run pm:push -- <YYYY-Www> --dry`, then push the same week and verify the response. Never report a card comment/state change based only on a successful plan push. Keep credentials in the site's existing environment loader; do not print them.

- Plan file missing mid-week: create the skeleton table, populate only from the user's own list.
- YouTrack unreachable: run from the file alone and say so.
- Session works on something not in the plan: add a row tagged "plansız giriş" instead of losing the work; flag it at checkout so the week's story stays honest.

## Integration

- Weekly summary: `aimultiple-cem-report` (summary mode reads this file first, dailies second).
- Card conventions: `aimultiple-youtrack-tasks`.
- Incoming requests: the /aim-pm form is the intake; INBOX cards are its queue. Nothing enters the weekly plan from there without passing triage.
- The board at /aim-pm is downstream of this file. `scripts/pm-push.mjs` in the berkkalelioglu.com repo reads `weekly-plan/<YYYY-Www>.md` straight from iCloud; the same script reads the inbox (`--inbox`) and closes an intake row (`--done <id> --card AIM-xx`).
- The nudge rule is the point of the skill. A checkin that lists no nudge when a row is stalled is a failed checkin.
