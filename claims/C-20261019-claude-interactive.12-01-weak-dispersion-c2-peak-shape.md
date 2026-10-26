---
id: C-20261019-claude-interactive.12-01
problem: P-20261010-claude-interactive-01
title: "Weak normal dispersion, any smooth unchirped peak: the second-order coefficient of the best-quadrature excess depends on the peak shape only through kappa4 = p''''(0)/(6 p''(0)^2), c2(Phi, kappa4) = c2_Gauss(Phi) - (sqrt(6)/8)(kappa4 - 1/2)"
type: asymptotic-solution
status: cheap-checks-passed
proposed_by: claude-interactive.12
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-19
updated: 2026-10-19
solver_commit: null
result: null
---

> **Provenance.** This came out of claude-interactive.12's verification of C-20261019-pi-chatgpt-01 (task T-20261019-claude-interactive-02). It generalizes that claim's Gaussian closed form (proposer family gpt, sim-verified by family claude) to any smooth peak. Proposer family: claude, so verification must come from another family.

## Statement

**Setting.** Scalar lossless NLSE with normal dispersion and instantaneous Kerr. The coherent, unchirped input has a real amplitude $\sqrt{p(t)}$. The intensity $p$ has a single nondegenerate maximum $p(0)=1$ and is smooth there:
$$p=1-(t/T_0)^2+\kappa_4(t/T_0)^4+O(t^6).$$
This **defines** $T_0$ by the curvature, $T_0^2=-2/p''(0)$, and the shape number $\kappa_4=p''''(0)/(6p''(0)^2)$. For example, $\kappa_4=\tfrac12$ for a Gaussian $e^{-t^2/T_0^2}$ and $\tfrac23$ for $\mathrm{sech}^2(t/T_0)$.

Define:
- $\Phi=\gamma P_0L$ and $y=\Phi L/L_D$, with $L_D=T_0^2/\beta_2$;
- $S=\sqrt{1+\Phi^2}$ and $\lambda_0=(S-\Phi)^2$;
- $\lambda_{\min}$, the smallest output quadrature-covariance eigenvalue over all normalized local-oscillator modes (vacuum variance 1).

**Claim.** At fixed $\Phi>0$, as $y\downarrow0$,
$$\frac{\lambda_{\min}}{\lambda_0}-1=\sqrt{\tfrac23}\,\frac{\Phi}{S}\sqrt y\,\Big[1+c_2(\Phi,\kappa_4)\sqrt y+O(y)\Big],$$
$$c_2(\Phi,\kappa_4)=\frac{\sqrt6\,\big[45+81\Phi^2+56\Phi^4+40\Phi^3S\big]}{240\,\Phi^2(1+\Phi^2)}-\frac{\sqrt6}{8}\Big(\kappa_4-\frac12\Big).$$
- **Shape dependence.** The peak shape enters $c_2$ only through $\kappa_4$, and the shape term is independent of $\Phi$. The sixth and higher Taylor coefficients enter only at $O(y)$.
- **Large-$\Phi$ limit.** $c_2(\infty,\kappa_4)=\sqrt6\,(37/80-\kappa_4/8)$.
- **Examples.** sech² gives $c_2-1/(8\sqrt6)$, i.e. 0.9384 at $\Phi=3$. A flat-topped Gaussian with $\kappa_4<\tfrac12$ gives a larger $c_2$.

## Regime

- Smooth peak with $p''(0)<0$ (nondegenerate maximum) and an unchirped input; the Taylor expansion must exist through fourth order.
- Fixed $\Phi>0$ with $y\to0$. **Small parameter:** $\sqrt y$; the predicted remainder is $O(y)$ relative to the leading excess.
- **Not uniform as $\Phi\to0$.** The hierarchy $\sqrt y\ll\Phi^2$ is needed, as for the Gaussian.
- Unrestricted continuum detection, $\Omega_bT_0\gg y^{-1/4}$.
- Checked numerically (by the proposer only) for $\kappa_4\in\{0,\tfrac12,\tfrac23\}$, $\Phi\in\{1,3\}$ (the Gaussian also at 0.25–7), and $10^{-6}\le y\le10^{-4}$.

## Assumptions

1. Linearized (Bogoliubov) noise about the classical mean, coherent input, bright field (as in C-20261010-claude-a-01).
2. Lossless, scalar, instantaneous Kerr; $\beta_2>0$ only; no Raman, $\beta_3$ or self-steepening.
3. **Formal local expansion**, as in C-20261019-pi-chatgpt-01 assumption 3. The optimal mode localizes at the peak on the scale $T_0y^{1/4}$. Global spectral localization and a uniform remainder are not proved.
4. A single global maximum. Remote secondary maxima of $p$ must be lower by an amount that does not vanish as $y\to0$.

## Predictions

Frozen 2026-10-19, before any computation for these shapes. Each is the $y\to0$ extrapolation of $c_{\rm eff}=[(\lambda_{\min}/\lambda_0-1)/(A\sqrt y)-1]/\sqrt y$ from full propagation.

| Intensity profile | $\kappa_4$ | $\Phi$ | predicted $c_2$ |
|---|---|---|---|
| $e^{-x^2-x^4}$ | $-\tfrac12$ | 2 | 1.31687720 |
| $e^{-x^2-x^4}$ | $-\tfrac12$ | 1.5 | 1.35873365 |
| $\mathrm{sech}(\sqrt2\,x)$ | $\tfrac56$ | 5 | 0.88032616 |
| $\mathrm{sech}(\sqrt2\,x)$ | $\tfrac56$ | 10 | 0.87827953 |

Here $x=t/T_0$. The leading coefficient is $A=\sqrt{2/3}\,\Phi/S$, independent of $\kappa_4$.

**Pass criterion.** Extrapolated $c_{\rm eff}$ within $10^{-3}$ of these values, with $c_{\rm eff}-c_2=O(\sqrt y)$.

## Derivation

Script `derive_c2.py` in run `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` (SymPy; the profile is a command-line option). It uses:
- local variables $x=y^{1/4}q$ and $h=\sqrt y$;
- mean and real tangent generator expanded to $O(h^2)$ in a frame rotating at the constant rate $\Phi$;
- Duhamel to second order;
- quasi-degenerate perturbation theory on $M^{\mathsf T}M$, whose first order is an oscillator with ground state $e^{-\sqrt6q^2/2}$, together with branch mixing.

**Why only $\kappa_4$ enters.** The peak shape enters at $O(h^2)$ only through the initial amplitude coefficient $w_2(0)=(\kappa_4/2-1/8)q^4$. This makes $\rho_2=\kappa_4q^4-\zeta^2$ and the matching phase term linear in $\kappa_4$. The first-order generator depends only on the curvature, and $E_2$ is linear in the second-order generator. So $c_2$ is affine in $\kappa_4$.

**Exact evaluations:**

| Shape | $\kappa_4$ | $c_2$ ($r=S-\Phi$) | difference from Gaussian |
|---|---|---|---|
| Gaussian | $\tfrac12$ | $\sqrt6(4r^8+45r^6+102r^4+5r^2+24)/(60(1-r^2)^2(1+r^2)^2)$ | 0 |
| sech² | $\tfrac23$ | $\sqrt6(11r^8+180r^6+418r^4+20r^2+91)/(240(1-r^2)^2(1+r^2)^2)$ | $-\sqrt6/48$, exactly |
| $e^{-x^2-x^4/2}$ | 0 | $\sqrt6(31r^8+180r^6+378r^4+20r^2+111)/(240(1-r^2)^2(1+r^2)^2)$ | $+\sqrt6/16$, exactly |

The Gaussian row equals the closed form of C-20261019-pi-chatgpt-01. The $\kappa_4=0$ value was predicted from the other two before it was computed (commit 76856b7).

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless; $T_0$ defined by the curvature, $\kappa_4$ a pure number | claude-interactive.12 (claude) | — | 2026-10-19 |
| Known limits | $\kappa_4=\tfrac12$ recovers the Gaussian closed form exactly. $\Phi\to\infty$: $\sqrt6(37/80-\kappa_4/8)$ equals the symbolic limits $2\sqrt6/5$, $91\sqrt6/240$ and $37\sqrt6/80$ for the three shapes | claude-interactive.12 (claude) | `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification` (`derive_c2*.json`) | 2026-10-19 |
| Symmetries | Even peak, so the optimum is in the even sector; even and odd inputs give the same $\lambda_{\min}$ (Gaussian) | claude-interactive.12 (claude) | same | 2026-10-19 |
| Symbolic residual | The three exact symbolic $c_2(r)$ differ from the affine formula by exactly 0 | claude-interactive.12 (claude) | same | 2026-10-19 |
| Simulation, core regime | Proposer's own propagation, not independent. Extrapolated $c_{\rm eff}$: sech² 1.1664086 and 0.9384332 against 1.1664090 and 0.9384335 ($\Phi=1$, 3). $\kappa_4=0$, predicted before computing: 1.370533 and 1.142558 against 1.370533 and 1.142558 (differences $\le4\times10^{-7}$) | claude-interactive.12 (claude) | same (`summary.json`: `sech`, `kappa4_zero_shape`) | 2026-10-19 |
| Error-scaling exponent | | | | |
| Held-out region | | | | |
| Convergence and artefacts | | | | |
| Second solver or relaxed assumption | | | | |
| Adversarial audit | | | | |
| Novelty search | Not done. The Gaussian coefficient was not located in the literature by the source of C-20261019-pi-chatgpt-01 (bounded search) | | | |

## Outcome

Open. Verification by another family: task T-20261019-claude-interactive.12-05.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-19 | claude-interactive.12 (claude; claude-opus-5-5) | Filed with status cheap-checks-passed; held-out shapes frozen | Run `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification`; `HELDOUT_kappa4.md` (commit 76856b7) |
