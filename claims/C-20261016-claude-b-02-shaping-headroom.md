---
id: C-20261016-claude-b-02
problem: P-20261016-claude-interactive-01
title: "Headroom of input spectral shaping for dispersive-wave yield: persistent gain 1.0-1.55x for phase-only or passive masks, falling as the transform-limited yield rises from 0.05 to 0.32 (chirp alone at most 1.06x); in the burst regime exp[(d_*^TL - d_*^shaped)/delta3], growing as delta3 -> 0 (Gaussian N=3: kappa = 0.0025 for chirp, 0.006 for the optimised phase mask; 2.0x at delta3 = 0.01, 3.1x at 0.006)"
type: scaling-law
status: proposed
proposed_by: claude-b
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-16
updated: 2026-10-16
solver_commit: null
result: null
---

## Statement

**Setting.**
- Model M0 (TOD-perturbed NLSE, Roy convention $\delta_3=\beta_3/(6|\beta_2|T_0)$, no Raman or self-steepening) with a transform-limited Gaussian laser $u_{\rm laser}=e^{-\tau^2/2}$.
- Input $\hat u_{\rm in}=m(w)\hat u_{\rm laser}(w)$:
  - phase-only class $\mathcal S_\phi$: $m=e^{i\phi}$;
  - passive class $\mathcal S_{A\phi}$: $|m|\le1$.
- Yield: photons at $w\ge w_z=1/(6\delta_3)$, per laser photon, at $\xi_f$.
- Headroom: $H_{\mathcal S}=\max_{\mathcal S}\eta/\eta^{\rm TL}$.

**(a) Large-yield regime ($\eta^{\rm TL}\approx0.05$–0.3).** Achieved headroom from the adjoint optimisation, a lower bound on $H$ (see Checks for the numbers per point):
- chirp alone gives at most 1.06;
- phase-only gives 1.55, 1.50, 1.27 and 1.12 at $\xi_f=2$, at TL yields 0.052, 0.164, 0.206 and 0.319;
- the **persistent** gain (wide window, $\xi=6$) is 1.54, 1.40, 1.17 and 1.01. The headroom for radiated DW falls from about 1.5 to about 1 as the TL yield rises, and at $N=8$, $\delta_3=0.05$ the $\xi=2$ gain was an output-plane transient;
- passive gives 1.00–1.03× the phase-only value (amplitude freedom adds at most 3%; the optima keep more than 99.99% of the energy).

At $N=3$ the extra photons are persistent dispersive waves: the gain holds to $\xi=6$, and only 1–2% of band photons lie near a soliton. The gain also holds with Raman ($f_R=0.18$, $T_0=50$ fs).

What the optimised masks look like: a strong positive chirp (equivalent to GDD $C\approx2$–3, stretching the launch 2–3×) plus a negative quartic phase, which delays the compression to $\xi\approx1$–1.5.

They do **not** act through a sharper compression. Their $d_*$ is larger than TL's (A10, refuted), and their unperturbed spectral overlap with the band is smaller. The mechanism is open.

**(b) Burst regime ($d_*/\delta_3\gg1$).** By C-20261016-claude-b-01, the DW yield of any launch is $\propto e^{-d_*[m]/\delta_3}$, where $d_*[m]$ is the narrowest analyticity strip of the unperturbed evolution of the shaped launch. Hence
$$H_{\mathcal S}(\delta_3)=\exp\!\Big(\frac{d_*^{\rm TL}-\inf_{\mathcal S}d_*}{\delta_3}\Big)\,(1+o(1))\ \ \text{up to a prefactor ratio}.$$
The headroom therefore grows exponentially as $\delta_3\to0$ for any class that can lower $d_*$, at a rate $\kappa_{\mathcal S}=d_*^{\rm TL}-\inf_{\mathcal S}d_*$ that is a property of the **integrable** NLSE alone.
- For the Gaussian at $N=3$ with $\xi_f=2$ and quadratic-plus-cubic phase, $\kappa\approx0.0025$, reached by GDD $C_2\approx-0.2$ with no benefit from cubic phase. Chirp therefore gives 1.07 at $\delta_3=0.01$ and 1.28 at 0.006.
- The adjoint-optimised phase mask (Legendre degree 24) reaches $\kappa\ge0.0061$ (its $d_*$ is 0.1858). That gives 2.04× at $\delta_3=0.01$, 2.38× at 0.0075 and 3.07× at 0.006, matching the frozen prediction $H_{0.01}^{0.01/\delta_3}$ to within 8%.
- So the card's "phase-only at most 2×" conjecture fails for DW yield at the small-yield corner ($N=3$, $\delta_3\le0.01$) and fails for every $\delta_3$ below about $\kappa/\ln2$.
- **With Raman** ($f_R=0.18$, $T_0=50$ fs) this M0-optimised mask *reduces* the DW yield, to 0.03–0.08× TL. Burst-regime headroom must be optimised in the full model; the $\kappa$ above applies to M0 only.

**(c) Measurement caveat.** The band-photon count at the output plane is not the DW yield when the pulse there is mid-compression. Shaping can move a compression to the output plane and inflate the band count by up to about 2000× (Gaussian $N=3$, $\delta_3=0.006$, chirp $C=0.5$) without raising the DW yield.

## Regime

- (a): Gaussian, $N=3$–8, $\delta_3=0.02$–0.05, $\xi_f=2$; band yields 0.05–0.32. Tested points are listed below.
- (b): $d_*/\delta_3\gtrsim20$, tested at Gaussian $N=3$, $\delta_3=0.006$–0.01 (gated DW yield, $\xi_f=2$).

## Assumptions

1. Model M0, lossless; the mask acts in the spectral domain on the laser band ($|\hat u_{\rm laser}|>10^{-5}$ of its peak).
2. The phase is a Legendre series of degree 24 without constant and linear terms. Passive amplitudes are per bin, bounded to [0, 1].
3. The optimiser is L-BFGS(-B) on $-\ln\eta$ with exact discrete-adjoint gradients (checked to $10^{-8}$), from three starts (TL, best GDD, random), with at most 100–150 iterations. **Optimised values are lower bounds on the true maxima.**
4. A fixed length $\xi_f=2$. The yield is not maximised over length.

## Predictions

Frozen as H3a–H3e in commit d1b7f71, H3f (A3) in f736bd3, H3g (A6) in 0f566ae, A7 in 237c977, H3h (A8) in 52ddfd0, and H3i (A10) in 7eb2f0b. Outcomes are in Checks.
- **Not in the frozen set.** In the burst regime, the headroom of any mask at $\delta_3'$ follows from its value at $\delta_3$ as $\ln H(\delta_3')\approx(\delta_3/\delta_3')\ln H(\delta_3)$.
- **Lab, large-yield regime** (programmable shaper, transform-limited DW yield 0.05–0.3):
  - the masks found here give 1.1–1.55× and GDD alone about 1.06× or less;
  - a measured phase-only gain well above 2× there would indicate physics outside M0, or a better optimum than found here;
  - Petty (2024) measured about 1.4× with GDD in a regime with Raman and self-steepening, which this claim does not model.
- **Lab, burst regime** (DW yield below about $10^{-3}$): the gain of a fixed mask should grow with $T_0$ at fixed $N$ as $\exp(\kappa\cdot6|\beta_2|T_0/\beta_3)$.

## Derivation

(b) follows from C-20261016-claude-b-01. (a) is numerical.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Adjoint gradient | Phase and amplitude, plain and checkpointed: relative error $10^{-8}$ against central finite differences | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| (a) $N=3$, $\delta_3=0.05$ | $\eta^{\rm TL}=0.1643$. GDD 1.023 at $C=1.3$. Phase-only 1.503 (starts: TL 1.232, GDD 1.503, random 1.233; 150 iterations, not converged). Passive 1.506 (energy kept 0.99999). Persistence at $\xi=6$: band 0.2241 against TL 0.1595 (1.40×); 1.4% of band photons near the soliton | claude-b (claude) | 2026-10-16-claude-b-dw-shaping | 2026-10-16 |
| (a) $N=3$, $\delta_3=0.02$ | $\eta^{\rm TL}=0.0518$. GDD 1.040. Phase-only 1.546 (TL 1.096, GDD 1.546, random 1.096; 60 iterations). Passive 1.550 (energy kept 0.999999). Persistence at $\xi=6$: band 1.54× and gated 1.53×; 0.8% of band photons near the soliton. **Frozen H3a ($>2\times$ here) refuted**; its premise ('deep in the burst regime') was wrong, since $\eta^{\rm TL}=0.05$ | claude-b (claude) | 2026-10-16-claude-b-dw-shaping | 2026-10-16 |
| (a) $N=6$, $\delta_3=0.03$ | $\eta^{\rm TL}=0.2060$. GDD 1.057 at $C=1.0$. Phase-only 1.274 (TL 1.125, GDD 1.274, random 1.122; 120 iterations). Passive 1.307 (energy kept 0.99995). Window converged: TL $\eta_B$ is $2\times10^{-5}$ relative between windows 83 and 333. Persistence (window 320): at $\xi=6$ the band yields are 0.2449 (phase) and 0.2550 (passive) against TL 0.2085, i.e. 1.17× and 1.22×, down from 1.27× and 1.31× at $\xi=2$. So part of the $\xi=2$ gain is transient.

**Re-optimisation for persistence** (band yield at $\xi_f=4$, window 220, 40 iterations; `opt_N6_d0.03_xi4_it40_TW220.json`):
- TL $\eta_B(4)=0.2089$; GDD 1.024;
- phase-only 1.102 from both the TL and GDD starts, and 1.099 from the random start; passive 1.103;
- this is below the persistent 1.17–1.22× of the $\xi_f=2$ masks, so the persistent optimum is not found by this short run (a lower bound only) | claude-b (claude) | 2026-10-16-claude-b-dw-shaping | 2026-10-16 |
| (a) $N=8$, $\delta_3=0.05$ | $\eta^{\rm TL}=0.3186$ on the optimisation grid (window 70, which wraps DW; 0.3237 converged). GDD 1.003. Phase-only 1.123 (TL 1.123, GDD 1.092, random 1.117). Passive 1.125 (energy kept 0.99998). Because of the window wrap, these headrooms carry an uncertainty of about 2%. Persistence (window 440): band yields at $\xi=$2, 3, 4, 6 are 0.357, 0.318, 0.316, 0.315 (phase) and 0.358, 0.318, 0.319, 0.312 (passive), against TL 0.322, 0.322, 0.319, 0.311. **The gain is gone by $\xi=3$** (1.01× at $\xi=6$): the optimiser exploited an output-plane transient | claude-b (claude) | 2026-10-16-claude-b-dw-shaping (`window_check.json`) | 2026-10-16 |
| (a) chirp alone | 1.023, 1.040, 1.057, 1.003 at $(N,\delta_3)$ = (3, 0.05), (3, 0.02), (6, 0.03), (8, 0.05) | claude-b (claude) | 2026-10-16-claude-b-dw-shaping | 2026-10-16 |
| (b) chirp, frozen H3f (A3) | Gated DW $\eta(C)/\eta(0)$ against $\exp(-\Delta d_*/\delta_3)$. At $\delta_3=0.01$: 11 of 12 points within a factor 2; it fails at $C=-0.8$ (3.8×), where the sharpest compression is at $\xi=1.60$, too close to $\xi_f$ for the DW to clear the gate. At $\delta_3=0.006$: 11 of 12 within a factor 2 and 9 of 12 within 25%. It fails at $C=-1.0$, for the same reason (sharpest compression at $\xi=1.84$). Optimum at $C\approx-0.2$ in both theory and simulation | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| (b) cubic phase, frozen H3g (A6) | **Refuted as frozen**: predicted 5.3× at $\delta_3=0.01$, measured 0.755×. The input $d_*=0.175$ was an isolated fit outlier, found before the result was seen (A7). With the robust $d_*=0.1944$: predicted 0.78 against 0.755 measured at 0.01, and **0.667 against 0.701 measured at the held-out 0.006** (frozen in A7 before that result) | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| (b) polynomial phase, $\inf d_*$ | 18 pairs $(C_2,C_3)$ with robust minimum: 0.1905–0.2076, never below the GDD-only 0.1894 | claude-b (claude) | 2026-10-16-claude-b-dw-oracle | 2026-10-16 |
| (b) optimised phase, $\delta_3=0.01$ (gated objective) | Gaussian $N=3$, $\xi_f=2$: GDD 1.069. Phase-only **2.038**, with all three starts (TL, GDD, random) converging to the same value. Passive 2.051 (energy kept $1-5\times10^{-10}$) | claude-b (claude) | 2026-10-16-claude-b-dw-shaping | 2026-10-16 |
| (b) transfer of the optimised mask (A8, frozen) | **Confirmed.**
- (1) $d_*[\text{mask}]=0.1858$ (robust), a decrement of 0.0061 from TL's 0.1920. Predicted from the measured $H_{0.01}$: 0.0071 ± 30%.
- (2) Gated headroom 2.378 at $\delta_3=0.0075$ and 3.073 at 0.006, against the predicted $H_{0.01}^{0.01/\delta_3}$ = 2.584 and 3.276 (−8% and −6%).

The headroom grows exponentially as $\delta_3\to0$, with rate $\kappa\approx0.006$–0.007 for the optimised mask against 0.0025 for chirp. The ungated band count is 2.6× at 0.01, 6.9× at 0.0075 and 75× at 0.006: output-plane transients | claude-b (claude) | 2026-10-16-claude-b-dw-shaping (`transfer_*.json`, `mask_dstar_*.json`) | 2026-10-16 |
| Relaxed assumption: Raman (H4c, frozen) | The M0-optimised phase mask at $N=3$, $\delta_3=0.05$, evaluated in M1 ($f_R=0.18$, $T_0=50$ fs, RK4IP): gain 1.708 at $\xi=2$ and 1.456 at $\xi=6$, against 1.504 and 1.405 in M0. The $N=3$, $\delta_3=0.02$ mask: gain 1.546 and 1.540 in M0, against 1.538 and 1.538 in M1, although Raman lowers the TL yield 3.1×. It keeps more than half its gain (prediction): **confirmed at both large-yield points**.

**Burst regime: refuted.** The gated-objective mask optimised in M0 at $\delta_3=0.01$ (2.04× in M0), evaluated in M1 with RK4IP, gives a gated DW yield of 0.078× TL at $\delta_3=0.01$ and 0.034× at 0.0075, against 2.035× and 2.378× in M0. Its sharpened late compression is destroyed by Raman. Burst-regime shaping gains are therefore model-specific | claude-b (claude) | 2026-10-16-claude-b-dw-shaping (`h4c_*`, `h4c_gated_N3_d0.01_merged.json`) | 2026-10-16 | claude-b (claude) | 2026-10-16-claude-b-dw-shaping (`h4c_*`) | 2026-10-16 |
| Large-yield mechanism (A10, frozen) | Do large-yield optimised masks act through $d_*$? Predicted from inverting the TL collapse $F(d_*/\delta_3)$: $d_*=0.153$ ($N=3$, $\delta_3=0.02$ mask) and 0.095 ($\delta_3=0.05$ mask). Computed from the $\delta_3=0$ evolution: **0.1996 and 0.2813**, both larger than TL's 0.1922. **Refuted.** In the large-yield regime the optimised masks (strong positive chirp plus negative quartic phase; launches stretched 2–3×; compression delayed to $\xi\approx1$–1.5) raise the yield without sharpening the compression. The mechanism is not identified | claude-b (claude) | 2026-10-16-claude-b-dw-shaping (`mask_dstar_*.json`) | 2026-10-16 |
| (c) caveat | GDD $C=-0.4$, $\delta_3=0.01$: band 4.1× TL at $\xi=2$, 82% within 10 of the soliton (peak power 5.9); at $\xi=4$ band 0.75× and 4% near the soliton. Cubic $(-0.2,-0.6)$ at $\delta_3=0.006$: band 314×, gated 0.70× | claude-b (claude) | 2026-10-16-claude-b-dw-shaping, -oracle | 2026-10-16 |
| Second solver | Optimised $N=3$, $\delta_3=0.05$ masks evaluated in FastDifferentiableMMNLO by claude-b.7 (same family). Band yields: TL 0.16429435, phase 0.22945044, passive 0.24594767. These agree with numpy to $10^{-5}$ ($6\times10^{-7}$ once the residual self-steepening $s=10^{-6}$ is removed). Windows 70, 140 and 280 change $\eta_B$ by 0.1–0.2% (band-edge binning). Interpolating the mask onto a 2× finer grid changes the gated yields by 3–12%. The masks are tied to their bin representation | claude-b.7 (claude) | 2026-10-16-claude-b.7-solver-masks | 2026-10-16 |
| Adversarial audit | not done | | | |
| Novelty search | No gradient- or adjoint-optimised DW-yield headroom was found in the card's literature review. Petty (2024), about 1.4× from GDD, and Li et al. (2020), cubic plus quadratic phase "strongly enhances" (snippet only), are the closest. Not repeated here | claude-b (claude) | — | 2026-10-16 |

## Outcome

Proposed. The headroom in (a) is a lower bound from local optimisation.
