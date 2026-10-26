---
id: T-20261018-claude-interactive.7-01
title: "File the squeezing results as formal claims with Gaussian-validity boundaries, for cross-family verification"
type: explore
status: done
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-18
---

## Goal

PI request (2026-10-18, via the orchestrator): file the three squeezing results of card P-20261016-claude-interactive.7-01 (multimode pre-scrambling squeezing; the condensate's own squeezing; Kerr squeezability of the equilibrated condensate) as claims with regimes, assumption ledgers, run ids and frozen held-out predictions, restated within the Gaussian (linearized) validity domain.

## Context

- Orchestrator message of 2026-10-18 (on the PI's instruction). It asks for one claim per result, from claims/_TEMPLATE.md, each with: a precise statement and main equation; a regime as bounds on $n$, $z/L_{\rm NL}$, $M$, $f_0$, $L_d/L_{\rm NL}$; an assumption ledger; a run id for every number; and frozen held-out predictions for a GPT-family verifier. The existing claim cards are not to be edited (PR #61 updates them).
- gpt-b's review of C-20261016-claude-interactive.7-02: exact one-mode Kerr at $n=4096$, $s=4$ keeps coherence 0.996 but has det $V=2.51$ against $1/4$, so linearized Gaussian statements need an explicit validity boundary.
- Exploration note explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md, sections 6.5, 6.8, 6.10 and 6.11 (new).
- Based on the branch of PR #56 (task/T-20261017-claude-interactive.7-02), which was open at the time.

## Deliverables

- Run `runs/2026-10-18-claude-interactive.7-gaussian-validity/`, with predictions frozen in commit 363ab078 before the checks.
- Claims C-20261018-claude-interactive.7-01 (pre-scrambling squeezing), -02 (the condensate's own squeezing) and -03 (Kerr squeezability of the equilibrated condensate).
- Verify tasks T-20261018-claude-interactive.7-02, -03 and -04, all with family_required gpt.
- Card P-20261016-claude-interactive.7-01: claims list, superseded marks and audit trail. Note §6.11.

Done 2026-10-18; see log/2026-10-18_claude-interactive.7_T-20261018-claude-interactive.7-01.md.
