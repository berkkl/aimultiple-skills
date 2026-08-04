---
name: aimultiple-benchmark-spec-template
description: |
  Generates benchmark specification documents in AIMultiple's standard format. Use when creating a new benchmark spec for any vendor comparison. The spec is a customer-facing document shared with sponsors. It must be concise (3-5 pages), operational, and free of internal methodology details.
---

# Benchmark Spec Template

## Activation

Use this skill when creating a new benchmark specification document. The output is a concise spec shared with participants and used to guide implementation. This is NOT an internal methodology document.

## Critical constraint: audience and length

The spec goes to sponsor companies (CTO-level readers). They need to understand what we measure and how, not our internal edge-case handling. Target 3-5 pages. If the spec exceeds 5 pages, it is too detailed.

**Include:** What we measure, how we calculate it, what tasks we run, who participates, what we publish, article outline.

**Do NOT include:** Retry policies, timeout configurations, environment specs (OS, VM details), ground truth refresh schedules, statistical justifications, page-view-count tables, raw-vs-aggregated metric breakdowns, internal fairness rationale paragraphs, failure/edge-case handling procedures. These belong in an internal methodology note, not the spec.

## Discovery phase (mandatory)

Do not draft any spec content until this phase is complete. Ask the user:

1. What product category is being benchmarked? One sentence.
2. Target use case framing (e.g. "for AI agents," "for competitive intelligence").
3. Are all participants the same product type? If not, how will fair comparison work?
4. Approximate scale (number of tasks, URLs, or queries).
5. What tools and infrastructure execute the benchmark?
6. How will success be verified for each task type?

If any are missing, flag as open item. Do not assume.

## Spec structure

Follow this section order. Use sentence case for all H2 and below headings.

### Title and aim

- Title: `[Domain] Benchmark`
- One or two paragraphs covering: what is being evaluated, scope/scale, use case framing, why this product category is the right one. Mention excluded product types and why in 1 sentence each.

### Evaluation metrics

Each metric gets its own H3 with: definition, measurement methodology, and calculation formula. Keep each metric to 5-10 lines max.

Standard metrics to consider (include only what applies):
- **Success rate:** Define success criteria, calculation formula.
- **Latency / response time:** Sync vs async handling, percentiles (P50/P90), what the clock starts and stops on.
- **Load test:** 3 concurrency tiers (state as hypotheses open to feedback), metrics per tier.
- **Data availability / coverage:** If providers differ in what fields they return.
- **Cost:** Normalized per-successful-outcome metric. If providers have different pricing models, show a small table mapping pricing model to calculation method.

Do NOT create separate tables for "raw metrics," "aggregated per task," and "aggregated per provider." One definition per metric is enough. Aggregation (averages, percentiles) is implied.

### Tasks (if applicable)

Each task: 1-2 line description of what the agent/script does, then a "Pass" condition. No "Fail" condition (it is the inverse of Pass). No "Stress" or "Why we chose this" explanations. No ground truth methodology. Keep each task to 4-5 lines.

### Pricing comparison table

One line: "Will be structured as usual showing prices for different volumes and [normalized cost metric]."

### Publishing

List 4-6 target user search intents. Note these are examples.

### Participants

Inclusion criteria in one sentence. Then a table with provider name, product name, and pricing model. Keep it scannable.

### Article outline

Section-by-section outline of the final published article. Include chart types where relevant. Include a "Common Failure Patterns" section with XX% placeholders. End with "Deployment Recommendations" segmented by use case.

## Core rules

1. Every metric has a calculation formula. No metric defined by description alone.
2. Each metric is defined once. Do not repeat the same metric at different aggregation levels.
3. Load test tiers are hypotheses. State openness to feedback.
4. Pricing uses a normalized per-successful-outcome unit.
5. Do not include internal methodology details. The spec is operational, not exhaustive.
6. Do not include editorial commentary or methodology justifications aimed at internal readers.
7. Product category stated once. Every participant must fit it.
8. Sentence case for H2 and below headings.
9. No section numbering (no "1. Product category", "2. Metrics"). Use plain headings.

## Failure scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Spec exceeds 5 pages | Too much internal detail leaked into customer doc | Move excess to internal methodology note |
| Metrics repeated at multiple aggregation levels | Same metric appears in 2+ tables | Collapse to single definition with formula |
| Tasks include methodology rationale | "Stress" labels, "Why this task" paragraphs | Remove. Keep action + pass condition only |
| Sections numbered | "1. Product category", "2. Metrics" | Remove numbers, use plain headings |
| Internal details in spec | Retry policies, timeout configs, environment specs, ground truth refresh | Move to internal methodology note |
| Capability without pass condition | A task is listed but pass criteria are vague | Block until concrete pass condition defined |

## Integration points

- Internal methodology details go into a separate note driven by `aimultiple-benchmark-methodology-design`.
- Implementation follows `aimultiple-python-research-standards`.
- Final article goes through `aimultiple-publication-quality-gate`.
