---
id: T-20261016-claude-interactive.7-12
title: "Shot-to-shot mode-power statistics of thermalizing multimode light in a realistic experiment model, against published data"
type: explore
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.7
created: 2026-10-16
---

## Goal

Predict the shot-resolved, mode-resolved output statistics that existing GRIN thermalization experiments would record, and compare with any published shot-resolved data.

A first look (exploration note section 6.7; run 2026-10-16-claude-interactive.7-grin-shot-statistics) used 15 GRIN modes in the resonant model, one condensed launch and 128 shots per ensemble. A fixed launch with a quiet laser at n = 1e10 repeats to g2 - 1 ~ 1e-8 for z <= 75 L_NL, against 0.867 for the Dirichlet (thermal) state. The noise stays Gaussian until z_E(n/F_in). With 1% common-mode amplitude jitter the relative variance reaches 0.34 at z = 100 L_NL. Phases redrawn per shot give the Dirichlet law within about 30 L_NL.

What a realistic model needs:
- hundreds of modes and real intra-group disorder (with T-20261016-claude-interactive.7-04 and -11);
- the pulse shape, dispersion and time-integrated detection. Without dispersion, the instants of one pulse sample one trajectory over the lengths s z (exact scaling of the resonant model). The first look (pulse_stats.py) finds a deterministic temporal speckle: relative variance 0.3-0.7 across the FWHM at z = 30-300 L_NL, reproducible between pulses to 1e-4 for z <= 100. Dispersion and walk-off couple the slices; check whether the speckle survives;
- measured laser noise (pulse energy, pointing, SLM phase noise) entering as F_in.

Deliverables of the comparison:
- the length, in L_NL and in metres, at which a fixed launch's shot-to-shot statistics become thermal, for named published set-ups;
- whether any published data are shot-resolved at a fixed launch. If they are, compare with the predicted relative variances. If none are, specify the measurement.

## Context

- Problem card P-20261016-claude-interactive.7-01 (Lab test), claims C-20261016-claude-interactive.7-01 (Dirichlet) and -02 (scrambling length with F_in).
- Exploration note explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md, sections 6.3, 6.5 and 6.7.

## Deliverables

- A run with the solver (multimode, pulsed or long-window CW, stochastic input ensembles) and a short note.
- An update of the card's Lab test.
