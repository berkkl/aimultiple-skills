---
name: aimultiple-topic-research
description: |
  Researches a topic deeply using web sources and existing knowledge. Produces a fact-checked research brief for learning or benchmark preparation. Use when you need to understand a new domain before benchmarking, writing, or building a curriculum. Without this skill, research is ad hoc and prone to hallucination.
---

# Topic Research

## Activation

Use this skill when:

- The user asks to research or learn about a new topic.
- A benchmark requires domain knowledge the user does not yet have.
- Triggered directly via `/topic-research <topic>`.
- Called as part of the `/learn-topic` chain.

## Required Inputs

- **Topic**: The subject to research. Can be broad ("cloud VPS") or specific ("IOPS benchmarking for NVMe storage").
- **Depth hint** (optional): "overview", "benchmark-ready", or "deep-dive". Defaults to "benchmark-ready".
- **Focus areas** (optional): Specific sub-topics to prioritize.

## Workflow

1. **Scope the topic.** Restate the topic in one sentence. Ask the user to confirm or narrow it.

2. **Gather from existing knowledge.** Write down what you already know about the topic. Be explicit about confidence levels. Mark anything you're unsure about as `[needs verification]`.

3. **Search the web.** Use WebSearch and WebFetch to find:
   - Official documentation and specs.
   - Recent technical articles (prefer primary sources).
   - Industry reports or comparisons.
   - Pricing pages and product documentation where relevant.
   Target at least 5-8 distinct sources for a benchmark-ready brief.

4. **Cross-reference.** Compare web findings against existing knowledge. For each conflict:
   - Note both versions.
   - Determine which source is more authoritative.
   - Mark the resolution and reasoning.

5. **Fact-check critical claims.** Apply `aimultiple-source-validation` evidence tiers:
   - Tier A (primary sources) for any claim that would affect benchmark design.
   - Tier B acceptable for background context.
   - Flag Tier C claims explicitly.

6. **Compile the research brief.** Structure it as:
   - **Topic overview**: What it is, why it matters, who uses it.
   - **Key concepts**: Core terminology and how things work.
   - **Current state**: Latest developments, versions, standards.
   - **Common misconceptions**: Things that are easy to get wrong.
   - **Open questions**: What the research did not resolve.
   - **Sources**: List all sources with URLs, access dates, and tier ratings.

7. **Save the brief.** Write to `learning-sessions/<topic-slug>/research-brief.md`. Create the directory if it does not exist.

## Output Format

A structured markdown document. Each section should be dense and concrete. No filler paragraphs. Every factual claim should have an inline source reference or a `[needs verification]` tag.

## Failure Scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Web search returns mostly marketing content | No Tier A sources found | Widen search terms, try official docs directly, flag gaps |
| Existing knowledge conflicts with web sources | Cross-reference step finds contradictions | Present both, mark which is more recent/authoritative |
| Topic is too broad | Research brief exceeds 3 pages | Ask user to narrow scope or split into sub-topics |
| Key information is behind paywalls | Sources are gated | Mark claims as provisional, note alternative verification paths |

## Integration Points

- Uses `aimultiple-source-validation` for evidence grading.
- Feeds into `aimultiple-curriculum-builder` as the knowledge base.
- Feeds into `aimultiple-market-landscape` for competitor-specific research.
- Can trigger `aimultiple-fact-check-workflow` for high-stakes claims.
