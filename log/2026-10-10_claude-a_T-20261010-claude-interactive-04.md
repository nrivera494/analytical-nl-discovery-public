---
date: 2026-10-10
agent: claude-a
model: claude-opus-5-5
family: claude
task: T-20261010-claude-interactive-04
duration_min: 204
---

Round 3, approach 1 of 4 on P-20261010-claude-interactive-01: dispersionless exact theory of filtered Fano bounds. This branch stacks on PR #27 (task/T-20261010-claude-interactive-01), which it merges.

**Timing.** Budget 240 min from 10:34 EDT. I stopped substantive work at 13:58 EDT, after about 3 h 24 min, because every item of the task was done or moved to a loose-end task (T-20261010-claude-a-01 to -07). The extra time went to the task's continuation order (more held-out checks, convergence, sharper exponents). The session protocol followed.

**Subagents.**
- claude-a.1 (claude-opus-5-5): solver discrete-adjoint check, run `2026-10-10-claude-a-solver-dispersion-check`.
- claude-a.2 (claude-opus-5-5): literature search; its report is folded into the Literature section below.

All numbers below come from run `2026-10-10-claude-a-dispersionless-fano` unless another run is named. File names in parentheses are inside the run folder.

## Did

1. **Exact model.** Checked the task's starting observation and wrote out the exact linearized covariance with the reservoir. Built an independent Python implementation (`dlfano.py`) of $V$ and of the spectral-bin covariance $V^{\rm amp}$. Built a second, independent linearized split-step and RK4 tangent propagator (`lin_ssfm.py`) for dispersion and self-steepening.
2. **Scans.**
   - Kerr scan over $\Phi=1$–30, plus a dense $\lambda_{\rm gen}$ and parity scan over $\Phi=2$–60.
   - Raman over $T_0=50$, 200 and 1000 fs, $T=0$ and 300 K (plus 77 and 150 K at 1 ps), $\Phi=5$, 10 and 20.
   - Self-steepening.
   - Two polarizations, including birefringence at any beat length.
   - Dispersion of both signs for $x=\Phi^2L/L_D\le3$, and the $\lambda_{\min}$ law down to $y=\Phi L/L_D=10^{-6}$.
   - Bin-threshold, time-step and bin-width convergence.
3. **Held-out cases.** Five sets of predictions, each frozen in `HELDOUT.md` and committed before computing:
   - the sech pulse, Kerr and Raman 300 K (dc191b0, ebeb0b7);
   - the $\sqrt y$ law at $\Phi=2$ and 40, and for the sech (3a46f26);
   - the flat-top $y^{2/3}$ law, a test of the mechanism (326c335);
   - the momentum bound with $\beta_3$ (98430d6);
   - the thermal formulas at an unscanned $T_0=500$ fs, $\Phi=15$ (7398320). My first freeze text contained hand-evaluated formula values that were wrong. I corrected them in commit 7ea70c7 before computing; the frozen ratio windows were not changed.
   - the momentum-bound tightness for a flat-top pulse (0475fdd).
   - All seven sets passed. For the flat-top, $\lambda_{\rm gen}/\lambda_P=0.954$ and 0.976 at $\Phi=5$ and 15 (`heldout_flattop_lamgen.json`).
4. **Binary filters.**
   - Found the dithering formula.
   - Built a faster and better search: box relaxation, then dithering, then tabu.
   - Found and checked a rigorous parity bound for non-negative filters.
5. **Write-up.**
   - Three claim cards: C-20261010-claude-a-01 ($\lambda_{\min}$), -02 ($\lambda_{\rm gen}$), -03 (parity bound).
   - One exploration note on binary filters, and a derivation note.
   - Run metadata, `summary.json` and a figure (`summary.png`).

## Found

### 1. Starting observation: confirmed, exactly

- **Covariance.** $X_{\rm out}=X_{\rm in}$ and $Y_{\rm out}=Y_{\rm in}+KX_{\rm in}+N_R$, with $K=2\Phi\sqrt p\hat R\sqrt p$. The reservoir covariance $N=2\Phi f_R\sqrt p\hat H\sqrt p$ uses $\tilde H=2|\mathrm{Im}\,\tilde h|\coth(\hbar|\omega|/2k_BT)$. Its commutator is fixed by unitarity.
- **Checks.**
  - $V+i\Omega\succeq0$ to $10^{-12}$.
  - The split-step propagator reproduces $V$ to $10^{-13}$ at $\beta_2=0$.

### 2. $\lambda_{\min}(V)$ (C-20261010-claude-a-01)

- **Without a reservoir.** Exact: $V_{\min}(\sigma_{\max}(K)/2)$. For Kerr this is $V_{\min}(\Phi)$ for every shape, matching the grid to $10^{-12}$.
- **With Raman.**
  - Over all modes it is at most $V_{\min}((1-f_R)\Phi)$, reached by far-detuned modes, which real dispersion removes. Equality holds to 0.5% at $T_0=50$ fs.
  - For longer pulses at 0 K, slow modes at the peak do better (0.01352 < 0.01445 at $T_0=200$ fs, $\Phi=5$). I first wrote this as an equality; corrected.
  - Band-limited to the pulse band, it tends to the thermal single-slice value $\simeq1/(4\Phi^2)+f_R\tilde H(0)/(2\Phi)$, which is $0.115/\Phi$ at 300 K. That holds provided the band is wide enough ($\Omega_bT_0\gtrsim30$: within 1%).
  - **Refuted open prediction.** I had registered (cb7ad63) that, with my default band, $T_0=5$ ps would come within 5%. It gives 1.069 (`open_prediction_5ps.json`).
  - The excess I had read as a slow approach in $T_0$ (+2% to +17% at 1 ps) is the cost of the default band cutoff. It is self-similar in $T_0$ and scales as $(\Omega_bT_0)^{-1.7}$, down to a 0.6% floor (`band_cost_check.json`). Card corrected.
  - So the reservoir leaves no floor. It changes $\Phi^{-2}$ into $\Phi^{-1}$.
- **Polarization.** $\lambda_{\min}=V_{\min}(\Phi_{\rm eff})$ exactly. Isotropic fibre: $\Phi_{\rm eff}=\tfrac\Phi3(1+\sqrt{1+3\cos^22\chi})$. Strong birefringence: $\tfrac\Phi2(1+\sqrt{1-\tfrac{20}9c_xc_y})$.
- **New: weak normal dispersion.**
  $$\lambda_{\min}/V_{\min}(\Phi)-1=\frac{\Phi^{3/2}}{\sqrt{1+\Phi^2}}\sqrt{|p''(0)|\beta_2L/3}\,[1+c_2\sqrt y],\qquad y=\Phi L/L_D,\ c_2\simeq1.0 .$$
  - Derived from a harmonic-oscillator balance between the intensity curvature and the CW dispersive correction to Kerr squeezing.
  - Measured exponent: 0.502 at $\Phi=2$, 5, 10, 20 (`lam_min_dispersion.json`).
  - Held-out ($\Phi=2$, $\Phi=40$, sech at $\Phi=10$): every point lies in the frozen window [0.97, 1.06]. The ratios are 1.003–1.031.
  - So $\lambda_{\min}(V)$ is the first quantity to leave its dispersionless value. The small parameter is $\sqrt{\Phi L/L_D}$, not $\Phi^2L/L_D$.
- **Mechanism test (held-out, frozen at commit 326c335).** A flat-top pulse $e^{-t^4}$ has $p''(0)=0$, so the harmonic balance becomes a quartic-oscillator ground state. The prediction was $0.64226\,\tfrac{\Phi}{\sqrt{1+\Phi^2}}y^{2/3}$. Measured: exponent 0.6669 ($\Phi=10$) and 0.6668 ($\Phi=3$); ratios 1.0001–1.0123 for $y\le10^{-3}$, all inside the frozen window [0.95, 1.08] (`lam_min_dispersion_flattop.json`).
- **Anomalous dispersion.** $\lambda_{\min}$ collapses as the grid is refined: $5\times10^{-4}$, $2\times10^{-5}$, then about 0, for $dt=0.04$, 0.02, 0.01 at $\Phi=10$, $y=10^{-3}$. These are dark modulation-instability sidebands.

### 3. $\lambda_{\rm gen}$ (C-20261010-claude-a-02)

- **Bound.** $\lambda_{\rm gen}\le\lambda_P=\langle\omega^2\rangle_{\rm in}/\langle\omega^2\rangle_{\rm out}$. It is rigorous for any number- and momentum-conserving dynamics (Kerr plus any $\beta(\omega)$), given one mean-field propagation.
  - Gaussian: $1/(1+4\Phi^2/3\sqrt3)$. Sech: $1/(1+32\Phi^2/35)$.
  - Tight to 0.81–0.996 for Kerr with $\Phi=1$–40, at every bin threshold tested.
  - At the most conservative threshold ($10^{-12}$) the ratio is 0.932, 0.952, 0.978, 0.988 for $\Phi=20$, 30, 40, 50, consistent with tending to 1.
  - The open prediction for $\Phi=50$ (registered at 11:56, before any converged $\Phi=50$ run) passed: 0.991 (`open_prediction_phi50.json`).
  - On converged bins for $\Phi=20$–80 (`lamgen_deficit.json`) the deficit $1-\lambda_{\rm gen}/\lambda_P$ is $\le2\%$ from $\Phi=35$ on. It has an overall slope of about $-1.1$ with oscillations, and levels near 1.1% at $\Phi=60$–80, where grid accuracy becomes marginal.
- **With Raman.**
  - The 1D-integral bound $\lambda_{P,R}$ holds in all 18 cases.
  - The long-pulse thermal form $[I_1+\tfrac\Phi2f_R\tilde H(0)\int p'^2]/[I_1+\Phi^2I_2]\to0.211/\Phi$ (Gaussian, 300 K) is within 7% of $\lambda_{\rm gen}$ for $T_0\ge200$ fs.
  - At $T_0=50$ fs, $\lambda_{\rm gen}/\lambda_{P,R}=0.23$–0.75.
  - **Held-out thermal check** ($T_0=500$ fs, $\Phi=15$; `heldout_thermal.json`): $\lambda_{\rm gen}/\lambda_{\rm th}=0.982$ (150 K) and 0.985 (300 K). Band-limited $\lambda_{\min}$ divided by the slice value is 1.051 and 1.041. All inside the frozen windows.
  - **Temperature** ($T_0=1$ ps, $\Phi=10$; `scan_raman_temperature.json`): $\lambda_{\rm gen}=0.0119$, 0.0167, 0.0217, 0.0319 at 0, 77, 150, 300 K. The thermal excess is linear in $T$ to 6%, at $6.3$–$6.7\times10^{-5}$ per K against $6.9\times10^{-5}$ from the formula.
  - The best binary goes from 0.507 to 0.520 over the same range. Band-limited $\lambda_{\min}$ divided by the slice value is 1.26, 1.10, 1.08, 1.07.
- **Wasted squeezing.** $\lambda_{\rm gen}/\lambda_{\min}\to4I_1/I_2$: $3\sqrt3=5.20$ (7.2 dB) for the Gaussian, 4.375 for the sech. In the thermal Raman regime it is about 2.0–2.3, tending to 1.84.
- **With dispersion.**
  - The dispersionless $\lambda_{\rm gen}$ holds within 2% for $x\le0.1$, both signs.
  - The bound with the actual output bandwidth is 0.85–0.96 tight up to $x=3$ (normal).
  - The bound's violation flagged the unconverged anomalous points ($x\ge1$).
- **$\beta_3$ held-out** (`momentum_beta3.json`, frozen at commit 98430d6): 16 cases ($\Phi=5,10$; $\delta_3=\pm0.01,\pm0.05$; $\beta_2L/T_0^2\in\{0,0.1/\Phi^2\}$).
  - The bound holds in all 16, and all are inside the frozen window [0.75, 1.0].
  - $\lambda_{\rm gen}/\lambda_P$ = 0.827–0.909.
  - The grid centroid readout equals the closed-form $\lambda_P$ to 2e-05 relative.
  - The output centroid stays at 0 (max |shift| 7e-11).
- **Self-steepening.** Even in $s$; at most 2.3% change at $\Phi s=0.1$.
- **Correction to my own derivation.** I had claimed that weights with independent slopes on the two sides of $\omega=0$ also reach $\lambda_P$. That is refuted: $|\omega|$ gives $F=13.8$ and $\omega\Theta(\omega)$ gives 6.9 at $\Phi=10$ (`dither_ramp.json`). Only $g\propto\omega$ works. The note has been corrected.

### 4. Best binary filter

**Question 2 of the task: scaling with $\Phi$.**
- It does not follow $1/(4\Phi^2)$. It falls slowly: 0.70–0.68 ($\Phi=2$–5), 0.47 (10), 0.40 (20), 0.32 (25), 0.40 (30), 0.36 (40), 0.33 (50).
- Fitted for $\Phi\ge10$: $F_{\rm bin}\approx0.47(\Phi/10)^{-0.21}$ (padding 8).
- The scatter of about ±10% (non-monotone values) shows the search is still limited.
- My earlier "saturation at 0.43–0.56" was a search artefact of the tabu method.
- **Bin width.** $\Phi=10$ is converged (padding 4/8/16: 0.478/0.471/0.470).
  - Padding 8 to 16: $\Phi=20$ 0.400 to 0.391 ($-2.3\%$), $\Phi=30$ 0.401 to 0.375 ($-6.3\%$), $\Phi=40$ 0.359 to 0.312 ($-13\%$; `binary_relax2_pad16_phi40.json`).
  - The resolution dependence grows with $\Phi$. At padding 16 the fitted slope for $\Phi=10$–40 is $-0.27$, against $-0.21$ at padding 8.
  - **It converges.** At $\Phi=20$, padding 4/8/16/32 gives 0.436/0.400/0.391/0.388 (`binary_relax2_pad32_phi20.json`). The steps shrink about 3.5× per halving of bin width, extrapolating to about 0.386. So padding 16 is within 1% at $\Phi=20$; larger $\Phi$ needs finer bins.

**How the search was done.** For each point, the best over:
1. nested tabu search (`binary_search4`): bright subsets, threshold starts, tabu, exact recomputation;
2. box relaxation $J(d)=1+d^{\mathsf T}(\Sigma-D)d/\bar n^{\mathsf T}d$ over $[0,1]^n$, solved by L-BFGS-B from 6–9 starts, then error-diffusion dithering, then tabu polish (`binary_relax_*.json`);
3. continuation in $\Phi$ (`continuation_kerr.log`).

**Structure.**
- The optimal filters are mostly one-sided in frequency, with dithered partial density.
- Dithering formula: $F_{\rm bin}\simeq1-(1-F_d)\langle d^2\rangle/\langle d\rangle$, to about 1%.

**Parity bound (rigorous; C-20261010-claude-a-03).**
- For a parity-symmetric problem every non-negative filter has $F\ge(\lambda_{\rm odd}+\lambda_{\rm even})/2$.
- $\lambda_{\rm even}$ stays 0.12–0.30 for $\Phi=7$–40.
- Its open prediction ($\lambda_{\rm even}\ge0.05$ for $40<\Phi\le100$, registered 11:42) holds: 0.097, 0.070, 0.055 at $\Phi=70$, 85, 100 (`open_prediction_lameven.json`). The decay steepens there, so the bound weakens at very large $\Phi$.
- On the bin set $\bar n\ge10^{-6}\bar n_{\max}$ the best binary sits 2.0–8.1 dB above it, against 2.3–26.5 dB above $\lambda_{\rm gen}$ ($\Phi=1$–40). For $\Phi\ge5$ the ranges are 3.4–8.1 dB and 11.8–26.5 dB.

**Structure of the best filters** (`binary_structure.json`).
- For $\Phi=7$–30 they are one-sided combs: 19–59 selected blocks, 87–94% of the photons on one side.
- Their odd-sector fraction is $f_{\rm odd}=0.38$–0.45, close to the parity limit 1/2.
- The noise comes mostly from the even sector (0.22–0.35 of $F$), with 0.10–0.14 from the odd sector. Overlap² with the momentum mode is 0.25–0.36.
- At $\Phi=40$ the best filter found is instead a symmetric comb ($f_{\rm odd}=0.03$, 158 blocks) that uses only the even sector.

**Breaking parity helps** (`binary_vs_beta3.json`). With $\beta_3$ alone, the best binary falls from 0.47 to about 0.30 ($\Phi=10$, $\delta_3\ge0.03$) and from 0.44 to 0.19 ($\Phi=20$, $\delta_3=0.1$). This is consistent with the parity mechanism. The point $\Phi=20$, $\delta_3=0.2$ is unconverged (bound violated) and excluded.

**Raman.** At 300 K the best binary changes by less than 0.03 from its 0 K value (tabu search), and with the better search it is within 3% of the Kerr-only optimum (`binary_relax_raman.json`). Yet Raman raises $\lambda_{\rm gen}$ by up to 2×.

**Gaps in dB, Kerr, Gaussian, dispersionless.** All runs from `2026-10-10-claude-a-dispersionless-fano`. Gap = 10 log10(best binary / quantity).

| $\Phi$ | $\lambda_{\min}$ | $\lambda_{\rm pass}$ | $\lambda_{\rm gen}$ | $\lambda_P$ (formula) | $F_{\rm par}$ | best binary | formula vs binary | $\lambda_{\rm gen}$ vs binary | $\lambda_{\min}$ vs binary | $F_{\rm par}$ vs binary |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.1716 | 0.1717 | 0.4558 | 0.5650 | 0.484 | 0.774 | 1.37 | 2.30 | 6.54 | 2.04 |
| 2 | 0.05573 | 0.05577 | 0.2313 | 0.2451 | 0.286 | 0.702 | 4.57 | 4.82 | 11.0 | 3.91 |
| 3 | 0.02633 | 0.02635 | 0.1229 | 0.1261 | 0.184 | 0.662 | 7.20 | 7.31 | 14.0 | 5.55 |
| 5 | 0.009805 | 0.009813 | 0.04461 | 0.04939 | 0.308 | 0.677 | 11.4 | 11.8 | 18.4 | 3.42 |
| 7 | 0.005051 | 0.005055 | 0.02130 | 0.02583 | 0.0757 | 0.488 | 12.8 | 13.6 | 19.8 | 8.09 |
| 10 | 0.002488 | 0.002490 | 0.01146 | 0.01282 | 0.156 | 0.471 | 15.7 | 16.1 | 22.8 | 4.81 |
| 12.5 | 0.001595 | — | 0.008011 | 0.008245 | 0.106 | 0.450 | 17.4 | 17.5 | 24.5 | 6.27 |
| 15 | 0.001109 | 0.001110 | 0.005537 | 0.005740 | 0.129 | 0.439 | 18.8 | 19.0 | 26.0 | 5.32 |
| 20 | 0.0006242 | 0.0006247 | 0.003048 | 0.003237 | 0.152 | 0.400 | 20.9 | 21.2 | 28.1 | 4.21 |
| 25 | 0.0003997 | — | 0.002057 | 0.002074 | 0.0812 | 0.322 | 21.9 | 21.9 | 29.1 | 5.98 |
| 30 | 0.0002777 | 0.0002777 | 0.001420 | 0.001441 | 0.121 | 0.401 | 24.4 | 24.5 | 31.6 | 5.18 |
| 40 | 0.0001562 | — | 0.000799 | 0.0008112 | 0.0614 | 0.359 | 26.5 | 26.5 | 33.6 | 7.67 |
| 50 | 0.0001000 | — | — | 0.0005193 | — | 0.331 | 28.0 | — | 35.2 | — |

- All rows are in `summary.json` (`kerr_gaussian`).
- $\lambda_{\min}$ at $\Phi=12.5$–50 is the exact $V_{\min}(\Phi)$.
- $\lambda_{\rm gen}$ at $\Phi=12.5$, 25 and 40 is $\lambda_{\rm odd}$ from `parity_bound.json`.
- All values use bin threshold $10^{-6}$; see section 7 for threshold effects.
- $\lambda_{\rm pass}$ exceeds $\lambda_{\min}$ by at most 0.06%.
- **Held-out sech** (`heldout_results.json`, `binary_relax_sech.json`, `parity_bound_sech.json`):

| case | $\lambda_{\min}$ | $\lambda_{\rm pass}$ | $\lambda_{\rm gen}$ | formula | best binary | formula vs binary (dB) | $\lambda_{\rm gen}$ vs binary (dB) | $\lambda_{\min}$ vs binary (dB) |
|---|---|---|---|---|---|---|---|---|
| Kerr $\Phi=5$ | 0.009805 | 0.009814 | 0.03544 | 0.04192 | 0.756 | 12.56 | 13.29 | 18.87 |
| Kerr $\Phi=15$ | 0.001109 | 0.001110 | 0.004660 | 0.004838 | 0.452 | 19.71 | 19.87 | 26.11 |
| Raman 300 K $\Phi=5$ | 0.01527 | 0.01527 | 0.07440 | 0.08197 | 0.766 | 9.70 | 10.12 | 17.00 |
| Raman 300 K $\Phi=15$ | 0.001840 | 0.001840 | 0.01810 | 0.01941 | 0.456 | 13.71 | 14.01 | 23.94 |

- **Raman, Gaussian:** all 18 rows with gaps are in `summary.json` (`raman_gaussian`). The best binary there is the minimum of the tabu search and the relaxation search (`binary_relax_raman.json`).
  - The relaxation search lowers the 300 K values to 0.483 ($T_0=200$ fs, $\Phi=10$), 0.406 (200 fs, 20), 0.484 (1 ps, 10) and 0.410 (1 ps, 20). These are within 3% of the Kerr-only optima.
  - Gaps at $T_0=1$ ps, 300 K, against the best binary: $\Phi=10$, formula 11.6, $\lambda_{\rm gen}$ 11.8, band-limited $\lambda_{\min}$ 15.2 dB; $\Phi=20$, 14.7, 14.8, 18.0 dB.
  - On the held-out sech the relaxation search gives 0.766 and 0.456. Both stay inside the frozen window [0.40, 0.80].

### 5. Validity against dispersion: where it breaks

In $x=\Phi^2L/L_D$:
- $\lambda_{\rm gen}$ holds to 2% for $x\le0.1$, 5% at $x=0.3$ and 14% at $x=1$.
- The best binary changes little at $\Phi=10$ for $x\le0.1$ (about $\pm2\%$), but already by about 10% at $\Phi=20$, $x=0.1$ (details below). At larger $x$, normal dispersion lowers it: $\Phi=10$, $x=1$: 0.388. At $\Phi=20$ (relaxation search, `scan_dispersion_phi20_rest.json`) it is 0.304 at $x=1$ and 0.275 at $x=3$, against 0.40 dispersionless.
  - Normal dispersion makes binary filtering markedly better. This is the hand-off to the normal-dispersion lane (T-20261010-claude-interactive-05).
  - **Onset, with the relaxation search at padding 4** (`binary_vs_dispersion.json`). The binary optimum responds at first order in $\beta_2$, with opposite signs.
    - $\Phi=10$: about $\pm1.7\%$ at $x=0.1$; $-6\%$ (normal) and $+7\%$ (anomalous) at $x=0.3$.
    - $\Phi=20$: $-9\%$ and $+11\%$ at $x=0.1$; $-17\%$ and $+26\%$ at $x=0.3$.
    - Over the same range $\lambda_{\rm gen}$ stays within 1%.
  - So the dispersionless binary value is the most fragile quantity after $\lambda_{\min}$. It holds to about 2% only for $x\lesssim0.1$ at $\Phi=10$ and $x\lesssim0.03$ at $\Phi=20$; the window narrows with $\Phi$. No scaling variable was identified.
- **$\Phi=20$ rows completed.** Those lost when the scan was stopped:
  - $\lambda_{\rm gen}$ changes by $-1.1\%$ (anomalous, $x=0.3$), $+6\%$ (normal, $x=1$) and $+19\%$ (normal, $x=3$).
  - The bandwidth bound holds, with ratio 0.94–0.96.
  - Anomalous $x\ge1$ is unconverged on this grid ($V$ not positive, bound violated) and excluded, as at $\Phi=5$ and 10.
- $\lambda_{\min}(V)$ breaks first, as $\sqrt{x/\Phi}$.
- **Solver cross-check** (subagent claude-a.1, run `2026-10-10-claude-a-solver-dispersion-check`, solver b9fa957, unmodified).
  - Method: FastDifferentiableMMNLO with the discrete adjoint (`adjoint_mode=:discrete_rk4ip`). The full $1024\times1024$ map $S$ was built row by row and checked against central finite differences to $10^{-10}$–$10^{-8}$. Gaussian, $\Phi=5$.
  - $\lambda_{\rm gen}$ matches `lin_ssfm.py` to 4–8 digits in all five cases:

    | case | solver | `lin_ssfm.py` |
    |---|---|---|
    | $x=0$ | 0.044606 | 0.04461 |
    | $x=0.1$, normal | 0.045480 | 0.04548 |
    | $x=0.1$, anomalous | 0.043639 | 0.04364 |
    | $x=1$, normal | 0.050661 | 0.05066 |
    | $x=1$, anomalous | 0.033700 | 0.0337 |

  - $\lambda_{\min}$, normal dispersion: 0.011060 ($x=0.1$; claim-01 formula with $c_2$: 0.011072) and 0.014568 ($x=1$).
  - At $x=0.1$ the solver's most-squeezed mode has rms width 0.17 ps, against the predicted $T_0(y/24)^{1/4}=0.170$ ps.
  - Anomalous: the most-squeezed mode is a modulation-instability sideband pair at $\sqrt{2\gamma P_0/|\beta_2|}$, with $\lambda_{\min}\approx5\times10^{-5}$.
  - Halving $dz$ changes everything by less than $2\times10^{-7}$. The physical shock term (1550 nm) changes $\lambda_{\rm gen}$ by $6\times10^{-6}$.
  - **Solver problem found.** The nonlinear step multiplies by a fixed anti-alias window that the API cannot switch off. At $\beta_2=0$ this makes the map non-symplectic at the band edge and corrupts the full-$V$ $\lambda_{\min}$ (0.0048 against the exact 0.0098). Band-limited $\lambda_{\min}$ and $\lambda_{\rm gen}$ are unaffected. Task T-20261010-claude-a-07.
  - Not run: the $N_t=400$ variants and the $dz/2$ runs of b0 and m0.1.

### 6. Self-steepening and polarization

- **Self-steepening.** The canonical photon-flux normalization $b=\tilde A/\sqrt{1+s\omega}$ is needed for a symplectic map: defect $7\times10^{-9}$, against about 10 with the naive one. Every filter quantity is even in $s$.
- **Polarization** ($\Phi=10$).
  - Elliptical $\chi=\pi/8$: $\lambda_{\rm gen}$ is 0.01518 polarization-resolved and 0.01626 polarization-insensitive.
  - Linear or circular input reduces to scalar with $\Phi_{\rm eff}$.
- **Intermediate beat length** (`birefringence.py`, a 4×4 RK4 tangent map per time slice; symplectic defect $\le2\times10^{-7}$).
  - With 45° linear input, $\lambda_{\min}=V_{\min}(\Phi_{\rm eff}(b))$, where $b=\Delta\beta/\gamma P_0=2\pi L_{NL}/L_B$.
  - $\Phi_{\rm eff}/\Phi$ goes from 1 to 5/6. It is within 1% of the isotropic value for $b\le0.03$ and within 0.5% of the strong-birefringence value for $b\ge5$.
  - It collapses in $b$ for $\Phi=5$, 10 and 20 to within about 1%, with beat-phase oscillations in between (`birefringence_lammin.json`).
  - At $\Phi=10$, $\lambda_{\rm gen}$ goes from 0.01147 to 0.01668 (resolved and insensitive bins). It is always below the total-momentum bound, at ratio 0.89–0.94.
  - The best binary is 0.45–0.52 (resolved) and 0.48–0.53 (insensitive) at every $b$ (`birefringence_Phi10_45deg.json`).
- **Anisotropic Raman.** Derivation note §6. The delayed response splits into three independent channels (bilinears $M_0$, $M_1$, $M_2$; kernels $a+b/2$, $b/2$, $b/2$).
  - Linear input stays an exact scalar shear with the parallel kernel $a+b$.
  - Circular input stays an exact scalar shear with kernel $\tfrac23(1-f_R)\delta+f_R(a+b/2)$. Long-pulse $\Phi_{\rm eff}=[\tfrac23(1-f_R)+f_R(1-\rho/2)]\Phi$, which is 0.718–0.723$\,\Phi$ for Lin–Agrawal-type parameters (from the gnlse-python source; the paper was not accessed).
  - Elliptical input loses the exact structure.
  - **Numbers** for linear and circular input (`vector_raman_exact.py`). Lin–Agrawal-type kernels, two candidate isotropic/anisotropic splits, $\Phi=10$:

    | $T_0$, $T$ | linear $\lambda_{\rm gen}$ | linear binary | circular $\lambda_{\rm gen}$ | circular binary |
    |---|---|---|---|---|
    | 200 fs, 0 K | 0.0170 | 0.510 | 0.0282–0.0283 | 0.527–0.549 |
    | 200 fs, 300 K | 0.0611 | 0.535 | 0.0854–0.0865 | 0.565–0.574 |
    | 1 ps, 0 K | 0.0120 | 0.501 | 0.0213–0.0214 | 0.535–0.543 |
    | 1 ps, 300 K | 0.0373 | 0.525 | 0.0638–0.0644 | 0.556–0.567 |

    - The split changes $\lambda_{\rm gen}$ by at most 1.3%. Symplecticity holds in all 12 runs.
    - **Raman-model dependence.** Against Blow–Wood with $f_R=0.18$, these kernels raise $\lambda_{\rm gen}$ at 300 K by 1.9× ($T_0=200$ fs) and 1.17× (1 ps). The Boson-peak term puts reservoir noise inside the SPM band.
  - **Elliptical input, propagated** (`vector_raman_prop.py`, `vector_raman_prop.json`): the three-channel model and its reservoir integrated in $z$ with a Lyapunov covariance.
    - Validated against the exact circular and linear reductions (6 digits in $\lambda_{\min}$, $\lambda_{\rm gen}$ and binary) and against the Kerr-only elliptical run ($\lambda_{\rm gen}$ 0.016258 vs 0.016260). Physical, with $V+i\Omega\succeq0$.
    - At $\chi=\pi/8$, $T_0=200$ fs, $\Phi=10$, insensitive bins: $\lambda_{\rm gen}=0.0277$ (0 K) and 0.091–0.093 (300 K); best binary 0.656 and 0.684.
    - At 300 K elliptical input is noisier than circular (0.085–0.087) and linear (0.061), and it is the worst case for binary filters.
    - The anisotropic channels move 2% of the peak power between $\sigma_\pm$ ($\sigma_+$ fraction 0.854 to 0.834).
    - **Ellipticity scan** (300 K, split A, `vector_raman_chiscan.json`; $\chi=0$ and $\pi/4$ from the exact reductions):

      | $\chi$ | 0 | 0.1 | 0.2 | 0.3 | 0.39 | 0.5 | 0.6 | 0.7 | 0.785 |
      |---|---|---|---|---|---|---|---|---|---|
      | $\lambda_{\rm gen}$ | 0.061 | 0.066 | 0.074 | 0.084 | 0.093 | 0.097 | 0.097 | 0.094 | 0.085 |
      | best binary | 0.535 | 0.578 | 0.626 | 0.695 | 0.684 | 0.646 | 0.612 | 0.580 | 0.574 |

    - $\lambda_{\rm gen}$ peaks near $\chi\approx0.5$–0.6 at 1.6× its linear value. The binary optimum is worst near $\chi\approx0.3$–0.4.
    - From $\chi=0.7$ to circular, $\lambda_{\rm gen}$ drops 10% although only 0.7% of the power is in $\sigma_-$. A weak $\sigma_-$ component carries amplified anisotropic-Raman noise into insensitive counts. Not analysed further.
    - **$T_0=1$ ps** (`vector_raman_1ps.json`, $\chi=\pi/8$, split A): $\lambda_{\rm gen}=0.0170$ (0 K) and 0.0580 (300 K), between linear (0.0120, 0.0373) and circular (0.0213, 0.064). Best binary 0.662 and 0.683, again the worst of the three inputs. The $\sigma_+$ fraction at the peak moves only from 0.854 to 0.856.
    - Not done: other $\Phi$; band-limited $\lambda_{\min}$. Those remain in T-20261010-claude-a-06.

### 7. Convergence findings that change how numbers should be quoted

- **Bin threshold.**
  - The grid value of the centroid readout needs the far spectral wings. With bins down to $10^{-6}\bar n_{\max}$ it is 0.6–10% above $\lambda_P$ for $\Phi=10$–24, and up to 3× at $\Phi=60$. With $10^{-9}$ it equals $\lambda_P$ to $10^{-4}$.
  - $\lambda_{\rm gen}$ moves only 0.4–3% between thresholds $10^{-6}$ and $10^{-12}$ for $\Phi\le40$. For $\Phi\ge44$ at $10^{-6}$ it is not converged: it exceeds $\lambda_P$, which the rigorous bound forbids (`lam_gen_dense.json`, `grid_check*.json`).
  - $\lambda_{\rm even}$, and with it the parity bound, depends strongly on the bin set. At $\Phi=20$, $F_{\rm par}=0.152$, 0.144, 0.061 for $10^{-6}$, $10^{-9}$, $10^{-12}$. So that bound is stated for an explicit bin set.
  - Physically the set is limited by $\bar n_i\gg1$, which linearization requires.
- **Time step.** $dt$ from $0.8/\Phi$ down to $0.2/\Phi$ (capped at 0.04) changes nothing at the fifth digit.
- **Raman time step** (the orchestrator's "$dt\le3$ fs or show convergence"; `raman_dt_convergence.json`). Kernels are bin-averaged exactly.
  - $\lambda_{\rm gen}$, band-limited $\lambda_{\min}$ and the centroid readout change by $<0.05\%$ from $dt=8$ to 2 fs ($T_0=200$ fs) and from 40 to 10 fs (1 ps).
  - The full-grid $\lambda_{\min}$ moves with $dt$ toward $V_{\min}(0.82\Phi)$ (0.00370 at $dt=2$ fs, against 0.00369), as claim -01 item 3(a) says.

### 8. Cross-checks with other round-3 branches

Read in the last hour, as the task allows. These are cited as unverified work in progress; I did not adopt their methods or redo their lanes.

- **claude-b, T-20261010-claude-interactive-05** (branch at 8908a17).
  - Their C-20261010-claude-b-02 (first committed 11:32 EDT, ten minutes before my C-20261010-claude-a-02 at 11:42) states the same momentum (spectral-centroid) bound: Fano factor $=\langle\delta\omega^2\rangle_{\rm in}/\langle\delta\omega^2\rangle_{\rm out}$, an upper bound on $\lambda_{\rm gen}$.
    - Their pure-SPM limit $1/(1+0.770\Phi^2)$ equals my $1/(1+4\Phi^2/3\sqrt3)$, with $4/3\sqrt3=0.7698$.
    - Their $\lambda_{\rm gen}$ lies 0.25–0.93 dB below it at $\Phi=1$–10, matching my ratios 0.81–0.94.
    - These are independent derivations by the same family, so a gpt-family verification is still needed. The two cards could be merged or cross-referenced; see Proposed card changes.
  - Their C-20261010-claude-b-01 uses $Z=Nz/L_D$ and $\Phi=NZ$, so my $y=\Phi L/L_D$ equals $Z^2$.
    - Their semiclassical factor $4Z^2\Lambda(Z)=1.09$ at $Z=0.1$ matches my $\lambda_{\min}$ law at $y=0.01$ (measured 1.089; formula with $c_2$: 1.090).
    - So my $\sqrt y$ law, $4Z^2\Lambda\simeq1+\sqrt{2/3}\,Z(1+c_2Z)$, is the small-$Z$, large-$\Phi$ expansion of their $\Lambda(Z)$.
  - Their C-20261010-claude-b-03 recovers, in its dispersionless limit, a Raman correction $\propto1/\Phi$. That is the same structure as my thermal slice; I have not mapped their $\hat c(0)$ onto my $f_R\tilde H(0)/2$.
- **gpt-a, T-20261010-claude-interactive-03** (branch at 2a40651).
  - Their dispersionless Kerr pilot at $\Phi=1$ gives $\lambda_{\min}=0.171572883$ against $(\sqrt2-1)^2$, independently of my code (solver discrete adjoint). This confirms C-20261010-claude-a-01 item 2.
  - Their interim tables have no dispersionless rows yet, so my parity bound cannot be compared there.
  - Their binary certificates come within 0.001–0.27 dB of their best binary in the anomalous and normal cases. That is far tighter than my parity bound (2–8 dB, dispersionless), so where both apply, theirs likely dominate. This is for task T-20261010-claude-a-03 to settle.
  - They also flag formal optima that select dark bins, which matches my bin-set finding (section 7).

## Changed

- New: `claims/C-20261010-claude-a-01-dispersionless-lambda-min.md`, `-02-momentum-mode-lambda-gen.md`, `-03-parity-bound-nonnegative-filters.md`, all `proposed`.
- New: `claims/notes/C-20261010-claude-a-01-derivation.md` (serves all three).
- New: `explorations/2026-10-10-claude-a-binary-filters-dispersionless.md`.
- New: `runs/2026-10-10-claude-a-dispersionless-fano/` (scripts, json, `HELDOUT.md`, `meta.yaml`, `config.yaml`, `summary.json`, `summary.png`).
- New: `runs/2026-10-10-claude-a-solver-dispersion-check/` (subagent claude-a.1).
- `tasks/T-20261010-claude-interactive-04-...md`: status done.
- New loose-end tasks, listed below.
- Merged origin/task/T-20261010-claude-interactive-01 (PR #27) into this branch, and later `origin/main` (which by then contained PRs #26 and #27); no conflicts.

## Not verified

- **Same family.** No check by another family. All three claims need verification by a gpt agent (tasks below).
- **Process note.** Twice I typed hand-evaluated formula values into a freeze text before the code printed them. Both were wrong.
  - The fifth freeze was corrected in a separate commit (7ea70c7) before computing.
  - The sixth was corrected before its freeze commit.
  - In both cases the frozen windows were stated as ratios and were not changed.
- **Binary optimum.** Not converged in search (about ±10% scatter at $\Phi\ge20$). Not converged in bin width at $\Phi=20$ (padding 8 to 16: −2.3%) or $\Phi=30$ (−6.3%). Quote it with the search method and the bin width.
- **Band-limited $\lambda_{\min}$ with Raman.** It depends on the chosen band ($1.2\max|\bar\phi'|+3/t_{\rm rms}$). The thermal-slice limit is approached slowly; the 5 ps prediction is untested.
- **Parity bound.** Its values depend on the darkness threshold of the admitted bins (section 7). Bin width does not change it: padding 16 gives the same value to 3 digits (`parity_pad16.json`).
- **No CAS check.** The $I_1,I_2$ closed forms and the CW dispersive correction $\tfrac23aL\Phi^2/\sqrt{1+\Phi^2}$ were done by hand. The latter is confirmed numerically by the exponent and prefactor.
- **Solver check (claude-a.1).** Covers only $\Phi=5$ (see section 5). The $\sqrt y$ law for $\lambda_{\min}$ was checked with the solver at one point ($y=0.02$: 0.1%, mode width 1%). Its exponent has not been measured with the solver (task T-20261010-claude-a-01).

## Proposed card changes

For P-20261010-claude-interactive-01. Not edited by me.

1. **"One closed-form anchor".** Add that $\lambda_{\min}(V)=V_{\min}(\Phi_{\rm peak})$ is exact for Kerr for every pulse shape, and $V_{\min}(\sigma_{\max}(K)/2)$ with a delayed response and no reservoir (C-20261010-claude-a-01). With the thermal reservoir the large-$\Phi$ law becomes $\Phi^{-1}$ ($0.115/\Phi$ at 300 K), not a floor. So the card's "Raman ... should impose a floor" should read "changes $\Phi^{-2}$ to $\Phi^{-1}$".
2. **Answer form.** Add $y=\Phi L/L_D$ as the group controlling $\lambda_{\min}(V)$ with weak normal dispersion. $\lambda_{\min}$ leaves the dispersionless value as $\sqrt y$, while filter quantities are controlled by $x=\Phi^2L/L_D$ (2% at $x=0.1$).
3. **Structure to start from.** Add the momentum bound $\lambda_{\rm gen}\le\langle\omega^2\rangle_{\rm in}/\langle\omega^2\rangle_{\rm out}$ (rigorous for Kerr plus any linear dispersion), and the parity bound for non-negative filters. Both are cheap: one mean-field propagation, or one parity-blocked eigenproblem.
4. **"Risks".** In the dispersionless regime, for $\Phi\ge5$, the rigorous bounds are loose by 12–27 dB ($\lambda_{\rm gen}$) and 3–8 dB (parity, on a stated bin set) against the best binary found. The binary optimum itself depends on the search method by up to 1.5 dB, and on bin width at large $\Phi$ (up to 6% at $\Phi=30$). Quote binary optima with the search method and the bin width.
5. **Literature.** Add the items in the Literature section below, at their stated access levels.
6. **Duplicate result.** C-20261010-claude-a-02 and claude-b's C-20261010-claude-b-02 (unverified WIP) state the same momentum bound. They were found independently in different regimes (dispersionless, and normal dispersion). Cross-reference them on the card, or merge them, so that one other-family verification covers both.

## Literature

**How it was searched.** Subagent claude-a.2 searched for about 50 minutes on 2026-10-10: WebSearch in standard mode, with one extended query, and WebFetch on arXiv, ar5iv, Optica, APS and doi.org pages. I read none of the papers myself.

**Access levels.**
- "Full text (raw)": text extracted from the PDF and read.
- "Full text (targeted)": full text retrieved but read through a summarizing model answering specific questions, so details may be imprecise.
- "Abstract only".
- "Not accessed".

**Search strings**, verbatim, standard mode unless marked:
- Shirasaki Haus squeezing of pulses in a nonlinear interferometer JOSA B 1990
- Kitagawa Yamamoto number-phase minimum-uncertainty state Kerr nonlinear interferometer Phys Rev A 1986
- self-phase modulation quantum noise spectral centroid mean frequency conserved momentum squeezing pulse fiber
- "momentum squeezing" soliton fiber quantum noise frequency spectral filtering
- quantum noise self-phase modulation spectral broadening photon number correlations between spectral components red blue wings sub-shot-noise weighted detection
- optimal linear combination of spectral photon numbers Kerr fiber pulse photon-number correlations eigenvector optimal weighting noise reduction spectrally resolved detection
- nonlinear Schrödinger equation conserved momentum operator quantum noise "mean frequency" fluctuations coherent pulse self-phase modulation bandwidth broadening sub-shot-noise
- "frequency squeezing" OR "spectral centroid" squeezing self-phase modulation pulse quantum noise fiber
- quantum limited center frequency jitter spectrally broadened pulse self-phase modulation conserved first spectral moment photon number weighted frequency
- (extended) quantum noise of self-phase modulated pulse: optimal weighted spectral photon-number measurement limited by momentum (mean frequency) conservation, Fano factor equals ratio of input to output spectral width
- effect of group velocity dispersion on Kerr squeezing of optical pulses fiber analytic perturbation degradation normal dispersion squeezing pulse
- modulational instability squeezing optical fiber anomalous dispersion sidebands quadrature squeezing quantum noise
- Raman noise limits Kerr squeezing scaling with nonlinear phase spontaneous Raman phase noise fiber squeezing theory Drummond Corney
- Tanaś Kielich self-squeezing of light propagating through nonlinear optically isotropic media elliptical polarization
- spectral edge filtering self-phase modulation photon-number squeezing limit 3 dB half spectrum normal dispersion theory Fano factor 1/2
- plus 39 more author- and title-specific strings, listed in the subagent's report (kept in this session's transcript; summarized by the items below).

**By claim item.**

- **$\lambda_{\min}$ closed form, (a): known.**
  - Single-mode Kerr squeezing: Kitagawa & Yamamoto, PRA 34, 3974 (1986), [DOI:10.1103/PhysRevA.34.3974](https://doi.org/10.1103/PhysRevA.34.3974), abstract only.
  - Time-slice picture of dispersionless SPM:
    - Joneckis & Shapiro, JOSA B 10, 1102 (1993), [DOI:10.1364/JOSAB.10.001102](https://doi.org/10.1364/JOSAB.10.001102), abstract only;
    - Kärtner, Joneckis & Haus, Quantum Opt. 4, 379 (1992), [DOI:10.1088/0954-8998/4/6/003](https://doi.org/10.1088/0954-8998/4/6/003), abstract only;
    - Shirasaki & Haus, JOSA B 7, 30 (1990), [DOI:10.1364/JOSAB.7.000030](https://doi.org/10.1364/JOSAB.7.000030), abstract only.
  - Validity of the linearized $1/(4\Phi^2)$ law: Bajer, Miranowicz & Tanaś, [arXiv:quant-ph/0212158](https://arxiv.org/abs/quant-ph/0212158), full text (targeted).
  - So item 2 of C-20261010-claude-a-01 is a restatement for Kerr. What is new there is the nonlocal Raman generalization and the reservoir form.

- **Momentum bound, (b): not found.**
  - Searched with the strings above (centroid, momentum, optimal weighting, bandwidth ratio).
  - Known: linearized soliton theory conserves photon number and momentum (Haus & Lai, JOSA B 7, 386 (1990), [DOI:10.1364/JOSAB.7.000386](https://doi.org/10.1364/JOSAB.7.000386), abstract only).
  - Levandovsky, Vasilyev & Kumar, OL 24, 43 (1999), [DOI:10.1364/OL.24.000043](https://doi.org/10.1364/OL.24.000043), full text (raw), state the conservation explicitly. They argue the optimal passive soliton filter is even in $\omega$, so momentum drops out. That is consistent with the parity structure of C-20261010-claude-a-03, though no parity bound is stated.
  - "Momentum squeezing" by an interferometer: Werner, PRL 81, 4132 (1998), [arXiv:quant-ph/9904099](https://arxiv.org/abs/quant-ph/9904099), full text (targeted).
  - The SPM example of Uddin et al., Nat. Photon. 19, 751 (2025), [DOI:10.1038/s41566-025-01677-2](https://doi.org/10.1038/s41566-025-01677-2), [arXiv:2311.05535](https://arxiv.org/abs/2311.05535), full text (targeted, SPM section), has no centroid bound.
  - Still to do: read Haus & Lai 1990 in full (momentum detectors).

- **Dispersion, (c): partially known.**
  - CW modulation-instability squeezing is stronger with anomalous dispersion: Potasek & Yurke, PRA 35, 3974 (1987), [DOI:10.1103/PhysRevA.35.3974](https://doi.org/10.1103/PhysRevA.35.3974), abstract only.
  - Pulsed squeezing with dispersion, numerical: Doerr, Shirasaki & Khatri, JOSA B 11, 143 (1994), [DOI:10.1364/JOSAB.11.000143](https://doi.org/10.1364/JOSAB.11.000143), abstract only.
  - The $\sqrt{(2/3)\Phi L/L_D}$ law was not found.

- **Raman law, (d): known for CW; credit it.**
  - Shapiro & Boivin, OL 20, 925 (1995), [DOI:10.1364/OL.20.000925](https://doi.org/10.1364/OL.20.000925), abstract only.
  - Voss, Köprülü & Kumar, JOSA B 23, 598 (2006), [arXiv:quant-ph/0410214](https://arxiv.org/abs/quant-ph/0410214), full text (targeted, Sec. 5.A, Eq. 100). CW squeezing "asymptotically scales as $1/\phi_{NL}$", with a coefficient set by $k_BT$ and the zero-frequency slope of $\mathrm{Im}$ of the Raman response.
  - Pulses and solitons, numerical or experimental:
    - Kärtner, Dougherty, Haus & Ippen, JOSA B 11, 1267 (1994), [DOI:10.1364/JOSAB.11.001267](https://doi.org/10.1364/JOSAB.11.001267), abstract only;
    - Boivin, Kärtner & Haus, PRL 73, 240 (1994), [DOI:10.1103/PhysRevLett.73.240](https://doi.org/10.1103/PhysRevLett.73.240), abstract only;
    - Yu & Lai, JOSA B 12, 2340 (1995), [DOI:10.1364/JOSAB.12.002340](https://doi.org/10.1364/JOSAB.12.002340), abstract only;
    - Dong et al., OL 33, 116 (2008), [arXiv:0709.2280](https://arxiv.org/abs/0709.2280), full text (targeted).
  - Our pulsed coefficient $f_R\tilde H(0)/2$ has not been mapped onto Voss Eq. (100). The subagent's summary gave that equation's prefactor inconsistently, so the equation needs reading directly.

- **Polarization, (e): partially known.**
  - The two-circular-mode self-squeezing Hamiltonian $\propto a_1^{\dagger2}a_1^2+a_2^{\dagger2}a_2^2+4d\,a_1^\dagger a_2^\dagger a_1a_2$ (with $d=1$ for a fully symmetric $\chi^{(3)}$) is in Tanaś, Miranowicz & Gantsog, Progress in Optics 35 (1996), [arXiv:1110.4602](https://arxiv.org/abs/1110.4602), full text of Sec. 4.3 (raw).
  - Agarwal & Puri, PRA 40, 5179 (1989), [DOI:10.1103/PhysRevA.40.5179](https://doi.org/10.1103/PhysRevA.40.5179), abstract only.
  - The original Tanaś & Kielich papers (Opt. Commun. 45, 351 (1983); Opt. Acta 31, 81 (1984)) were not accessed and no DOI was found. They are listed here as leads, not sources.
  - Our closed form assumes $d=1$. For general $d$, $\Phi_{\rm eff}=\Phi[1+\sqrt{1+(4d^2-1)\cos^22\chi}]/(1+2d)$. This was proposed by claude-a.2 and checked by hand by claude-a (eigenvalues of $\begin{pmatrix}c_+&2d\sqrt{c_+c_-}\\2d\sqrt{c_+c_-}&c_-\end{pmatrix}$); there is no run.

- **Binary filters, (f): partially known.**
  - Normal-dispersion filtering experiments reached Fano factors of about 0.55 after loss correction:
    - Sizmann, Fauster & Leuchs, J. Mod. Opt. 45, 2425 (1998), [DOI:10.1080/09500349808230495](https://doi.org/10.1080/09500349808230495), abstract only;
    - Krylov, Bergman & Lai, OL 24, 774 (1999), [DOI:10.1364/OL.24.000774](https://doi.org/10.1364/OL.24.000774), abstract only.
  - Microstructure-fibre broadening with filtering reached 10.3 dB corrected: Hirosawa et al., PRL 94, 203601 (2005), [arXiv:quant-ph/0501043](https://arxiv.org/abs/quant-ph/0501043), abstract only.
  - No statement about the dispersionless binary optimum against $\Phi$ was found.
  - **A heuristic I do not adopt.** claude-a.2 suggested that a half-spectrum filter gives $F\to1/2$ through momentum conservation. Run data refute it: the half-spectrum filter has $F=11.6$ at $\Phi=10$. The sign-weighted count $\sum\mathrm{sgn}(\omega)n$ is not the conserved centroid, and its jump at $\omega=0$ maps onto the bright peak.

- **Vector Raman (my own searches, 12:10–12:16 EDT).**
  - Search strings, standard mode:
    - `Lin Agrawal "Raman response function for silica fibers" Optics Letters 2006 anisotropic fa fb fc 96 fs`
    - `vector Raman response silica fiber isotropic anisotropic "R_a(t)" "R_b(t)" "f_a h_a" "f_c h_a" "f_b h_b" polarization Lin Agrawal`
  - Lin & Agrawal, OL 31, 3086 (2006), [DOI:10.1364/OL.31.003086](https://doi.org/10.1364/OL.31.003086) (resolves to ol-31-21-3086): not accessed. The author-site PDF returned 404.
  - Parameter values taken from the gnlse-python implementation (github.com/WUST-FOG/gnlse-python, `gnlse/raman_response.py`, function `raman_linagrawal`, read in full): $f_R=0.245$, $\tau_1=12.2$ fs, $\tau_2=32$ fs, $\tau_b=96$ fs, $f_b=0.21$, $f_c=0.04$, $f_a=0.75$, with parallel response $(f_a+f_c)h_a+f_bh_b$.
  - That code does not give the isotropic/anisotropic split, so $\rho=\int b$ is uncertain between 0.21 and 0.25.
- **Not located.** Rivera, Uddin, Sloan & Soljačić, Nanophotonics 2025 (the problem card lists [DOI:10.1515/nanoph-2024-0634](https://doi.org/10.1515/nanoph-2024-0634)). claude-a.2's searches did not find it. Not accessed by us.

## Loose ends

Task ids are listed in the section "Tasks created" at the end of this entry.

## Tasks created

| Task | Type | Family | Loose end |
|---|---|---|---|
| T-20261010-claude-a-01 | verify | not-claude | C-20261010-claude-a-01, including the √(ΦL/L_D) law, with the solver |
| T-20261010-claude-a-02 | verify | not-claude | C-20261010-claude-a-02, the momentum bound and its tightness |
| T-20261010-claude-a-03 | audit | not-claude | C-20261010-claude-a-03, the parity bound, cross-checked with T-20261010-claude-interactive-03 certificates |
| T-20261010-claude-a-04 | loose-end | any | binary optimum: bin-width and search convergence, large-Φ asymptotics |
| T-20261010-claude-a-05 | derive | any | $\lambda_{\rm even}(\Phi)$ |
| T-20261010-claude-a-06 | loose-end | any | anisotropic Raman (two polarizations). The intermediate beat length was done in this session; the task text still lists it, so a taker can skip that part |
| T-20261010-claude-a-07 | infra | any | solver switch for the nonlinear-step anti-alias window and the shock term |
