---
name: aimultiple-source-validation
description: |
  Governs evidence quality for AIMultiple research outputs. Use when collecting claims, citing numbers, fact-checking an article draft, or promoting a casual note into a publishable statement. Without this skill, output drifts toward weak sourcing, unverifiable market claims, and precision theater on predictions.
---

# Source Validation

## When to use

Before any factual claim is promoted from a chat answer or a note into publishable text. Also when reviewing a draft and flagging unsupported statements.

## Evidence tiers

- **Tier A (primary).** Official company docs, product pages, filings, direct datasets, benchmark papers authored by the researcher, named analyst reports (Gartner, Forrester, IDC, McKinsey, BCG, Bain, Deloitte, EY, KPMG, PwC, IBM, Google, G2).
- **Tier B (secondary analysis with transparent methodology).** Industry publications that show their sources and method. Acceptable when primary is unavailable.
- **Tier C (opinion / uncited commentary).** Not acceptable as the sole source for any publishable claim.

## Core rules

1. Every publishable claim needs at least one Tier A source. If only Tier B is available, flag the claim as provisional.
2. Pricing and cost claims need either a direct quote from a vendor page or multi-source triangulation.
3. Vendor capability claims need one concrete example: a benchmark task, a case study, or a documented feature.
4. Never cite an AI-generated summary as a primary source.
5. Tag every claim with a confidence label: high / medium / low.
6. Record the claim date and the source date separately. A 2021 source used for a 2026 claim is a failure mode.
7. Any time-sensitive claim older than 90 days needs reconfirmation before reuse.
8. If a source is gated, behind a paywall, or unavailable, mark the claim as provisional.
9. When two sources contradict, surface the contradiction explicitly. Do not quietly pick one.
10. No anonymous social media claims in final outputs.
11. Observed fact vs inference must be labeled differently in the sentence.

## Precision rule

Never quote a prediction to more than two significant figures. "Gartner predicts 5.67% CAGR reaching $6.87 Bn in 2025" becomes "Gartner predicts 6% per annum, reaching $7 Bn in 2025". Precision theater implies certainty that predictions do not have.

## External link spam check

Before citing an external URL, check it via `websiteseochecker.com/domain-authority-checker/`:
- Spam risk >1 is a red flag.
- Domain authority <40 is a red flag.
- Exceptions: official company sites, published datasets, or the only available source for a real-life example, and only when the source is clearly trustworthy.

## Error table

| Symptom | Recovery |
|---|---|
| Claim uses one weak source | Add a Tier A source or drop the claim |
| Claim date and source date mismatched | Rewrite with absolute dates and verify freshness |
| Inference presented as fact | Relabel as inference, or find evidence |
| Precision implying more certainty than justified | Round to two significant figures |
| External source fails spam / DA check | Replace or mark as provisional |

## Integration

- Feeds `aimultiple-article-checklist` phase 1 and 2.
- Gates `aimultiple-publication-quality-gate`.
- Supports `aimultiple-slug-eval` when evaluating whether a topic has enough evidence to justify a new article.
