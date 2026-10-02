---
name: aimultiple-youtrack-tasks
description: Opens, updates and closes cards in the team's YouTrack project RES through the YouTrack MCP, with the card writing protocol (ASD-STE100-based, no personal names), the update cadence and engineer-hour logging. Use when the user says "kart aç", "task aç", "youtrack", "durum güncelle", "kartı kapat", "kartları güncelle", references a RES-xx card, or brings a request that should become tracked work.
---

Codex: read [the runtime adaptations](../../codex-migration/RUNTIME.md) before
following this skill. They replace Claude-specific tool and session behavior.

# YouTrack cards (RES)

Project RES "AIM Researcher" on aimresearcher.youtrack.cloud. Board "AIM Researcher" has one sprint per ISO week (`2026-W41`). A new card goes into the current sprint automatically. The research team, QA, the CEO and the CMO read these cards. Write them as work documents.

AIM (project "Berk PM") is a private project since 2026-10-02. Do not open team cards there.

## Writing protocol

Use Turkish or English, one language per card. Card text follows `aimultiple-internal-writing` (ASD-STE100 rules at about 80%, both parts). Check a long description or comment with its `lint_internal.py` before you post it. Card-specific rules:

- Use the name the repo uses for a benchmark, tool or model.
- Give numbers with units. Give dates as absolute dates (2026-10-05).

**No people in the text.** People go in the fields (Reporter, Assignee). Summary, description and comments contain:

- No names, no @mentions, no "X said", "X wants" or "send this to X".
- No chat or e-mail quotes. Link the source document, or state the fact.
- Decisions as decisions: "Scores use a 0-100 scale."
- Dependencies as a linked card ("depends on RES-12") or a role ("waiting for: customer reply", "waiting for: management approval").

Exception: a card opened for another person starts with one line, `Requested by: <name>`.

| Before | After |
|---|---|
| agentic-cli: Vedat'ın istediği yeni agent'ları ekle. Vedat yazdı, Berkk pipeline'a aldı; hangi agent'lar olduğu mesajdan okunacak. | **Agentic-CLI benchmark'ına yeni agent'ları ekle** / Requested by: Vedat / Amaç: Benchmark üç yeni agent'ı ölçer. |
| Cem 16 Eylül'de yayını durdurdu, önce mevcut yazılar düzelsin dedi. | Yayın, mevcut yazılar standarda uyana kadar durdu (2026-09-16). |

## Card format

Summary: one imperative sentence of max 10 words that names the object (benchmark or article slug). A deadline goes in Due Date, not the summary.

```
Requested by: <name>          (only for a card opened for another person)

## Goal | Amaç
<1-2 sentences: what is different when the card is done>

## Steps | Adımlar
1. <one instruction>

## Done when | Bitme koşulları
- <verifiable result: live URL, file path, DB table id, run folder>

## Links | Bağlantılar
- <spec, handoff, doc, article URL>
```

Write a methodology risk (fairness, fake win, known data weakness) as its own step. Add `## Open questions | Açık sorular` only for real questions, and give the role that answers each one.

Fields:

- Type: Task by default. Use Epic when the work has 3+ parts with separate progress. Create the epic, then the subtasks with `parentIssue`, then write the real subtask IDs into the epic. Other types: Article Edit, New Article, Bug.
- Priority: Urgent (management top priority, customer blocker), Major (deadline or customer impact), Normal (default).
- Subsystem: Benchmarks, Articles, Customer, Tooling.
- Assignee: the person who does the work, by default the session user. State: To do.
- Estimation: engineer hours for the full card, from the table below, when the scope is clear.
- Due Date: only for a real deadline.

## Update cadence

- When work starts, set State to In Progress.
- At the end of each session that changed a card (checkout, `/save-handoff`, "kartları güncelle"), post one comment and log the engineer hours. Merge a second comment on the same day into the first one.
- If a card stays blocked for more than 2 working days, set State to Parked. The comment says what unblocks it.
- If an In Progress card has no comment for 3 working days, the next session names it. It asks: continue, Parked, or close.
- A handoff can be older than the work. Before a status comment says "draft", "not published" or "not run", check the live page, file or run folder. On 2026-10-02 a comment called a live article a draft.
- The description is the spec and the comments are the log. Change the description only when the scope changes, and write what changed in a comment.

```
Done: <1-3 items, concrete artifact or number>      | Yapılan:
Next: <one step>                                    | Sıradaki:
Blocked: <RES-xx or role, or "none">                | Engel:
```

YouTrack puts a timestamp on each comment, so do not add a date line.

## Engineer hours

Engineer hours are the hours a mid-level engineer needs to reach the card's result without AI tools, by the most direct route. They are an estimate. AI speed does not reduce the number. Actual time is not tracked.

Estimate the result, not the volume of the session's output. An AI session writes notes, research reports, helper scripts and long documents that a person would not write for the same result. Do not count them. Example: a YouTrack project with a board and a sprint is 1 h of setup in the UI. The research note and the sprint script from that session add nothing.

At each session update, log one work item per work type with `log_work`, for the result that the session moved:

- `durationMinutes` and `date` (the session date).
- `workType`: Development (code, harness, pipelines, setup), Testing (benchmark runs, QA, verification), Documentation (articles, edits, charts, reports), Investigation (research, fact checks, product tests).
- `description`: the basis line, for example `2 charts (3 h) + 1,200-word section (7.2 h)`.

The work items add up in the card's "Engineer hours" field. Main menu > Timesheets shows the weekly total per person. YouTrack shows periods in 8-hour days: "1d 3h" is 11 hours. Say the hours in comments.

Reference table v2 (2026-10-02). It is an internal calibration, not an industry standard. v1 counted output volume and gave 11 h for a 1 h setup. Review the table after 4 weeks of data.

| Unit the result needs | Engineer hours |
|---|---|
| Tool or project setup in a web UI | 1 h |
| Code the result needs (harness, parsers, pipelines) | 1 h per 25 lines |
| Benchmark run: one model or tool over the full task set, with setup, monitoring and failure triage | 3 h |
| Grading or output review a person would do by hand | 5 min per item |
| New publishable article text | 6 h per 1,000 words |
| Edit to a live article | 20 min per OLD/NEW pair |
| New benchmark participant end to end: database rows, article text, tables, charts | 3 h |
| Fact check against a primary source | 30 min per claim |
| Chart: data prep, build, upload | 1.5 h |
| Rows into an existing database table | 10 min |
| Hands-on product or vendor test with written findings | 4 h per product |
| Document someone else reads (spec, customer e-mail, team guide) | 1 h per 500 words, max 2 h |

- Sanity check: ask how long a competent person needs for this result by the direct route. If the table gives more, log the direct estimate.
- Do not count waiting time (runs, queues, replies).
- Count a dead end only when the card records it as a finding.
- If the result matches no row, use the closest row and write that in the basis line.

## Closing a card

Set Done only when each "Done when" item has evidence. If the logged total misses work, log one more work item for the gap. Then post:

```
Result: <what is live, and where>
Engineer hours: <field total> (<n> work items)
Evidence: <URL or path>
```

Read the card after the state change. A state change can fail without an error.

## Board owner tasks

- Every Monday, run `python3 skills/aimultiple-youtrack-tasks/new_sprint.py`. It creates the sprint for the ISO week, moves the unresolved cards from the last sprint and makes the new sprint the default. YouTrack has no recurring sprints.
- The MCP cannot create projects, fields, boards or sprints. Make setup changes through the REST API with the board owner's token.

## Other people's cards

- Change only cards where the session user is Assignee or Reporter. Leave other cards as they are, unless their owner asks.
- Read the card's history before you write a field. If a person set a value by hand (Estimation, a work item, State, Priority), keep it. On 2026-10-02 a session overwrote a hand-set Estimation.

## Failure cases

- If a card is not on the board, set its sprint in the card's Board field in the UI. The MCP cannot set sprints.
- If a required input cannot be recovered (which request, which scope), ask. Do not ask about values with a clear default.
- Open one card per independent piece of work.

## Integration

- `aimultiple-session-pm`: checkin reads RES. Checkout runs the update cadence above.
- `/save-handoff` Step 6 posts the update to the RES card that the handoff names.
- Benchmark cards: the fairness note from `aimultiple-benchmark-methodology-design` goes in Steps at creation.
- Intake form (berkkalelioglu.com/aim-pm → INBOX): triage per `aimultiple-session-pm`. A request that is real work becomes a RES card.
