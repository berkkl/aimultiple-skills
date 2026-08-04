---
name: aimultiple-internal-briefing
description: |
  Produces sourced, concise answers to internal questions from Cem or the team. Use when the task is answering a specific question, preparing a briefing, or summarizing existing research for internal consumption. Without this skill, internal answers either lack sources or balloon into full article drafts.
---

# Internal Briefing

## Activation

Use this skill when the request is an internal question, not a publishable article. Typical triggers:

- "What do we know about X?"
- "Can you check Y for Cem?"
- "Summarize our position on Z."
- Direct questions about a vendor, market segment, or benchmark result.

## Workflow

1. Restate the question in one sentence to confirm scope.
2. Pull relevant facts from existing research notes, benchmark data, or prior drafts in this workspace.
3. If workspace evidence is insufficient, search external primary sources.
4. Separate the answer into two sections:
   - **What we know** (sourced facts, with source IDs or URLs).
   - **What needs verification** (gaps, stale data, inferences we haven't confirmed).
5. If the question touches a benchmark, reference the locked methodology rather than ad-hoc numbers.
6. Keep the response short. Target 3-8 sentences for simple questions, up to one page for complex ones.

## Core Rules

1. Every factual statement gets a source reference, even in internal answers.
2. Do not write at publication quality. Prioritize speed and clarity over polish.
3. Flag anything older than 90 days as potentially stale.
4. If the answer requires a judgment call, state the reasoning and the alternatives. Do not present one option as obvious.
5. Do not pad. If the honest answer is "we don't have good data on this," say that.
6. Anti-slop rules still apply. Internal does not mean sloppy writing.

## Output Format

Short prose with inline source references. No headers unless the answer covers multiple sub-questions. Use a bullet list only if listing discrete items (vendors, features, dates).

End with a one-line summary of confidence level and any recommended next step.

## Failure Scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Question is too broad | Answer would require a full article | Ask for a narrower scope before answering |
| Only Tier C sources available | No primary evidence found | State the gap and recommend where to look |
| Answer mixes fact and opinion | Inference not labeled | Split into "what we know" and "what we think" |
| Stale data presented as current | Source date > 90 days old | Flag the date and note reconfirmation needed |

## Integration Points

- Uses `aimultiple-source-validation` for evidence grading.
- If the answer later gets promoted to an article, hand off to `aimultiple-anti-slop-writing` and `aimultiple-fact-check-workflow`.
- Does NOT require `aimultiple-publication-quality-gate` (internal only).
