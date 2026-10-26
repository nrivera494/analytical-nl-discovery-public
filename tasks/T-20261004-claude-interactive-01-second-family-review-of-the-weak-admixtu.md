---
id: T-20261004-claude-interactive-01
title: "Second-family review of the weak-admixture and collective-noise squeezing cards"
type: registry-review
status: done
priority: 2
problem: null
claim: null
family_required: not-claude
lease_hours: 8
created_by: claude-interactive
created: 2026-10-04
---

## Goal

A model family other than Claude reviews three cards: P-20261004-claude-interactive-01 (weak LP02/LP11 admixture), P-20261004-claude-interactive-02 (collective-coordinate noise of a multimode soliton) and, added for round 1, P-20261004-root-03 (minimum noise for a multimode soliton launch). The review either confirms the stated gaps or narrows or demotes the cards with evidence.

## Context

Both cards were written by claude-interactive on the PI's instruction on 2026-10-04, with abstract-level literature only. Start with:

1. Re-derive the parabolic-profile overlap ratios ($\sigma=1$ for LP02 and LP11) and the capture formula $[\pi\delta/(2\sinh(\pi\delta/2))]^2$.
2. Read Steiglitz & Rand, PRA 79, 021802 (2009), and the soliton-trapping literature, to decide how much of P-20261004-claude-interactive-01 is already known.
3. Search for multimode or vector-soliton Gordon–Haus and Raman-jitter analyses for P-20261004-claude-interactive-02.

Shared definitions are in `docs/multimode-squeezing-scope.md`.

## Deliverables

Updated cards with an access level for every source, an audit-trail row, and `gpt` (or your family) added to `audited_by` if the review is complete. Also a session log.

## Completion

Completed by gpt-b (gpt-6-astra; gpt) on 2026-10-04. The independent report is `docs/review-2026-10-04-gpt-b-soliton-noise.md`, with symbolic/quadrature run `2026-10-04-gpt-b-overlap-capture`. All three cards were narrowed and reviewed by gpt; they remain candidates pending the independent Claude review. Source-access loose ends are T-20261004-gpt-b-01. No parallel reviewer branch or PR was read.
