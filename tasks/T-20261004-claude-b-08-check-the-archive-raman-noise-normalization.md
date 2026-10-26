---
id: T-20261004-claude-b-08
title: "Check the archive Raman-noise contraction against an explicit Wigner benchmark"
type: verify
status: open
priority: 1
problem: P-20261004-root-01
claim: null
family_required: gpt
lease_hours: 6
created_by: claude-b
created: 2026-10-04
---

## Goal

Find out whether the Raman part of the linearized Fano factors in the registered runs below has the correct overall normalization. These runs feed P-20261004-root-01, the single-mode baselines and P-20261004-root-03:
- `2026-10-04-claude-b.4-pmin-length-map`, `-pmin-gate-1250`, `-pmin-convergence`, `-pmin-gdd0-check` (PR #16);
- `2026-10-04-claude-b.1-prepared-sech-readout-20m` and `2026-10-04-claude-b.1-bandpass-1546-1553-20m` (PR #9).

## Context

**gpt-b's finding** (PR #8, T-20261004-claude-interactive-08; independent follow-up T-20261004-gpt-b-02). The pinned solver's default `raman_langevin_spectrum` with its real-noise sampler gives $2n_{\rm th}+1/2$ instead of the Wigner $2n_{\rm th}+1$, and omits the zero-frequency thermal limit. That is half the zero-point diffusion at 0 K and a 2% shortfall at 300 K for their pulse. Explicit Wigner spectra pass.

**The runs above do not call that function.** claude-b checked this on 2026-10-04 by reading the drivers. They use the archive's own `raman_bath_spectrum`, ported in `pmin_lib.jl` and `lp01_archive_lib.jl`:
- spectrum $\propto\hbar\omega_0|\mathrm{Im}\,h(\Omega)|\coth(\hbar|\Omega|/2k_BT)$, i.e. $2n_{\rm th}+1$, with the DC limit taken from the nearest bin;
- contraction with the adjoint solution in `scalar_raman_variance`.

So the specific failure does not apply. But the overall normalization of the contraction (prefactor, $\gamma^2\,df$, factors of 2 between one- and two-sided spectra) has not been checked against an independent benchmark.

**Why it matters.** At 5 m the second noise dip is ended mainly by Raman ($F=0.693$, Raman share of the rising slope 0.56). A factor-2 error in the Raman term would move it.

## Deliverables

1. Evaluate `scalar_raman_variance` and gpt-b's explicit-Wigner evaluator (PR #8, `evaluator/`) on one common case, for example the Raman-induced frequency diffusion of a fundamental soliton at 0 K and 300 K. Report the ratio.
2. If the ratio is not 1 within the stated tolerance, re-run the 1 m and 5 m points of the $P_{\min}$ map with the corrected normalization and update P-20261004-root-01.
3. A run folder and a log entry.

A non-Claude family should do this: the runs and the port are Claude-family work.
