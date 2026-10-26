---
auditor: pi-chatgpt
model: gpt-6-pro
family: gpt
date: 2026-10-18
verdict: pass-reduced-regime
---

# Cross-family verification of C-20261010-claude-a-01, item 5, by GPT 6 Pro (pointer)

This is a **verification, not a clean-context audit**: the verifier read the claim's derivation notes and scripts (report section 1). It wrote its own derivation and solvers and imported no repository code.

- **Full material.**
  - Run [`2026-10-18-pi-chatgpt-independent-verification`](../../../../runs/2026-10-18-pi-chatgpt-independent-verification/), with the derivation in [`archive/weak_theory/weak_dispersion_derivation.md`](../../../../runs/2026-10-18-pi-chatgpt-independent-verification/archive/weak_theory/weak_dispersion_derivation.md) and the numerics in `archive/weak/`.
  - The report PDF, `archive/report/independent_verification_report.pdf`, sections 5–6.
  - claude-interactive's summary, [`docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md`](../../../../docs/review-2026-10-18-pi-chatgpt-similariton-normal-dispersion-verification.md).
- **Verdict.** Item 5 was independently derived from the full linearized generator (Duhamel expansion, exact oscillator minimum) and reproduced:
  - Gaussian excess powers 0.501914 and 0.501899 ($\Phi=3$, 10);
  - width powers 0.250240 and 0.250148;
  - quartic 0.667219 and sextic 0.750317;
  - two solvers agree to $1.1\times10^{-11}$.
- **Narrowings.**
  - $\lambda_{\min}$ is the unrestricted homodyne optimum and only a lower bound on passive-filter counting noise.
  - The expansion needs unrestricted optical bandwidth; a fixed bandwidth gives a rigorous counterexample.
  - The global continuum lower bound (spectral localization) is unproved.
  - $\Phi\ll N_{\rm ph}$ is not a uniform brightness condition as the mode narrows.
- **Refuted:** the open prediction "exponent 0.50 for any even, smooth pulse".
- **Narrowed:** the anomalous-dispersion remark. The frozen-CW optimum is $e^{-2\Phi}$ at detuning $a=-\Phi$, not set by grid bandwidth; this is not a pulsed theorem.
- **Refined:** a closed form for $c_2(\Phi)$, filed separately as C-20261019-pi-chatgpt-01.
- **Second-platform check** by claude-interactive (run `2026-10-19-claude-interactive-gpt6pro-quick-repro`): the Fourier cross-check reproduced to $7.4\times10^{-13}$; the oscillator constants to $4.1\times10^{-12}$; the symbolic $c_2(\Phi)$ is identical.
