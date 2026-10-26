---
date: 2026-10-06
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261006-claude-interactive-01
duration_min: 420
---

Also covers progress on T-20261004-gpt-b-02. The duration is approximate active time. The work ran from 2026-10-05 07:00 to 2026-10-06 09:00 EDT with idle gaps, in an interactive session with the PI.

## Did

- **Raman spectrum correction.** In soliton_jitter.ipynb and squeezing_spectral_filter.ipynb, replaced the Raman Langevin spectrum with the symmetrized one ($\coth(\hbar|\omega|/2k_BT) = 2n_{th}+1$, finite DC limit). The legacy one is kept alongside. Re-executed both notebooks. The helper is `example_notebooks/raman_bath_spectrum.jl`.
- **Stochastic check of the adjoint contraction.**
  - Monte Carlo with `stochastic_solve_raman`: Raman noise only, paired random streams, four (spectrum, temperature) variants.
  - A deterministic single-kick test of the adjoint kernel.
  - A check of the noise sampler's covariance.
- **Review of squeezing_spectral_filter.ipynb.** Covered grid, step and adjoint-mode convergence; Raman kernel resolution; the self-steepening factor on the noise; the excess-noise cells; filter handling; variable reuse. Plotted the input sensitivity spectra with and without excess pump noise.
- **Moved the agents' solver to a private copy.** This followed the PI's ruling that agents never modify the original.
  - Created nrivera494/FastDifferentiableMMNLO-agents (private), seeded at `b9fa957`. Its tree is identical to the original's `9c12887`.
  - Pushed the change as `d79f150` on `task/T-20261004-gpt-b-02` and opened [agents' PR #1](https://github.com/nrivera494/FastDifferentiableMMNLO-agents/pull/1).
  - Repointed the submodule. Rewrote `docs/SOLVER.md`. Added AGENTS.md hard rule 14 and updated session step 1 and the Solver section. Added `git submodule sync` to the launcher.
- **Hand-off material for the original.** Wrote `docs/solver-upstream/` (README, LEDGER, the note for this change), so the PI can carry solver changes to the original.
- **Run record.** Registered run `2026-10-05-claude-interactive-raman-stochastic`.

## Found

All numbers are from run `2026-10-05-claude-interactive-raman-stochastic`.

- **Notebook results with the corrected spectrum (300 K).**
  - Jitter: Raman timing variance ×1.0043 at every $L/L_D$ (7.1 $L_D$: 3.728e-31 → 3.744e-31 s²).
  - Squeezing, on the notebook's grid: Raman term ×1.311; total Fano 0.2671 → 0.2830 (−5.73 → −5.48 dB).
  - At 0 K both Raman terms double.
- **The adjoint contraction is exactly the stochastic model's variance.** Single kicks at 1–30 THz match the discrete-adjoint prediction to 1e-6 (at most 1.4e-4 at 30 THz). The sampler covariance matches the assumed form to 1.0003 ± 0.0002.
- **The Monte Carlo agrees only at the 1–2σ level.** It was stopped early by a time limit (85–192 seeds). For jitter, corrected/legacy paired ratios are 1.0040–1.0048 against 1.0043. For squeezing, the paired ratio is 1.290 ± 0.010 against 1.317 (2.7σ, unexplained).
- **Default continuous adjoint.** It is inaccurate for the squeezing observable at dz = 1 mm: single-kick errors of 20–60% at z = 3 m, vacuum Fano −4.8%, Raman term +14%. The discrete adjoint is converged at dz = 1 mm. For jitter the two modes agree to 1e-5.
- **Raman kernel resolution.** The sampled kernel integrates to 0.904 at the notebook's dt = 12.2 fs (∝dt²). With the filter held fixed, the squeezing level moves from −5.44 to −4.72, −5.27 and −5.32 dB between $2^{12}$ and $2^{15}$ points.
- **Self-steepening on the noise term** would raise the Raman term by 7%.
- **Excess pump noise.** The notebook's model gives ×1.28 (notebook grid) and ×1.41 (converged), not the stated ~1.5×. A common-mode energy fluctuation of the same size gives ×1.69.
- **Where the residual noise comes from.** Most of it originates from input vacuum at 1600–1650 nm, on the Raman Stokes side.
- **The public stochastic Raman path still uses the legacy spectrum.** It never passes `Cω`, so it has half the zero-point part and a zero DC term.
- **The original solver repository is unmodified.** Before the move it had only `main` at `9c12887` and no pull requests, so no agent had pushed to it.

## Changed

- `.gitmodules`, solver pin `9c12887` → `b9fa957` (same tree).
- `docs/SOLVER.md`, `AGENTS.md`, `automation/run_session.sh`, `automation/README.md`, `docs/plan-2026-10-round1.md`.
- New: `docs/solver-upstream/{README,LEDGER,2026-10-06-raman-langevin-spectrum}.md`.
- New: `runs/2026-10-05-claude-interactive-raman-stochastic/` (meta.yaml, config.md, summary.json, figure).
- Tasks: T-20261006-claude-interactive-01 (done) and -02 to -08 (open).
- Solver, agents' copy: `d79f150` on `task/T-20261004-gpt-b-02` (PR #1, not merged). The same change is in `2f632d9` on the original's history, local in `~/agent-work/solver-raman` only.
- `~/agent-work/solver-raman`: the original is now a fetch-only remote named `original` with push URL `DISABLED`; `origin` is the agents' copy.
- T-20261004-gpt-b-02 stays open. Its task file is on the unmerged branch of PR #8, and its `src/` option and tests are not done.

## Not verified

- **Which spectrum is physical.** It rests on the linearization argument recorded in `docs/solver-upstream/2026-10-06-raman-langevin-spectrum.md`, which agrees with gpt-b's Wigner-representation reading. The stochastic check cannot decide it; both codes take the spectrum as input.
- **The squeezing Monte Carlo tension (2.7σ)** is not resolved (T-20261006-claude-interactive-06).
- **The $2^{15}$ squeezing value is not shown to be converged.** It is −5.32 dB; $2^{16}$ was not run. The Raman z-quadrature also differs between rows (1, 2, 5 mm).
- **The standard stochastic GNLSE form with self-steepening** was not checked against a source (T-20261006-claude-interactive-04).
- **The CPU test suite** was not run; `src/` is unchanged.
- **Other agents' clones and the PI's local copy.** In `~/agent-work/{gpt-a,gpt-b,claude-a,claude-b}/solver` and `~/agent-work/solver-cache`, the push URL of `origin` now points at the agents' copy. Their fetch URL follows only after they pull main and run `git submodule sync`. The PI's local copy `FastDifferentiableMMNLO for agents/` still pushes to the original; that is the PI's decision.

## Loose ends

- Normalize the sampled Raman response: T-20261006-claude-interactive-02.
- Use the discrete adjoint for noise contractions: T-20261006-claude-interactive-03.
- Self-steepening factor on the Raman Langevin term: T-20261006-claude-interactive-04.
- Converged squeezing with a re-optimized filter (P-20261004-root-03): T-20261006-claude-interactive-05.
- Monte Carlo vs adjoint ratio tension: T-20261006-claude-interactive-06.
- Remaining squeezing-notebook issues: T-20261006-claude-interactive-07.
- Audit agents' noise runs for these issues: T-20261006-claude-interactive-08.
- Opt-in `src/` spectrum option with tests, and fixing the public `RamanLangevin` default: T-20261004-gpt-b-02 (existing; not on main until PR #8 merges).
- Carry the change to the original: PI, from `docs/solver-upstream/LEDGER.md`.
