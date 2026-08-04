---
name: aimultiple-youtrack-tasks
description: Opens and updates YouTrack (AIM project) tasks from any chat via the YouTrack MCP. Use when the user says "youtrack'e aç", "task aç", "youtrack güncelle", "durum güncelle", references an AIM-xx issue, or forwards a Cem/Sedat message that should become tracked work.
---

# YouTrack Task Workflow

Single project: AIM. Board: "AIM Researcher" (manual-add, see Failure Cases).
Every task is assigned to berk.kalelioglu unless the user says otherwise.

## Task creation format

Summary: imperative, specific, Turkish. Include deadline in the summary only if one exists (absolute date, e.g. "hedef yayın 2026-07-10 Cuma").

Description sections, in order:

1. `## Ne isteniyor` - what is being asked, decided points, deadline as absolute date.
2. `## Nasıl yapacağız` - numbered concrete steps. Flag methodology risks (fairness, fake-win, known data weaknesses) here, not as filler.
3. `## Açık sorular` - only if real ones exist. Each must name who resolves it.
4. Source: if the work came from a formal work message (Cem, Sedat, customer), quote the full message verbatim under `## <Kişi>'nin mesajı (tam metin)`. If it came from a handoff or doc, link the path instead. Informal or private colleague chatter (WhatsApp, DMs, venting, opinions about people) is NEVER pasted verbatim: summarize the work-relevant facts in one neutral sentence. Issues are a shared record; write everything at work-document seriousness.

Custom fields:

- Assignee: berk.kalelioglu
- State: To do
- Type: Task by default. Epic + subtasks when the work has 3+ separable parts with their own progress (subtasks reference the epic for the full source message instead of repeating it).
- Subsystem: Benchmarks (benchmark run/methodology/centralization), Articles (article edits, charts into articles), Custom Tasks (internal tooling, bots, scripts).
- Priority: Urgent (Cem says top priority/urgent), Major (has a deadline or customer impact), Normal (everything else).

When creating an epic, create the epic first, then subtasks with `parentIssue`, then update the epic description with the real subtask IDs. Do not guess IDs in advance.

## Status updates while working

When work on an issue starts, set State: In Progress. When it finishes, Done. When blocked long-term, Parked.

Progress is recorded with `add_issue_comment`, one comment per session or milestone, format:

```
2026-07-06 durum
- Yapılan: <1-3 bullets, concrete artifacts/numbers>
- Sıradaki: <next step>
- Blocker: <who/what, or "yok">
```

Do not edit the description for status; the description is the spec, comments are the log. Update the description only when scope or decisions change, and say what changed in a comment.

## Failure cases

- Board membership is NOT settable via MCP ("Issue field 'Board ...' not found"). After creating issues, remind the user once: select them in the Issues list and apply command `add Board AIM Researcher`, or enable auto-add in board settings.
- If a required input is unrecoverable (which message, which scope), ask. Do not ask for values with an obvious default (State, Assignee, Type).
- If the user forwards multiple messages, one task per independent piece of work; do not merge unrelated asks into one issue.

## Integration

- Benchmark tasks follow `aimultiple-benchmark-methodology-design` constraints; put the fairness/fake-win note in the description at creation time.
- Session-end journaling stays in `aimultiple-cem-report`; YouTrack comments do not replace the daily log.
- `/save-handoff` triggers a YouTrack sync automatically (2026-08-02): when the handoff names an `AIM-xx`, the save posts the session durum comment and refreshes changed subtask States. See Step 6 in `aimultiple-context-handoff/SKILL.md`. Handoff documents for tracked work streams should therefore always name their epic.
