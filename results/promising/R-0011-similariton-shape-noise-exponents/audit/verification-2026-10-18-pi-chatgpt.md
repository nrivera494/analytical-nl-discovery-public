---
auditor: pi-chatgpt
model: gpt-6-pro
family: gpt
date: 2026-10-18
verdict: pass-reduced-regime
---

# Cross-family verification of C-20261008-claude-a-02 by GPT 6 Pro (pointer)

This is a **verification, not a clean-context audit**: the verifier read the claim's derivation notes and scripts (report section 1). It wrote its own solvers and imported no repository code.

- **Full report.** The PI's ChatGPT session (GPT 6 Pro, family gpt) wrote a 26-page report and a reproducibility archive, committed as run [`2026-10-18-pi-chatgpt-independent-verification`](../../../../runs/2026-10-18-pi-chatgpt-independent-verification/). The similariton part is [`archive/similariton/TECHNICAL_NOTES.md`](../../../../runs/2026-10-18-pi-chatgpt-independent-verification/archive/similariton/TECHNICAL_NOTES.md). claude-interactive's summary is [`docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md`](../../../../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md).
- **Verdict.** Pass in a reduced regime:
  - (a) holds as variance envelopes of photon-normalized fixed low-order shape variables, $G^{1/3}$ and $G^{5/3}$, with prefactors oscillating in $\ln G$;
  - (b) holds for the five-component orthonormal spectral projection only;
  - (c) holds in the reduced model.
- **Superseded statements** (now claim C-20261019-pi-chatgpt-02, not part of R-0011): $C_{PP}\propto G/\varepsilon_0^2$ is wrong ($\propto G^{7/3}/\varepsilon_0^2$); "with ASE there is no squeezing" is wrong as an unconditional statement.
- **Not verified:** the uniform edge remainder $O(\varepsilon_0^2\ln(1/\varepsilon_0))$; any all-mode quantum covariance limit.
- **Regime correction:** $N_0\ge10^4$ is insufficient at high gain; the linearization needs $\Phi_{NL}^2/N_0\ll1$.
- **Methods:** a real-space finite-volume covariance integrator (8 modes, 32–1024 cells) and a lens-coordinate full NLSE with exact tangent and adjoint, coherent vacuum and both ASE quadratures.
- **Second-platform check** by claude-interactive (run `2026-10-19-claude-interactive-gpt6pro-quick-repro`): archive checksums verified; the quick suite (the short-gain counterexample) reproduced to the same digits. The exponents of R-0011 were not rerun.
