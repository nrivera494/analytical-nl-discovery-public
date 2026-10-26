---
agent: claude-a
model: claude-opus-5-5
family: claude
task: T-20261016-claude-interactive-02
problem: P-20261016-claude-interactive-03
status: exploration; H5a confirmed; H5b quantitative part refuted, qualitative part confirmed; H5c confirmed; not a claim
---

# Quantum-limited timing jitter of the leading Raman soliton after fission (H5, first pass)

## Question

What is the timing jitter of the most red-shifted soliton produced by fission of a transform-limited sech $N$-soliton? The sources are vacuum fluctuations of the coherent input and the thermal plus zero-point Raman phonon bath. How does it compare with launching a fundamental soliton directly? This is the merged jitter part of the card, in a first, restricted form. The card's target is jitter at fixed shift, length and efficiency; here only fixed length is done.

## Method

- **Code.** Run `2026-10-16-claude-a-raman-soliton-frontier`, script `h5_jitter.jl`. FastDifferentiableMMNLO, agents' copy b9fa957 (clean). Discrete RK4IP adjoint (`adjoint_mode=:discrete_rk4ip`).
- **Model.** Single mode, Agarwal (Blow–Wood) Raman, self-steepening built in, $\beta_2=-20.6$ ps²/km, $\gamma=1.40$ /W/km (SMF-like), 1550 nm, 300 K.
- **Observable.** The temporal centroid of the leading soliton: the first moment of $|A(L,t)|^2$ weighted by a window of half-width $\max(6/|q|_{\max},1)T_0$ around the tallest output peak. Its terminal condition is $w(t)(t-J)A/\int w|A|^2$, mapped with the solver's own time-to-spectral gradient map.
- **Variances**, following `example_notebooks/soliton_jitter.ipynb`:
  - vacuum: $\sum|\partial J/\partial\bar B(0)|^2$ in photon units;
  - Raman: $\gamma^2\sum_z\sum_\omega|\hat B(z,\omega)|^2C(\omega)\,\Delta f\,\Delta z$, with $B=-2\,\mathrm{Im}(A\bar\lambda)$. $C(\omega)$ is the symmetrized ($\coth$) bath spectrum of `raman_bath_spectrum.jl`, copied unchanged from solver branch `task/T-20261004-gpt-b-02`.
- **Launch.** TL sech, $T_0=100$ fs, $L=4L_D/N$.
- **Baseline.** An isolated fundamental soliton with the leading soliton's output peak power (so $T_1=\sqrt{|\beta_2|/\gamma P_{\rm pk}}$), propagated over the same physical length. Its full-pulse centroid jitter is computed the same way.

## Validation, N = 1

Full-pulse centroid against soliton perturbation theory: vacuum $T_0^2(\pi^2/12+\zeta^2/3)/\bar n$; Raman $(16/45)T_0^2F_0\zeta^3/\bar n$ (thermal-limit SPT, as in the notebook).

| $z/L_D$ | vacuum / SPT | Raman / SPT |
|---|---|---|
| 1 | 1.0004 | 1.093 |
| 2 | 1.0023 | 1.086 |
| 4 | 1.0118 | 1.084 |

The 8–9% Raman excess over the thermal-limit formula is consistent with the zero-point part and the full gain spectrum, which that formula omits. I did not check this further.

## Results ($T_0=100$ fs, $L=4L_D/N$)

$R$ is the variance of the leading soliton over that of the isolated baseline.

| $N$ | leading: vacuum (s²) | leading: Raman (s²) | $R_{\rm vac}$ | $R_{\rm ram}$ | $R_{\rm tot}$ |
|---|---|---|---|---|---|
| 2 | $5.44\times10^{-35}$ | $2.49\times10^{-35}$ | 0.670 | 0.925 | 0.734 |
| 3 | $1.16\times10^{-34}$ | $3.71\times10^{-35}$ | 0.494 | 1.193 | 0.576 |
| 4 | $7.61\times10^{-35}$ | $3.12\times10^{-35}$ | 0.439 | 1.549 | 0.554 |
| 5 | $4.76\times10^{-35}$ | $2.35\times10^{-35}$ | 0.399 | 1.744 | 0.536 |

**Frozen before computing $N=4$ and 5** (H5a in `HYPOTHESES.md`, commit a3e68a1):
- $R_{\rm vac}(4)\in[0.30,0.50]$: 0.439, confirmed.
- $R_{\rm vac}(5)\in[0.25,0.43]$: 0.399, confirmed.
- $R_{\rm ram}(4)\in[1.07,1.79]$: 1.549, confirmed.
- $R_{\rm ram}(5)\in[1.22,2.04]$: 1.744, confirmed.
- $R_{\rm tot}$ decreasing from $N=3$ to 5: confirmed.

**Reading.** At equal output peak power and equal length, the fission-generated leading soliton has less vacuum-limited timing jitter than a directly launched fundamental soliton. The ratio falls roughly as $N^{-0.7}$. It has more Raman-bath jitter, rising roughly as $N^{0.6}$. The total falls slowly. The baseline is not matched in red shift: the isolated soliton is short over the whole length and shifts further.

## At fixed red shift (the card's comparison)

Script `h5_jitter_fixedshift.jl`. The isolated soliton, with the leading soliton's output peak power, is propagated until its spectral centroid reaches the leading soliton's red shift, instead of over the same length.

| $N$ | shift (rad/ps) | $L$ (m) | $L_b$ (m) | $R_{\rm vac}$ | $R_{\rm ram}$ | $R_{\rm tot}$ |
|---|---|---|---|---|---|---|
| 2 | 23.3 | 0.971 | 1.431 | 0.170 | 0.300 | 0.197 |
| 3 | 108.9 | 0.647 | 0.961 | 0.130 | 0.401 | 0.156 |
| 4 | 192.4 | 0.485 | 1.058 | 0.038 | 0.191 | 0.049 |
| 5 | 255.1 | 0.388 | 1.109 | 0.017 | 0.108 | 0.023 |

H5b was frozen after $N=2$, 3 and before $N=4$, 5 were printed (commit 93284ae).
- The power-law windows for $N=4$, 5 are **refuted**. All three ratios fall far below them: $R_{\rm tot}=0.049$ and 0.023 against $[0.09,0.17]$ and $[0.08,0.15]$.
- The qualitative prediction ($R_{\rm tot}<0.25$) is confirmed.
- The extrapolation failed because $L_b/L$ grows with $N$: 1.47, 1.49, 2.18, 2.86. The leading soliton gains energy by Raman transfer and leaves fission already shifted, so it reaches a given shift in a much shorter fibre. The variance ratio tracks roughly $(L/L_b)^3$.

**Reading.** At fixed peak power and fixed red shift, the leading soliton from fission has a timing variance 5× ($N=2$) to 40× ($N=5$) smaller than a directly launched fundamental soliton. The direct soliton needs a 1.5–2.9× longer fibre to reach the same shift, and its jitter grows steeply with length. Both sources are computed with the same validated adjoint machinery (vacuum and symmetrized Raman bath, 300 K).

**At the Raman-transfer maximum** (H5c, frozen at f0e1bce before computing):

| $(N,T_0)$ | shift (rad/ps) | $L$ (m) | $L_b$ (m) | $R_{\rm vac}$ | $R_{\rm ram}$ | $R_{\rm tot}$ |
|---|---|---|---|---|---|---|
| (3, 140 fs) | 79.3 | 1.269 | 1.684 | 0.192 | 0.613 | 0.234 |
| (4, 200 fs) | 135.8 | 1.942 | 3.336 | 0.135 | 0.575 | 0.165 |

$R_{\rm tot}<0.25$, so H5c is confirmed. The advantage is smaller than at $T_0=100$ fs for the same $N$ (0.156 and 0.049).

**Empirical observation (post hoc, not frozen, for a follow-up).** $R_{\rm tot}/(L/L_b)^3=0.63$, 0.51, 0.51, 0.54 for $N=2$–5. So $R_{\rm tot}\approx0.55\,(L/L_b)^3$ within about 15%: the advantage is mostly the shorter fibre, with a roughly constant extra factor of about 2 from the fission itself. Whether the cube is a coincidence of mixed $z^2$, $z^3$ and $z^4$ contributions was not checked.

## Not done

Recorded as task T-20261016-claude-a-04.
- The comparison at fixed shift **and** fixed output efficiency (the leading soliton's energy fraction).
- Frequency (spectral-centroid) jitter instead of timing.
- The best phase masks of C-20261016-claude-a-04.
- A comparison with Corney & Drummond's frequency-coordinate covariance for $N=1$.
