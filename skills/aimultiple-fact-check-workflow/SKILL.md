---
name: aimultiple-fact-check-workflow
description: |
  Standardizes claim-by-claim fact checks for AIMultiple drafts, notes, and benchmark writeups. Use when asked to verify text, audit citations, or produce a fact-check deliverable. Without this skill, fact checks become ad hoc and hard to review.
---

# Fact-Check Workflow

## Activation

Use this skill when the task is to verify, audit, or clean up factual claims.

## Workflow

1. Break the text into atomic claims.
2. Assign each claim a stable claim id.
3. For each claim, capture:
   - claim text
   - claim date
   - source id
   - source date
   - evidence tier
   - confidence
   - status
4. Allowed statuses are:
   - verified
   - partially verified
   - contradicted
   - outdated
   - needs better source
5. For any claim that is not verified, propose the shortest correct rewrite or recommend removal.
6. If two strong sources conflict, mark the contradiction explicitly instead of forcing a false resolution.

## Output Format

Return a compact fact-check table or list that lets an editor audit each claim quickly. Each line should make clear what survives, what changes, and why.

## Core Rules

1. Verify the strongest or most decision-relevant claims first.
2. Prefer primary sources over commentary.
3. Separate factual correction from style editing.
4. Use absolute dates where timing matters.
5. If evidence is missing, say that directly instead of inferring.

## Failure Scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Claim too broad to verify | One sentence contains several assertions | Split it into atomic claims |
| Citation laundering | Secondary source cites an unclear primary | Find the original source or downgrade confidence |
| Outdated truth | Claim was true but no longer current | Mark as outdated and rewrite with date scope |

## Integration Points

- Uses `aimultiple-source-validation` to grade evidence quality.
- Feeds `aimultiple-anti-slop-writing` after factual cleanup.
- Must clear `aimultiple-publication-quality-gate` before external sharing.
