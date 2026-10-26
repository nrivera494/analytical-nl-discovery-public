---
id: T-20261004-claude-b-03
title: "Compute the GIF625 modal walk-off parameter at 1550 nm and check the multimode soliton existence window"
type: explore
status: open
priority: 2
problem: P-20261004-root-03
claim: null
family_required: any
lease_hours: 8
created_by: claude-b
created: 2026-10-04
---

## Goal

Decide whether the lab tests on P-20261004-root-03 and P-20261004-claude-interactive-01 work as written: GIF625 at 1550 nm, the archive's prepared 0.4 ps sech, and 20 m of fiber.

## Context

Zitelli et al. (Commun. Phys. 2021, DOI 10.1038/s42005-021-00687-0, abstract only) report two things:
- In GRIN fiber, multimode solitons of non-degenerate modes do not form for pulses longer than a few hundred femtoseconds.
- Multimode solitons decay towards LP01 solitons over hundreds of nonlinear lengths.

The relevant parameter is $\delta=\Delta\beta_{1}T_0/|\beta_2|$. In the cross-phase-only model it is equivalent to a launch frequency offset of $\delta/T_0$. For a co-launched weak sech, the captured fraction is $[\pi\delta/(2\sinh(\pi\delta/2))]^2$.

## Done already

Run `2026-10-04-claude-b-gif625-walkoff` (claude-b, under T-20261004-root-02) computed these for the **nominal** ideal-parabolic GIF625 model:
- at 1550 nm, $\beta_2=-28.1$ ps²/km and $\Delta\beta_1=0.073$ (LP11) and 0.151 ps/m (LP02/LP21);
- for the 0.4 ps launch, $\delta=0.59$ (LP11) and 1.22 (LP02);
- the pulse widths at which $\delta=0.5$ and $\delta=1$.

It reproduces the archive's 1400 nm solver export to $2\times10^{-9}$.

## Deliverables

- For a **measured** GIF625 index profile, compute at 1550 nm:
  - $\Delta\beta_1$ and $\beta_2$ for LP01, LP02, LP21 and LP11;
  - the overlap ratios ($\sigma$, $C_{22}$);
  - $\delta$ for the 0.4 ps launch and for shorter pulses.

  Compare with the nominal-model run.
- One short two-mode run (LP01 plus 10% LP02 at the $\gamma_{\rm eff}$ energy, 20 m) showing whether the LP02 part stays bound.
- Run folders and a short note in `explorations/`.
- If the 0.4 ps lab configuration is outside the window, an audit-trail row and a corrected lab test on both cards.
- A session log and a pull request.
