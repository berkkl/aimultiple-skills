---
name: aimultiple-benchmark-methodology-design
description: |
  Defines fair, reproducible AIMultiple benchmarks. Use when designing methodology, selecting models and reasoning settings, launching or extending a comparison, choosing metrics or judges, or interpreting results.
---

Codex: read [the runtime adaptations](../../codex-migration/RUNTIME.md) before
following this skill. They replace Claude-specific tool and session behavior.

# Benchmark Methodology Design

## Activation

Use this skill before implementing or launching a benchmark, adding a model, changing run settings, or interpreting benchmark results.

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
9. Judge method: exact match, rubric, programmatic scoring, or model-as-judge. If any task is open-ended, its judging follows `aimultiple-open-ended-judging`; that skill decides the panel, anonymization, disagreement handling and scale.
10. Number of runs, retry policy, and tie-breaking rules. Minimum 20 runs per task per provider if reporting P50/P90. Minimum 30 if reporting P95 or higher.
11. Version locks for models, APIs, and datasets.
12. Measurement model per provider type. If providers have different architectures (API vs. remote browser vs. agent platform), define what clock starts and stops for each type. Document this in the methodology note.
13. Ground truth strategy. Define how ground truth is captured, when it expires, and what tolerance is applied for volatile data.
14. Model and reasoning alignment: apply the configuration procedure below before production.

## Model and reasoning alignment before production

Standing preference from Berkk (2026-09-11), for both Codex-led and Claude-led
model benchmarks: compare each participant at its strongest supported reasoning
setting unless the user has explicitly chosen another comparison policy.

1. Separate model selection from reasoning selection. For a strongest-capability
   comparison, identify the strongest in-scope model available through the chosen
   interface and its highest supported effort. Honor an explicitly selected model;
   flag a conflict with the benchmark goal before launch instead of silently
   substituting another model. A model choice alone does not select its effort.
2. Verify the supported settings against dated primary documentation and the
   installed CLI/SDK version. Set effort explicitly where supported. An unexplained
   `default`, `auto`, or omitted parameter does not establish maximum effort.
   Resolve inherited defaults and dynamic routing; record fixed or uncontrollable
   settings as limitations requiring a scope decision.
3. Apply the same policy across participants. Highest supported effort may be
   named `high`, `xhigh`, or `max`; matching labels does not prove equal compute.
   Equal cost, token budgets, or runtime is a different comparison policy that
   must be selected before the run. Check output limits, timeouts, and tool limits
   for restrictions that undermine the intended reasoning setting.
4. Before production, show Berkk a compact table: tool/interface, exact model and
   version, supported maximum, requested effort, verified effective setting and
   evidence, and material limits or exceptions. Resolve missing choices and
   goal/configuration conflicts before dispatch. Reuse explicit decisions already
   made in the session; do not ask for the same approval again.
5. Use a setup check or authorized smoke run to verify the effective configuration
   from outgoing request settings or native session metadata. A manifest label,
   successful response, token count, or model's self-description is not sufficient.
   Distinguish the setting sent from any backend behavior that is not observable.
6. Freeze the selected configuration and evidence with the run manifest. If the
   model or effort is ignored, downgraded, or silently changed, stop new dispatches
   for that participant and resolve the mismatch. Keep different configurations
   separate; never relabel old results or change settings in response to low scores.

The [benchmark preflight skill](../aimultiple-benchmark-preflight-check/SKILL.md)
checks this procedure immediately before production, including added models and
resumed runs whose configuration or runtime has changed.

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
- Model/effort comparison table, selection decisions, and effective-setting evidence
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
