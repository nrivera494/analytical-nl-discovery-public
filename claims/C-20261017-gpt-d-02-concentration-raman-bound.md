---
id: C-20261017-gpt-d-02
problem: P-20261016-claude-interactive-02
title: "Conditional arctangent Raman energy-loss ceiling from intensity concentration"
type: bound
status: promoted
agent: gpt-d
model: gpt-6-astra
family: gpt
proposed_by: gpt-d
proposer_model: gpt-6-astra
proposer_family: gpt
verified_by: claude-interactive.8
verifier_family: claude
audited_by: claude-interactive.8
auditor_family: claude
created: 2026-10-17
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0005
---

## Statement

In the lossless scalar photon-conserving shock GNLSE, assume constant
$A_{\rm eff}$ and the normalized single-oscillator response
$h_R(t)=(a^2+b^2)e^{-at}\sin(bt)/b$ for $t>0$, with
$a=1/\tau_2>0$ and $b=1/\tau_1>0$. Define
$I=|A|^2$, $E=\int I\,dt>0$,
$Q=\int I^2dt/E^2$ and
$\kappa_U=n_2f_R(a^2+b^2)/(2cA_{\rm eff})$.
Then the proposed bound is

$$\boxed{0\le-\frac{dE}{dz}\le\kappa_UE^2F(Q),\qquad
F(Q)=\frac2\pi\arctan\!\left(\frac{\pi\tau_2Q}{2}\right)
<\min(1,\tau_2Q).}$$

$Q$ is intensity concentration, with units inverse time. For finite peak
power $P_{\max}$, $Q\le P_{\max}/E$, so the weaker bound replacing $Q$
by $P_{\max}/E$ requires only energy and peak-power measurements.
This improves the energy-only ceiling and the supremum-Raman-weight
$L^2$ or peak-power ceiling for the specified oscillator.

If a **separately justified** cap $Q(z)\le Q_*$ holds for $0\le z\le L$,

$$\frac{E(L)}{E_0}\ge
\frac1{1+\kappa_UE_0L F(Q_*)}.$$

Without such a cap, integrating the measured $F(Q(z))$ gives an
along-trajectory comparison, not an a priori prediction from the launch.
The physical setting is single-mode silica or fluoride oscillator models;
the measurable prediction is a ceiling on Raman energy loss conditional
on the intensity autocorrelation integral or peak power.

## Regime

Exact inequality within the stated model for
$0<\tau_2Q<\infty$, $0<\tau_1/\tau_2<\infty$,
$0\le\kappa_UE_0L<\infty$. No sech, soliton or small-parameter
assumption is used. Proposer quadrature checks cover
$10^{-3}\le\tau_2Q\le10^2$; positive-profile and propagation tests
are specified in runs 2026-10-17-gpt-d-raman-sharpening and
2026-10-17-gpt-d-raman-propagation.

$F=\tau_2Q+O((\tau_2Q)^3)$ at small concentration and
$1-F=4/(\pi^2\tau_2Q)+O((\tau_2Q)^{-3})$ at large concentration.
These describe the bound, not pulse-family saturation.

## Assumptions

- Scalar, deterministic, single spatial mode, lossless GNLSE with real
  dispersion, constant positive $A_{\rm eff}$ and $n_2f_R$.
- Exact shock factor $\omega/\omega_0$, the positive-frequency photon
  interpretation where used, and sufficient regularity for the core
  Raman energy identity. An orthogonal frequency projection is permitted.
- Real causal normalized **single oscillator** as specified. The closed
  arctangent expression is not claimed for arbitrary multiband responses.
- Nonnegative intensity $I\in L^1\cap L^2$ and $E>0$. Finite peak power
  is needed only for the peak-power version.
- A cap on $Q$ throughout the fiber is an additional hypothesis for
  the stated retention corollary. Neither $Q$ nor $P_{\max}$ is claimed
  conserved or monotone.
- Optimality is claimed only for a relaxed spectral-allocation problem,
  not for physically realizable intensity autocorrelations.

## Predictions

Frozen in commit 6df0927ef31369add037f36db21643b14d68bf51, before the
tests, in [M/predictions.md](../runs/2026-10-17-gpt-d-raman-sharpening/predictions.md).
For $\tau_2Q=10^{-3},10^{-2},0.1,1,10,100$, level-set quadrature must
match $F$ within relative $10^{-8}$. No ratio $\rho/F>1+10^{-8}$ in
the specified profile suite: sech, Gaussian, rectangular, super-Gaussian,
incoherent pairs, chirped coherent pairs and seeded positive mixtures.
The conditional inequality must also hold at every monitored propagation
plane in the frozen core/held-out suite.

## Derivation

Let $f=|\widetilde I|^2/E^2$. Positivity and Parseval give
$0\le f\le1$ and $\int f\,d\Omega/(2\pi)=Q$.
Maximize $\int Wf$ over this relaxed class by filling the largest values
of $W$. For the oscillator these frequencies are
$[-\Omega_+,-\Omega_-]\cup[\Omega_-,\Omega_+]$, where
$\Omega_+\Omega_-=a^2+b^2$ and $\Omega_+-\Omega_-=\pi Q$.
The common endpoint value is
$2a(a^2+b^2)/[(\pi Q)^2+4a^2]$.
Differentiating the optimal integral with respect to $\pi Q$ and
integrating from zero yields the stated arctangent. Its independence
from $b$ follows from these level sets.
The relaxed optimizer has a hole at zero frequency and is not asserted
to be an admissible intensity spectrum.
Details: [proof note](notes/proof-2026-10-17-gpt-d-raman-sharpening.md).

## Checks

Rows by gpt-d are **proposer checks**; rows by claude-interactive.8 are the
independent cross-family verification and audit. M denotes
2026-10-17-gpt-d-raman-sharpening, P denotes
2026-10-17-gpt-d-raman-propagation, Q denotes the derived run
2026-10-17-gpt-d-raman-conditional, and L denotes
2026-10-17-gpt-d-raman-literature. C, S and H denote the verifier's runs
2026-10-17-claude-interactive.8-concentration, -sech-tightness and -hc-relaxed.

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units and symmetries | $Q$ has inverse-time units; $\tau_2Q$ and $F$ are dimensionless. Phase/time shifts and energy rescaling preserve the normalized bound | gpt-d (gpt), analytic | M | 2026-10-17 |
| Known limits | Approaches the supremum-weight slope at small $Q$ and the universal ceiling at large $Q$; strictly below both for finite positive $Q$ | gpt-d (gpt), analytic | M | 2026-10-17 |
| Level-set integral | Maximum relative error $1.34\,10^{-13}$ against direct quadrature | gpt-d (gpt) | M, Q | 2026-10-17 |
| Profiles | All 82 frozen profile tests pass; largest $\rho/F=0.98012330$. This is not evidence of sharpness over physical profiles | gpt-d (gpt) | M, Q | 2026-10-17 |
| Core and held-out propagation | All 36,011 primary accepted planes pass; largest $\rho/F=0.50200193$ | gpt-d (gpt) | P, Q | 2026-10-17 |
| Retention comparison | Core: universal 0.632137, observed-$Q$ cap 0.755777, observed-path comparison 0.840231, actual 0.952963. The latter two are postcomputed, not a priori certified continuum caps | gpt-d (gpt) | P, Q | 2026-10-17 |
| Convergence and second solver | Direct identity, step/grid/window refinements and Julia/Python field checks pass for source propagation run; no separate physical optimality claim | gpt-d (gpt) | P | 2026-10-17 |
| Independent proof check | Bathtub argument rederived. For $\Omega\ne0$, $W=2a\omega_0^2/[(\Omega-\omega_0^2/\Omega)^2+4a^2]$, which proves the single-interval level sets on each side. Positivity of $I$ is used only for $f\le1$; $W\ge0$ only for the lower bound | claude-interactive.8 (claude), analytic | C | 2026-10-17 |
| Independent level sets | Numerical bathtub that does not assume the level-set shape (4,000,001-point grid) equals $F$ within $1.6\times10^{-10}$ at $r\in\{0.381,2\}$, $10^{-3}\le\tau_2Q\le300$; band edges match within $1.3\times10^{-5}$ | claude-interactive.8 (claude) | C | 2026-10-17 |
| Independent profiles and optimizer | 315 positive profiles: max $\rho/F=0.99592$ (at $\tau_2Q=58.6$). Fixed-$Q$ optimizer over positive intensities: best $\rho/F$ 0.520, 0.527, 0.622, 0.894, 0.977 at $\tau_2Q=0.1,0.3,1,3,10$ ($r=0.381$); refined search gives 0.5195 to 0.5268 for $\tau_2Q=0.01$ to 0.3. Bound never exceeded; not attained by physical intensities at finite $Q$ | claude-interactive.8 (claude) | C | 2026-10-17 |
| Independent propagation (held out) | Own GNLSE, 7 launches (SMF-28 surrogate $N=1$ 30/300 fs, $N=3$ 100 fs; held out $N=4$ 200 fs, $N=6$ 100 fs, $N=5$ 300 fs, fluoride $N=4$ 150 fs): 26,507 planes, 0 violations, max $\rho/F=0.409$. Two post-freeze 30 fs fission launches ($N=3$, $N=6$; 14,002 planes): 0 violations, max 0.434 at $\tau_2Q\le1.18$. Retention holds in all, e.g. $N=3$: 0.9327 ≥ 0.6496 ($Q_{\max}$ cap) ≥ 0.5758 ($P_{\max}$ cap) ≥ 0.5048 | claude-interactive.8 (claude) | C | 2026-10-17 |
| Convergence and second solver | Half step $3\times10^{-6}$, half $dt$ and double window $<10^{-13}$, sampled kernel at 1 and 3 fs $\le3.4\times10^{-4}$ (relative change of max ratio). Agents' solver b9fa957, $N=3$: $E(z)$ agrees within $3.2\times10^{-15}$, 0 violations on 101 planes | claude-interactive.8 (claude) | C | 2026-10-17 |
| Relaxed assumption (HC 13-mode silica) | General bathtub $F_W$ holds (propagation max $\rho/F_W=0.41$). The arctangent does not transfer: with $\tau_2=32$ fs, optimized positive intensities exceed $F$ by 1.9% ($\tau_2Q=2.5$, 12.8 fs effective duration) and 4.0% ($\tau_2Q=5$); a sech exceeds it by 2.5% at $T\approx1.7$ fs. With matched $\tau_{2,\rm eff}=52$ fs, $F_W/F$ reaches 1.080. Consistent with the card's single-oscillator restriction | claude-interactive.8 (claude) | H | 2026-10-17 |
| Independent audit | **Pass**, no blockers ([audit](notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-02.md), committed 6320014 before reading proposer material) | claude-interactive.8 (claude) | C, S, H | 2026-10-17 |
| Novelty | gpt-b's long-wave review already gives the weaker peak/supremum-weight inequality. Exact arctangent improvement not found in restricted primary-source search; novelty unestablished | gpt-d (gpt) | L | 2026-10-17 |

## Outcome

**Promoted 2026-10-19.** On the PI's decision of 2026-10-19 (task T-20261019-claude-interactive-07), the statement as audited is promising result [R-0005](../results/promising/R-0005-arctangent-raman-concentration-ceiling/RESULT.md). Gates G6 (T-20261017-gpt-d-04) and G8 are open.

Filed at cheap-checks-passed by gpt-d. Independently verified and audited by
claude-interactive.8 (claude) on 2026-10-17: verdict pass, status **audited**,
regime unchanged. This is a conditional improvement, not a solution of the
problem card's propagated-peak/long-wave reach closure.
- **Attainability.** The verifier's optimizer reaches about $0.52F$ at small $\tau_2Q$ ($r=0.381$), approaching $F$ only as $\tau_2Q\to\infty$. A sharp bound for non-negative intensities is open.
- **General responses.** The extension is the numerical $F_W$. The arctangent with Blow–Wood $\tau_2$ is exceeded under the HC silica response for intensities concentrated to about 13 fs or less.

See the [PI summary](../docs/summary-2026-10-17-gpt-d-C-20261017-gpt-d-02.md) and the
verifier's PI-format summary, first given in the description of PR #60 and since committed as
[docs/summary-2026-10-17-claude-interactive.8-C-20261017-gpt-d-02.md](../docs/summary-2026-10-17-claude-interactive.8-C-20261017-gpt-d-02.md) (3fd45a8; figure:
`runs/2026-10-17-claude-interactive.8-concentration/fig_summary.png`).
The independent verification task T-20261017-gpt-d-03 is done.
T-20261017-gpt-d-04/-05 track prior art and the realistic-response/dynamical-cap
limits; the verifier's HC findings (run H) are input to T-20261017-gpt-d-05.

## Audit trail

| Date | Agent (family) | Change and evidence |
|---|---|---|
| 2026-10-17 | gpt-d (gpt), gpt-6-astra | Proposed after a frozen analytic derivation and tests. The independent core audit was committed as bcecbc6 before comparison with gpt-b's review. No self-verification. |
| 2026-10-17 | claude-interactive.8 (claude), claude-opus-5-5 | Independent verification and adversarial audit, T-20261017-gpt-d-03. Tolerances and launches frozen in f784fed; audit committed in 6320014 before reading proposer material. Verdict pass, no blockers. Status cheap-checks-passed → audited; verified_by and audited_by set. Statement and regime unchanged. Runs C, S, H. |
| 2026-10-19 | claude-interactive.15 (claude), claude-opus-5-5 | Status audited → promoted; `result: R-0005`. Statement unchanged. G5 met (claude-interactive.8's clean-context audit); G6 and G8 open. The Outcome now points at the committed verifier summary instead of saying it could not be written. Task T-20261019-claude-interactive-08 |
