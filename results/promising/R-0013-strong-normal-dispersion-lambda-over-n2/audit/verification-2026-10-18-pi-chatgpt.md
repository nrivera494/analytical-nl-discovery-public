---
auditor: pi-chatgpt
model: gpt-6-pro
family: gpt
date: 2026-10-18
verdict: pass-reduced-regime
---

# Cross-family verification of C-20261010-claude-b-01 by GPT 6 Pro (pointer)

This is a **verification, not a clean-context audit**: the verifier read the claim's notes and scripts (report section 1). It wrote its own solvers and imported no repository code.

- **Full material.**
  - Run [`2026-10-18-pi-chatgpt-independent-verification`](../../../../runs/2026-10-18-pi-chatgpt-independent-verification/), with [`archive/strong/strong_report.md`](../../../../runs/2026-10-18-pi-chatgpt-independent-verification/archive/strong/strong_report.md) and the report PDF, section 7.
  - claude-interactive's summary, [`docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md`](../../../../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md).
- **Verdict.**
  - Before breaking, (a) is a conditional theorem plus an independent reproduction. The finite-dimensional symplectic lemma, $\lambda_{\min}=\varepsilon^2s_1^{-2}[1+O(\varepsilon^2)]$ under regular block limits, is proved. Direct hydrodynamics gives $\Lambda(0.75)=0.86284$ and $\Pi(0.75)=2.18007$. Full-NLSE deficits are 1.55%, 0.39% and 0.099% at $N=10$, 20 and 40, a fitted power of −1.986.
  - After breaking, the law is supported numerically at $Z=1.5$ ($N^2\lambda_{\min}\to0.3623$, converged to $1.2\times10^{-11}$). The shallow-water map does not continue through breaking, so $C_Z$ there is the full-NLSE tangent limit $C_\infty$. The sufficient conditions are stated and unproved.
- **Qualifications.**
  - $0<c\le2$ is a data statement only.
  - The 80-Hermite basis biases $\Lambda$ by 0.012% and $\Pi$ by 0.165% at $Z=0.1$.
  - $\lambda_{\rm pass}=\lambda_2$ holds in the dense tested cases but is not proved by parity, and the odd optimal mode is dark.
  - The continuum (white-vacuum) statement needs a Sobolev or microlocal estimate.
  - The small-$Z$ coefficient duplicates the weak-dispersion result (R-0012).
- **Second platform.** claude-interactive (run `2026-10-19-claude-interactive-gpt6pro-quick-repro`) reran only the weak-dispersion cross-check made with this code; the strong-dispersion cases were not rerun.
