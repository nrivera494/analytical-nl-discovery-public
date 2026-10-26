---
id: T-20261004-claude-interactive-08
title: "Reproduce single-mode soliton noise baselines in the solver"
type: explore
status: done
priority: 1
problem: P-20261004-claude-interactive-02
claim: null
family_required: any
lease_hours: 12
created_by: claude-interactive
created: 2026-10-04
---

## Goal

Check, before any multimode derivation, that the solver and analysis tooling reproduce the known **single-mode** results for the collective coordinates of a fundamental soliton (energy, phase, timing, centre frequency). Measure the growth exponents in $z$ and compare them with the literature formulas:
1. **Input vacuum** (Haus–Lai): energy variance conserved; phase variance grows as $z^2$; frequency variance constant; timing variance grows as $z^2$.
2. **Distributed gain with spontaneous emission** (Gordon–Haus): timing variance grows as $z^3$.
3. **Raman:** the mean self-frequency shift (Gordon 1986), and Raman-noise jitter (Corney–Drummond, arXiv:quant-ph/9912096).

## Context

Read AGENTS.md, `docs/plan-2026-10-round1.md`, the problem card, `docs/SOLVER.md` and, for the squeezing cards, `docs/multimode-squeezing-scope.md`. Distributed gain noise may not exist in the solver. If it doesn't, do items 1 and 3, and propose a minimal, opt-in, tested implementation following `docs/SOLVER.md`: a branch and pull request in the solver repository, plus a pin-bump note. Projection onto the collective coordinates should use the adjoint (dual) modes of the linearized soliton, and the projection code is part of the deliverable. Raw data: follow the interim local-storage rule in `runs/README.md`. Raw output goes to `~/analytical-nl-discovery-data/<run-id>/`, and its path is recorded as `raw_location` in `meta.yaml`. For this round's four problems, such runs may be cited by claims.

## Deliverables

- Run folders, and an exploration note with the measured exponents and prefactors against the formulas.
- The projection code under `evaluator/` or `explorations/`.
- If needed, a solver pull request.
- An audit-trail row on P-20261004-claude-interactive-02.
- A session log and a pull request.

## Completion

Completed by gpt-b (gpt; gpt-6-astra), 2026-10-04. See
`explorations/2026-10-04-gpt-b-soliton-noise-baselines.md` and runs
`2026-10-04-gpt-b-soliton-baselines` and
`2026-10-04-gpt-b-noise-pathwise`.

The leading scalar covariance baselines and Raman drift are reproduced with
explicit Wigner sources through existing solver interfaces. The default
Raman spectrum fails the zero-point normalization check; this failure is
preserved and assigned to T-20261004-gpt-b-02 for independent audit and an
opt-in repair. No solver patch or pin change was needed for the baseline.
No multimode derivation was started.
