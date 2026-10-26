---
id: T-20261004-claude-interactive-06
title: "Register the archive 1550 nm LP01 soliton noise baselines as solver runs"
type: explore
status: done
priority: 1
problem: P-20261004-root-03
claim: null
family_required: any
lease_hours: 12
created_by: claude-interactive
created: 2026-10-04
---

## Goal

Reproduce, with the pinned solver, the archive's single-mode 1550 nm soliton noise results, and register them as runs. They are the baseline that the multimode problems (root-03, -01, -02) are measured against.

## Context

Read AGENTS.md, `docs/plan-2026-10-round1.md`, the problem card, `docs/SOLVER.md` and, for the squeezing cards, `docs/multimode-squeezing-scope.md`. The source is `~/Desktop/fall2026_research/ai driven lab work/research_runs/2026-09-26_analytics/report.md`, together with its `results/preserved_recipes/README.md` and `results/prepared_sech_1550_0.4ps.npz`.

Reproduce at least:
1. **Pure-Kerr ideal-sech control** at 20 m: F = 0.012687341911 against the analytical 0.012687341923 at the nominal reference phase.
2. **Full-model coherent-reference readout** at 20 m GIF625: 36.76796 mW coupled power, η = 0.995, r = 0.7017289851, ψ = −2.181661565 rad. Archive values: F = 0.03232378 with oscillator Raman and 0.05294744 with anisotropic Raman.
3. **One bandpass-filtered LP01 soliton point** from the archive, chosen and recorded before running.

Copy only small configuration files into `runs/`. Raw data: follow the interim local-storage rule in `runs/README.md`. Raw output goes to `~/analytical-nl-discovery-data/<run-id>/`, and its path is recorded as `raw_location` in `meta.yaml`. For this round's four problems, such runs may be cited by claims.

## Deliverables

- Run folders with config, `meta.yaml` (including `solver_commit`) and `summary.json`.
- A short note in `explorations/` listing any discrepancy with the archive, with a convergence check.
- An audit-trail row on P-20261004-root-03.
- A session log and a pull request.

## Progress

2026-10-04, claude-b.1 (subagent of claude-b). All three cases were reproduced; every compared archive value agrees to the last digit of double precision. The pinned solver's source is byte-identical to the archive's copy.

- Case 1, pure-Kerr ideal sech: run `2026-10-04-claude-b.1-ideal-sech-kerr-20m`. F = 0.012687341911357897 at the nominal phase and 4.295819315491556 after π.
  - The difference from the analytical Green function is −1.1e-11 and −3.8e-10.
  - Under step halving the error falls with exponent 4.0 for Q_YY and for F after π.
  - At the nominal phase the fine-grid error is below the analytical quadrature's own resolution, so no exponent is quoted there.
- Case 2, prepared-sech reference readout at 20 m: run `2026-10-04-claude-b.1-prepared-sech-readout-20m`. F = 0.03232378149230158 (oscillator Raman) and 0.052947442066647844 (anisotropic), with the archive's noise split and output powers.
- Case 3, bandpass point pre-registered in commit 4c79445: run `2026-10-04-claude-b.1-bandpass-1546-1553-20m`. At 1546.5–1553.5 nm, F = 0.369938248889808 (oscillator) and 0.41491050276503666 (anisotropic).
- Convergence and the archive's checks are in each `summary.json` and in `explorations/2026-10-04-claude-b.1-lp01-soliton-baselines.md`. The checks are conservation (F = 1), the linear control and finite differences; a new step-halving test of the finite differences gives exponent 2.00.
- Loose ends:
  - T-20261004-claude-b.1-01: register the 30 m and simple 24 nm recipes.
  - T-20261004-claude-b.1-02: stochastic-propagation cross-check, since these runs share the archive's code.
