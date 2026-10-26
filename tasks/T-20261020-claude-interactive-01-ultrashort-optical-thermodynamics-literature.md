---
id: T-20261020-claude-interactive-01
title: "Literature review and candidate problem card(s): optical thermodynamics of ultrashort pulses in disordered multimode fibre, with self-steepening, Raman and other corrections"
type: literature
status: done
priority: 1
problem: null
claim: null
family_required: gpt
lease_hours: 8
created_by: claude-interactive
created: 2026-10-20
completed: 2026-10-20
completion_provenance:
  agent: gpt-f
  model: gpt-6-astra
  family: gpt
---

## Goal

The PI's request (2026-10-20): "introduce a problem card related to generalizing optical thermodynamics to ultrashort pulses in fiber, and understanding corrections due to self-steepening, Raman, and so on. The fiber should have a clear thermalizing mechanism such as disordered." The PI asked that a GPT-6 Astra (effort max) agent do the literature review and propose one or more problem cards.

## Context

Neighbouring cards that the new card(s) must not duplicate:
- P-005: finite-pulse limits of multimode thermalization, which owns the general finite-pulse kinetic closure;
- P-010: finite-pulse and walk-off corrections to Kerr self-cleaning, which owns the operational criterion;
- P-20261016-claude-interactive.7-01: the quantum state of RJ-thermalized light, for CW and spatial models.

The repository's thermalization work uses weak random coupling inside degenerate mode groups as a mixing model. The literature/solver audit found that deterministic multimode self-steepening already exists through the `omega + omega0` prefactor, alongside Raman; the original inference that it appeared only in experimental/stochastic backends was incorrect. No random linear mode-coupling operator was found. C-20261016-claude-interactive.7-03 is still a `cheap-checks-passed` GGE proposal, not a verified general endpoint theorem.

## Deliverables

- A review, `docs/review-2026-10-20-gpt-f-ultrashort-optical-thermodynamics.md`, with a source ledger (DOI or arXiv id and access level), a search log and a PI download list.
- One or more candidate cards, `problems/P-20261020-gpt-f-NN-*.md`, each naming a fibre with a quantified thermalizing mechanism, its dimensionless groups, the form of an answer and a measurable prediction.
- Tasks for loose ends.

The second-family literature check is T-20261020-claude-interactive-02.

## Completion

Completed by gpt-f (gpt-6-astra, family gpt) on 2026-10-20.

- Review and source/access ledger: `docs/review-2026-10-20-gpt-f-ultrashort-optical-thermodynamics.md`, including the full reading of arXiv:2506.23536v2, literal web queries, failed retrievals and the PI download list.
- One candidate: `P-20261020-gpt-f-01`, Raman drift and lifetime of local optical equilibrium in weakly disordered GRIN fibre. Priority 3, partial literature, low novelty confidence; no claim or result proposed.
- Small symbolic/arithmetic run: `2026-10-20-gpt-f-thermodynamic-ledger`. No propagation or kinetic simulation.
- Loose ends: T-20261020-gpt-f-01 through -06 for source access; -07 for the broadband invariant/rate window; -08 for an oracle implementation plan; -09 for the P-005 literature boundary.

Missing full texts and the unestablished physical rate hierarchy are explicit limitations of the completed review, not verified premises. The existing second-family task remains unchanged.
