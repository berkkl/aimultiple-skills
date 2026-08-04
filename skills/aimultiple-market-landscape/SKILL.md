---
name: aimultiple-market-landscape
description: |
  Maps the competitive landscape for a product category or market segment. Identifies key players, differentiators, pricing, target segments, and positioning. Use when preparing for a benchmark that compares vendors, or when the user needs to understand who does what in a market. Without this skill, competitor analysis is inconsistent and misses important dimensions.
---

# Market Landscape

## Activation

Use this skill when:

- The user needs to understand the competitive landscape for a benchmark.
- The user asks "who are the players in X?"
- Triggered directly via `/market-landscape <market>`.
- Called as part of the `/learn-topic` chain.

## Required Inputs

- **Market or category**: The product space to map (e.g., "cloud VPS providers", "web scraping APIs").
- **Scope** (optional): Number of vendors to cover. Defaults to 5-10 most relevant.
- **Benchmark context** (optional): If this feeds a benchmark, what's being measured. This shapes which differentiators matter.

## Workflow

1. **Define the market boundary.** State what counts as "in" this market and what's adjacent but out of scope. Confirm with the user.

2. **Identify players.** Use web search to build an initial list. Sources to check:
   - Industry comparison pages and "alternatives to X" articles.
   - G2, Capterra, or similar aggregator listings.
   - Recent funding/acquisition news (signals who's active).
   - Official vendor websites.

3. **For each player, gather:**
   - **What they do**: Core product, primary use case.
   - **Differentiator**: What makes them distinct from competitors. Be specific. Not "good performance" but "bare-metal ARM instances at 40% lower cost than x86 equivalents."
   - **Target segment**: Enterprise, SMB, developer, specific verticals.
   - **Pricing model**: Free tier, pay-as-you-go, committed use, enterprise contracts. Get actual numbers where public.
   - **Known strengths**: What users and reviewers consistently praise.
   - **Known weaknesses**: What users and reviewers consistently criticize.
   - **Scale indicators**: If available, things like number of data centers, regions, customer counts, or funding amounts.

4. **Cross-reference claims.** Vendor websites overstate capabilities. For each vendor:
   - Check at least one non-vendor source (review site, technical blog, benchmark result).
   - If a claim is only from the vendor's own marketing, mark it as `[vendor-claimed, unverified]`.

5. **Build the landscape map.** Create a comparison table plus short narrative profiles.

6. **Save the output.** Write to `learning-sessions/<topic-slug>/market-landscape.md`.

## Output Format

### Comparison Table

A markdown table with columns: Vendor | Core Offering | Differentiator | Target Segment | Pricing Model | Key Strength | Key Weakness

### Vendor Profiles

Below the table, a 3-5 sentence profile for each vendor covering what they do, who they serve, and what makes them worth benchmarking.

### Market Notes

A short section (3-5 sentences) on overall market dynamics: consolidation trends, emerging players, recent shifts.

## Failure Scenarios

| Scenario | Detection | Recovery |
|---|---|---|
| Pricing is not publicly available | Pricing page missing or "contact sales" | Note as "enterprise pricing, not public" and move on |
| Market boundary is unclear | Too many or too few vendors fit | Ask user to clarify scope or define inclusion criteria |
| Vendor has pivoted recently | Old sources describe different product | Flag the pivot, use most recent sources only |
| Only vendor-sourced claims available | No independent reviews found | Mark all claims as vendor-sourced, flag for verification |

## Integration Points

- Uses `aimultiple-source-validation` for evidence grading on vendor claims.
- Feeds into `aimultiple-curriculum-builder` to inform which concepts matter for the benchmark.
- Feeds into `aimultiple-benchmark-methodology-design` when the benchmark is being designed.
- Can be run independently of the learning workflow.
