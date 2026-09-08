---
name: load-handoff
description: Load a named handoff document and resume work from where the previous session left off.
---

Load and resume from a handoff document. The handoff name is: $ARGUMENTS

If no name was provided, read `handoffs/LATEST` to get the most recently saved handoff name and load that.

Follow the full `/load-handoff` procedure documented in `skills/aimultiple-context-handoff/SKILL.md`.

Load core only (`handoffs/<name>.md`). Do not auto-read `handoffs/<name>.backlog.md` unless asked or top remaining work is done.
