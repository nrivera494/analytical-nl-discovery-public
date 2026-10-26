---
id: T-20261004-claude-interactive-02
title: "Test the weak-LP02 capture law and its error scaling in two-mode soliton runs"
type: explore
status: done
priority: 1
problem: P-20261004-claude-interactive-01
claim: null
family_required: not-claude
lease_hours: 12
created_by: claude-interactive
created: 2026-10-04
---

## Goal

Test numerically the first-order structure stated on P-20261004-claude-interactive-01, for a weak LP02 admixture in an LP01 soliton. Answer three questions:
- Is $\sigma=2S_{01,02}/S_{01,01}$ equal to 1?
- Does the captured fraction follow $[\pi\delta/(2\sinh(\pi\delta/2))]^2$?
- Does the error of the first-order theory shrink as $\varepsilon^2$?

Also measure whether the filtered mode-resolved Fano factors and their correlation reach finite limits as $\varepsilon\to0$.

This is an exploration, not a claim. The formula was derived by claude-interactive, so a family other than Claude runs this check.

## Context

Read the card, `docs/multimode-squeezing-scope.md` and `docs/SOLVER.md`. LP02 is axisymmetric, so the solver's radial-mode model is enough; LP11 is out of scope here. The archive's prepared 1550 nm soliton is described in `~/Desktop/fall2026_research/ai driven lab work/research_runs/2026-09-26_analytics/report.md` (0.4 ps intensity FWHM sech, $T_0\approx0.227$ ps, GIF625). Use it as the reference pulse.

Raw data follows the interim local-storage rule in `runs/README.md`: `~/analytical-nl-discovery-data/<run-id>/`, recorded as `raw_location` in `meta.yaml` together with `solver_commit` and `solver_dirty` (`docs/SOLVER.md`).

## Steps

1. **Freeze the predictions before running anything.** In `explorations/<date>-<agent>-weak-admixture.md`, tabulate the predicted captured fraction for every $\delta$ you will run, and state the predicted error exponent (2 in $\varepsilon$, i.e. $\propto\varepsilon^2$). Commit the note before the first production run.
2. **Overlaps.** Compute $S_{01,02}/S_{01,01}$ and $S_{02,02}/S_{01,01}$ in two cases:
   - an ideal parabolic profile (expected 1/2 and 1/2), which checks the derivation;
   - the GIF625 model profile at 1550 nm used by the archive.

   Report $\sigma$ for both.
3. **Capture, Kerr only.** Turn off Raman and self-steepening and keep only $\beta_2$. Launch an LP01 fundamental soliton plus a co-launched LP02 copy of the same envelope, at $\varepsilon^2\in\{0.003,0.01,0.03,0.1\}$. Set $\delta$ by changing the LP02 group delay in the model, over $\delta\in\{0,0.5,1,1.5,2,3\}$, and also run the physical GIF625 value.
   - Propagate to $\zeta=20$.
   - The captured fraction is the LP02 energy inside $|\tau|<5$ once the radiation has left. Show it has converged in $\zeta$ and in the window.
   - Compare with the formula. Report the error against $\varepsilon^2$ and the fitted exponent.
4. **Noise.** For $\varepsilon^2\in\{0.003,0.01,0.03\}$, compute with linearized noise, first without Raman and then with both Raman responses:
   - the filtered LP01 and filtered LP02 count Fano factors, and their correlation coefficient;
   - for a symmetric bandpass of $\pm1/T_0$, and for one edge filter you choose and record before running.

   Check that the unfiltered LP02 count gives $F=1$ when Raman is off. Report whether each quantity approaches a finite limit as $\varepsilon\to0$.
5. **Convergence.** Double the time window and halve the step. Add LP03 to measure leakage through the phase-matched 01+03↔02+02 channel at $O(\varepsilon^2)$.

## Deliverables

- Run folders `runs/<date>-<agent>-*/` containing config, `meta.yaml`, `summary.json` and small figures.
- The exploration note, with the frozen predictions and the comparison.
- An audit-trail row and an updated "Signal of hidden simplicity" on P-20261004-claude-interactive-01.
- A session log and a pull request.

Any disagreement with the card's formulas is a result: record it plainly.


## Outcome (gpt-a; gpt-6-astra; gpt)

Completed the independent exploration and registered the frozen predictions and evidence in `explorations/2026-10-04-gpt-a-weak-admixture.md`. The bound projection and quadratic normalized-field error pass; the finite time-window interpretation fails because slow radiation remains. LP03, actual modal dispersion and the coherent-input Raman noise controls are reported. Continuous-frequency sharp-filter convergence remains incomplete and is assigned to `T-20261004-gpt-a-02`; the unavailable measured profile is assigned to `T-20261004-gpt-a-01`. No claim status was promoted.
