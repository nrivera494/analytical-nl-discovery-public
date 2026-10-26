# Held-out case, frozen before any computation (2026-10-10 10:42 EDT, claude-a, T-20261010-claude-interactive-04)

The case below was not computed while the formulas were built. It is evaluated only after the formulas are frozen, as a test.

- Pulse: sech, $A(0,t)=\sqrt{P_0}\,\mathrm{sech}(t/T_s)$, unchirped. $T_s=0.9445\,T_0$, so its intensity FWHM equals that of the Gaussian $e^{-t^2/2T_0^2}$ field, $1.6651\,T_0$.
- Model: the same dispersionless scalar model as the main cases.
- Points to score:
  1. Kerr only ($f_R=0$), at $\Phi_{\rm peak}\in\{5,15\}$.
  2. Kerr plus Raman (Blow–Wood, $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs) at 300 K, with $T_s=0.9445\times200$ fs, at $\Phi_{\rm peak}\in\{5,15\}$.
- Quantities: $\lambda_{\min}(V)$, $\lambda_{\rm pass}$, $\lambda_{\rm gen}$, and the best binary filter, using the same search procedure as for the Gaussian. Each is compared with what the frozen formulas predict.

## Frozen predictions (2026-10-10 11:01 EDT, before the held-out case was computed)

From the formulas only (file `heldout_frozen_predictions.json`):

| case | λ_min(V) | λ_gen | best binary |
|---|---|---|---|
| sech, Kerr, Φ=5 | V_min(5) = 0.009805 (exact) | in [0.80, 1.00] × λ_P with λ_P = 1/(1+0.9143Φ²) = 0.04192 | in [0.40, 0.80] |
| sech, Kerr, Φ=15 | V_min(15) = 0.001109 (exact) | in [0.80, 1.00] × 0.004838 | in [0.40, 0.80] |
| sech, Raman 300 K, T_s = 188.9 fs, Φ=5 | in [0.009805, 0.03162] (Kerr anchor ... long-pulse thermal slice) | ≤ λ_P,R = 0.08197 (exact upper bound) and ≥ 0.5 λ_P,R | in [0.40, 0.80] |
| sech, Raman 300 K, Φ=15 | in [0.001109, 0.008681] | ≤ 0.01941 and ≥ 0.5 × 0.01941 | in [0.40, 0.80] |

Wasted squeezing in the Kerr limit (closed form): λ_gen/λ_min(V) → 4 I₁/I₂ = 4.375 for the sech (Gaussian 3√3 = 5.196).

## Second frozen prediction: λ_min(V) with weak normal dispersion (2026-10-10 11:24 EDT; commit 3a46f26)

The formula below was derived after looking at Gaussian, $\Phi\in\{5,10,20\}$ rows of `scan_dispersion.json` (dt = 0.04) and Gaussian $\Phi=10$ rows of `lam_min_dispersion.json`. Nothing at $\Phi=2$, at $\Phi=40$, or for a sech pulse had been computed with dispersion when it was frozen.

**Formula.** With $\beta_2>0$, $y=\Phi L/L_D=\gamma P_0\beta_2L^2/T_0^2$, and intensity curvature $|p''(0)|$ at the peak:
$$\frac{\lambda_{\min}(V)}{V_{\min}(\Phi)}-1=\frac{\Phi^{3/2}}{\sqrt{1+\Phi^2}}\sqrt{\tfrac13|p''(0)|\,\beta_2L}\;\big[1+O(y^{1/2})\big].$$
For the Gaussian, $|p''(0)|=2/T_0^2$. For the sech, $|p''(0)|=2/T_s^2$.

**Held-out predictions.** Scored on converged grids (dt ≤ 0.01 $T_0$, or $T_s$) with $10^{-5}\le y\le10^{-3}$, where $y$ uses $T_s$ for the sech. The ratio (measured excess)/(formula) lies in [0.97, 1.06] for:
1. Gaussian, $\Phi=2$;
2. Gaussian, $\Phi=40$;
3. sech, $\Phi=10$.

## Third frozen prediction: λ_min(V) dispersion law for a flat-top pulse (2026-10-10 11:56 EDT, commit 326c335, before any flat-top run)

**Why this is a test of the mechanism.** The derivation of the $\sqrt y$ law (claim C-20261010-claude-a-01, item 5) is a ground-state energy. The kinetic term $b\Omega^2$, with $b=\tfrac13\tfrac{\Phi^2}{\sqrt{1+\Phi^2}}\beta_2L$, comes from the CW dispersive correction to Kerr squeezing. The potential term comes from the intensity profile at the peak, $\tfrac{2\Phi}{\sqrt{1+\Phi^2}}(1-p(t))$.

For the flat-top pulse $p=e^{-(t/T_0)^4}$, $p''(0)=0$, so the potential is quartic: $A t^4$ with $A=2\Phi/\sqrt{1+\Phi^2}$. The ground state of $b\Omega^2+At^4$ is $e_4\,b^{2/3}A^{1/3}$, with $e_4=1.0603620905$ (ground state of $-d^2/dx^2+x^4$).

**Prediction.** With $y=\Phi\beta_2L/T_0^2$:
$$\frac{\lambda_{\min}(V)}{V_{\min}(\Phi)}-1=0.64226\,\frac{\Phi}{\sqrt{1+\Phi^2}}\;y^{2/3}\,\big[1+O(y^{2/3})\big].$$
The exponent is $2/3$, not $1/2$.

**Frozen windows.** Gaussian-free test, same code path (`lin_ssfm.propagate_cols`), $dt\le0.01\,T_0$:
1. Fitted exponent over $10^{-6}\le y\le10^{-4}$ in [0.64, 0.69], at $\Phi=10$ and at $\Phi=3$.
2. (measured excess)/(formula) in [0.95, 1.08] for $10^{-6}\le y\le10^{-3}$, at both $\Phi$.

## Fourth frozen prediction: momentum bound with third-order dispersion (2026-10-10 12:03 EDT, commit 98430d6, before any β3 run)

Claim C-20261010-claude-a-02, item 1, says $\lambda_{\rm gen}\le\langle\omega^2\rangle_{\rm in}/\langle\omega^2\rangle_{\rm out}$ for Kerr plus any linear dispersion. Third-order dispersion breaks the parity symmetry of every other case computed so far.

**Prediction.** Gaussian, $\Phi\in\{5,10\}$, $\delta_3=\beta_3L/T_0^3\in\{\pm0.01,\pm0.05\}$, with $\beta_2L/T_0^2\in\{0,\ 0.1/\Phi^2\}$. The input is centred on the carrier, so the centroid is computed with $c=0$, which gives an upper bound regardless of $c$. Bin threshold $10^{-9}$. For every case:
- $\lambda_{\rm gen}\le\lambda_P(\beta_2,\beta_3)$, the bound computed from the output mean field;
- $\lambda_{\rm gen}/\lambda_P\in[0.75,1.0]$.

## Fifth frozen prediction: long-pulse thermal formulas at a new pulse length (2026-10-10 12:53 EDT, commit 7398320, before computing)

Blow–Wood, $f_R=0.18$, Gaussian, $T_0=500$ fs (a pulse length not scanned), $\Phi=15$ (not scanned with Raman), at 150 K and 300 K.
- C-20261010-claude-a-02 item 2: $\lambda_{\rm gen}\le\lambda_{P,R}$, and $\lambda_{\rm gen}/\lambda_{\rm th}\in[0.88,1.00]$. The formula gives $\lambda_{\rm th}=0.01175$ (150 K) and 0.02049 (300 K).
- C-20261010-claude-a-01 item 3(b): band-limited $\lambda_{\min}$ divided by the slice value lies in [1.00, 1.15]. Slice values: 0.00427 (150 K) and 0.00732 (300 K).

**Correction (12:53 EDT, commit 7ea70c7, before any computation of this case).** The formula values written above were evaluated by hand and are wrong. The same formulas evaluated by code give:
- $\lambda_{\rm th}=0.01273$ (150 K) and 0.01972 (300 K);
- slice values 0.00491 (150 K) and 0.00868 (300 K).

The frozen predictions are the ratio windows, $\lambda_{\rm gen}/\lambda_{\rm th}\in[0.88,1.00]$ and band/slice $\in[1.00,1.15]$. They are unchanged and are scored against the corrected values.

## Scoring summary (written after all held-out runs; 13:17 EDT)

| Freeze | Commit | Outcome | Run |
|---|---|---|---|
| sech pulse, Kerr and Raman 300 K, $\Phi=5,15$ | dc191b0, ebeb0b7 | all inside: $\lambda_{\min}$, $\lambda_{\rm gen}$, binary (tabu and later relaxation search) | `heldout_results.json`, `binary_relax_sech.json`, `binary_relax_raman.json` |
| $\sqrt y$ law at $\Phi=2$, 40 and sech | 3a46f26 | all inside [0.97, 1.06] (1.003–1.031) | `lam_min_dispersion.json`, `lam_min_dispersion_sech.json` |
| flat-top $y^{2/3}$ law | 326c335 | exponent 0.6669 and 0.6668; ratios 1.0001–1.0123 | `lam_min_dispersion_flattop.json` |
| momentum bound with $\beta_3$ | 98430d6 | 16/16 inside; ratio 0.827–0.909 | `momentum_beta3.json` |
| thermal formulas at $T_0=500$ fs, $\Phi=15$ | 7398320 (+7ea70c7) | inside: 0.982 and 0.985; band/slice 1.051 and 1.041 | `heldout_thermal.json` |

Open predictions written in the claim cards, scored at the same time:
- C-02, $\Phi=50$ ($\lambda_{\rm gen}/\lambda_P\in[0.9,1]$): passed, 0.991.
- C-03, $\lambda_{\rm even}\ge0.05$ for $40<\Phi\le100$: passed, 0.055 at $\Phi=100$.
- C-01, band-limited $\lambda_{\min}$ within 5% of the slice value at 5 ps: **failed**, 1.069. The cause is the band-cutoff cost.

## Sixth frozen prediction: tightness of the momentum bound for a third pulse shape (2026-10-10 13:37 EDT, commit 0475fdd, before computing)

Flat-top $p=e^{-(t/T_0)^4}$, dispersionless Kerr. Its 1D integrals, by quadrature, are $I_1=\int(\sqrt p)'^2=1.83813$ and $I_2=\int p\,p'^2=1.07516$, so $4I_1/I_2=6.84$. Then $\lambda_P=I_1/(I_1+\Phi^2I_2)$ is 0.064008 at $\Phi=5$ and 0.007541 at $\Phi=15$ (values printed by code before this commit).

**Prediction.** At $\Phi=5$ and 15, padding 8, bin threshold $10^{-9}$: $\lambda_{\rm gen}\le\lambda_P$, with $\lambda_{\rm gen}/\lambda_P\in[0.80,1.00]$, as for the Gaussian and sech.

Sixth freeze (0475fdd), scored at 13:38 EDT: passed. $\lambda_{\rm gen}/\lambda_P=0.954$ ($\Phi=5$) and 0.976 ($\Phi=15$) (`heldout_flattop_lamgen.json`).
