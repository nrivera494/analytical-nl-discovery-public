---
id: T-20261004-claude-interactive-03
title: "Map the normal-dispersion noise minimum P_min(L) from 0.25 to 5 m"
type: explore
status: done
priority: 1
problem: P-20261004-root-01
claim: null
family_required: any
lease_hours: 12
created_by: claude-interactive
created: 2026-10-04
---

## Goal

Measure how the minimum of the filtered-count Fano factor moves with fiber length. This is $P_{\min}(L)$ and $F_{\min}(L)$ for LP01 at 1250 nm in the archive's GIF625 normal-dispersion configuration, from 0.25 to 5 m. Measure the local exponent $\alpha(L)=-d\ln P_{\min}/d\ln L$ and test the crossover hypothesis on P-20261004-root-01. The hypothesis predicts $\alpha\to1$ at short $L$ and $\alpha\to0$ at long $L$, against $\alpha\approx0.79$ near 1 m in the archive.

This is an exploration. The hypothesis was written by claude-interactive, so any later claim built on it must be verified by a non-Claude family.

## Context

Read P-20261004-root-01, `docs/multimode-squeezing-scope.md` and `docs/SOLVER.md`. The archive configuration and its length forecast are in `~/Desktop/fall2026_research/ai driven lab work/research_runs/2026-09-28_theory_campaign/`:
- `inputs/` holds the input spectra;
- `opus_transport/freeze_lengths.py` holds the length forecast;
- `figures/phaseflow_length_forecast_summary.json` and `figures/phaseflow_length_forecast_scores.csv` hold the 0.75 and 1.25 m sweeps.

Its sampled minima are at 180 mW (0.75 m) and 120 mW (1.25 m), and the report gives about 142 mW at 1 m. The minima are shallow (F ≈ 0.91–0.93), so locate them by a local quadratic fit, not by the lowest sampled point. Copy only small configuration files into `runs/`.

Raw data follows the interim local-storage rule in `runs/README.md`: `~/analytical-nl-discovery-data/<run-id>/`, recorded as `raw_location` in `meta.yaml` together with `solver_commit` and `solver_dirty` (`docs/SOLVER.md`).

## Steps

1. **Reproduce.** Rebuild the 0.75, 1 and 1.25 m sweeps with the archive's fiber model, filter window, assumed −0.015 ps² input GDD and both Raman responses. Continue only if $P_{\min}$ agrees within 2%.
2. **Freeze.** Before any new length, write the two limiting predictions in `explorations/<date>-<agent>-pmin-length.md`, with your estimate of the crossover length from the card's dimensionless groups ($\zeta$, $N$, $\Omega_eT_0$) evaluated at $P_{\min}$. Commit that note first.
3. **Map.** Use $L\in\{0.25,0.4,0.6,0.75,1,1.25,1.6,2,3,5\}$ m. For each length:
   - sweep power at no worse than 5% resolution around the minimum;
   - fit $P_{\min}$ and $F_{\min}$;
   - record the decomposition into bright, shape, phase, partition and Raman terms at the minimum.

   Run the Agarwal response first, and the anisotropic one if time allows.
4. **Report.** Give $\alpha(L)$, $F_{\min}(L)$, the term that ends the minimum at each length, and whether the two limits hold. Use the plotting convention in the scope doc.
5. **Convergence.** Check time window and step at the shortest and the longest length.

## Deliverables

- Run folders `runs/<date>-<agent>-*/` containing config, `meta.yaml`, `summary.json` and small figures.
- The exploration note.
- An audit-trail row and an updated "Signal of hidden simplicity" on P-20261004-root-01.
- A session log and a pull request.

If the crossover picture fails, record that as the result.

## Outcome (claude-b.4, subagent of claude-b, 2026-10-04)

Steps 1–5 are complete for the oscillator Raman response. Results are in `explorations/2026-10-04-claude-b.4-pmin-length.md` (Part 2), with runs:
- `2026-10-04-claude-b.4-pmin-gate-1250`
- `2026-10-04-claude-b.4-pmin-length-map`
- `2026-10-04-claude-b.4-pmin-convergence`
- `2026-10-04-claude-b.4-pmin-gdd0-check`

The "Length scaling" bullet on P-20261004-root-01 is updated.

**Short answer.** The crossover picture fails for this configuration.
- With the assumed input chirp, the dip disappears below about 0.4 m. With the input GDD set to zero it does not disappear.
- The first-dip exponent is 0.63–0.83 over 0.4–2 m.
- Over 0.4–2 m the dip sits at a fixed in-band fraction, about 0.4 of the plateau-onset power.
- A second, deeper dip appears below the plateau at 5 m.

**Partly done:**
- The anisotropic response was run at all ten lengths after the oscillator work. The dense pass was run only at 2, 3 and 5 m, and no convergence test was done for it. The picture is unchanged, and at 1 m the result reproduces the archive's anisotropic curve. T-20261004-claude-b.4-03 was opened and closed for this.
- Lengths beyond 5 m and the second dip: T-20261004-claude-b.4-01.
- The chirp-induced disappearance: T-20261004-claude-b.4-02.
- The location rule at other filters and chirps: T-20261004-claude-b.4-04.
