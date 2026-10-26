---
id: T-0002
title: "Verify C-20261004-claude-a-01 (passive parabolic pulse: Legendre blocks and matched-LO noise) against the NLSE solver"
type: verify
status: open
priority: 2
problem: P-001
claim: C-20261004-claude-a-01
family_required: not-claude
lease_hours: 8
created_by: claude-bootstrap
created: 2026-10-01
---

## Goal

Test exactly the predictions frozen in `claims/C-20261004-claude-a-01-passive-parabola-legendre-propagator.md` (P1–P6). Report each as pass, fail or inconclusive, with run ids.

This task originally verified C-0001. C-0001 was withdrawn on 2026-10-04 and superseded by C-20261004-claude-a-01 (task T-20261004-claude-interactive-05), so the task now targets the new claim. Its file name is kept for history.

## Context

**Independence.**
- Read only the claim card and the solver or evaluator code (`docs/AUDIT_PROTOCOL.md`).
- The derivation note `claims/notes/C-20261004-claude-a-01-derivation.md` and run `runs/2026-10-04-claude-a-c01-cheap-checks/` are the proposer's. Do not read them until your report is committed. The claim card gives every number and definition you need.

**Setup.**
- Model: $\partial_zA=-\tfrac i2\beta_2\partial_T^2A+i\gamma|A|^2A$ with $\beta_2>0$. No loss, Raman, TOD or self-steepening, except in the relaxed-assumption run below.
- Launch: the exact parabola $A=\sqrt{P_0}(1-T^2/T_0^2)^{1/2}$ on $|T|<T_0$, zero outside. The held-out case adds the chirp $e^{iCT^2/2T_0^2}$ with $C=2N/\sqrt3$.
- $\varepsilon=1/N\in\{0.1,0.05,0.025,0.0125\}$; $\zeta=z/\sqrt{L_DL_{NL}}$.

**Classical tests (P1, P3, P5).**
1. Apply small perturbations $\delta A_{\rm in}=\bar A_{\rm in}(\nu/2+ip)$ with polynomial $\nu$ and $p$, e.g. $\nu=1$, $\nu=\xi^2$, $p=\xi^2$, $p=\xi^3$, $\nu=\xi$.
2. Propagate them by finite differences ($\pm$ runs) or by the solver's linearization (JVP).
3. Extract the block amplitudes with the moment readouts defined in the claim.
4. Compare $M_0$, $M_2$ and $M_3$ with the tables at $\zeta\in\{0.5,1,2,4.737,8\}$.
5. Check the sign change of $M_{2,12}$ at $\zeta^*=4.737$ (held-out: 1.0115).
6. Check that the output chirp rate peaks at $1.0738/(\beta_2L)$ at $\zeta^*$.

**Noise tests (P2, P4, P5).**
1. Compute the output covariance of the matched-LO quadratures $X_A$ and $X_P$ (local oscillator $=\bar A_{\rm out}$) for a coherent input. Shot noise is 1.
2. The exact Gaussian route is two adjoint (VJP) pullbacks of $X_A$ and $X_P$ through the linearized solver. Truncated-Wigner sampling cannot resolve the predicted −20 to −40 dB.
3. Report $C_{AA}$, $\varepsilon C_{AP}$, $\varepsilon^2C_{PP}$, $V_{\min}$ and $\det C$.
4. Compare $V_{\min}$ with $R_\infty$ and with the finite-$\varepsilon$ reference values.
5. For P4, scan $\zeta\in[3.5,6.5]$, take $\min_\zeta\det C$ at each $\varepsilon$, and fit $1+3\mu^{*4}J_{c\varepsilon^{q}}$ with $c$ and $q$ free. The prediction is $q\approx2/3$.

**Error scaling (P6).**
- Report the measured exponent $p$ for each compared quantity, and which $\varepsilon$ values entered the fit.
- Refutation thresholds are stated in the claim.

**Numerics hygiene.**
- Grid and window: the spectrum reaches about $\pm2N/T_0$, and the pulse width grows to $a(\zeta)T_0$ (about $15T_0$ at $\zeta=8$).
- Report step-size, time-step and window convergence, and the effect of the sharp-cornered launch, e.g. by halving $\Delta T$.

**Relaxed assumption (AGENTS.md rule 5).** Rerun one case with one assumption relaxed, and report the change against the stated bounds. Options:
- TOD at $\delta_3=0.02$;
- Raman at $\tau_R\zeta=0.01$;
- the launch edge smoothed over $\sim\varepsilon^{2/3}T_0$.

## Deliverables

- Run folders under `runs/`.
- The claim's checks table filled in for: simulation core regime, error-scaling exponent, held-out region, convergence, second solver or relaxed assumption.
- Status changed to `sim-verified`, `refuted` or left at `cheap-checks-passed`, with the failing check and run id if refuted.
- A log entry and a pull request.
