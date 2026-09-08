---
name: save-handoff
description: Save a named handoff document that captures the current project state for resuming after /clear.
---

Save a handoff document. The handoff name is: $ARGUMENTS

If no name was provided, check if a handoff was loaded earlier in this session (look for prior conversation referencing a handoff name). If so, reuse that name. If no name can be determined, ask the user for one.

Follow the full `/save-handoff` procedure documented in `skills/aimultiple-context-handoff/SKILL.md`.

Merge into `handoffs/<name>.md`. Prefer ≤5 top Remaining Work items in core; spill deferred work and bulk notes to `handoffs/<name>.backlog.md`.
