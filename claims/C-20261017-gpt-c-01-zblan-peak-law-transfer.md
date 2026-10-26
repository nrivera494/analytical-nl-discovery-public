---
id: C-20261017-gpt-c-01
problem: P-20261016-claude-interactive-03
title: "Frozen transfer of Raman peak laws to measured-response ZBLAN"
type: scaling-law
status: refuted
proposed_by: gpt-c
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-17
updated: 2026-10-17
solver_commit: null
result: null
---

## Statement

For the specified measured-response ZBLAN fibre model and $N=3,4,5,6$,
propose the finite-order extrapolation

$$f_1^*\sqrt N=1.29\pm10\%,\qquad
T_0^*=1.70\tau_g N^{1.62}\pm30\%,\qquad
E_1^*=\frac{2N^2|\beta_2|f_1^*}{\gamma T_0^*}\quad(\text{frozen prediction }\pm45\%).$$

Here $\tau_g=1/\Omega_{g,\max}$ is the inverse angular gain-peak frequency,
$T_0$ the input sech parameter, $N^2=\gamma P_0T_0^2/|\beta_2|$, and $f_1$
the local-ZS leading energy divided by launch energy. Star means the
bracketed local duration maximum at $LN/L_D=4$, $L_D=T_0^2/|\beta_2|$.
The energy is at a share optimum, never an absolute energy ceiling.
All numerical predictions cite run `2026-10-17-gpt-c-zblan-transfer`.

## Regime

$3\le N\le6$ at the four integer orders; $f_R=.24$; $LN/L_D=4$;
$0.22<y_g=N^2\tau_g/T_0<3.9$, shock parameter $<.028$ and normalized
third-order dispersion $|\beta_3|/(6|\beta_2|T_0)<.027$ over the frozen scan.
These are finite numerical tolerances, not controlled asymptotic errors.
Here $f_R$ is the Raman fraction, $L$ the output length, $P_0$ the launch
peak power, $\gamma$ the nonlinear coefficient, and $\beta_2,\beta_3$ the
second- and third-order propagation-constant derivatives. The shock
parameter is $1/(\omega_0T_0)$, where $\omega_0$ is pump angular frequency.

## Assumptions

Scalar, deterministic, transform-limited sech launch; constant mode area
and loss; cubic dispersion. Measured bulk Raman response from Yan et al.
(DOI 10.1364/JOSAB.29.000238, abstract/table and first-page preview accessed),
with eight modes. Published fibre model of Kormokar et al. (DOI
10.1364/JOSAB.409240, full text selected sections): 1940 nm, beta2=-18.9
ps²/km, beta3=.112 ps³/km, gamma=2.1 W^-1 km^-1, loss 50 dB/km. This combines
published material and fibre parameters; it is not a same-spool calibration.
No universal claim across ZBLAN compositions or fabrication histories.

## Predictions

Frozen before propagation in [predictions.md](../runs/2026-10-17-gpt-c-zblan-transfer/predictions.md).
$\tau_g=9.2314793$ fs; for N=3,4,5,6: T0*=93.0372,148.2714,212.8392,
285.9731 fs; E1*=1.29684,1.25284,1.21974,1.19334 nJ, with the stated
tolerances. All cases held out from phase1. Run `2026-10-17-gpt-c-zblan-transfer`.

The separate exit-width null $T_1=T_R^*\pm15\%$ was already rejected in
silica in run `2026-10-17-gpt-c-raman-sharpening`; it is not used to derive
these predictions. The new response-only overlap calculation gives
$T_R^*=22.0557541$ fs; the null is scored separately as a diagnostic.

The overlap convention is
$$R(T)=\frac{\pi}{2}\int_0^\infty
\frac{x^3[-\operatorname{Im}\widehat h_R(x/T)]}{\sinh^2(\pi x/2)}\,dx,
\qquad T_R^*=\arg\max_{T>0}R(T),$$
where $h_R$ is the causal, unit-integral measured-response fit,
$\widehat h_R(\Omega)=\int h_R(t)e^{-i\Omega t}\,dt$, and $x=\Omega T$.
The overall Raman fraction is omitted from R; it cannot change its maximizing
width. T and T1 are sech parameters, not intensity FWHM.

## Derivation

The share coefficient and finite-order exponent come from the independently
checked silica turnover branch, C-20261016-claude-a-02. Replacing the silica
response time by the measured gain-peak inverse frequency is a new, risky
material extrapolation; no theorem supports it. The input area formula
gives the energy prediction. An isolated-soliton Raman overlap maximum
does not imply a share-optimal fission exit width.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | tau_g and durations in fs; area formula gives energy | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer | 2026-10-17 |
| Known limits | Reference removes TOD, shock and loss | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer | 2026-10-17 |
| Symmetries | Constant phase and time translation inherited | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer | 2026-10-17 |
| Symbolic residual | No exact/asymptotic fission solution claimed | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer | 2026-10-17 |
| Simulation, core regime | Physical N=3–6: all four duration predictions fail; scaled shares pass for N=3,4 and fail for N=5,6. Energies pass only the broad frozen ±45% band. Both exit-width definitions fail the ±15% null at every physical order. All eight physical/reference maxima have qualified neighbors on both sides. | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer; `tables.md`, `summary.json` | 2026-10-17 |
| Error-scaling exponent | RK4IP field order 3.990–3.996; sampled kernel 2.000–2.007; shooting 1.99997–1.99999; independent Strang 1.99942. These are numerical error orders; no physical fission-law remainder is controlled. | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer; `accuracy.json` | 2026-10-17 |
| Held-out region | All material cases frozen in b042d48 before propagation, without material refitting. All 40 scores resolve as pass or fail using the full numerical intervals. | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer; `predictions.md`, `freeze.json`, `tables.md` | 2026-10-17 |
| Convergence and artefacts | All 17 grid/window/step/kernel comparisons pass; maximum relative share/gated-energy change 0.01666%, width change 0.03679%. Physical peak brackets use dt=1.30–2.46 fs; loss-corrected photon drift ≤1.64e-8. Narrow-window reference failures retained and recovered; one justified 65536-point doubled-window control. | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer; `accuracy.json`, `artifact_followup.md`, `inventory.json` | 2026-10-17 |
| Second solver or relaxed assumption | Physical TOD/shock/loss versus the reference: all reference shares pass, all positions fail, and energies pass only at N=3. Matched agents' Julia fixed-step Float64 RK4IP field agrees with Python to relative 2.46e-14; independent Strang field error 9.44e-5 at its finest step. | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer; `accuracy.json`, `solver_crosscheck.jl` | 2026-10-17 |
| Adversarial audit | Independent Claude-family verification remains open as T-20261017-gpt-c-05. Proposer attacks already refute the conjunction; they do not confer independently verified status. | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer | 2026-10-17 |
| Novelty search | All four broad parts are **partly published** (high confidence in ingredients): selection/overlap optimization, peak shares, duration turnover and area-law energy. Exact fission selection and general peak laws **not found**, medium confidence. Closest: Kormokar DOI 10.1364/JOSAB.478975 / arXiv:2301.02945 (full text selected); Judge DOI 10.1364/JOSAB.26.002064 and Pant DOI 10.1364/JOSAB.27.001894 (abstract only here; gpt-b's full-text findings attributed); Al-kadry DOI 10.1364/JOSAB.29.001347 (article abstract; associated thesis full text selected). Measured-response ZBLAN transfer itself is already in Kormokar; only the frozen quantitative extrapolation is new proposer content. [Review and search log](../docs/review-2026-10-17-gpt-c-raman-peak-novelty.md). | gpt-c (gpt), proposer | 2026-10-17-gpt-c-zblan-transfer | 2026-10-17 |

## Outcome

**Proposed → refuted by proposer tests.** The gain-peak rescaling fails
even in the reference model. In the physical model the measured input
optima are 149.80, 226.93, 303.81 and 380.07 fs, versus frozen predictions
93.04, 148.27, 212.84 and 285.97 fs. The fitted exit widths are
39.28–51.42 fs against the response-only 22.056 fs maximum. Numerical
brackets and controls cannot account for these discrepancies (run
`2026-10-17-gpt-c-zblan-transfer`). Neither the response-only overlap
construction nor the finite silica law is thereby refuted outside this
material extrapolation.

The [proposer report](notes/audit-2026-10-17-gpt-c-C-20261017-gpt-c-01.md)
and [PI summary](../docs/summary-2026-10-17-gpt-c-C-20261017-gpt-c-01.md)
give all scores and physical observables. T-20261017-gpt-c-05 requests
independent Claude verification; T-20261017-gpt-c-06 requests same-fibre
calibration and material uncertainty. Verifier/auditor fields remain null.

## Audit trail

| Date | Agent / model / family | Change and evidence |
|---|---|---|
| 2026-10-17 | gpt-c / gpt-6-astra / gpt | Filed new quantitative material extrapolation and separately scored width null; all material predictions frozen in b042d48 before propagation. Proposed → refuted by proposer tests in `2026-10-17-gpt-c-zblan-transfer`: bracketed peaks at all eight model/order combinations, 40 resolved scores, 17 passing numerical comparisons and two integrator/solver cross-checks. No self-verification; independent task T-20261017-gpt-c-05 remains open. |
