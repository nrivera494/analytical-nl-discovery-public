---
id: C-20261017-gpt-a-01
problem: P-20261016-claude-interactive-03
title: "Thirty-coefficient phase masks give constructive Raman-soliton headroom above the earlier witnesses at N=3,4,5"
type: bound
status: proposed
proposed_by: gpt-a
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-17
updated: 2026-10-17
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

For a fixed-energy sech laser passed through a phase-only spectral mask, the
ideal scalar Raman GNLSE admits the following constructive lower bounds:

$$H_\phi(N,T_0)=\sup_\phi\frac{f_1(\phi;N,T_0)}{f_1(0;N,T_0)}
\ge\begin{cases}1.021,&(N,T_0)=(3,140\,{\rm fs}),\\
1.104,&(N,T_0)=(4,200\,{\rm fs}),\\
1.180,&(N,T_0)=(5,280\,{\rm fs}).\end{cases}$$

Here $q=Nu$, the unmasked input is $u=\operatorname{sech}(t/T_0)$ with mass
2, and $f_1=2\operatorname{Im}\zeta_1/N^2$ is the isolated leading soliton's
ZS energy divided by laser input energy. The output plane is $L=4L_D/N$,
$L_D=T_0^2/|\beta_2|$. The tallest pulse must also be the reddest resolved
soliton under the declared census. Direct gated energy is reported separately.

The explicit witnesses are `selected_N3_coef.csv`, `selected_N4_coef.csv`,
and `selected_N5_coef.csv` in run `2026-10-17-gpt-a-phase-headroom`, with hashes
in `selected_masks.json`. They use Legendre orders 2–31 of the standard-FFT
frequency coordinate $k/(2\pi)$, clipped outside the populated laser band.
A fixed C2 continuation is checked without reoptimizing coefficients.
The conservative inequalities also apply to those C2 continuations; the
stationarity calculation refers only to the original declared basis.
These stronger bounds are new proposer content, separate from the
cross-family verification of C-20261016-claude-a-04. They are not upper bounds
or a law in N, and no converged optimum is asserted at N=4 or N=5.

## Regime

The claim is confined to the three stated points, within
$3\le N\le5$, $0.784\le N^2\tau_1/T_0\le1.090$,
$0.0435\le\tau_1/T_0\le0.0872$, $NL/L_D=4$,
$f_R=0.18$, and $\tau_2/\tau_1=32/12.2$.
All normalized higher-dispersion coefficients, shock parameter
$s=(\omega_0T_0)^{-1}$, and attenuation $\alpha L_D$ are zero in the main claim.
The enclosing bounds do not assert validity at untested intervening points.
There is no physical small-parameter asymptotic expansion. Numerical field
errors are checked against $O(h^4)$ for RK4IP and $O(\delta\tau^2)$ for the
midpoint ZS transfer, with Richardson readout extrapolation.

## Assumptions

1. Scalar deterministic GNLSE; instantaneous Kerr plus causal Blow–Wood Raman
   response with times $\tau_1=12.2$ fs and $\tau_2=32$ fs. No Raman noise.
2. Anomalous constant $\beta_2$, constant nonlinearity, no shock or loss in the
   main bounds. Physical examples use 1550 nm, $\beta_2=-21.7$ ps²/km and
   $\gamma=1.3$ W$^{-1}$km$^{-1}$; these are model parameters, not a broadband
   material certificate.
3. The phase shaper preserves spectral magnitude exactly. Each masked/TL pair
   has the same laser energy. Comparing different fixed-N durations changes
   that energy, so duration-peak fractions are not absolute-energy optima.
4. The leading pulse is isolated. The census screens all peaks above $5\times
   10^{-5}$ of the largest intensity and identifies resolved solitons above
   1% of input energy; no completeness below that floor is claimed.
5. Finite-basis stationarity is distinct from global or continuum optimality.
   The gradient norm is in original Legendre coefficient coordinates, in radians.

## Predictions

The pre-run predictions and tolerance ledger are in the run's `predictions.md`.
The primary freeze is `04cf1e92059772ef6bda543e933460698acd1ce6`;
selected coefficients were frozen in
`50602138e3472b9f2645bb02abdae031372a9722` before all selected-mask holdouts.
The numerical lower bounds above summarize training discovery, not predictions
claimed to precede optimization.

Frozen tests require at least 1% headroom at fixed N and durations 0.95 and
1.05 times training duration, and at $6L_D/N$; positive gated-energy headroom
with physical shock, $\beta_3=0.12$ ps³/km, or 0.2 dB/km loss; and positive
gated-energy headroom at the independently located TL duration peak.
Unchanged normalized-frequency transfer of the N=5 mask to held-out
$N=6,T_0=380$ fs predicts at least 5% headroom. Fixed-energy/length duration
detuning by ±10% and the published SMF-28 dispersion model (arXiv:2301.02945, full text) are domain attacks
without a promised minimum. None is used to select or retune a mask.

## Derivation

These are numerical witnesses, not an analytic optimum. Parseval proves fixed
input energy. A checkpointed discrete RK4IP adjoint and the implicit derivative
of the discrete ZS eigenvalue optimize 30 phase coefficients from three initial
starts per N. Independent repropagation, extraction and a pulse census select
the witnesses using training outputs only. Finite-difference checks validate
the adjoint. No inference from an optimizer endpoint to a global maximum is made.

## Checks

All numbers in this table belong to run `2026-10-17-gpt-a-phase-headroom`.
These are **proposer checks**, not independent verification.

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | $f_1$ and $H$ dimensionless; separate input and gated energies in nJ | gpt-a (gpt) | 2026-10-17-gpt-a-phase-headroom | 2026-10-17 |
| Known limits | Raman-off fundamental sech control passes | gpt-a (gpt) | same | 2026-10-17 |
| Symmetries | Constant and linear spectral phase omitted as phase/time symmetries | gpt-a (gpt) | same | 2026-10-17 |
| Symbolic residual | No claimed analytic waveform or asymptotic law | gpt-a (gpt) | same | 2026-10-17 |
| Simulation, core regime | Training remeasurement gives fractions 0.745613, 0.712400, 0.686274; final qualification recorded below | gpt-a (gpt) | same | 2026-10-17 |
| Error-scaling exponent | Four-step and three-readout-resolution checks in final qualification | gpt-a (gpt) | same | 2026-10-17 |
| Held-out region | Frozen before selected-mask evaluation; final outcomes recorded below | gpt-a (gpt) | same | 2026-10-17 |
| Convergence and artefacts | Only N=3 meets $10^{-5}$ gradient target on both grids; finer norms are $9.62\times10^{-6}$, $1.22\times10^{-4}$, $0.104$ | gpt-a (gpt) | same | 2026-10-17 |
| Second solver or relaxed assumption | Pinned Julia discrete RK4IP comparison and shock/TOD/loss tests | gpt-a (gpt) | same | 2026-10-17 |
| Adversarial audit | Pending Claude-family verification, T-20261017-gpt-a-03 | — | — | 2026-10-17 |
| Novelty search | Phase control: DOI 10.1364/OL.29.000271 (abstract only); Airy redistribution: DOI 10.1103/PhysRevLett.114.073901 (full text, supplement not read). No novelty certificate for the mechanism | gpt-a (gpt) | same | 2026-10-17 |

## Outcome

Proposed after the following completed proposer checks. No self-verification
or promotion is performed. T-20261017-gpt-a-03 requires family `claude`.
Unresolved stationarity/global/basis-size questions remain in
T-20261017-gpt-a-01; broadband material validation remains in T-20261017-gpt-a-02.

## Completed proposer qualification

All values cite `2026-10-17-gpt-a-phase-headroom/verification.json` and the
associated gate/census and stationarity records. The discrepancy bars are
observed numerical estimates, not statistical confidence intervals.

| N | T0 (fs) | f1 ± numerical discrepancy | H ± numerical discrepancy | H at the matched local TL duration peak |
|---:|---:|---:|---:|---:|
| 3 | 140 | 0.745615 ± 0.000038 | 1.022106 ± 0.000118 | 1.016237 |
| 4 | 200 | 0.712400 ± 0.000013 | 1.105943 ± 0.000037 | 1.104566 |
| 5 | 280 | 0.686275 ± 0.000197 | 1.185507 ± 0.000375 | 1.180085 |

The frozen ±5% duration, longer-length and shock/TOD/loss predictions pass,
as does unchanged N=5-mask transfer to N=6: H=1.097668. N=6 red shift falls
from 70.289 to 40.116 THz, so transfer is not a simultaneous shift gain.
The three original training-point masks increase both soliton energy and red
shift at fixed paired laser energy. The full energy/share/shift table is in
the run and the [proposer report](notes/audit-2026-10-17-gpt-a-C-20261016-claude-a-04.md).

RK4IP field-error orders are 3.86–3.96 and ZS readout orders approximately 2.
The selected N=4 Python/Julia fields agree to 4.79e-12. All three independent
finer-grid directional checks pass, but only N=3 meets the declared 1e-5
gradient target on both grids. The raw finite-effort initial-start ranges
are 0.745557–0.745589, 0.712387–0.712390 and 0.674379–0.684373, respectively;
these are not spreads across converged stationary basins.

**N=5 limitation.** Its fraction is stable across windows 160, 320 and 640 T0
within 1.97e-4, and the C2 counterparts still give H>1.1847. Its complex
waveform is not established as window-converged: the 160-to-320 comparison
has relative field difference 1.12, or 0.59 after phase/time alignment.
The 640-T0 diagnostic uses 65536 points solely to keep dt=2.734375 fs; its
exception and freeze d426430 are recorded before launch. This is a post-run
convergence diagnosis, not an added held-out success. Independent verification
must examine the N=5 waveform sensitivity as well as its stable energy fraction.

The final status is **proposed**, with no verifier or auditor assigned on this
card. See [PI summary](../docs/summary-2026-10-17-gpt-a-C-20261017-gpt-a-01.md).

## Audit trail

| Date | Agent (family) | Decision | Evidence |
|---|---|---|---|
| 2026-10-17 | gpt-a (gpt), gpt-6-astra | Filed stronger constructive bounds as new proposer content; no self-verification. | 2026-10-17-gpt-a-phase-headroom; Claude-family task T-20261017-gpt-a-03 |
