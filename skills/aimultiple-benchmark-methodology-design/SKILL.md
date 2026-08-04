---
name: aimultiple-benchmark-methodology-design
description: |
  Defines how to design fair, reproducible AIMultiple benchmarks before writing code or conclusions. Use when creating benchmark methodology, deciding metrics, selecting tasks, setting judge logic, or comparing vendors. Without this skill, benchmark results become hard to defend and easy to invalidate.
---

# Benchmark Methodology Design

## Activation

Use this skill before implementing a benchmark or interpreting benchmark results.

## Required Design Decisions

Lock these decisions before running comparisons:

1. Research question and decision the benchmark is meant to inform.
2. Product category definition in one sentence. Every participant must fit this category.
3. Inclusion and exclusion criteria for vendors or models.
4. Task set and why those tasks represent the target use case.
5. Input corpus, sampling logic, and any synthetic data generation.
6. Prompt templates, system instructions, and allowed tool use.
7. Output schema and pass or fail criteria per capability, not just globally.
8. Metrics: quality, latency, cost, stability, safety, and fallback behavior where relevant.
9. Judge method: exact match, rubric, programmatic scoring, or model-as-judge.
10. Number of runs, retry policy, and tie-breaking rules. Minimum 20 runs per task per provider if reporting P50/P90. Minimum 30 if reporting P95 or higher.
11. Version locks for models, APIs, and datasets.
12. Measurement model per provider type. If providers have different architectures (API vs. remote browser vs. agent platform), define what clock starts and stops for each type. Document this in the methodology note.
13. Ground truth strategy. Define how ground truth is captured, when it expires, and what tolerance is applied for volatile data.

## Fairness Rules

1. Use the same task set across compared systems unless a documented limitation requires narrowing scope.
2. Separate provider limitations from methodology choices.
3. If one vendor needs custom prompting or post-processing, document that explicitly.
4. Track exclusions, failed calls, and manual interventions.
5. Do not hide variance. Report spread, not only averages.
6. If a benchmark is only valid for one segment, state that boundary in the headline and summary.
7. When a benchmark uses an agent or orchestrator to drive providers, use the same agent and same scripts across all providers. If a provider requires a different agent (e.g. it bundles its own), document the asymmetry and do not present results in a single ranking without disclosing it.
8. Do not mix provider types (API, remote browser, agent platform) in one ranking table unless the measurement model accounts for the architectural differences. If it doesn't, use separate tracks.

## Relationship to the benchmark spec

The benchmark spec (`aimultiple-benchmark-spec-template`) is a 3-5 page customer-facing document. It covers what we measure and how we calculate it. It does NOT include internal methodology details.

This skill produces a separate internal methodology note. The methodology note contains everything the spec deliberately omits: retry policies, timeout configurations, environment specs, ground truth refresh schedules, statistical justifications, page-view-count tables, escalation testing procedures, failure/edge-case handling. These details are needed for implementation and reproducibility but are not shared with sponsors.

Do NOT put methodology note content into the spec. Do NOT put spec-level summaries into the methodology note. They are separate documents for separate audiences.

## Output requirements

Produce an internal methodology note that includes:

- Benchmark goal (reference the spec, do not duplicate)
- Run configuration (runs per task, execution order, parallelism rules)
- Timeout and retry policy
- Environment details (OS, VM, Playwright version, geo-targeting)
- Ground truth strategy (capture method, refresh schedule, tolerance)
- Escalation/calibration testing procedures
- Cost measurement methodology (raw inputs: bytes, seconds, units)
- Exclusion log template
- Known threats to validity

## Failure Scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Benchmark answers the wrong question | Metrics do not map to the buying decision | Rewrite the benchmark goal and metric set |
| Hidden prompt bias | One system gets materially different instructions | Normalize prompts or disclose the asymmetry |
| Unstable ranking | Results swing materially across reruns | Increase repetitions and report variance |
| Invalid generalization | Benchmark uses one niche workload but broad conclusion | Narrow the claim or widen the task set |
| Mixed provider types in one ranking | API scrapers, remote browsers, and agent platforms scored identically | Split into separate tracks or define per-type measurement models |
| Agent confound | Different agents used across providers | Standardize on one agent or disclose and separate results |
| Insufficient runs for percentile claims | Fewer than 20 runs per task but spec reports P50/P90 | Increase to minimum 20 runs or remove percentile claims |

## Integration Points

- `aimultiple-python-research-standards` implements the run pipeline.
- `aimultiple-source-validation` validates benchmark-related claims.
- `aimultiple-publication-quality-gate` checks reproducibility before release.
