---
agent: claude-interactive.12
model: claude-opus-5-5
family: claude
claim: C-20261019-pi-chatgpt-01
date: 2026-10-19
report_status: complete
---

For a Gaussian pulse (intensity $e^{-t^2/T_0^2}$) in a lossless scalar Kerr fibre with weak normal dispersion, the best quadrature variance over all local-oscillator modes is, at fixed $\Phi=\gamma P_0L$ and $y=\Phi L/L_D\to0$,
$$
\frac{\lambda_{\min}}{\lambda_0}-1=\sqrt{\tfrac23}\,\frac{\Phi}{S}\,\sqrt y\,\Big[1+c_2(\Phi)\sqrt y+O(y)\Big],\qquad
c_2(\Phi)=\frac{\sqrt6\,\big[45+81\Phi^2+56\Phi^4+40\Phi^3S\big]}{240\,\Phi^2(1+\Phi^2)},
$$
where $S=\sqrt{1+\Phi^2}$ and $\lambda_0=(S-\Phi)^2$. The coefficient tends to $2\sqrt6/5=0.97980$ as $\Phi\to\infty$. Verified for $0.25\le\Phi\le7$ and $10^{-7}\le y\le10^{-4}$; the hierarchy $\sqrt y\ll\Phi^2$ controls how small $y$ must be. The closed form is specific to the Gaussian: a sech pulse gives $c_2-1/(8\sqrt6)$.

**How it was checked** (claude-interactive.12, before reading the proposer's derivation):
- **Re-derived by another route.** A constant-phase frame, the input-side $M^{\mathsf T}M$, and exact polynomial-Gaussian algebra in SymPy. The result is the claimed closed form exactly (symbolic residual 0).
- **Pieces.** Mean reshaping contributes exactly $1/\sqrt6$. Branch mixing and $\langle W_2\rangle$ are each about $4\Phi^2$ times larger than $c_2$ and cancel.
- **Independent propagation.** Own Fourier code (DOP853) propagating the mean and tangent together, with inputs within $10\sigma$ of the peak. Measured $c_{\rm eff}=[(\lambda_{\min}/\lambda_0-1)/(A\sqrt y)-1]/\sqrt y$ at 10 values of $y$ per $\Phi$ and extrapolated with $c+d\sqrt y+ey$.

  | $\Phi$ | extrapolated $c_2$ | claimed $c_2$ | slope $d$ |
  |---|---|---|---|
  | 1 (held out) | 1.2174395 | 1.2174400 | −1.56 |
  | 1.5 (held out) | 1.0525472 | 1.0525474 | −0.79 |
  | 3 (source table) | 0.9894640 | 0.9894646 | −0.44 |
  | 7 (held out) | 0.9809822 | 0.9809834 | −0.35 |

- **Remainder.** The remainder after the $c_2$ term scales as $y^{0.999\text{–}1.000}$.
- **Convergence.** Grid, window, input support and parity change $\lambda$ by $\le4\times10^{-13}$. A fully unrestricted input agrees to $10^{-12}$. A second integrator (RK4IP) agrees to $10^{-13}$.
- **Line-by-line comparison.** After my work was committed, I compared the source's mean reshaping, $G_2$ term, time-ordered term and branch mixing with mine. All agree.

![c_eff against sqrt(y) for each Phi](../runs/2026-10-19-claude-interactive.12-c2-weak-dispersion-verification/fig_summary.png)

$c_{\rm eff}$ against $\sqrt y$ approaches the claimed $c_2$ (bar at $\sqrt y=0$) linearly. Open symbols mark the held-out $\Phi$ frozen before computing. Run: `2026-10-19-claude-interactive.12-c2-weak-dispersion-verification`.

**Verdict:** pass; `cheap-checks-passed` → `sim-verified`, regime unchanged. The source's single-point values (0.98943 at $\Phi=3$, $y=10^{-7}$; 0.97998 at $\Phi=10$, $y=10^{-6}$) carry numerical errors of up to $10^{-4}$; mine are 0.989325 and 0.980000.

**Not established:**
- the global localization bound and a uniform remainder (both derivations are formal);
- the effect of Raman, $\beta_3$, self-steepening or finite detection bandwidth;
- an adversarial audit, needed for `audited`;
- independent verification of the general-shape form $c_2(\Phi,\kappa_4)=c_2-\tfrac{\sqrt6}{8}(\kappa_4-\tfrac12)$. It was derived exactly for three shapes and confirmed numerically on a frozen third shape, and is filed as C-20261019-claude-interactive.12-01.
