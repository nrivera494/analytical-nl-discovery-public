---
agent: claude-interactive.9
model: claude-opus-5-5
family: claude
date: 2026-10-18
claim: C-20261018-pi-chatgpt-01
task: T-20261018-claude-interactive-02
---

# Passive-mask ceiling on Zakharov–Shabat eigenvalues (C-20261018-pi-chatgpt-01), as verified

**1. Result as verified.** For the focusing NLSE $iq_z+\frac12q_{tt}+|q|^2q=0$, every discrete Zakharov–Shabat eigenvalue $\zeta=\xi+i\eta$ of any pulse $q\in L^1(\mathbb R)$ obeys

$$\int|q|^p\,dt\ \ge\ C_p\,\eta^{p-1}\quad(p>1),\qquad C_p=\frac{p^p}{(p-1)^{p-1}}\,\frac{\sqrt\pi\,\Gamma(p/2)}{2\,\Gamma((p+1)/2)},$$

with equality for $q_*=\frac{p\eta}{p-1}\mathrm{sech}\frac{2\eta t}{p-1}$. A laser with spectral amplitude $S(k)\ge0$ passed through any passive mask $|m(k)|\le1$ therefore has $\eta_{\max}\le[\int|q_{\rm TL}|^{2n}/C_{2n}]^{1/(2n-1)}$ for every integer $n$. For $q_{\rm TL}=N\mathrm{sech}\,t$ with integer $N$ the case $n=N$ equals the TL value: **no passive mask raises the leading soliton above $\eta=N-\frac12$**, i.e. $f_{1,\rm opt}=(2N-1)/N^2$ of the laser energy, $E_{1,\max}=2(2N-1)|\beta_2|/(\gamma T_0)$. Gaussian lasers: at most 0.015% gain at $N=4$ (Hausdorff–Young route). Regime: input scattering data of the integrable NLSE (scalar, $\beta_2$ and Kerr only); $p>1$ in (A), integer $n$ in (B), integer $N\ge1$ in (C), any real $N>\frac12$ in (D).

**2. How it was checked.**
- **Proved.** I proved (A)–(C) myself before opening the proposer's note (commit 830c8d6): with $\theta=\arctan(|v_2|/|v_1|)$, $\theta'\le|q|-\eta\sin2\theta$, Young's inequality and an antiderivative in $\theta$; then the even-moment Fourier majorant. The note's proof is the same and has no gap in substance (it should state $q\in L^1$ and that $\theta$ is absolutely continuous). (E)/(F) constants rederived from Beckner.
- **Numerical.** I wrote an independent ZS solver: Fourier collocation, and Boffetta–Osborne transfer matrices with measured order 2.000. TL sech eigenvalues equal $N-\frac12$ to $2\times10^{-13}$; the source's Gaussian TL fractions are reproduced to $10^{-10}$; $q_*$ attains equality to 13 digits; (A) holds on 69 eigenvalues of random complex potentials.
- **Adversarial.** 13 L-BFGS-B searches per case with exact eigenvalue gradients: phase-only and amplitude-and-phase smooth masks, per-bin masks with up to 274 free parameters, sharp multi-step masks. Integer sech ($N=2,3,4,6$): every optimum is TL; the excess over $N-\frac12$ is ≤ 2e-12, which is solver error. Non-integer sech ($N=2.5$; held-out 4.5, 7.5) and Gaussian ($N=4$; held-out 5, 8; and 1.5): no mask beats TL at all, so the ceilings (0.002–0.44%) hold with room to spare.
- **Relaxed.** With Raman (agents' solver b9fa957), a TL $N=2$ sech's leading eigenvalue rises to 1.655 (+10.4%, $T_0=65$ fs) and 1.561 (+4.1%, 200 fs), above the ceiling 1.5; without Raman it stays within +0.16%. The bound covers input scattering data only, as the card states (run `2026-10-18-claude-interactive.9-raman-escape`).

**3. Plot.**

![Verification plot](../runs/2026-10-18-claude-interactive.9-mask-adversary/fig_summary.png)

Gain in $\eta_{\max}$ over the TL launch against soliton number $N$: the ceilings of the claim (curves) and the best of 13 adversarial passive-mask searches (points; open = held-out). Integer-$N$ sech points lie exactly on the ceiling, which is zero there. Run `2026-10-18-claude-interactive.9-mask-adversary`.

**4. Verdict.** Pass. C-20261018-pi-chatgpt-01: cheap-checks-passed → **audited**; the novelty audit (T-20261018-claude-interactive-03) is separate and pending. Counterexample to C-20261016-claude-a-01 **reproduced**: for $S=\pi\cos(1)e^k\mathrm{sech}(\pi k/2)$ (TL $\eta=0.21429$), passive masks give up to +2.8% and an explicit cubic phase $e^{-0.5i(k-1)^3/6}$ gives +1.1% (run `2026-10-18-claude-interactive.9-asym-counterexample`). C-20261016-claude-a-01: proposed → **refuted**; its sech part is now settled by (C).
