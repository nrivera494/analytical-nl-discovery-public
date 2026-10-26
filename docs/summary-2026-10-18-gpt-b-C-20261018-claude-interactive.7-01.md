---
agent: gpt-b
model: gpt-6-astra
family: gpt
claim: C-20261018-claude-interactive.7-01
date: 2026-10-18
report_status: complete
---

For the fixed tangent squeezed quadrature, the independent GRIN calculation gives
$$
\lambda_{\rm lin}=\sigma_{\max}^{-2},\qquad
\frac{V_{\rm fixed}}{\lambda_{\rm lin}}-1
\simeq(0.0920\pm0.0039)\frac{\sigma_{\max}^6}{n_0},
\qquad \Delta V_{\rm fixed}\propto n^{-0.9947\pm0.0103}.
$$
Here $V_{\rm fixed}$ is the nonlinear Wigner variance in that direction, $S$ the classical tangent map, $\sigma_{\max}$ its largest singular value, $n$ total photons per coherence cell, $n_0=nf_0$ with fundamental power fraction $f_0$, and vacuum variance is one. The coefficient is measured at normalized linear energy $E'=0.6$, disorder amplitude $\sigma=0.3$, and distance $z=10L_{\rm NL}$, where $L_{\rm NL}$ is the nonlinear length; it is not universal. The checked early regime is the scalar 15-mode electronic-Kerr model, $10^6\le n\le10^{10}$, $5\le z/L_{\rm NL}\le20$, $0.55\le f_0\le0.87$ and $\sigma_{\max}^6/n_0\le0.8$ on the tested launches.

Exact coherent-Kerr moments give the single-mode large-shear coefficient $1/8$ and the $n_0^{-1/3}$ optimized variance. Independent tangent and nonlinear Wigner propagation test the multimode correction; the quoted uncertainties are between-scramble SE. Frozen $E'=0.3,0.9$ cases pass the early/late curvature gates. Exact Fock benchmarks calibrate TWA but do not prove its error uniformly for 15 modes. Counting invariance under pure SPM does not prove robustness under intensity exchange; late counting discrepancies require their own resolution checks.

![Independent curvature test](../runs/2026-10-18-gpt-b-grin-squeezing/fig_summary.png)

Fixed-direction excess at $z=10L_{\rm NL}$; error bars are sampling SE, open points are held out. The line fits only $E'=0.6$.
Run: `2026-10-18-gpt-b-grin-squeezing`.

**Verdict:** verified as sharpened; `cheap-checks-passed` → `sim-verified`, for early quadrature squeezing only. Exact Gaussianity until coherence collapse is refuted. Late counting remains unresolved: the fresh optimized discrepancy changes from 2.590 to 0.402 dB on the final step refinement. No universal multimode curvature ceiling or new claim is filed.
