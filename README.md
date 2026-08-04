# AIMultiple Skills

Claude Code skills for AIMultiple research work: article writing and editing, fact checking, benchmark design and publication, and session handoffs. Each skill is one folder with a `SKILL.md` (YAML frontmatter + procedure).

## Install

Copy the `skills/` folders you want into your workspace (a `skills/` directory your CLAUDE.md points to) or into `~/.claude/skills/`. Reference them from your CLAUDE.md the way you load any skill file; the frontmatter `description` tells Claude when to activate each one.

Paths inside some skills assume Berkk's workspace layout (`AIM Articles/...`). Adapt those paths to your own workspace on first use.

## What is here

| Group | Skills |
|---|---|
| Writing and editing | `aimultiple-article-edit` (OLD/NEW edit pairs), `aimultiple-article-checklist`, `aimultiple-anti-slop-writing` (canonical style rules; `aimultiple-anti-slop` is the older short version kept for references), `aimultiple-publication-quality-gate`, `aimultiple-social-sharing` |
| Verification | `aimultiple-fact-check-workflow`, `aimultiple-source-validation` |
| Research | `aimultiple-topic-research`, `aimultiple-market-landscape`, `aimultiple-internal-briefing` |
| Benchmarks | `aimultiple-benchmark-methodology-design`, `aimultiple-benchmark-spec-template`, `aimultiple-benchmark-preflight-check`, `aimultiple-benchmark-centralization`, `aimultiple-benchmark-database` (includes `repo-template/` and the `upload_to_db.py` client), `aimultiple-python-research-standards` |
| Deliverables | `aimultiple-deliverable-xlsx` |
| Ops | `aimultiple-youtrack-tasks` |
| Handoffs | `aimultiple-context-handoff` (the procedure), `save-handoff`, `load-handoff`, `list-handoffs` (slash commands). Lets a long project survive across sessions: write a named handoff, clear, resume from it. |

## Rules of the road

- The anti-slop rules apply to every skill edit here too: no em dashes, no filler, procedures stay short.
- A skill that references a live system (YouTrack, the benchmark DB API) documents the flow but never contains a credential. Keys live in env vars.
- Improvements welcome: edit the SKILL.md, keep the frontmatter, open a PR or commit directly if you have access.
