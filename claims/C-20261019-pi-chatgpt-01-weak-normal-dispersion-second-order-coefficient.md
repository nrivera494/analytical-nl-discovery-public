---
id: C-20261019-pi-chatgpt-01
problem: P-20261010-claude-interactive-01
title: "Weak normal dispersion, Gaussian pulse: the next term of the best-quadrature excess has the closed coefficient c2(Phi) = sqrt(6)(45+81Phi^2+56Phi^4+40Phi^3 sqrt(1+Phi^2))/(240Phi^2(1+Phi^2)), tending to 2sqrt(6)/5"
type: asymptotic-solution
status: promoted
proposed_by: pi-chatgpt
proposer_model: gpt-6-pro
proposer_family: gpt
verified_by: claude-interactive.12
verifier_family: claude
audited_by: null
auditor_family: null
created: 2026-10-19
updated: 2026-10-19
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: R-0015
---

> **Provenance.** This result comes from the PI's ChatGPT session (GPT 6 Pro, family gpt) of 2026-10-18, which independently verified C-20261010-claude-a-01 item 5. The orchestrator claude-interactive filed it on the PI's instruction. Sources: run [`2026-10-18-pi-chatgpt-independent-verification`](../runs/2026-10-18-pi-chatgpt-independent-verification/) (report section 5.5; `archive/weak_theory/`), and the [review summary](../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md).

## Statement

**Setting.** Scalar NLSE with normal dispersion, instantaneous Kerr, and coherent input $u(0,x)=e^{-x^2/2}$ ($x=t/T_0$; intensity $e^{-x^2}$), with no loss. Define:
- the peak nonlinear phase $\Phi=\gamma P_0L$;
- the weak-dispersion parameter $y=\Phi L/L_D$;
- the dispersionless minimum $\lambda_0=V_{\min}(\Phi)=(\sqrt{1+\Phi^2}-\Phi)^2$;
- $S=\sqrt{1+\Phi^2}$.

$\lambda_{\min}$ is the smallest eigenvalue of the output quadrature covariance, optimized over arbitrary normalized complex local-oscillator modes (vacuum variance 1).

**Claim.** At fixed $\Phi>0$, as $y\downarrow0$,
$$\frac{\lambda_{\min}}{\lambda_0}-1=A(\Phi)\sqrt y\,\big[1+c_2(\Phi)\sqrt y+O(y)\big],\qquad A=\sqrt{\tfrac23}\,\frac{\Phi}{S},$$
$$c_2(\Phi)=\frac{\sqrt6\,\big[45+81\Phi^2+56\Phi^4+40\Phi^3S\big]}{240\,\Phi^2(1+\Phi^2)},\qquad c_2(\infty)=\frac{2\sqrt6}{5}=0.9797958971 .$$
Equivalently, the coefficient of $y$ in the relative excess is $B=A\,c_2=\dfrac{45+81\Phi^2+56\Phi^4+40\Phi^3S}{120\,\Phi S^3}$.

This refines the empirical $c_2\simeq1.0$ of C-20261010-claude-a-01.

## Regime

- Gaussian intensity $e^{-x^2}$ only. Other peak shapes have other leading powers, $m/(m+1)$ for a peak of order $2m$.
- Fixed $\Phi>0$, with $y\to0$. The expansion is not uniform as $\Phi\to0$: $c_2\propto\Phi^{-2}$, and a sufficient hierarchy is $\sqrt y\ll\Phi^2$.
- Unrestricted continuum detection: optical bandwidth $\Omega_bT_0\gg y^{-1/4}$. At fixed detection bandwidth the expansion fails (C-20261010-claude-a-01).
- Numerically supported for $\Phi\in\{2,3,10,40\}$ and $10^{-7}\le y\le10^{-4}$. *[Added 2026-10-19 (claude-interactive.12, family claude): verified by an independent derivation and propagation for $\Phi\in\{0.25,0.5,1,1.5,3,7\}$ over $10^{-7}\le y\le10^{-4}$, with $\Phi=1$, 1.5 and 7 held out. The extrapolation $y\to0$ agrees with $c_2$ to $1.1\times10^{-6}$ for $\Phi\ge1$, $3\times10^{-5}$ at $\Phi=0.5$ and 0.05% at $\Phi=0.25$. Run `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification`.]*
- **Small parameter:** $\sqrt y$. The predicted remainder is $O(y)$ relative to the leading excess.

## Assumptions

1. Linearized (Bogoliubov) noise about the classical mean, with coherent input and a bright-field condition (see C-20261010-claude-a-01; not uniform as the mode narrows).
2. Lossless, scalar, instantaneous Kerr; no Raman, higher-order dispersion or self-steepening.
3. **Formal local expansion.** The optimal mode localizes at the intensity peak on the scale $x\sim y^{1/4}$. Remote, oscillatory or mixed-branch competitors are assumed absent; the global spectral-localization lower bound is not proved. A uniform $O(y^{3/2})$ remainder is not proved.
4. The expansion includes mean reshaping to second order, the time-ordered $G_1G_1$ and $G_2$ Duhamel terms, the noncommutation of $D=-\partial_q^2$ and $q^2$, and mixing with the other quadrature branch. Omitting any of these changes $B$ (report section 5.5).

## Predictions

Frozen by the orchestrator on 2026-10-19 before any Claude-family verification. Values marked † are the source's; values marked ‡ were computed by the orchestrator from the closed form and are new.
1. **Table.** $c_2(2)=1.01069098$†, $c_2(3)=0.98946456$†, $c_2(10)=0.98034160$†, $c_2(40)=0.97982793$†.
2. **Held out‡.** $c_2(1)=1.21744000$, $c_2(1.5)=1.05254743$, $c_2(7)=0.98098336$.
3. **Measured effective coefficient.** $[(\lambda_{\min}/\lambda_0-1)/(A\sqrt y)-1]/\sqrt y$ approaches $c_2(\Phi)$ as $y\to0$, with an $O(\sqrt y)$ deviation. Source†: 0.98943 at $\Phi=3$, $y=10^{-7}$; 0.97998 at $\Phi=10$, $y=10^{-6}$. *[claude-interactive.12, 2026-10-19, run `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification`: the same two points give 0.989325 and 0.980000, on a smooth $\sqrt y$ approach to $c_2$. The source's values are off by $+1.05\times10^{-4}$ and $-2.4\times10^{-5}$, i.e. $8\times10^{-12}$ and $2\times10^{-11}$ relative in $\lambda$, the scale of its finite-difference grid error. The measured slopes $d$ in $c_{\rm eff}=c_2+d\sqrt y+O(y)$ are −1.56, −0.79, −0.44 and −0.35 at $\Phi=1$, 1.5, 3 and 7.]*
4. **Leading coefficient‡.** $A(1)=0.5773503$, $A(1.5)=0.6793662$, $A(7)=0.8082904$.

## Derivation

The derivation is in the run: `archive/weak_theory/weak_dispersion_derivation.md` and `archive/weak_theory/second_order_symbolic.py` (SymPy, exact polynomial action on the harmonic ground state; it derives $B$ and does not insert the closed form), plus report section 5.5. Auditors do not read these until their report is committed.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless; $y$, $\Phi$ and $\lambda$ are in vacuum units | claude-interactive (claude) | — | 2026-10-19 |
| Known limits | $c_2\to2\sqrt6/5$ as $\Phi\to\infty$, checked by hand: the numerator tends to $96\sqrt6\Phi^4$ and the denominator to $240\Phi^4$. $c_2\sim\Phi^{-2}$ as $\Phi\to0$, consistent with the stated non-uniformity | claude-interactive (claude) | — | 2026-10-19 |
| Symbolic residual | The source's SymPy script, rerun unmodified on a second platform, gives an identical result. Its $r$-form ($r=S-\Phi$) and the closed $S$-form agree to 12 digits at $\Phi=1$, 1.5, 2, 3, 7, 10, 40 | claude-interactive (claude) | `2026-10-19-claude-interactive-gpt6pro-quick-repro` | 2026-10-19 |
| Simulation, core regime | Source: full mean and tangent propagation (eighth-order finite differences, DOP853, 3072–4096 points, tolerance $2\times10^{-13}$) gives effective coefficients 0.98943 ($\Phi=3$, $y=10^{-7}$) and 0.97998 ($\Phi=10$, $y=10^{-6}$) | pi-chatgpt (gpt) | `2026-10-18-pi-chatgpt-independent-verification` | 2026-10-18 |
| Error-scaling exponent | Fit $c_{\rm eff}=c+d\sqrt y+ey$ over $10^{-7}\le y\le10^{-4}$ (10 points per $\Phi$). The remainder $\lvert (c_{\rm eff}-c_2)\sqrt y\rvert $ scales as $y^{p}$ with $p=0.9989$, 1.0002, 1.0003, 0.9994 at $\Phi=1$, 1.5, 3, 7 (claim: $O(y)$). The slopes $d$ are −1.563, −0.790, −0.438 and −0.350. The fitted excess exponent is 0.5012–0.5015, and the mode rms width is $(y/24)^{1/4}$ to 0.1% at $y\le10^{-6}$ | claude-interactive.12 (claude) | `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` | 2026-10-19 |
| Held-out region | All three frozen values pass. Extrapolated $c_{\rm eff}(y\to0)$: 1.2174395 (claim 1.21744000) at $\Phi=1$; 1.0525472 (1.05254743) at $\Phi=1.5$; 0.9809822 (0.98098336) at $\Phi=7$; and 0.9894640 (0.98946456) at the source's $\Phi=3$. Three fit variants agree to $\le2.4\times10^{-6}$. Outside the frozen set: $\Phi=0.5$ gives 2.42791 (2.42794) and $\Phi=0.25$ gives 7.8227 (7.8269). The slope grows about as $\Phi^{-3.6}$, consistent with the stated $\sqrt y\ll\Phi^2$ hierarchy | claude-interactive.12 (claude) | `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` | 2026-10-19 |
| Convergence and artefacts | Own Fourier interaction-picture code with DOP853 (rtol $3\times10^{-14}$ for $y\le10^{-6}$); inputs restricted to $\lvert x\rvert \le10\sigma$; at $y=0$ it returns $\lambda_0$ to $\le4.5\times10^{-13}$. At $\Phi=1$, 3, 7 and $y=10^{-4}$, $10^{-7}$: doubling $N$, windows 8 and 14, and input support $7\sigma$ and $14\sigma$ each change $\lambda$ by $\le4\times10^{-13}$ relative and $c_{\rm eff}$ by $\le9\times10^{-7}$. The tolerance scan sets the rtol. Even plus odd inputs change nothing ($5\times10^{-15}$). The mode's edge amplitude is $\le10^{-11}$. The fully unrestricted map (all grid points) at $y=10^{-4}$ equals the restricted one to $1.1\times10^{-12}$. At $\Phi=3$, $y=10^{-4}$, $\lambda$ agrees with the source's Fourier solver to $6\times10^{-14}$ | claude-interactive.12 (claude) | `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` | 2026-10-19 |
| Second solver or relaxed assumption | Second integrator: fixed-step RK4IP with Richardson agrees with DOP853 to $\le1.2\times10^{-13}$. Independent derivation by another route (constant-phase frame, input-side $M^{\mathsf T}M$ perturbation theory): the closed form is reproduced exactly, symbolic residual 0. Relaxed: (i) the formal local expansion (assumption 3), by full propagation, with no remote competitor at $y=10^{-4}$ (unrestricted input); (ii) the pulse shape: for sech the same derivation predicts $c_2-1/(8\sqrt6)$, and propagation confirms it to $4\times10^{-7}$ at $\Phi=1$ and 3, so the closed form is specific to the Gaussian. Not relaxed: Raman, $\beta_3$, self-steepening, loss, finite bandwidth (task T-20261019-claude-interactive.12-02). FastDifferentiableMMNLO not used | claude-interactive.12 (claude) | `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` | 2026-10-19 |
| Adversarial audit | Not done. claude-interactive.12's check followed the clean-context order: own derivation and simulation committed before reading the proposer's material (commits 23111dd, eeb688e, e136364). It is a verification, not an adversarial audit (task T-20261019-claude-interactive.12-03). Line-by-line comparison after reading: the source's mean reshaping, $G_2$ (dilation, $\pm1/(2\Phi)$, $\Phi q^4-2\Phi s^2$), time-ordered $G_1G_1$ term and branch mixing all check out, and its intermediate $r$-form equals mine ([report](notes/audit-2026-10-19-claude-interactive.12-C-20261019-pi-chatgpt-01.md), section F) | claude-interactive.12 (claude) | `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` | 2026-10-19 |
| Novelty search | Source: not located in prior primary literature (bounded search; older full texts not accessed) | pi-chatgpt (gpt) | — | 2026-10-18 |

## Outcome

**Sim-verified (2026-10-19).** The Claude-family verification (claude-interactive.12, task T-20261019-claude-interactive-02) passed with verdict `pass`, regime unchanged. It reproduced the closed form exactly by an independent derivation. With its own propagation it found that $c_{\rm eff}$ extrapolates to $c_2$ within $1.1\times10^{-6}$ at $\Phi=3$ and at the held-out $\Phi=1$, 1.5 and 7, with an $O(y)$ remainder (measured exponent 0.999–1.000). [Audit report](notes/audit-2026-10-19-claude-interactive.12-C-20261019-pi-chatgpt-01.md); [summary](../docs/summary-2026-10-19-claude-interactive.12-C-20261019-pi-chatgpt-01.md).
- **Still open:** a rigorous global-localization bound and uniform remainder (T-20261019-claude-interactive.12-01); realistic-fibre corrections (T-20261019-claude-interactive.12-02); a non-gpt adversarial audit for `audited` (T-20261019-claude-interactive.12-03); Done in the same session: the general-shape form $c_2(\Phi,\kappa_4)=c_2(\Phi)-\tfrac{\sqrt6}{8}(\kappa_4-\tfrac12)$, filed as C-20261019-claude-interactive.12-01 for verification by another family (T-20261019-claude-interactive.12-05).

**Promoted (2026-10-19).** As verified, the claim is promising result [R-0015](../results/promising/R-0015-weak-normal-dispersion-c2-closed-form/RESULT.md), under the PI's decision to promote sim-verified claims. G5 is open (task T-20261019-claude-interactive.12-03), and so is G6 (task T-20261019-claude-interactive-13).

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Filed from GPT 6 Pro's verification report (proposer family gpt) with status cheap-checks-passed; held-out values frozen | Runs `2026-10-18-pi-chatgpt-independent-verification`, `2026-10-19-claude-interactive-gpt6pro-quick-repro` |
| 2026-10-19 | claude-interactive.12 (claude; claude-opus-5-5) | Claude-family verification (task T-20261019-claude-interactive-02), verdict pass. Status cheap-checks-passed → sim-verified; verified_by and verifier_family set. Checks rows filled; measured values added beside the source's in prediction 3 and to the regime (no narrowing). Four tasks created | Run `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification`; [audit report](notes/audit-2026-10-19-claude-interactive.12-C-20261019-pi-chatgpt-01.md) |
| 2026-10-19 | claude-interactive (claude; claude-opus-5-5), on PI instruction | Status sim-verified → promoted; result R-0015 (promising tier) | Task T-20261019-claude-interactive-14 |
