---
id: C-20261010-claude-b-02
problem: P-20261010-claude-interactive-01
title: "Momentum conservation fixes the Fano factor of the spectral-centroid readout at <dw^2>_in/<dw^2>_out; this bounds lambda_gen from above and, for a Gaussian in normal dispersion, lies within 0.9 dB of it, while the best binary filters found stay 10-22 dB higher"
type: bound
status: proposed
proposed_by: claude-b
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-10
updated: 2026-10-10
solver_commit: null
result: null
---

## Statement

**(a) Identity.**
- **Model.** Any scalar fibre model of the form $\partial_zA=i\hat D(i\partial_T)A+i\gamma|A|^2A$, with arbitrary dispersion operator $\hat D$ (all orders of $\beta(\omega)$), instantaneous Kerr nonlinearity, no loss, no Raman, no self-steepening.
- **Conservation.** The momentum $\hat P=\sum_k\omega_k\hat n_k$ commutes with the Hamiltonian, because the Kerr term conserves frequency in every four-wave-mixing process. Here $\omega_k$ is the detuning of bin $k$ and $\hat n_k$ its photon number.
- **Readout.** Take a coherent input with mean spectrum $\bar n^{\rm in}_k$. Let $\bar\omega=\sum\omega\bar n/\sum\bar n$, which is the same at input and output. The weighted count $\hat N_w=\sum_kw_k\hat n_k$ with $w_k=\omega_k-\bar\omega$ has the weighted Fano factor (the quantity minimized by $\lambda_{\rm gen}$)
$$F_{\rm cen}\equiv\frac{\mathrm{Var}(\hat N_w)}{\sum_kw_k^2\bar n^{\rm out}_k}=\frac{\sum_k(\omega_k-\bar\omega)^2\bar n^{\rm in}_k}{\sum_k(\omega_k-\bar\omega)^2\bar n^{\rm out}_k}=\frac{\langle\Delta\omega^2\rangle_{\rm in}}{\langle\Delta\omega^2\rangle_{\rm out}} ,$$
the squared ratio of input to output rms bandwidths.
- **Validity.** The identity is exact in the full quantum model, up to $O(1/N_{\rm ph})$ corrections to the mean output spectrum. It holds for any power, length and dispersion sign, before and after wave breaking.
- **Consequence.** It gives the bound
$$\lambda_{\rm gen}\le\frac{\langle\Delta\omega^2\rangle_{\rm in}}{\langle\Delta\omega^2\rangle_{\rm out}} .$$

**(b) Closed form for $\beta_2$-only fibre.**
- **Exact relation.** Conservation of the Hamiltonian gives, for any input $u_0$, in soliton units:
$$\langle\Delta\omega^2\rangle_{\rm out}=\langle\Delta\omega^2\rangle_{\rm in}+\frac{N^2}{\int\rho_0\,d\tau}\Big(\int\rho_0^2d\tau-\int\rho(z)^2d\tau\Big).$$
Here $\rho=|u|^2$, and the sign is for normal dispersion.
- **Gaussian.** For the unchirped Gaussian, $\langle\Delta\omega^2\rangle_{\rm in}=1/(2T_0^2)$, and
$$F_{\rm cen}=\frac{1}{1+2N^2K(Z)},\qquad K(Z)=\frac{\int\rho_0^2-\int\rho_Z^2}{\int\rho_0}=\frac{2}{3\sqrt3}Z^2\,[1+O(Z)] .$$
$K$ comes from one mean-field propagation; tabulated values of $K(Z)/Z^2$ are below. As $N\to\infty$ at fixed $Z$, $N^2F_{\rm cen}\to1/(2K(Z))$.

| $Z$ | 0.1 | 0.3 | 0.5 | 0.75 | 1.0 | 1.25 | 1.5 | 2.0 | 2.5 | 3.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| $K/Z^2$ | 0.3804 | 0.3488 | 0.3020 | 0.2437 | 0.1954 | 0.1579 | 0.1303 | 0.0940 | 0.0699 | 0.0534 |
| $1/(2K)$ | 131.4 | 15.93 | 6.623 | 3.648 | 2.559 | 2.026 | 1.705 | 1.330 | 1.144 | 1.040 |

(run `2026-10-10-claude-b-nd-semiclassical`, `curve_N200.json`; $N$ = 100 gives the same to 4 digits; $2/(3\sqrt3)=0.3849$.)

**(c) Near-tightness for the Gaussian in normal dispersion (numerical).**
- **Result.** On every resolved oracle point,
$$0.02\ {\rm dB}\le10\log_{10}\frac{F_{\rm cen}}{\lambda_{\rm gen}}\le0.87\ {\rm dB}$$
(0.03–0.87 dB on the oracle grid; 0.02–0.65 dB on held-out set 2).
The range is 0.09–0.78 dB for $N\ge14$. The points are $N$ = 5–40 and $z/z_{\rm wb}$ = 0.1–3, plus $N=10$ at $z/z_{\rm wb}$ = 5 and 9; 33 resolved points in all (run `2026-10-10-claude-b-nd-oracle`, `summary.json`; heldout rows included).
- **Sandwich.** Combined with C-20261010-claude-b-01, the leading coefficient $\Gamma(Z)=\lim N^2\lambda_{\rm gen}$ satisfies
$$\Pi(Z)\le\Gamma(Z)\le\frac{1}{2K(Z)}.$$
The left inequality is the card's hierarchy $\lambda_{\rm pass}\le\lambda_{\rm gen}$; the right is (a).
  - The two sides are 4.5 dB apart at $Z=0.3$, 2.2 dB at $Z=0.75$, 0.73 dB at $Z=1.5$ and 0.12 dB at $Z=3$.
  - $\lambda_{\rm gen}/\lambda_{\min}$ is 5.3–7.5 dB on all oracle points with $\Phi\ge2$. So $1/(2N^2K)$ is a fast estimate of $\lambda_{\rm gen}$ to within 0.9 dB, and it sits 5.5–8 dB above $\lambda_{\min}(V)$.

**(d) Consequence for binary filters (numerical, best found).**
- **Search.** Three stages:
  1. exhaustive intervals, then flip descent from structured and 60 random starts, then 400-step iterated local search;
  2. flip descent from roundings of a non-negative-weight solution, then 1000-step iterated local search;
  3. transfer of filters between $N$ at fixed $z/z_{\rm wb}$ via $v=\omega/N$.
- **Gap.** For $N\ge14$ and $\Phi\ge4$ the best binary filter found lies 10.3 to 22.2 dB above $\lambda_{\rm gen}$. At smaller $\Phi$ the gap is smaller, e.g. 5.1 dB at $N=20$, $\Phi=2.1$.
- **Scaling.** At fixed $z/z_{\rm wb}$ it decreases only as $N^{-0.36}$ to $N^{-0.47}$ ($z/z_{\rm wb}$ = 0.3, 0.7, 1.0; $N$ = 10–40), while $\lambda_{\rm gen}\propto N^{-2}$. So the gap grows roughly as $N^{1.5}$.
- **Larger $N$** (2026-10-11; run `2026-10-11-claude-b-nd-binary-theory`). These points use count covariances from a discrete adjoint of the split-step map, validated against the finite-difference oracle to $2\times10^{-9}$.
  - **Binary.** At $N$ = 56, 80, 112 the best binary filter found keeps the same slow law: $F\approx1.24\,N^{-0.43}$ at $z/z_{\rm wb}=0.7$ ($N$ = 20–112), and slope $-0.62$ at 1.0 ($N$ = 20–80). A harder search moves these values by $\le1.2\%$.
  - **Faster tiers.** The non-negative-weight heuristic, $\lambda_{\rm even}$ and the parity bound decay faster: slope $\approx-0.7$ over $N$ = 20–112 at 0.7, steepening to $-1.3$ between $N$ = 80 and 112 ($\lambda_{\rm even}$ = 0.094 → 0.060).
  - **Parity bracket.** It therefore widens, from 5.1 dB at $N=40$ to 7.2 dB at $N=112$ ($z/z_{\rm wb}=0.7$).
  - **Binary-ness.** The binary filters fall 5.5 dB behind the non-negative-weight optimum at $N=112$, against 3.6 dB at $N=40$. So at large $N$ the binary constraint itself, not only the sign constraint, sets the gap.
  - **Graded readouts.** A readout with graded non-negative gains (multi-pixel detection with positive post-detection weights, not a partially transmitting mask) can exploit the fringe-locked even mode, which binary patterns cannot.
  - **Design rule across $Z$** (empirical, Kerr only, best found): $F_{\rm bin}\approx1.6/\sqrt N$ within a factor 1.6 for $z/z_{\rm wb}$ = 0.3–1.5 and $N$ = 20–112 (`summary.json` of the same run), i.e. about $-5$ to $-8$ dB of binary-filter squeezing.
    - Fitted slopes: $-0.31$ (0.3), $-0.43$ (0.7), $-0.62$ (1.0), $-0.53$ (1.5).
    - At $z/z_{\rm wb}=0.3$ both $\lambda_{\rm even}$ and $F_{\rm bin}$ are non-monotonic in $N$ (e.g. 0.352, 0.400, 0.278 at $N$ = 40, 56, 80), so a power law is only a trend there.
- **How the filters found work.** One broad band plus narrow bands near the spectral centre. Each part alone has $F$ = 2–10, but the two counts are anticorrelated with coefficient −0.88 to −0.96 ($N$ = 10–40, $z/z_{\rm wb}=0.7$; `runs/2026-10-10-claude-b-nd-oracle/comb_diagnostic.json`). The filter therefore cancels phase-quadrature noise between two spectral regions, a self-homodyne readout with positive weights only.
- **Cause.** The centroid weight changes sign at $\bar\omega$, and a filter with a single detector cannot apply negative weights.
  - A heuristic minimization over non-negative weights $w\ge0$ (projected gradient, 28 starts) was run on every resolved point with $\Phi\ge4$. It ends 0.3–4.7 dB below the best binary filter and 6.2–17.5 dB above $\lambda_{\rm gen}$; both gaps grow with $\Phi$.
  - So the sign constraint accounts for most of the gap, and binary-ness adds the rest.
  - This heuristic is not a bound, since a heuristic minimum can only overestimate the true one.
- **Certified part of the gap.** The parity bound of C-20261010-claude-a-03 (claude-a; unverified work in progress, read at 13:34 on branch `task/T-20261010-claude-interactive-04`; its proof sketch was checked here) applies, because this problem is parity-symmetric. It gives $F[T]\ge F_{\rm par}=(\lambda_{\rm odd}+\lambda_{\rm even})/2$ for every non-negative filter on the parity-symmetric kept bin set.
  - Evaluated on all 33 resolved oracle points (`runs/2026-10-10-claude-b-nd-oracle/parity_bound.json`): $\lambda_{\rm odd}=\lambda_{\rm gen}$ everywhere, so the $\lambda_{\rm gen}$ mode is odd, as the centroid is.
  - $F_{\rm par}$ lies 7–16 dB above $\lambda_{\rm gen}$ for $N\ge10$, growing with $N$: 7.0, 8.6, 10.8, 13.2, 15.4 dB at $z/z_{\rm wb}=0.7$ for $N$ = 10, 14, 20, 28, 40.
  - The best binary filters found are 2.2–6.4 dB above $F_{\rm par}$, held-out set 2 included (9.4 dB at N20, 1.5, likely a weak search there). On held-out set 2, $F_{\rm par}$ is 9.0–13.7 dB above $\lambda_{\rm gen}$ (`runs/2026-10-10-claude-b-nd-heldout2/parity_bound.json`).
  - So most of the binary gap is certified, and 2–6 dB remain open.
  - With the 300 K Raman reservoir (run `2026-10-10-claude-b-nd-raman`, `parity_raman.json`), the best binary filters found lie only 3.1–4.1 dB above $F_{\rm par}$ (N10, N20; $T_0$ = 50 fs–1 ps). In silica at room temperature, $F_{\rm par}$ from one covariance therefore brackets the binary optimum to within about 4 dB.
  - The certification is insensitive to the bin set: raising the darkness threshold from $10^{-12}$ to $10^{-4}$ of $\bar n_{\max}$ raises $F_{\rm par}$ by 6–12%, and the best binary filters lose $\le0.3\%$ when restricted to the bright set (`parity_threshold.json`).
- **Status.** Apart from the parity certification above, statement (d) is about the filters found, not a certified lower bound on $\min_TF[T]$. A further 8 × 2500-step iterated local search changes the best value by 0 at N20 and by $-0.08\%$ at N40, $z/z_{\rm wb}=0.7$ (`runs/2026-10-10-claude-b-nd-oracle/long_search.json`). Halving the bin width changes it by $-0.2\%$ to $-0.6\%$ (run `2026-10-10-claude-b-nd-convergence`). A fourth search, seeded by binarized combinations of the optimal even and odd sector modes (84 starts plus ILS at five points), finds nothing better (`parity_search.json`).

## Regime

**(a) and (b).**
- Instantaneous Kerr, lossless, no Raman, no self-steepening.
- Coherent input.
- Any $N$, $z$, $\beta(\omega)$ for (a); $\beta_2$ only for (b).
- Error: none for (a) beyond $O(1/N_{\rm ph})$ in the mean spectra.

**(c) and (d).** Unchirped Gaussian, normal dispersion:
- $5\le N\le40$;
- $0.1\le z/z_{\rm wb}\le3$ (i.e. $0.1\le Z\le3.2$), plus two points at $z/z_{\rm wb}$ = 5 and 9;
- $\Phi\ge1$;
- linearized noise ($\Phi/\sqrt{N_{\rm ph}}\ll1$).

## Assumptions

1. Scalar single-mode field with instantaneous Kerr nonlinearity, no Raman delayed response, no Raman reservoir, no loss.
   - **Raman.** The Raman response transfers momentum to phonons (the self-frequency shift), and its reservoir adds centroid noise, so (a) does not hold with Raman. Solver values at $N=10$, $z=0.7z_{\rm wb}$, $T_0=100$ fs, 1550 nm, Agarwal Raman, coth reservoir at 300 K (run `2026-10-10-claude-b.6-solver-weighted-raman`, $\mathrm{d}t\to0$):

| readout | Kerr only | with deterministic Raman | + reservoir (total) |
|---|---|---|---|
| centroid | 0.0352 | 0.0375 (7.2% above the bandwidth ratio) | 0.0733 (reservoir adds 0.0358) |
| $\lambda_{\rm gen}$ eigenvector | 0.0334 | — | 0.0719 |
| best binary | 0.4513 | — | 0.4905 |

     - The weighted-counting Fano factors roughly double.
     - The binary filter's rises by 9%, so the binary-over-weighted gap shrinks from 11.3 to 8.3 dB.
     - At $N=20$, $z=0.3z_{\rm wb}$ with self-steepening and Raman:
       - the centroid is 0.0735, against 0.0345 Kerr only;
       - the Kerr-optimal $\lambda_{\rm gen}$ eigenvector degrades from 0.0289 to 0.1065, so that weight is fragile and the centroid weight is robust.
   - **Self-steepening.** In the oracle's self-steepening model (power-normalized spectra), neither $\sum\omega|\alpha|^2$ nor $\sum\omega|\alpha|^2/(1+s\omega)$ is conserved. At $sN$ = 0.082 and 0.164, $F$ of the $\omega$-weight exceeds the bandwidth ratio by 1.24 and 1.90 (run `2026-10-10-claude-b-nd-oracle`, self-steepening rows).
   - With self-steepening, (a) needs a model that conserves both photon number and energy. This is untested.
2. Coherent input. For other inputs, replace the numerator of (a) with $\mathrm{Var}_{\rm in}(\hat P)$.
3. Weighted counting means multi-pixel spectral detection with arbitrary real weights applied after detection (the readout of $\lambda_{\rm gen}$). The centroid weight needs negative weights. One realization is a split detector with linear spectral weighting, or a spectrometer with a camera.
4. (c) and (d) use the linearized oracle with spectral bins of width $2\pi/(40T_0)$. They are therefore subject to the grid and keep-fraction choices of run `2026-10-10-claude-b-nd-oracle`.

## Predictions

**Held-out set 2** (frozen in commit `cdb6951` before computing; run `2026-10-10-claude-b-nd-heldout2`):
- $F_{\rm cen}=1/(1+2N^2K(Z))$ within 1%, with $K$ from the reduced curve only. The predicted values are 0.023019 ($N=16$, $z/z_{\rm wb}=0.5$), 0.003312 ($N=24$, 1.25) and 0.007618 ($N=12$, 2.5).
- $F_{\rm cen}10^{-0.1}\le\lambda_{\rm gen}\le F_{\rm cen}$.
- Best binary filter found at least 10 dB above $\lambda_{\rm gen}$.

**Scores** (`runs/2026-10-10-claude-b-nd-heldout2/summary.json`): all pass.

| case | $F_{\rm cen}$ vs prediction | momentum check | $10\log_{10}(F_{\rm cen}/\lambda_{\rm gen})$ | best binary over $\lambda_{\rm gen}$ |
|---|---|---|---|---|
| N16, 0.5 | $-0.28\%$ | $1+1\times10^{-6}$ | 0.65 dB | 14.0 dB |
| N24, 1.25 | $-0.35\%$ | $1+1.7\times10^{-5}$ | 0.10 dB | 20.1 dB |
| N12, 2.5 | $-0.28\%$ | $1+2\times10^{-6}$ | 0.02 dB | 17.6 dB |

**Held-out set 3** (frozen in `d6ab3a9`; run `2026-10-10-claude-b-nd-heldout3`; $N=18$, $z/z_{\rm wb}=0.9$). All three pass:
- $F_{\rm cen}$ is $-0.33\%$ from $1/(1+2N^2K)$, and $\lambda_{\rm gen}$ is 0.32 dB below it.
- The parity bound $F_{\rm par}$ is 12.5 dB above $\lambda_{\rm gen}$ (predicted $\ge7$ dB).
- The best binary filter is 4.6 dB above $F_{\rm par}$ (predicted 2–6.5 dB).

**Held-out set 4** (frozen in `7c6ea32`; $N=28$, $z/z_{\rm wb}=0.5$). All three pass:
- $F_{\rm cen}$ is $-0.10\%$ from the prediction, and $\lambda_{\rm gen}$ is 0.41 dB below it.
- $F_{\rm par}$ is 12.1 dB above $\lambda_{\rm gen}$.
- The best binary filter is 5.5 dB above $F_{\rm par}$.

**For the lab.** For a Gaussian at $N=20$, $z=0.7z_{\rm wb}$ ($Z=0.742$; parameters as in C-20261010-claude-b-01):
- the output rms bandwidth is $\sqrt{\langle\Delta\omega^2\rangle_{\rm out}}=\sqrt{54.7}/T_0=7.39/T_0$, against $0.707/T_0$ at the input;
- the spectral centroid therefore fluctuates at $F_{\rm cen}=9.15\times10^{-3}$, i.e. $-20.4$ dB relative to the shot noise of a coherent pulse with the output spectrum (oracle row `N20_zr0.7`: $N^2F_{\rm cen}=3.659$).

With the Raman reservoir at $T_0=100$ fs and 300 K, $F_{\rm cen}$ rises to 0.0278 ($-15.6$ dB) at this point (run `2026-10-10-claude-b-nd-raman`; reservoir only, deterministic response not included).

**Few detectors.** The centroid weight needs a graded, signed readout. Quantizing it to $K$ equal-photon bands, each weighted by its mean detuning, gives the following (`runs/2026-10-10-claude-b-nd-oracle/few_detectors.json`, Kerr only):

| point | $K=4$ | $K=8$ | $K=16$ | best binary | $\lambda_{\rm gen}$ |
|---|---|---|---|---|---|
| N20, $z/z_{\rm wb}=0.7$ | $-7.7$ dB | $-11.8$ dB | $-15.7$ dB | $-4.7$ dB | $-20.6$ dB |
| N40, $z/z_{\rm wb}=1$ | $-2.4$ dB | $-13.6$ dB | $-16.9$ dB | $-6.1$ dB | $-28.3$ dB |

- A split detector ($K=2$, $w=\mathrm{sign}(\omega-\bar\omega)$) is above shot noise at five of six points.
- With 16 bands the readout beats the best binary filter by 9–11 dB, but stays 5–11 dB above $\lambda_{\rm gen}$. The number of bands needed grows with $N$.

## Derivation

1. **Conservation.** In the quantum NLSE, $\hat H=\sum_k\hbar D(\omega_k)\hat n_k+\tfrac{\hbar\gamma'}{2}\sum_{k_1+k_2=k_3+k_4}\hat a^\dagger_{k_3}\hat a^\dagger_{k_4}\hat a_{k_1}\hat a_{k_2}$ commutes with $\hat P$ and $\hat N$. So $\hat P_{\rm out}-\bar\omega\hat N_{\rm out}=\hat P_{\rm in}-\bar\omega\hat N_{\rm in}$ as operators.
2. **Variance.** For a coherent input the bin counts are independent Poisson variables, so $\mathrm{Var}=\sum(\omega_k-\bar\omega)^2\bar n^{\rm in}_k$. Dividing by $\sum w_k^2\bar n^{\rm out}_k$ gives (a).
3. **Bound.** $\lambda_{\rm gen}$ is the minimum of this ratio over all real $w$, hence the bound.
4. **Closed form.** For (b), $H=\int(\tfrac12|u_\tau|^2+\tfrac{N^2}2|u|^4)\,d\tau$ (normal dispersion, after conjugation) is conserved, and $\int|u_\tau|^2=\int\omega^2|\tilde u|^2$.
5. **Small $Z$.** $\int\rho_0^2-\int\rho_Z^2=Z^2\int\rho_0\rho_{0,\tau}^2+O(Z^3)$, and for $\rho_0=e^{-\tau^2}$ this gives $2Z^2\sqrt\pi/(3\sqrt3)$.
6. **Semiclassical reading.** The centroid functional pulls back to a pure input-phase functional. So its $O(1)$ amplitude part vanishes identically, and its variance is $O(\varepsilon^2)$ relative to the output shot noise. Any binary weight has an $O(1)$ amplitude part that does not cancel at a finite number of edges. Details in `explorations/2026-10-10-claude-b-semiclassical-normal-dispersion.md`, sections 4–5.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Dimensionless ratio of second moments | claude-b (claude) | — | 2026-10-10 |
| Known limits | $w=1$ (photon number) gives $F=1$; $Z\to0$ gives $K\to0.3849Z^2$. Pure SPM (no dispersion): centroid $F=1/(1+0.770\Phi^2)$ to $10^{-6}$, and $\lambda_{\rm gen}$ is 0.25–0.93 dB below it at $\Phi$ = 1–10 | claude-b (claude) | 2026-10-10-claude-b-nd-semiclassical, 2026-10-10-claude-b-nd-dispersionless | 2026-10-10 |
| Symmetries | Centroid $\bar\omega=0$ by parity. Generality of (a): the identity also holds for anomalous dispersion ($N$ = 1.5, 3) and with third-order dispersion for both signs of $\beta_2$, to $\le2.1\times10^{-6}$ on resolved grids. The anomalous $N=3$ case fails by 44% on an under-resolved 512-point grid and recovers to $10^{-6}$ at 1024 and 2048 points | claude-b (claude) | 2026-10-10-claude-b-nd-oracle, 2026-10-10-claude-b-nd-centroid-general | 2026-10-10 |
| Symbolic residual | Not done | | | |
| Simulation, core regime | Identity (a): $F$ of $w=\omega-\bar\omega$ from the full count covariance equals the bandwidth ratio to $\le1.1\times10^{-5}$ at all 33 resolved pure-Kerr points. Closed form (b): $N^2F_{\rm cen}$ from the reduced curve agrees with the finite-$N$ oracle values | claude-b (claude) | 2026-10-10-claude-b-nd-oracle, 2026-10-10-claude-b-nd-semiclassical | 2026-10-10 |
| Error-scaling exponent | Not applicable to (a). The gap in (c) does not shrink with $N$: 0.20 dB at $N=40$, $z/z_{\rm wb}=0.7$ | | | |
| Held-out region | Set 2 (frozen `cdb6951`): 9 of 9 predictions for this claim pass ($F_{\rm cen}$ within 0.35%, $\lambda_{\rm gen}$ 0.02–0.65 dB below it, binary gap 14–20 dB) | claude-b (claude) | 2026-10-10-claude-b-nd-heldout2 | 2026-10-10 |
| Convergence and artefacts | The identity fails on three under-resolved oracle grids (+0.7% at N14 $z/z_{\rm wb}=1.5$, +3.3% at N28 1.5, +19% at N20 2.0, Nt = 512/1024), which makes it a useful aliasing detector | claude-b (claude) | 2026-10-10-claude-b-nd-oracle | 2026-10-10 |
| Second solver or relaxed assumption | FastDifferentiableMMNLO (commit b9fa957, discrete RK4IP adjoint, blind): the centroid Fano factor equals the bandwidth ratio to $2\times10^{-12}$ when the weight covers all bins (N10 and N20 points), and to $\le2.4\times10^{-6}$ on all 12 grid points $N$ = 5, 10, 20 × $z/z_{\rm wb}$ = 0.3–1.5. On those 12 points the solver reproduces the numpy $\lambda_{\rm gen}$ to $\le1.0\times10^{-5}$ and the best binary $F$ to $\le2.6\times10^{-6}$ (run `2026-10-10-claude-b.6-solver-grid`). The $\lambda_{\rm gen}$ eigenvector weights reproduce the numpy $\lambda_{\rm gen}$ to $10^{-8}$. Relaxed assumptions: Raman breaks the identity by 7–10% (deterministic) and the reservoir adds about 0.036 at $T_0=100$ fs; see Assumptions | claude-b.6 (claude) | 2026-10-10-claude-b.6-solver-weighted-raman | 2026-10-10 |
| Adversarial audit | Not done | | | |
| Novelty search | **Concurrent overlap.** claude-a's C-20261010-claude-a-02 (branch `task/T-20261010-claude-interactive-04`, unverified, read at 13:34 after this claim was written) states the same centroid bound, $\lambda_{\rm gen}\le\langle(\omega-c)^2\rangle_{\rm in}/\langle(\omega-c)^2\rangle_{\rm out}$, in the dispersionless setting with a Raman extension. Its dispersionless Gaussian form $(1+\tfrac{4}{3\sqrt3}\Phi^2)^{-1}$ and tightness numbers (0.81 at $\Phi=1$, 0.89 at $\Phi=10$) agree with run 2026-10-10-claude-b-nd-dispersionless (0.807, 0.888). The PI may merge the two claims. This card adds the normal-dispersion closed form via energy conservation, the semiclassical limit, tightness through breaking, and the binary-gap analysis. Otherwise: momentum conservation of the quantum NLSE and conserved soliton frequency noise are standard. A statement that the spectral-centroid Fano factor equals the bandwidth ratio, or its use as a bound on weighted counting, was not found. Searches are listed in log 2026-10-10_claude-b_T-20261010-claude-interactive-05 | claude-b (claude) | — | 2026-10-10 |

## Outcome

Open.
