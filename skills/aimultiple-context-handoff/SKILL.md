---
name: aimultiple-context-handoff
description: |
  Manages context window lifecycle for long-running projects. Monitors usage, forces clean handoffs before degradation, and maintains named, cumulative project briefs that carry the full relevant history across unlimited sessions. Each handoff distills everything that matters and drops what is stale.
---

# Context Window Handoff

## Why This Exists

Large language models degrade as context fills up. They lose track of earlier instructions, repeat mistakes, hallucinate details, and slow down. This skill forces a clean break before that happens and preserves a distilled, cumulative project state so no progress is lost.

The handoff document is not a session log. It is a project brief. Each save merges the current session's work into the existing brief, keeps what is still relevant, and drops what is done or obsolete. A fresh session loading a handoff should understand the full project state without reading any prior conversation.

## Named Handoffs

Handoffs are identified by name, not timestamp. Each name represents a distinct work stream.

Examples:
- `/save-handoff game-design` — brainstorming, feature planning, design decisions
- `/save-handoff save-system` — implementing the save/load system
- `/save-handoff networking` — multiplayer and netcode work
- `/save-handoff ui-overhaul` — UI redesign track

The same name is reused across sessions. `/save-handoff save-system` on session 10 overwrites the previous `save-system` handoff with a merged, up-to-date version. The file is `handoffs/save-system.md`. Simple, predictable, no timestamps in filenames.

## File Location

All handoffs live in `handoffs/` in the current working directory.

- `handoffs/<name>.md` — the handoff document for that work stream
- `handoffs/LATEST` — contains the name of the most recently saved handoff (so `/load-handoff` with no argument loads the last one)

## Always-On Monitoring (enforced via CLAUDE.md)

These thresholds apply to every session automatically.

| Context Used | Action |
|---|---|
| 20% | Warn the user once. Suggest scoping remaining work or saving a handoff early. |
| 50% | Stop all work. Execute `/save-handoff`. Ask the user for a name if none was used in this session yet. |

## `/save-handoff <name>` — Write the Handoff Document

### Usage

- `/save-handoff game-design` — saves to `handoffs/game-design.md`
- `/save-handoff` (no name) — if a handoff was loaded earlier in this session, reuse that name. Otherwise, ask the user for a name.

### Step 1: Stop current work

Do not start new tool calls, file edits, or research. Finish the current sentence and stop.

### Step 2: Load the previous version (if one exists)

Check if `handoffs/<name>.md` already exists. If it does, read it. This is your starting point, not a blank document. If it does not exist, start fresh.

### Step 3: Merge, not append

The new handoff must be a single, self-contained document. A fresh session reading only this file should have everything it needs. Apply these rules:

**What to carry forward from the previous version:**
- Project goal and scope (update if it evolved)
- Architecture decisions that still hold, with their reasoning
- Gotchas and failure patterns that are still relevant
- Remaining work items that are not yet done
- File inventory (cumulative list of all project files and their purpose)

**What to update with this session's work:**
- Current state (rewrite, do not append a new "session 3 state" section)
- Files modified (merge into the cumulative file inventory)
- New decisions made this session (add to decisions, do not duplicate)
- New gotchas discovered (add, remove any that are no longer relevant)
- Remaining work (remove completed items, add new ones, reorder by priority)

**What to drop:**
- Session-specific chatter. No "in session 2 we discussed..." narration.
- Information the model can derive by reading the code. Do not explain what a function does if the code is clear. Do explain why a non-obvious approach was chosen.

**What to replace (not duplicate):**
- If a system was added in session 2 and reworked in session 5, the handoff describes the current version only. The old design is gone.
- If a decision was reversed, remove the old decision and write the new one. Do not keep both.
- If a file was rewritten, update its entry in the file inventory. Do not keep the old description alongside the new one.

### Step 4: Write the document

Save to `handoffs/<name>.md`. Create `handoffs/` if it does not exist.

Write the name to `handoffs/LATEST`, overwriting previous content.

### Step 5: Document structure

```markdown
# Handoff: <name> — <one-line description>
Last updated: <YYYY-MM-DD HH:MM>
Sessions so far: <N>

## Goal
What this work stream is about. One paragraph max. Updated if scope changed.

## Current State
Where things stand right now. What works, what does not, what is partially done. Be concrete. Reference specific files and functions, not vague descriptions.

## Architecture & Key Decisions
Decisions that constrain future work. Each entry has the decision and its reasoning. Organized by topic, not by session. Remove decisions that were superseded.

## File Inventory
Every project file relevant to this work stream, with a one-line description and current status.

| File | Purpose | Status |
|---|---|---|
| path/to/file.py | Does X | done |
| path/to/other.py | Handles Y | in progress — Z is incomplete |

## Remaining Work
Ordered by priority. Concrete enough that a fresh session can start the top item without asking questions.

1. **<task>**: <what specifically needs to happen, which files to touch, any constraints>
2. ...

## Gotchas & Failure Patterns
Things that went wrong or required workarounds. Only include if still relevant. What happened, why, and what to do instead.

## Context for Next Session
Files to read before starting work. Commands to run. Background knowledge the model needs that is not in the code.
```

### Step 6: YouTrack sync (added 2026-08-02)

If the handoff document names a YouTrack issue or epic (an `AIM-xx` reference anywhere in it), post the session's progress to YouTrack per `skills/aimultiple-youtrack-tasks/SKILL.md` before telling the user:

- One `add_issue_comment` on the named epic in the standard durum format (date, Yapılan, Sıradaki, Blocker). One comment per session; if this session already posted one and nothing material changed since, skip.
- Update subtask States that the session's work visibly changed (started -> In Progress, finished -> Done). Do not touch unrelated subtasks.
- If the handoff names no `AIM-xx`, skip silently. Do not create issues from this step; creation stays an explicit ask.

### Step 7: Tell the user

Print the path to the handoff document. Say: "Handoff `<name>` saved. Type `/clear`, then `/load-handoff <name>` to continue." If Step 6 posted updates, name the issues touched in one line.

## `/load-handoff [name]` — Resume a Handoff

### Usage

- `/load-handoff game-design` — loads `handoffs/game-design.md`
- `/load-handoff` (no name) — reads `handoffs/LATEST` to get the most recent name, loads that

### Procedure

1. Read the handoff document from `handoffs/<name>.md`.
2. Read files listed in "Context for Next Session". Read key files from the file inventory (prioritize "in progress" files).
3. Print a short summary: goal, current state, and the top 3 remaining work items.
4. Ask the user to confirm or reprioritize before starting work.
5. Remember the loaded name so `/save-handoff` (no argument) reuses it at the end of the session.

Do not re-read the entire codebase. Trust the handoff document. Only read files it points you to.

## `/list-handoffs` — Show Available Handoffs

List all `.md` files in `handoffs/`, showing name and the first line (title) of each. Mark which one is LATEST.

## Warning at 20%

When context hits 20%, insert this once into your response:

> Context is at X%. Quality degrades past 50%. If more work remains, consider `/save-handoff` soon.

Do not repeat this warning in the same session.

## Failure Scenarios

| Scenario | Recovery |
|---|---|
| Context jumps past 50% in one turn | Write handoff immediately. Skip the 20% warning. |
| No previous handoff with that name exists | Start a fresh handoff document. No merge needed. |
| Previous handoff is very large | Review each section. Replace stale entries, do not just trim lines. Every line that remains must earn its place. |
| User refuses to stop at 50% | Warn once that quality will degrade. If they insist, continue but flag reliability risk in each response. |
| `handoffs/` directory not writable | Write to working directory root. |
| User calls `/load-handoff` with no name and no `LATEST` exists | List available handoffs if any exist. Otherwise tell the user no handoffs were found. |
| User calls `/load-handoff <name>` but file does not exist | Tell the user that handoff does not exist. Run `/list-handoffs` to show what is available. |

## Quality Rules for Handoff Documents

- The document must be self-contained. No references to "the previous session" or "as we discussed."
- Every file path must be real and current. Do not list files that were deleted.
- Remaining work items must be actionable. "Fix the bug" is not actionable. "Fix the off-by-one in `score.py:42` where the loop skips the last item" is.
- Every line must carry information that the next session cannot get from reading the code alone. If a section has nothing non-obvious to say, omit it.
- When a feature is added or changed, the handoff describes the current state of that feature. Not the history of how it got there.
- The handoff grows as the project grows. A simple script might need 30 lines. A game with save systems, networking, and UI might need 300. That is fine. The constraint is relevance, not length.
- The litmus test: if a fresh Opus 4.6 session read only this file plus CLAUDE.md, could it continue the project without asking clarifying questions? If not, add what is missing.
