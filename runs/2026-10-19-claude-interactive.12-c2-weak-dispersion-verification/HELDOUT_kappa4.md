# Frozen prediction: third peak shape (written before computing)

claude-interactive.12, 2026-10-19, 08:40 EDT (commit 76856b7). Committed before any symbolic or numerical evaluation for this shape.

**Hypothesis.** $E_2$ is linear in the $O(y)$ generator, and the peak's quartic coefficient $\kappa_4$ enters only there (in $\rho_2$ and the phase). So $c_2$ is affine in $\kappa_4$. From the two exact evaluations, Gaussian ($\kappa_4=\tfrac12$) and sech ($\kappa_4=\tfrac23$, shift $-1/(8\sqrt6)$), it follows that
$$c_2(\Phi,\kappa_4)=c_2(\Phi)-\frac{3}{4\sqrt6}\Big(\kappa_4-\frac12\Big),$$
for an intensity peak $1-x^2+\kappa_4x^4+O(x^6)$.

**Test shape.** Intensity $e^{-x^2-x^4/2}$, amplitude $e^{-x^2/2-x^4/4}$, so $\kappa_4=0$. The predicted shift is $+3/(8\sqrt6)=+0.15309$:

| $\Phi$ | Gaussian $c_2$ | predicted $c_2(\Phi,0)$ |
|---|---|---|
| 1 | 1.21744000 | 1.37053 |
| 3 | 0.98946456 | 1.14256 |

**Pass criteria.**
- The symbolic derivation with this profile equals the prediction exactly.
- The propagated $c_{\rm eff}$, extrapolated from $10^{-6}\le y\le10^{-4}$, is within $10^{-4}$ of it.
