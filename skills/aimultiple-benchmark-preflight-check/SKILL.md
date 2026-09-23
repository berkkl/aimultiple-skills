---
name: aimultiple-benchmark-preflight-check
description: |
  Validates a benchmark spec before implementation and verifies model/reasoning alignment before production runs. Use before launch, when adding a model, or when resuming with changed settings or runtime. Catches fairness violations, statistical errors, and unverified technical claims.
---

Codex: read [the runtime adaptations](../../codex-migration/RUNTIME.md) before
following this skill. They replace Claude-specific tool and session behavior.

# Benchmark Preflight Check

## Activation

Run this skill after a benchmark spec is complete (or after a major revision) and before implementation starts. If the spec fails any check, it is not ready for implementation.

Immediately before production, repeat the model/reasoning checks in section 5a
against the actual runner and effective configuration. Repeat them for added
models and resumed runs with changed settings or runtime; an earlier spec pass
does not verify the eventual execution settings. Apply this in both Codex and
Claude Code.

## Checklist

Work through every item. For each, mark PASS, FAIL, or N/A. If any item is FAIL, stop and fix the spec before proceeding.

### 1. Product Category

- [ ] The spec defines the product category in one sentence.
- [ ] Every participant fits the stated category.
- [ ] If participants span different product types (API vs. browser vs. agent platform), the spec either uses separate tracks with separate rankings, or documents how the measurement model accounts for the difference.

### 2. Discovery Completeness

- [ ] The execution environment is specified (agent framework, browser mode, runtime).
- [ ] The measurement model is defined per provider type (what clock starts, what clock stops).
- [ ] Ground truth strategy is defined, including how volatility is handled.
- [ ] No technical claims are made without citation or verification. Search the spec for assertions about what tools "can" or "cannot" do. Each must have a source.

### 3. Capability Coverage

- [ ] Every capability (layer) in the spec has a concrete success definition with pass/fail conditions.
- [ ] Success definitions are verifiable programmatically, not by human judgment (unless human judgment is the explicit judge method and inter-rater reliability is addressed).
- [ ] Failure criteria are defined with the same specificity as success criteria.

### 4. Statistical Validity

- [ ] Run count per task per provider is at least 20 if the spec reports P50/P90.
- [ ] Run count is at least 30 if the spec reports P95 or higher percentiles.
- [ ] Total run count is feasible within the stated timeline and budget. Calculate: (tasks x providers x runs x estimated_avg_duration). If this exceeds available time, reduce scope before starting.
- [ ] The spec does not promise statistics that the run count cannot support.

### 5. Fairness

- [ ] The same agent/orchestrator is used across all providers, OR the spec documents the asymmetry and separates results.
- [ ] The same task scripts are used across all providers, OR per-provider adaptations are documented.
- [ ] No provider gets a structural advantage from the test setup (e.g. testing on sites where one provider has special partnerships).
- [ ] Latency comparison accounts for architectural differences between provider types.

### 5a. Model and Reasoning Configuration

Apply [the methodology skill's configuration procedure](../aimultiple-benchmark-methodology-design/SKILL.md#model-and-reasoning-alignment-before-production).

- [ ] The comparison policy is explicit and consistent across participants; the standing policy is highest supported reasoning effort unless the user selected another policy.
- [ ] The model/effort table was shown to Berkk before production; missing choices and conflicts with the stated goal are resolved, using existing explicit decisions where available.
- [ ] Exact models, interface versions, supported maximum settings, and dated evidence are recorded. Model selection and effort selection were checked separately.
- [ ] Effective request/session settings match the frozen table. Unresolved defaults or omitted parameters, unapproved fallback routing, and unsupported settings remain FAIL, not assumed matches.
- [ ] Output, tool, and time limits support the selected policy; fixed or uncontrollable settings and other exceptions have an explicit scope decision.
- [ ] Execution detects model/effort drift and stops new dispatches for the affected participant. Changed configurations cannot be merged into or relabeled as old results.

### 6. Ground Truth

- [ ] Ground truth values are captured close enough to test execution that volatility does not invalidate results.
- [ ] For volatile targets (e-commerce prices, search results): tolerance ranges are defined and justified.
- [ ] The spec names specific target URLs/queries. If targets are "TBD," the spec is not ready.

### 7. Scope Consistency

- [ ] Numbers are internally consistent. (Task count x run count x provider count = total runs. Check this arithmetic.)
- [ ] If capabilities were added or removed during drafting, all references to the old count are updated. Search for stale numbers.
- [ ] Timeout values are defined and realistic for the task complexity.

### 8. Implementability

- [ ] A developer can read the spec and build the test harness without asking clarifying questions about what "success" means.
- [ ] The spec does not require tools or access that the team does not have.
- [ ] Cost estimate exists (API costs x total runs). If budget is not confirmed, flag it.

## Output

Produce a table:

| Check | Status | Notes |
|---|---|---|
| Product Category | PASS/FAIL | ... |
| Discovery Completeness | PASS/FAIL | ... |
| ... | ... | ... |

If any check is FAIL, list the specific fix needed. Do not approve the spec with open FAILs.

## Integration Points

- Runs after `aimultiple-benchmark-spec-template` produces a spec.
- Runs after `aimultiple-benchmark-methodology-design` produces a methodology note.
- Blocks `aimultiple-python-research-standards` (implementation) until all checks pass.
