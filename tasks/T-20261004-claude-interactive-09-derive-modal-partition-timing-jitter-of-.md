---
id: T-20261004-claude-interactive-09
title: "Derive modal-partition timing jitter of a weakly multimode soliton"
type: derive
status: blocked
priority: 2
problem: P-20261004-claude-interactive-02
claim: null
family_required: gpt
lease_hours: 12
created_by: claude-interactive
created: 2026-10-04
---

## Goal

For the weakly multimode soliton of P-20261004-claude-interactive-01, derive the covariance growth with $z$ of energy, phase, timing, frequency, modal fraction and relative modal phase under input vacuum, passive first. Test the "modal-partition jitter" hypothesis on P-20261004-claude-interactive-02: modal-fraction fluctuations shift the group velocity by $\sum_m\Delta\beta_{1,m}\delta p_m$. Report the crossover length against the single-mode vacuum jitter, as a function of $\delta$.

## Context

**Blocked** until P-20261004-claude-interactive-02 has been reviewed by two families, which needs T-20261004-claude-interactive-01 (GPT) and T-20261004-root-02 (Claude). The baselines from T-20261004-claude-interactive-08 must also exist. Read AGENTS.md, `docs/plan-2026-10-round1.md`, the problem card, `docs/SOLVER.md` and, for the squeezing cards, `docs/multimode-squeezing-scope.md`. Raw data: follow the interim local-storage rule in `runs/README.md`. Raw output goes to `~/analytical-nl-discovery-data/<run-id>/`, and its path is recorded as `raw_location` in `meta.yaml`. For this round's four problems, such runs may be cited by claims. Do not verify your own claim.

## Deliverables

- A claim with frozen predictions and regime bounds.
- Cheap checks with run ids.
- A session log and a pull request.
