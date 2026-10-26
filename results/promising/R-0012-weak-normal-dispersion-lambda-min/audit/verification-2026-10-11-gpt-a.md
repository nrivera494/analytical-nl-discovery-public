---
auditor: gpt-a
model: gpt-6-astra
family: gpt
date: 2026-10-11
verdict: pass-reduced-regime
---

# Cross-family verification of C-20261010-claude-a-01 by gpt-a (pointer)

gpt-a assessed C-20261010-claude-a-01 as candidate 3 of its highlights audit (task T-20261011-gpt-a-01). The full report is [`docs/review-2026-10-11-gpt-a-highlights-audit.md`](../../../../docs/review-2026-10-11-gpt-a-highlights-audit.md), section "Candidate 3". The evidence is run `2026-10-11-gpt-a-highlights-audit-c3`, which used gpt-a's own algebra, Fourier Raman covariance and split-step tangent code, not the repository solver.

- **Classification.** The task was framed as a clean-context audit. gpt-a did not read the derivation notes, but its inputs (run `2026-10-11-gpt-a-highlights-audit-c1`, `input-manifest.json`) included the proposer's run scripts. The claim card records it as a verification, not a clean-context audit, and it is filed so here.
- **Verdicts.**
  - Items 1–2: pass within linearized theory. For an isolated peak on continuous time, "minimum" means spectral infimum. Arbitrary test kernels reproduce the SVD formula to $2.2\times10^{-13}$.
  - Item 3(b):
    - the thermal-slice closed form passes, and is published (Voss et al. 2006, eq. (100));
    - the limiting approach passes in a reduced regime, which requires a low-frequency band as well as time localization;
    - the finite "below 1%" regime **fails**: 7.50% excess at $T_0=200$ fs, $\Phi=10$, 300 K, $\Omega_bT_0=30$.
  - Item 4: pass for the isotropic and strong-birefringence (no walk-off) Kerr models, to $5.2\times10^{-10}$. The intermediate beat length and vector Raman were not tested.
  - Item 5: pass with reduced regime: Gaussian (nondegenerate) peaks, and the quartic exponent. The fitted exponents are 0.50186–0.50192 ($\Phi=2$–20) and 0.66719–0.66722 (quartic). It is an asymptotic expansion, not an exact equality over the whole finite interval. Any "square root for every smooth even pulse" statement is refuted.
- **Not tested:** item 3(a) (the short-pulse unrestricted Raman equality), self-steepening, the anomalous-dispersion assertions.
