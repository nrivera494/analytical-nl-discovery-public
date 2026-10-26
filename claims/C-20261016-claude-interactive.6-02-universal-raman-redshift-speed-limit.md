---
id: C-20261016-claude-interactive.6-02
problem: P-20261016-claude-interactive-02
title: "Universal Raman speed limit: in the photon-conserving GNLSE the Raman energy loss obeys |dE/dz| <= kappa_U E^2 for any field and any dispersion, so a lossless fibre keeps at least 1/(1 + kappa_U E L) of the launched energy"
type: bound
status: promoted
proposed_by: claude-interactive.6
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: gpt-d
verifier_family: gpt
audited_by: gpt-d
auditor_family: gpt
created: 2026-10-16
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0003
---

## Sharpened statement (cross-family, gpt-d, 2026-10-17)

**Current audited scope:** the energy identity, universal energy-squared ceiling
and lossless retention theorem below. The original Statement and Regime remain
unchanged as historical proposer text. Their inverse-square tightness assertion
remains **refuted** and is excluded from the current scope. The corrected
exponent, exact sech curve and concentration improvement are separately filed
GPT claims C-20261017-gpt-d-01 and C-20261017-gpt-d-02, not verified by their
proposer.

Let $I=|A|^2$, $E=\int I\,dt>0$,
$\widetilde f(\Omega)=\int f(t)e^{i\Omega t}dt$,
$W=\Omega\operatorname{Im}\widetilde h_R$ and $k=h_R'(0^+)$.
In the scalar deterministic photon-conserving model in the original Statement,

$$\boxed{0\le-E'=\frac{n_2f_R}{cA_{\rm eff}}
\int W|\widetilde I|^2\frac{d\Omega}{2\pi}
\le\kappa_UE^2,\qquad
\kappa_U=\frac{n_2f_R k}{2cA_{\rm eff}},\qquad
\frac{E(L)}{E_0}\ge(1+\kappa_UE_0L)^{-1}.}$$

The exact hypotheses are constant positive $A_{\rm eff}$ and $n_2f_R$,
arbitrary **real** dispersion, no gain or linear loss, and sufficient field
regularity and decay for integration by parts. The normalized response is real
and causal, $h_R(0^+)=0$, $0<k<\infty$, and $W\ge0$ is integrable.
Require enough Fourier-inversion regularity for
$\int W\,d\Omega/(2\pi)=k/2$; decay and bounded variation of $h_R'$ together
with the stated integrability suffice. Causality or finite $k$ alone is
not the full premise.

The dimensionless domain is $E/E_0>0$, $0\le\kappa_UE_0L<\infty$;
there is no long-pulse, soliton-order or dispersion-sign restriction.
The photon-number interpretation additionally needs positive optical support
and finite positive $\mathcal N$. An orthogonal support projection preserves
the identities; the solver's default smooth blue-edge window does not belong
to the exact lossless model.

Proof: the nonlinear energy balance gives the spectral identity; $I\ge0$
gives $|\widetilde I|\le E$; passivity and the sum rule give the ceiling;
integrate $(1/E)'\le\kappa_U$. The mathematical constant is sharp under
intensity concentration, without a claim of subcycle material validity.
See the [independent proof](notes/proof-2026-10-17-gpt-d-raman-sharpening.md),
[audit](notes/audit-2026-10-17-gpt-d-C-20261016-claude-interactive.6-02.md)
and [PI summary](../docs/summary-2026-10-17-gpt-d-C-20261016-claude-interactive.6-02.md).

The frozen core plus eight held-out propagation launches cover $1\le N\le6$
and intensity FWHM 30--300 fs in the declared SMF-28 surrogate, plus a
published-parameter ZBLAN oscillator with surrogate dispersion. All monitored
planes respect both inequalities. Largest accepted-plane $\rho=0.31037732$
(including RK stages: 0.31037870); the core retains 0.95296272 versus the
lower bound 0.63213680. These numbers and the numerical regime trace to
run 2026-10-17-gpt-d-raman-propagation. They do not certify a measured
broadband fiber specimen. The initial freeze is commit 6df0927 and the
independent audit was committed as bcecbc6 before the gpt-b comparison.

## Statement

**Model.** The scalar GNLSE with constant effective area $A_{\rm eff}$ and the shock factor, which is the model of the agents' solver. Here $\tilde A(\omega)$ is the field spectrum, $\Omega=\omega-\omega_0$, $\gamma_0=n_2\omega_0/(cA_{\rm eff})$, and $\mathcal F$ the Fourier transform:
$$\partial_z\tilde A=i[\beta(\omega)-\beta_0-\beta_1\Omega]\tilde A+i\gamma_0\frac{\omega}{\omega_0}\mathcal F\{A[(1-f_R)|A|^2+f_R\,h_R*|A|^2]\}.$$
- $\beta(\omega)$ is arbitrary, and the fibre is lossless.
- $h_R$ is real and causal, with $\int h_R=1$, $h_R(0^+)=0$, and $\Omega\,{\rm Im}\,\tilde h_R(\Omega)\ge0$ (a passive response).

Write $I=|A|^2$, $E=\int I\,dt$, $\mathcal N=\int|\tilde A|^2/(\hbar\omega)\,d\omega/2\pi$, and $\bar\omega=E/(\hbar\mathcal N)$. Then:

1. $d\mathcal N/dz=0$. The energy obeys the identity
$$\frac{dE}{dz}=-\frac{n_2f_R}{cA_{\rm eff}}\int\frac{d\Omega}{2\pi}\,\Omega\,{\rm Im}\,\tilde h_R(\Omega)\,|\tilde I(\Omega)|^2\le0 .$$
   It does not depend on $\beta(\omega)$.
2. **(the bound)** For every field,
$$\Big|\frac{dE}{dz}\Big|\le\kappa_U E^2,\qquad \kappa_U=\frac{n_2f_R\,h_R'(0^+)}{2cA_{\rm eff}} .$$
   No peak-power or bandwidth control is needed.
3. Hence, over a length $L$:
$$\frac{E_{\rm out}}{E_{\rm in}}\ge\frac{1}{1+\kappa_UE_{\rm in}L} .$$
   Equivalently, the photon-harmonic-mean wavelength $\bar\lambda=2\pi c/\bar\omega$ grows at most at the constant rate
$$\frac{d\bar\lambda}{dz}\le\frac{\pi\hbar\,n_2f_R\,h_R'(0^+)}{A_{\rm eff}}\,\mathcal N .$$
   This holds whatever the input shape, chirp, mask, or fibre dispersion.

For the single-oscillator response $h_R=\frac{\tau_1^2+\tau_2^2}{\tau_1\tau_2^2}e^{-t/\tau_2}\sin(t/\tau_1)$, $h_R'(0^+)=\tau_1^{-2}+\tau_2^{-2}$. For silica ($\tau_1=12.2$ fs, $\tau_2=32$ fs, $f_R=0.18$) in SMF-28 ($A_{\rm eff}=64.5$ µm², $n_2=2.6\times10^{-20}$ m²/W), $\kappa_U=9.31\times10^{-4}$ pJ⁻¹ m⁻¹ (run `2026-10-16-claude-interactive.6-c02-heldout`, `summary.json`).

## Regime

Exact within the model, with no small parameter. Its tightness is set by $\tau_R/T$:
- The bound is approached only when the intensity spectrum $|\tilde I(\Omega)|$ stays close to $E$ across the whole Raman band, which needs features shorter than $\tau_1$.
- For a sech pulse of width $T$, the ratio of rate to bound falls roughly as $(\tau/T)^2$ once $T\gg\tau_1$.
- It is a useful constraint only for $\kappa_UE_{\rm in}L\lesssim1$. Example: for $E_{\rm in}=4.25$ nJ in SMF-28, that means $L\lesssim0.25$ m.

## Assumptions

- Scalar, single mode, deterministic; lossless.
- Constant $A_{\rm eff}$ and constant $n_2$, with the shock factor exactly $\omega/\omega_0$, as in the agents' solver.
- With frequency-dependent $A_{\rm eff}$, the photon-conserving form of Laegsgaard keeps item 1 with $|\tilde I|$ replaced by the intensity of the transformed field. Item 2 then needs the bound $|\tilde I_B|\le\int|B|^2$, which still holds, but $\int|B|^2$ is no longer the energy. This is not developed here.
- The Raman response is passive: $\Omega\,{\rm Im}\,\tilde h_R\ge0$, $h_R(0^+)=0$, and $h_R'$ of bounded variation. A response with a jump at $t=0$ makes $\int\Omega\,{\rm Im}\,\tilde h_R$ diverge, and item 2 then fails.
- The discrete solver adds a fixed blue-edge anti-alias window in the Kerr prefactor. It removes photons at about $3\times10^{-4}$ per metre in the test case, so the solver's conservation is approximate there (run `2026-10-16-claude-interactive.6-h1-conservation`, `summary_window_diagnosis.json`).

## Predictions

Frozen in commit `4f0f1ff` (`claims/notes/T-20261016-claude-interactive-04-hypotheses.md`, H1). The test case is SMF-28: a TL sech launch with $N=3$, $T_0=56.7$ fs, $E=4.25$ nJ, $L=1$ m.
- The identity integrated over $z$ matches $E(L)-E(0)$ to a relative mismatch $\le10^{-3}$.
- The bound holds at every saved plane. The predicted slack ratio was $<0.1$; this prediction failed (see Checks).
- The photon mean frequency is monotone.

**Held-out**, frozen with this card and not yet run:
- Item 3 holds for lossless reruns of three `2026-10-16-claude-interactive.6-h2-fission` launches: TL $N=4$ and $N=6$ at 100 fs, and $N=6$ at 300 fs, up to 17 nJ.
  - *Correction made at 13:12, before the test ran:* the frozen text said "every run of h2-fission", but those runs include the silica IR edge, and item 3 holds only without loss. The test script `runs/2026-10-16-claude-interactive.6-c02-heldout/c02_heldout.py` was written for lossless reruns.
- The rate-to-bound ratio is largest at the first compression point and stays below 0.5 for TL sech launches with $N\le6$ and $T_0\ge56.7$ fs.

## Derivation

Use Parseval with $\tilde f(\Omega)=\int f e^{i\Omega t}dt$, so that $\Omega\leftrightarrow i\partial_t$. Write $G=AV$ with $V=(1-f_R)I+f_Rh_R*I$, which is real.
- **Photon number:** $\frac{d}{dz}\int\frac{|\tilde A|^2}{\omega}=\frac{2\gamma_0}{\omega_0}{\rm Re}\,i\int\tilde A^*\tilde G=\frac{2\gamma_0}{\omega_0}{\rm Re}\,i\int IV\,dt=0$.
- **Energy:** $\frac{dE}{dz}=\frac{2\gamma_0}{\omega_0}{\rm Re}\,i\int\tilde A^*\Omega\tilde G=-\frac{2\gamma_0}{\omega_0}{\rm Re}\int A^*\partial_t(AV)=-\frac{\gamma_0}{\omega_0}\int I\,\partial_tV\,dt$. The Kerr part vanishes, which leaves $-\frac{\gamma_0f_R}{\omega_0}\int\frac{d\Omega}{2\pi}\,\Omega\,{\rm Im}\,\tilde h_R\,|\tilde I|^2$.
- **The bound:** $|\tilde I(\Omega)|\le\int I=E$, and $\int\frac{d\Omega}{2\pi}\,\Omega\,{\rm Im}\,\tilde h_R=\frac12 h_R'(0^+)$, which is the inverse transform of $-i\Omega\tilde h_R$ at $t=0$, averaged across the jump of $h_R'$.
- **Integration:** with $E=\hbar\mathcal N\bar\omega$ and $\mathcal N$ fixed, $d\bar\omega/dz\ge-\kappa_U\hbar\mathcal N\bar\omega^2$. So $1/\bar\omega$ grows at most linearly, which is item 3.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | $\kappa_U$ in J⁻¹ m⁻¹; $\pi\hbar n_2f_Rh'\mathcal N/A_{\rm eff}$ in m/m | claude | — | 2026-10-16 |
| Known limits | $f_R\to0$: energy conserved. Long pulses: the identity reduces to the linear-$T_R$ (Gordon) rate $-\frac{8T_R\lvert\beta_2\rvert}{15T^4}$ for a sech soliton (checked analytically) | claude | — | 2026-10-16 |
| Symmetries | The identity is invariant under time and frequency translation of $A$: $\lvert\tilde I\rvert$ is unchanged | claude | — | 2026-10-16 |
| Symbolic residual | The sum rule $\int\frac{d\Omega}{2\pi}\,\Omega\,{\rm Im}\,\tilde h_R=h_R'(0^+)/2$ was checked by quadrature on the analytic oscillator spectrum, with a $1/\Omega^2$ tail correction. It agrees to $4\times10^{-11}$ (silica: 3847.59 ps⁻²) and $8\times10^{-12}$ (fluoride stand-in). $\Omega\,{\rm Im}\,\tilde h_R\ge0$ at every sampled $\Omega$ | claude | 2026-10-16-claude-interactive.6-c02-heldout (`sumrule.json`) | 2026-10-16 |
| Simulation, core regime | Identity against $\Delta E$: relative mismatch $2.9\times10^{-5}$. Bound holds at all 201 planes. Max rate/bound = 0.225 at $z=0.06$ m (compression point), so the frozen slack prediction $<0.1$ was **wrong**. $\bar\omega$ decreased at every plane | claude (numpy) | 2026-10-16-claude-interactive.6-h1-conservation | 2026-10-16 |
| Error-scaling exponent | Central inequality is exact. The separate long-sech tightness statement fails: actual GNLSE RHS gives decay exponent 3.00158, versus the stated 2. Short-pulse saturation-gap exponent is 1.00198, versus independently predicted 1. | gpt (gpt-d) | 2026-10-16-gpt-d-c02-rate40, 2026-10-16-gpt-d-c02-rate80, 2026-10-16-gpt-d-c02-rate160; 2026-10-16-gpt-d-raman-bound-audit | 2026-10-16 |
| Held-out region | Lossless TL launches.<br>– Max rate/bound: 0.174 for $N=4$ at 100 fs (7.56 nJ, at $z=0.037$ m); 0.148 for $N=6$ at 100 fs (17.0 nJ); 0.082 for $N=6$ at 300 fs (5.66 nJ). All below the predicted 0.5, and all at the first compression.<br>– Energy retention holds at every saved plane: $E(0.3\,{\rm m})/E_0=0.898$ and 0.879 against the bounds 0.321 and 0.174; $E(1.5\,{\rm m})/E_0=0.893$ against 0.112.<br>– **Artefact found:** the identity's own mismatch is $2.9\times10^{-5}$ at 300 fs but 1.3% ($N=4$) and 25.7% ($N=6$) at 100 fs. In the discrete model this signals aliasing of the nonlinear product at dt = 3 fs, so those two runs were redone at dt = 1.5 fs, $n_t=2^{15}$ (`summary_fine.json`). The identity then holds to $1.5\times10^{-4}$ and $7.5\times10^{-5}$.<br>– Resolved maxima: 0.175 ($N=4$) and **0.089** ($N=6$). The aliased value 0.148 was 66% too high.<br>– Resolved retention at 0.3 m: 0.904 and 0.883, against the bounds 0.321 and 0.174.<br>– Held-out prediction (below 0.5, largest at the first compression): **confirmed** | claude (numpy) | 2026-10-16-claude-interactive.6-c02-heldout (`summary.json`, `summary_fine.json`) | 2026-10-16 |
| Convergence and artefacts | Photon drift in the numpy RK4IP scales as $dz^{2.99}$ (third order; the frozen prediction of fourth order was wrong): $8.9\times10^{-7}$ at 0.125 mm, $6.8\times10^{-6}$ at 0.25 mm. Julia solver drift $-3.0\times10^{-4}$ at 1 m, explained by its blue-edge window: numpy with the same window gives $-3.1\times10^{-4}$ at both dz | claude | 2026-10-16-claude-interactive.6-h1-conservation | 2026-10-16 |
| Second solver or relaxed assumption | Julia agents' solver (b9fa957), same case: $\eta(1.75\,\mu$m$)$ 0.7108 against 0.7100 (numpy). Relaxed $A_{\rm eff}(\omega)$, photon-conserving form: photon drift $4.1\times10^{-6}$, the integrator level. The naive $\gamma(\omega)$ prefactor form violates photon number by −11.8% in 1 m | claude | 2026-10-16-claude-interactive.6-h1-conservation | 2026-10-16 |
| Adversarial audit | Fail as written because the inverse-square tightness law is false. The identity, constant, energy-rate bound and retention theorem independently pass; no bound violation found. Three-start matched discrete-RK4IP phase search reaches 0.865773 of the integrated ceiling normalization. Full report: claims/notes/audit-2026-10-16-gpt-d-C-20261016-claude-interactive.6-02.md | gpt (gpt-d) | 2026-10-16-gpt-d-c02-adjoint; 2026-10-16-gpt-d-c02-mask-fine-shaped; 2026-10-16-gpt-d-c02-rate160 | 2026-10-16 |
| Novelty search | Monotone mean frequency in the photon-conserving form: Bonetti et al., JOSA B 37, 445 (2020), DOI 10.1364/JOSAB.377891 (full text read by gpt-a; abstract only for this agent). Not checked whether the spectral identity in item 1 is written there. The $E^2$ bound and the energy-retention bound were not found in the sources on the card; no dedicated search was made | claude | — | 2026-10-16 |
| Independent identity, constant and passivity | Independent integration by parts and positive oscillator spectrum confirm the identity and factor one-half. Silica kappa = 0.00093103132 pJ^-1 m^-1; both used responses are analytically passive. | gpt (gpt-d) | 2026-10-16-gpt-d-raman-bound-audit | 2026-10-16 |
| Independent core and held-out propagation | Core identity mismatch 2.77e-6; all three held-out bounds pass. Resolved rate maxima 0.175075, 0.0892784 and 0.0824761. Auditor's frozen chirped coherent pulse pair also passes. | gpt (gpt-d) | 2026-10-16-gpt-d-c02-core; 2026-10-16-gpt-d-c02-heldout4; 2026-10-16-gpt-d-c02-heldout6-fine; 2026-10-16-gpt-d-c02-heldout6long; 2026-10-16-gpt-d-c02-own | 2026-10-16 |
| Independent convergence and second solver | Step, grid and window refinements preserve bounds. Julia core retention 0.88517745 versus independent Python 0.88517859; resolved photon drift is at integration-error scale. | gpt (gpt-d) | 2026-10-16-gpt-d-c02-core-step; 2026-10-16-gpt-d-c02-heldout6-step; 2026-10-16-gpt-d-c02-heldout6-fine; 2026-10-16-gpt-d-c02-heldout6-wide; 2026-10-16-gpt-d-c02-julia-core | 2026-10-16 |
| Tightness and area relaxation | Formal positive-frequency short-pulse model reaches rate/bound 0.95564 after window check. Frequency-dependent area passes the transformed-field identity and its weighted-norm bound; unweighted E-squared extension is not asserted. | gpt (gpt-d) | 2026-10-16-gpt-d-c02-short0p5-wide; 2026-10-16-gpt-d-c02-area | 2026-10-16 |
| Independent novelty search | Bonetti DOI 10.1364/JOSAB.377891 and Linale DOI 10.1364/OL.401096: full texts read, exact general spectral identity/E-squared ceiling not explicitly found. Bound is a short corollary of the model. arXiv:2607.05244 energy sections give the inverse-cube long-pulse law. Novelty remains unestablished. | gpt (gpt-d) | 2026-10-16-gpt-d-c02-literature | 2026-10-16 |

### Cross-family narrowing checks, 2026-10-17

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Exact hypotheses and proof | Independently derived identity, positive-weight sum rule, ceiling and retention; added integrability/inversion/support qualifications | gpt-d (gpt) | 2026-10-17-gpt-d-raman-sharpening | 2026-10-17 |
| Frozen propagation | Core plus eight held-out launches; 36,011 accepted planes, 144,017 RHS evaluations; largest accepted $\rho=0.31037732$, no rate/retention violation | gpt-d (gpt) | 2026-10-17-gpt-d-raman-propagation | 2026-10-17 |
| Identity and invariants | Largest primary identity residual over bound $5.59\,10^{-14}$; integrated mismatch $1.36\,10^{-6}$; accepted-plane photon drift $5.42\,10^{-8}$ | gpt-d (gpt) | 2026-10-17-gpt-d-raman-propagation | 2026-10-17 |
| Error scaling and artifacts | Core integrated-balance/photon-drift step exponents 4.972/4.465. Held-out half-step/grid/doubled-window checks pass. Sampled-kernel normalization/rate-error exponents 2.00026/4.00215 at $dt\le3$ fs | gpt-d (gpt) | 2026-10-17-gpt-d-raman-propagation; 2026-10-17-gpt-d-raman-sharpening | 2026-10-17 |
| Second solver | Pinned Julia versus Python: final retention within $1.04\,10^{-10}$ absolute, maximum $\rho$ within $2.84\,10^{-6}$ relative | gpt-d (gpt) | 2026-10-17-gpt-d-raman-propagation | 2026-10-17 |
| Relaxation | 0.2 dB/m uniform loss passes the loss-aware comparison; passive two-oscillator mixture passes with its own sum-rule constant | gpt-d (gpt) | 2026-10-17-gpt-d-raman-propagation | 2026-10-17 |
| Retained failures | Historical inverse-square law remains false. Initial stage-inclusive photon-drift flag is preserved; accepted-plane reanalysis passes. New claim's finite-range near-cancellation slope failure is recorded separately | gpt-d (gpt) | 2026-10-17-gpt-d-raman-propagation; 2026-10-17-gpt-d-raman-sharpening | 2026-10-17 |
| Audit and novelty | Narrowed core passes adversarial review, including the cited earlier discrete-adjoint attack. Bonetti DOI 10.1364/JOSAB.377891 (full text) supplies the model; arXiv:2607.05244 (full text, energy sections) already gives inverse-cube energy loss. Novelty of the ceiling remains unestablished | gpt-d (gpt) | 2026-10-17-gpt-d-raman-literature; 2026-10-16-gpt-d-c02-adjoint | 2026-10-17 |

## Outcome

**Promoted 2026-10-19.** On the PI's decision of 2026-10-19 (task T-20261019-claude-interactive-07), the narrowed core (the energy identity, the $\kappa_UE^2$ ceiling and the retention bound, with the hypotheses of the sharpened statement) is promising result [R-0003](../results/promising/R-0003-raman-energy-loss-ceiling-and-retention/RESULT.md). The inverse-square tightness law stays refuted and is not part of the result; the exact sech curve is R-0004. Gates G6 (prior art, T-20261017-gpt-d-04) and G8 are open.

Verified and audited **as narrowed above**. Status refuted -> audited applies
only to the narrowed core; the original inverse-square corollary remains refuted
in the unchanged proposer text and audit trail. No result promotion is requested.
New content is filed separately (C-20261017-gpt-d-01/-02; verified and audited by claude-interactive.8 on 2026-10-17, now results R-0004 and R-0005).

## Audit trail

| Date | Agent (family) | Change and evidence |
|---|---|---|
| 2026-10-16 | gpt-d (gpt), model gpt-6-astra | Cross-family clean-context audit committed as 4f82776. Status proposed -> refuted **as written**, solely because the stated long-pulse inverse-square tightness law fails (2026-10-16-gpt-d-c02-rate40, 2026-10-16-gpt-d-c02-rate80, 2026-10-16-gpt-d-c02-rate160). The central energy-rate and retention inequalities passed all independent tests. The original statement, assumptions, predictions, derivation and regime remain unchanged; no artificial regime reduction is used to conceal the failed scaling. |
| 2026-10-17 | gpt-d (gpt), model gpt-6-astra | PI-authorized narrowing: refuted -> audited for the core identity, ceiling and retention only, with explicit regularity/passivity/model hypotheses. Independent report committed as bcecbc6; frozen held-out propagation, direct RHS, convergence, two solvers and relaxed assumptions pass (2026-10-17-gpt-d-raman-propagation). Historical failure remains. New corrected/exact sech law and conditional improvement filed as C-20261017-gpt-d-01/-02 with GPT proposer checks only. |
| 2026-10-19 | claude-interactive.15 (claude), claude-opus-5-5 | Status audited → promoted; `result: R-0003`. The result holds the narrowed core only; the statement and the refuted tightness law are unchanged. G5 met (gpt-d's clean-context audits of 2026-10-16 and 2026-10-17); G6 and G8 open. The Outcome sentence on the gpt-d claims now records their verification. Task T-20261019-claude-interactive-08 |
