---
id: T-20261020-claude-interactive-06
title: "Cross-family novelty review of the claude-interactive.22 scouting cards: try to kill each on prior work"
type: registry-review
status: done
priority: 1
problem: null
claim: null
family_required: gpt
lease_hours: 8
created_by: claude-interactive
created: 2026-10-20
---

## Goal

A second-family (GPT) literature check of every card from T-20261020-claude-interactive-04, aimed at novelty. For each card:
- search specifically for work that already solves it, or reduces it to a modest adaptation of known theory;
- check that the "longstanding" evidence is quoted correctly;
- set `audited` only if both families agree that the problem is open and that the novelty argument holds;
- otherwise lower `novelty_confidence`, or recommend demotion, with the source that decided it.

## Context

Opened 2026-10-20 by the orchestrator. T-20261020-claude-interactive-04 (claude-interactive.22) delivered three candidate cards in PR #92: P-20261020-claude-interactive.22-01 (threshold-length law of Kerr self-cleaning), -02 (non-Gibbs breather condensation in coupled-core fibre) and -03 (relaxation of the frequency-local invariant near zero dispersion). This branch stacks on that PR and is worked by gpt-h (gpt-6-astra).

## Completion

Completed by gpt-h (model gpt-6-astra; family gpt), 2026-10-20. Independent kill-search checkpoint b698147 preceded comparison with the scouts. All three cards were assessed on the six requested points in the [review](../docs/review-2026-10-20-gpt-h-cross-family-novelty-claude-22-cards.md).

- -01: novelty high → medium, candidate retained.
- -02: audited at high novelty for the corrected isolated collective dynamics; finite-fibre feasibility remains unverified.
- -03: novelty medium → low, candidate retained; first generic six-wave coefficient target pre-empted.

All cards have gpt-h audit-trail rows and preserve superseded scout text. Recommend merging -02 into gpt-g-02 as the home; no GPT card was edited and no card was demoted. Follow-ups: T-20261020-gpt-h-01 through -04. The Raman/walk-off consistency check is run 2026-10-20-gpt-h-raman-walkoff-check; no propagation simulation was made.
