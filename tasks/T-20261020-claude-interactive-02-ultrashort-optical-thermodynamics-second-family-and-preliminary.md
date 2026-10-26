---
id: T-20261020-claude-interactive-02
title: "Second-family literature check and preliminary progress on the ultrashort-pulse optical-thermodynamics card(s)"
type: derive
status: done
priority: 1
problem: P-20261020-gpt-f-01
claim: null
family_required: not-gpt
lease_hours: 8
created_by: claude-interactive
created: 2026-10-20
---

## Goal

The PI asked (2026-10-20) for an Opus 5.5 agent to make preliminary progress on the problem card(s) from T-20261020-claude-interactive-01. The work has two parts:

1. **Second-family literature check.** Check gpt-f's review and card(s) against the sources, as the second family. If the two families agree on what is open, set the card to `audited`, with an audit-trail row.
2. **Preliminary progress** on the highest-priority card:
   - an exploration note with the reduced model and its invariants;
   - the leading-order derivation;
   - small, convergence-checked numerics;
   - claims at `proposed` where a statement is sharp enough.

## Context

Opened 2026-10-20 by the orchestrator. T-20261020-claude-interactive-01 delivered one candidate card, P-20261020-gpt-f-01 (Raman drift and lifetime of local optical equilibrium in weakly disordered GRIN fibre), with its review (PR #89). This branch stacks on that PR and is worked by claude-interactive.21 (claude-opus-5-5).

## Deliverables

- An audit-trail row on each card.
- An exploration note in `explorations/`, with run folders.
- Claims if any.
- Tasks for loose ends.

## Outcome (2026-10-20, claude-interactive.21)

- **Part A done.** P-20261020-gpt-f-01 is `audited` (`audited_by: [gpt, claude]`), with its regime and derivation target corrected. Review: `docs/review-2026-10-20-claude-interactive.21-ultrashort-thermo-second-family.md`.
- **Part B recorded.** Exploration note `explorations/2026-10-20-claude-interactive.21-raman-parity-selection.md`; runs `2026-10-20-claude-interactive.21-regime-screen` and `2026-10-20-claude-interactive.21-raman-parity` (pre-registered P1–P4 with outcomes) and `2026-10-20-claude-interactive.21-raman-clamp` (two pre-registered clamp tests, inconclusive); claim C-20261020-claude-interactive.21-01 (`cheap-checks-passed`).
- **Loose ends:** T-20261020-claude-interactive.21-01 to -07.
- **Log:** `log/2026-10-20_claude-interactive.21_T-20261020-claude-interactive-02.md`.
