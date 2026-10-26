---
id: C-20261016-claude-a-02
problem: P-20261016-claude-interactive-03
title: "Raman transfer to the leading fission soliton: linear in T_R/T0 for long pulses, maximal where the compressed-soliton bandwidth N²/T0 meets the Raman gain peak 1/τ1 (T0* ≈ 1.7 τ1 N^1.62), with peak energy fraction f1* ≈ 1.29/√N (within −4%/+2.4% across five Raman responses)"
type: scaling-law
status: refuted
proposed_by: claude-a
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: gpt-c
verifier_family: gpt
audited_by: gpt-c
auditor_family: gpt
created: 2026-10-16
updated: 2026-10-17
solver_commit: b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa
result: null
---

## Statement

**System.** A transform-limited sech pulse, $A(0,T)=\sqrt{P_0}\,\mathrm{sech}(T/T_0)$, is launched into a single-mode silica fibre with anomalous dispersion. The model is the scalar GNLSE in soliton units, $\tau=T/T_0$, $\xi=z/L_D$, $N^2=\gamma P_0T_0^2/|\beta_2|$:
$$\partial_\xi u=\tfrac{i}{2}u_{\tau\tau}+iN^2\,u\big[(1-f_R)|u|^2+f_R\,h*|u|^2\big],\qquad u(0)=\mathrm{sech}\,\tau .$$
The Raman response is Blow–Wood: $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs, so $T_R=f_R\int t\,h\,dt=1.462$ fs. The Raman parameter is $\tau_R=T_R/T_0$.

**Observable.** The leading output soliton is the most red-shifted soliton once fission is complete. Its energy fraction is $f_1=4\eta_1/E$, where:
- $\eta_1$ is the largest Zakharov–Shabat (ZS) eigenvalue of $q=Nu$, windowed around that soliton, with its spectral centroid removed;
- $E=2N^2$.

The inverse-scattering partition gives $f_1^{\rm IST}=(2N-1)/N^2$. The excess is $\varepsilon=f_1/f_1^{\rm IST}-1$, taken where it has saturated in $L$.

**Claim.** For $N=2$–10, including non-integer $N=3.5$:
- **(a) Perturbative law.** As $\tau_R\to0$ at fixed $N$, $\varepsilon\simeq c_N\,\tau_R$, linear on average.
  - Average exponents $d\ln\varepsilon/d\ln\tau_R$ over the smallest-$\tau_R$ decades measured: 1.00 ($N=2$, 800–6400 fs), 1.12 ($N=3$, 800–6400 fs), 1.01 ($N=4$, 800–3200 fs), 1.01 ($N=5$, 1600–6400 fs).
  - $c_2=4.89\pm0.02$, flat to 0.3%; local exponent 1.004 between 3200 and 6400 fs.
  - For $N\ge3$, $c_N$ is **not** monotone in $T_0$. It fluctuates by about ±7%:
    - $c_3=24.2$, 18.6, 16.7, 18.7 at 800, 1600, 3200, 6400 fs;
    - $c_4=78$, 73, 77 at 800, 1600, 3200 fs;
    - $c_5=149$, 140, 148 at 1600, 3200, 6400 fs.

    A plausible cause, not tested, is a dependence on the breather phase at which the bound state splits.
  - Representative values: $c_3\approx18$, $c_4\approx76$, $c_5\approx145$.
- **(b) Maximum.** At fixed $N$, $\varepsilon$ is unimodal in $T_0$. For the Blow–Wood response its maximum sits at
  $$T_0^*\approx(14.2\pm0.9)\,T_R\,N^{1.62}=(1.70\pm0.1)\,\tau_1N^{1.62}\qquad(\text{fit over }N=2\text{–}8,\ \text{max residual }6\%),$$
  i.e. $x^*\equiv N^2T_R/T_0^*=0.094$, 0.107, 0.106, 0.120, 0.129, 0.140, 0.156 for $N=2$, 3, 3.5, 4, 5, 6, 8. For silica, $T_0^*\approx21\,{\rm fs}\,N^{1.62}$. The $N=8$ peak (602 fs) was predicted at 620 fs from the $N=2$–6 fit before it was computed (H3m).
  - The position is **not** set by $T_R$ alone. It tracks $\tau_1$ (the inverse of the Raman gain-peak frequency) across four single-oscillator responses. The $1.7\,\tau_1N^{1.62}$ prediction is compared with the measured peak:
    - Blow–Wood: $N=2$–8, the fit above;
    - $(\tau_1,\tau_2,f_R)=(10,19.5,0.18)$: predicted 101 and 161 fs, measured 100 and 140–200 fs ($N=3,4$; grid estimates);
    - $(16,58.7,0.18)$: predicted 162 and 258 fs, measured 140–200 and 280 fs;
    - an As2S3-like $(15.5,230.5,0.10)$: predicted 156 and 249 fs, measured 160 and 240 fs (held out, H3o).

    The first two have the same $T_R$ as silica; the third has $T_R=0.21$ fs, seven times smaller.
  - In one variable: at every measured maximum, $y^*\equiv N^2\tau_1/T_0^*$ lies in $[0.78,1.30]$. This holds for all $N=2$–8 and all four responses ($y^*=0.78$, 0.89, 0.89, 1.00, 1.08, 1.16, 1.30 for Blow–Wood $N=2$, 3, 3.5, 4, 5, 6, 8, drifting as $N^{0.38}$; 0.87–1.14 for the others).
  - Reading: the transfer is maximal where the bandwidth of the compressed $N$-soliton, $N^2/T_0$, matches the Raman gain-peak frequency $1/\tau_1$ (see Derivation). This form was read off the data after H3k. Its $\tau_1$ dependence was then tested on the held-out As2S3-like response (H3o).
  - The excess falls on both sides: Raman-dominated break-up for $T_0\ll T_0^*$, and the perturbative law (a) for $T_0\gg T_0^*$.
- **(c) Peak content.** The largest leading-soliton fraction over $T_0$ is
  $$f_1^*=(1+\varepsilon^*)\frac{2N-1}{N^2}\approx\frac{1.29}{\sqrt N}.$$
  The measured $f_1^*\sqrt N$ is 1.21 ($N=2$), then 1.27, 1.28, 1.29, 1.29, 1.30, 1.28 ($N=3$, 3.5, 4, 5, 6, 8; peak located on the $T_0$ grid). At single held-out points near their predicted peaks, $N=7$ gives 1.29 ($T_0=500$ fs) and $N=10$ gives 1.27 ($T_0=870$ fs, 65536-point grid, saturated). So for $N=3$–10, $f_1^*\sqrt N=1.27$–1.30.

  This exceeds both the IST value and the bound on input soliton content under any passive mask, $2/N$ (sketch 1 of the card), for every $N\ge3$. For example, $f_1^*(6)=0.529$, against the IST value 0.306 and $2/N=0.333$.

  The peak value depends only weakly on the response. Relative to Blow–Wood, $f_1^*$ changes by:
  - $-1.5$ to $+1.2\%$ for the two same-$T_R$ responses;
  - $-3.6\%$ ($N=3$) and $-4.05\%$ ($N=4$) for the As2S3-like one;
  - $+2.4\%$ ($N=3$, 4) for the multi-component Lin–Agrawal silica response ($f_R=0.245$, boson-peak term with $\tau_b=96$ fs; held out, H3s). Its maxima sit at the Blow–Wood positions ($y^*=0.78$ and 0.98, using $\tau_1=12.2$ fs). At equal peak amplitude, a Gaussian launch gives a peak leading-soliton energy within 4% ($N=4$, exploration) and 2.5% ($N=6$, held out, H3n) of the sech value. So $E_1^*\approx2.58\,N_{\rm peak}^{3/2}$ (soliton units) is nearly launch-shape independent.
- **Corollary (from (b) and (c)), in physical units.** At the optimal duration the leading-soliton energy is
  $$E_1^{\max}=f_1^*\,\frac{2N^2|\beta_2|}{\gamma T_0^*}\approx1.5\,N^{-0.12}\,\frac{|\beta_2|}{\gamma\tau_1}.$$
  It is nearly independent of $N$: it is set by the fibre ($|\beta_2|/\gamma$) and the Raman gain-peak time $\tau_1$.

  **Lab numbers** for SMF-28 at 1550 nm ($|\beta_2|=21.7$ ps²/km, $\gamma=1.3$ /W/km, silica $\tau_1=12.2$ fs). The optimal sech duration is $T_{\rm FWHM}=1.763\,T_0^*$:

  | $N$ | $T_{\rm FWHM}$ | launch energy | leading soliton $f_1^*$ | leading-soliton energy |
  |---|---|---|---|---|
  | 3 | 218 fs | 2.4 nJ | 0.75 | 1.8 nJ |
  | 4 | 347 fs | 2.7 nJ | 0.65 | 1.75 nJ |
  | 6 | 671 fs | 3.2 nJ | 0.53 | 1.7 nJ |

  For comparison, the IST partition gives 1.35, 1.19 and 0.97 nJ. Scanning the laser duration at fixed $N$ (power set by $N$) is predicted to show this maximum.
- **(d) Self-steepening.** With the Kerr prefactor $1+i s\partial_\tau$, $s=1/(\omega_0T_0)$, the energy fraction falls by the quantum-defect factor $(1-sW_c)$, where $W_c$ is the soliton's normalized red shift. The photon-number fraction $f_1/(1-sW_c)$ equals the $s=0$ value of $f_1$:
  - within 1% at $T_0=100$ fs ($N=2$–6);
  - within 0.25% at the transfer maximum, $(4,200)$ and $(6,400)$ fs. There the quantum defect removes up to 17% of the energy.

## Sharpened statement (cross-family, gpt-c, 2026-10-17)

**Verdict: refuted as submitted; the following finite numerical approximation
survives.** The submitted Statement and Derivation are retained unchanged.
In the deterministic BW/sech reference model,
$$f_1^*\simeq\frac{1.29}{\sqrt N}\quad(N=3,\ldots,10),\qquad
T_0^*\simeq21\,{\rm fs}\,N^{1.62}\quad(N=3,\ldots,16).$$
Here $f_1^*$ denotes a bracketed local duration maximum of the resolved,
reddest soliton's ZS energy share at the specified finite output checkpoint.
It is not a proved global maximum or an infinite-length limit. The sampled
reference peak brackets have $7.1\times10^{-4}\le\tau_R\le1.3\times10^{-2}$,
$0.80\le y=N^2\tau_1/T_0\le1.84$ and $1.4\le zN/L_D\le8$,
with $f_R=0.18$, $\tau_2/\tau_1=32/12.2$, and $s=\delta_3=\alpha L=0$.
These bounds describe the tested points, not every point of a continuous box.

Run `2026-10-17-gpt-c-raman-sharpening` measures every integer order 3–16.
The scaled share rises from approximately 1.267 at N=3 to 1.295 at N=5,
then falls to 1.222 at N=16. Its per-order numerical resolution envelopes,
duration brackets and output checkpoints are in the run's `tables.md`.
Over N=3–10, the numerical envelopes stay within 2.1% of the coefficient
1.29; this is a finite sampled accuracy statement, not an asymptotic remainder.
Thus a constant scaled share is useful at small order but is not established
as a large-order limit. The finite-range duration exponent is about 1.62;
regression-residual intervals and the larger full-bracket sensitivity are
reported separately in `final_position.json`. No constant $y^*$ fits all
measured duration brackets; a later large-N limit remains open.

The BW scans at N=9,11,13,15 were held out from the coefficient freeze
`abe44ab382621ff706ca234ac7bac8fca06d6b02`. Scaled-share predictions pass
including their numerical envelopes. All four full duration brackets also
pass the frozen 5% position tolerance, as scored in `final_metrics.json`;
no heldout point refits the guide. The plotted drift curve is a descriptive interpolation,
not a new asserted physical law or a controlled asymptotic expansion.

At equal peak-based order and separately optimized duration, HC lowers the
share by about 0.9–2.3% and the As-like response by about 3.5–6.4% over
the tested orders. Gaussian shares rise by about 7–12%, but after the
different launch norms are included the normalized leading energies differ
by about 0.6–4.9%. This does not establish equal-energy/FWHM/length shape
universality. The multi-mode HC response has no unique $\tau_1$; figures
use an explicitly declared 12.2 fs reference time.

The energy-maximum corollary remains false, since at fixed N
$$E_1=\frac{2N^2|\beta_2|}{\gamma T_0}f_1,
\qquad E_1'\big|_{f_1'=0}=-E_1/T_0<0.$$
The specified realistic SMF-28 model (published dispersion including
$\beta_3$, HC, shock, uniform loss) gives local-ZS efficient-point energies
about 1.44–1.46 nJ for N=3,4,6. Directly gated energy and photon fractions
are reported separately, with output length and spectral support. A fixed
3 nJ input, 10 kW peak limit and 2 m output gives a best resolved sampled
gated energy of 1.811 nJ; this is not a certified continuous optimum.

The proposed new exit-width rule fails: the converged BW N=4 near-optimum
fitted width is 21.323 fs, versus an overlap maximum of 15.558 fs. The
per-response width comparisons also fail at high order. No selection-rule
claim is filed. A controlled fission-law remainder, uniform long-pulse
$c_N$ coefficients and global/unbounded-order statements remain unproved;
therefore status stays **refuted**, rather than sim-verified or audited.

See the [2026-10-17 report](notes/audit-2026-10-17-gpt-c-C-20261016-claude-a-02.md)
and [PI summary](../docs/summary-2026-10-17-gpt-c-C-20261016-claude-a-02.md).
All numerical statements in this section cite run
`2026-10-17-gpt-c-raman-sharpening`; its source ledger records literature
access and the physical-model dispersion reference.

## Regime

The governing scope is the 2026-10-17 sharpened statement above. The earlier
audit restrictions below are retained with their original run and date.

**Cross-family audit restriction, 2026-10-16 (gpt-c, gpt).** The bundled
claim is refuted because the physical-units corollary is not an energy
maximum. Its dimensional value is **energy at a share-optimal operating
point**, $E_{1,\mathrm{eff}}$, with output distance and model specified. The
submitted Statement and Derivation are retained as the record of the claim.

The following narrower empirical content survives the independent checks:

- Constant-beta2, scalar, deterministic TL-sech/BW model with $s=0$ and no
  loss. Near-peak scans cover $N=2,3,4,4.5,5,6,8$; $N=7,10$ are individual
  near-peak checks. The duration-position fit is checked for $N=2,3,4,5,6,8$,
  with $y^*\in[0.797,1.262]$. The corresponding measured peak fractions are
  consistent with the approximate $1.29/\sqrt N$ law for $N\ge3$. These are
  finite scans, not a proof of global unimodality. Accepted checkpoints
  require resolved leading-pulse scattering and explicit edge diagnostics.
- The $N=12,16$ frozen central points pass the wider $\sqrt N f_1\in[1.20,1.38]$
  interval on a finer grid. They do not extend the tighter small-N constant
  or the physical SMF-28 interpretation to arbitrary N.
- For $N=2$, $\tau_R\in[2.28\times10^{-4},1.83\times10^{-3}]$, the independent
  excess exponent is about 1.007. Weak late edge radiation and the clean-only
  fit are reported separately. A pointwise constant coefficient with relative
  remainder $O(\tau_R)$ is not established for $N\ge3$; the broader submitted
  statement of that remainder is not endorsed.
- The physical efficient-point comparison is conditional on the published
  dispersion fit, HC Raman, constant $\gamma_0$, shock and uniform loss, at
  $N\in\{3,4,6\}$ and $zN=4$. The sampled points have
  $\tau_R^{HC}\in[0.00657,0.01896]$, $s\in[0.00219,0.00633]$,
  $\delta_3\in[0.00275,0.00796]$ and $\alpha L\le2.15\times10^{-4}$.
  Their efficient-point energy is about 1.44-1.46 nJ under local interpolation,
  with explicit duration brackets in the audit. No absolute energy ceiling
  is asserted. Wavelength-dependent mode area and spool calibration remain open.

The numerical evidence and limitations are in
[the independent audit](notes/audit-2026-10-16-gpt-c-C-20261016-claude-a-02.md),
run `2026-10-16-gpt-c-raman-audit`.

### Submitted regime (superseded; retained)

- $N\in[2,10]$: integers 2–8, $N=3.5$ and $N=10$. $N=7$ only at $T_0=500$ fs; $N=8$ at 200, 400, 450, 600 and 800 fs; $N=10$ only at 870 fs.
- $\tau_R=T_R/T_0\in[2.3\times10^{-4},5.8\times10^{-2}]$, i.e. $T_0=25$–6400 fs with silica Raman. Equivalently $x=N^2\tau_R\in[9\times10^{-4},1.05]$.
- Small parameter of (a): $\tau_R$, with the relative error $O(\tau_R)$. The measured local exponents approach 1 (values under Checks).
- $L$ beyond saturation. Saturation means $\varepsilon$ changes by less than 5% between successive $L\in\{2.5,3,4,6,8,16,32,64,128\}/N\cdot L_D$. It is reached by $L=3$–$4/N$ for $x\gtrsim0.02$ and needs up to $L=128/N$ for $N=2$ at $T_0=6400$ fs.
- $\beta_3=0$, $s=0$ and no loss define the model of the statement. Item (d) and the relaxed-assumption checks give the size of the changes.
- The red shifts the model produces after fission are large and outside the validity of a constant-$\beta_2$, single-oscillator silica model. In normalized frequency they reach about 340 at $N=8$, $T_0=800$ fs, $L=4L_D/N$ (0.43 rad/fs), and 650 at $N=10$, $T_0=870$ fs, $L=3L_D/N$ (0.74 rad/fs). The excess is already saturated much earlier: at $L=2.5L_D/N$ for $N=8$, where the shift is about half its $L=4L_D/N$ value, and at $L=2L_D/N$ for $N=10$. The shift at which saturation sets in was not measured.
- **Grid requirement.** For $N\ge7$ the leading soliton reaches the Nyquist edge of a 16384-point grid over $160T_0$ by $L=4/N$, and is then aliased (diagnostic `h3_peaks_N8_T400.json`). $N\ge7$ values are taken from 32768-point runs only (65536 for $N=10$).

## Assumptions

1. Scalar, single-mode, single-polarization field.
2. Dispersion $\beta_2$ only; $\beta_3=0$ in the statement. Relaxed: $\delta_3=\beta_3/(6|\beta_2|T_0)\in\{0.02,0.05\}$ (see Checks).
3. Frequency-independent $\gamma$; no self-steepening in (a)–(c). Relaxed in (d).
4. Raman response: Blow–Wood ($f_R=0.18$) for the statement. For response tests:
   - two same-$T_R$ single-oscillator variants (H3k);
   - an As2S3-like response with $f_R=0.10$, $\tau_2=230.5$ fs (H3o);
   - the multi-component Lin–Agrawal response (H3s).

   Hollenbeck–Cantrell was untested in the submitted work; the independent
   2026-10-17 tests and their limits are recorded in the sharpening section.
5. No loss, no gain, no noise (deterministic propagation).
6. Transform-limited sech launch. Shaped launches are claim C-20261016-claude-a-04.
7. Leading-soliton identification by the tallest peak, with ZS measurement on a window of half-width $\max(6/|q|_{\max},1)\,T_0$. Each row is checked with:
   - $|\mathrm{Re}\,\zeta_1|<0.05$;
   - windowed energy $\approx4\eta_1$;
   - photon-number drift $<10^{-4}$;
   - no window or Nyquist limit.

   Rows failing any check are excluded. The per-peak census at $N=8$ showed that the tallest peak can differ from the reddest soliton when the latter is aliased. That is why the $N\ge7$ grid requirement above exists. On the grids used, the census confirms that the tallest peak is the reddest soliton at $(5,280\,{\rm fs})$ and $(6,400\,{\rm fs})$ (`h3_peaks_N5_T280.json`, `h3_peaks_N6_T400.json`).
8. Periodic time window.

## Predictions

Frozen in `runs/2026-10-16-claude-a-raman-soliton-frontier/HYPOTHESES.md` before the corresponding computation. The commits are:
- 3af8dfa: H3a–d;
- 94bd1ac: H3e;
- d11ec48: H3f;
- 5628392: H3g;
- fa39dd9: H3h;
- 3a4a64a: H3i;
- 73e23c6: H3j;
- 99ab7d9: H3k;
- c2e18dc: H3m;
- 2f0357e: H3n;
- 995962c: H3o and H3p ($c_5$ was first frozen in this card at ec14071);
- 4a74fe8: H3q;
- 047c44d: H3r;
- 81518cc: H3s.

Outcomes:

| Frozen prediction | Outcome | Run file |
|---|---|---|
| H3a: excess $>0$ for all $N\ge2$ once fission is complete | confirmed: all 70 $(N,T_0)$ points | `h3_summary.json` |
| H3b: excess linear in $\tau_R$, exponent $1.0\pm0.25$, as a global law | **refuted**: $\varepsilon$ is non-monotone in $T_0$; holds only for $T_0\gg T_0^*$ | `h3_main`, `h3_dense` |
| H3c: monotone in $N$ at $T_0=50$ fs | **refuted**: $\varepsilon(3)=0.207>\varepsilon(4)=0.199$ | `h3_main` |
| H3d: saturates between $L=4/N$ and $8/N$ | confirmed where fission is complete; for $N=2$ at $T_0\ge400$ fs saturation needs $L\ge16/N$ | `h3_main`, `h3_small`, `h3_n2long` |
| H3e: $\varepsilon(5,200\,{\rm fs})\in[0.40,0.62]$ | confirmed: 0.562 | `h3_heldout` |
| H3e: $\varepsilon(5,100\,{\rm fs})\in[0.30,0.50]$ | confirmed: 0.381 | `h3_heldout` |
| H3e: $\varepsilon(6,800\,{\rm fs})\ge0.55$ | **refuted**: 0.465 | `h3_heldout` |
| H3e: $\varepsilon(8,800\,{\rm fs})\in[0.6,1.2]$ | confirmed: 0.879 (32768-point grid) | `h3_n8fine` |
| H3f(i): $N=3,4$: $\varepsilon\to0$ with local exponent in $[0.8,1.4]$ (1600 to 3200 fs) | confirmed: 1.16, 0.92 | `h3_small` |
| H3f(ii): $N=2$, linear law against a finite limit | confirmed: exponents 0.99, 1.04, 1.004 | `h3_small`, `h3_n2long`, `h3_conv_small` |
| H3f(iii): $x^*$ equal for $N=2$–5 within factor 1.6 | confirmed: 0.094–0.129, ratio 1.38 | `h3_summary.json` |
| H3f(iv): $\varepsilon^*(5)\in[0.50,0.75]$ | confirmed: 0.608 | `h3_dense`, `h3_n5peak` |
| H3g(i): $\varepsilon(5,340)>\varepsilon(5,200)$ and $>\varepsilon(5,560)$ | confirmed: 0.595 against 0.562 and 0.422 | `h3_n5peak`, `h3_heldout`, `h3_dense` |
| H3g(ii): $f_1^*(5)\sqrt5=1.30\pm0.09$ | confirmed: 1.294 | `h3_dense` |
| H3g(ii): $f_1(8,800\,{\rm fs})\in[0.40,0.50]$ | confirmed: 0.4405 | `h3_n8fine` |
| H3g(iii): $c_4\in[25,60]$ | **refuted**: $c_4=73$–78 | `h3_small`, `h3_conv_small` |
| H3h: photon fraction with self-steepening within 1% of the $s=0$ value, $N=4,6$ | confirmed: $+0.17\%$, $-0.93\%$ | `h3_relaxed` |
| H3q: same within 1.5% at the transfer maximum, $(4,200)$ and $(6,400)$ fs | confirmed: $-0.05\%$, $-0.23\%$ | `h3_sspeak` |
| Verifier prediction (frozen in this card at aa10039), tested by me: $f_1^*\sqrt N\in[1.20,1.38]$ for $N=10$ at $T_0$ within 15% of $21\,{\rm fs}\,N^{1.62}$ | confirmed: 1.269 at 870 fs | `h3_n10` |
| H3r: $c_3(6400\,{\rm fs})\in[14.0,16.5]$, $c_5(6400\,{\rm fs})\in[118,140]$ | **refuted**: 18.7 and 147.6; $c_N$ is non-monotone in $T_0$ | `h3_c35` |
| H3s: Lin–Agrawal response, $f_1^*\sqrt N\in[1.20,1.38]$ ($N=3,4$) | confirmed: 1.297, 1.319 | `h3_lin` |
| H3i(i): $f_1(7,500\,{\rm fs})\in[0.46,0.52]$ | confirmed: 0.4877 (32768-point grid, saturated) | `h3_n7fine` |
| H3i(ii): $\varepsilon(6,560\,{\rm fs})\ge0.66$ | **refuted** (narrowly): 0.647 | `h3_n7` |
| H3j: $N=3.5$: peak $f_1\in[0.653,0.737]$, at $T_0^*\in[120,200]$ fs | confirmed: 0.684 at 170 fs | `h3_n35` |
| H3k: same-$T_R$ responses move $T_0^*$ by less than 10% (null hypothesis "$T_R$ only") | **refuted**: $T_0^*$ moves by $-30$ to $+45\%$, roughly with $\tau_1$ | `h3_rshape` |
| H3k: and $f_1^*$ by less than 3% | confirmed: $-1.5$ to $+1.2\%$ | `h3_rshape` |
| H3m(i): $f_1(8,600\,{\rm fs})\in[0.43,0.49]$ | confirmed: 0.4539 (32768-point grid, saturated) | `h3_n8peak` |
| H3m(ii): $f_1(8,600)>f_1(8,800)$ and $>f_1(8,450)$ | confirmed: 0.4539 against 0.4405 and 0.4399 | `h3_n8peak`, `h3_n8fine` |
| H3n: Gaussian launch, peak 6 (held out): $E_1^*=4\eta_1\in[34.5,39.5]$ | confirmed: 37.11 at 380 fs (sech: 38.07) | `h3_gauss6` |
| H3p: $c_5=\varepsilon(5,3200\,{\rm fs})/\tau_R\in[150,600]$ (frozen in this card at ec14071) | **refuted** (narrowly): 139.7, saturated in $L$ | `h3_c5` |
| H3o: As2S3-like response, peak $f_1$ within 4% of Blow–Wood ($N=3$, 4) | $N=3$ confirmed ($-3.6\%$); $N=4$ **refuted** narrowly ($-4.05\%$). A finer $T_0$ grid does not change either | `h3_as2s3`, `h3_as2s3fine` |
| H3o: peak $T_0$ within a factor 1.5 of $1.7\tau_1N^{1.62}$ (156, 249 fs) | confirmed: 160, 240 fs | `h3_as2s3`, `h3_as2s3fine` |

**Predictions for a verifier, not computed by me:**
- $f_1^*(N)\sqrt N\in[1.20,1.38]$ for $N=12$ and 16, at $T_0$ within 15% of $21\,{\rm fs}\,N^{1.62}$. $N=10$ was checked by me (1.269). Use at least 65536 points over $160T_0$.
- With the Hollenbeck–Cantrell response, $f_1^*\sqrt N$ stays in $[1.20,1.38]$ for $N=3$–6. Lin–Agrawal was checked by me for $N=3,4$ (H3s). A pure time rescaling of $h$ only rescales $T_0$, so it is not a test.
- The excess at fixed $(N,T_0)$ is independent of $\beta_2$ and $\gamma$, by soliton scaling.
- For any single-oscillator response (other $\tau_1$, $\tau_2$, $f_R$), the maximum over $T_0$ lies at $y^*=N^2\tau_1/T_0^*\in[0.7,1.4]$ for $N=3$–6.

## Derivation

**Mechanism.** Energy conservation of the Raman GNLSE without self-steepening is exact: $\int|u|^2$ is constant. An isolated soliton keeps $\eta$ to first order under Raman. Hence $\eta_1$ can grow only by taking energy from the other fission products while they overlap: interpulse Raman gain, as in Kormokar et al. 2023 and in Luan et al. 2006.

**(a) Exponent 1.** Take two overlapping solitons separating under differential Raman acceleration $a\propto\tau_R$. Their frequency difference grows as $\Delta\Omega=a\xi$. The interpulse Raman gain rate is $\propto\tau_R\Delta\Omega$ for $\Delta\Omega$ below the Raman gain peak. The overlap ends when the accumulated delay $\int\Delta\Omega\,d\xi$ reaches a soliton width. The transferred energy is therefore
$$\propto\tau_R\int\Delta\Omega\,d\xi\propto\tau_R\times(\text{width}),$$
independent of how slowly they separate. This gives exponent 1. A transfer rate that did not grow with $\Delta\Omega$ would instead give $\varepsilon\propto\tau_R\,\xi_{\rm sep}\propto\tau_R^{1/2}$, which the data exclude: the measured exponent is 1.004 for $N=2$. The coefficients $c_N$ are not derived. They grow faster than any single power of $N$ over 2–4.

**(b) Position of the maximum: spectral matching to the Raman gain peak.** At its first compression, the integer-$N$ sech soliton has peak amplitude $\sum_k(2N-2k+1)=N^2$ and bandwidth $\sim N^2/T_0$. The fission products separate in frequency on that scale.
- Interpulse Raman gain is largest at frequency separations near the gain peak, $\Omega_R\approx1/\tau_1$ (13 THz for silica).
- Matching the two gives $T_0^*\propto\tau_1N^p$ with $p\approx2$. This explains why $T_0^*$ follows $\tau_1$ across four responses whose $T_R$ differs sevenfold.
- For $T_0\gg T_0^*$ the products overlap only on the low-frequency, linear-in-$\Omega$ flank of the gain, which gives the perturbative law (a). For $T_0\ll T_0^*$ the products overshoot the gain peak and Raman acts before the integrable fission.

The measured exponent is $p=1.62$, not 2. Neither this nor the prefactor 1.7 is derived. An earlier heuristic, $x=N^2T_R/T_0$ (the shift acquired over a fission length relative to the bandwidth), gives the scale for silica but not the $\tau_1$ dependence.

**(c)** $f_1^*\propto N^{-1/2}$ is empirical. No derivation.

**(d) Self-steepening.** Self-steepening makes the Raman process conserve photon number, $\sum|\tilde u|^2/(1-sW)$ in the numpy sign convention, instead of energy. A soliton at normalized red shift $W_c$ carries energy $(1-sW_c)$ times its photon number. The photon fraction is unchanged within 1%, so to this accuracy self-steepening does not alter the interpulse transfer.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Soliton units; $T_R$, $\omega_0$ and $\beta_2$ only through $\tau_R$, $s$ and $N$ | claude | — | 2026-10-16 |
| Known limits | Raman off: $\varepsilon=+0.0001$, $+0.0023$, $-0.0009$, $-0.0010$, $-0.0085$ for $N=2,3,4,6,8$ (window truncation of the unsplit breather). $\varepsilon\to0$ linearly as $\tau_R\to0$ | claude | `2026-10-16-claude-a-raman-soliton-frontier` (`h3_main`, `h3_small`, `h3_conv_small`) | 2026-10-16 |
| Symmetries | Photon number (energy for $s=0$) conserved to $\le10^{-6}$ on accepted rows ($\le7\times10^{-5}$ for $N=2$ at the base step). $\mathrm{Re}\,\zeta_1\approx0$ on accepted rows | claude | same | 2026-10-16 |
| Symbolic residual | — | | | |
| Simulation, core regime | 70 $(N,T_0)$ points, $N=2$–10 (Blow–Wood); 106 points in total with the other responses. Collapse plot of $f_1\sqrt N$ against $y=N^2\tau_1/T_0$ | claude | same (`h3_summary.json`, `h3_excess.png`, `h3_collapse.png`) | 2026-10-16 |
| Error-scaling exponent | Local $d\ln\varepsilon/d\ln\tau_R$: $N=2$: 0.99, 1.04, 1.004 (800–6400 fs); $N=3$: 1.41, 1.38, 1.16, 0.84 (400–6400); $N=4$: 1.10, 0.92 (800–3200); $N=5$: 1.10, 0.92 (1600–6400). Average over the range: 1.00, 1.12, 1.01, 1.01 | claude | `h3_small`, `h3_n2long`, `h3_conv_small` | 2026-10-16 |
| Held-out region | Held out: $N=5$, 7, 8, 10 and 3.5. Confirmed: H3e (3 of 4), H3g(i–ii), H3i(i), H3j. Refuted: H3e(6,800), H3i(ii) | claude | `h3_heldout`, `h3_n5peak`, `h3_n7fine`, `h3_n8fine`, `h3_n35` | 2026-10-16 |
| Convergence and artefacts | $(4,200\,{\rm fs})$: $\varepsilon=0.47236$ under $dt/2$, $h/2$ and window $\times2$. $(6,400)$: 0.728526 under all three. $(8,200)$: 0.57375 under all three. Small $\tau_R$: $h/2$ and $h/4$ agree to $10^{-5}$ in $\varepsilon$ ($N=2,3,4$). $N\ge7$: aliasing found and excluded (see Regime) | claude | `h3_conv`, `h3_conv_small`, `h3_peaks_N8_T400.json` | 2026-10-16 |
| Second solver or relaxed assumption | FastDifferentiableMMNLO (agents' copy b9fa957, Agarwal Raman, self-steepening built in) against numpy RK4IP with $s=1/(\omega_0T_0)$: $f_1$ agrees to $2\times10^{-4}$ $(3,100)$, $8\times10^{-4}$ $(4,200)$ and $2.2\times10^{-4}$ $(6,400)$, the last on the transfer maximum with a 32768-point grid. Self-steepening: (d). $\beta_3$: content measured with the local dispersion $1+6\delta_3W_c$ rises by $+1.6$ to $+11\%$ at $\delta_3\le0.05$ ($N=2$–4, $T_0=100$ fs); the nominal-$\beta_2$ ZS content is not the soliton content there | claude | `solver_check.json`, `solver_check2.json`, `h3_relaxed`, `h3_beta3.json` | 2026-10-16 |
| Adversarial audit | **Fail as written:** share-optimal energy is not an energy maximum. Empirical surviving scope is restricted above; see the independent report for unresolved assumptions. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit` | 2026-10-16 |
| Novelty search | Kormokar, Shamim & Rochette (2023) predict and measure the excess but give no maximum in $T_0$, collapse variable, small-$\tau_R$ law or $N^{-1/2}$ law in the text read (figures not viewed). Their $N=6$, $T_{\rm FWHM}=700$ fs value (53.0%) matches $f_1(6,400\,{\rm fs})=52.8\%$ here. Sources and access levels are in the log | claude | — | 2026-10-16 |
| Novelty search, independent | Items (a)–(d) of the PI brief are **partly published**: first-order collision transfer (Chi–Wen, DOI 10.1364/OL.14.001216); duration turnover and close peak shares (Kormokar, DOI 10.1364/JOSAB.478975); silica response-overlap width near the inferred efficient-point width (Judge, DOI 10.1364/JOSAB.26.002064; Pant, DOI 10.1364/JOSAB.27.001894). All **full text**. High confidence in those antecedents; exact fixed-N scaling/selection and universality not found, moderate confidence. Energy at the share optimum is not an energy ceiling. Here (d) means the energy corollary, not this card's self-steepening item. See [review](../docs/review-2026-10-16-gpt-b-raman-transfer-energy-novelty.md) for digitisation, access limits and mechanism caveats. | gpt-b (gpt; gpt-6-astra) | `2026-10-16-gpt-b-raman-literature` | 2026-10-16 |
| Independent units and optimality | Fail for the energy maximum: at a positive share maximum, $E_1'=-E_1/T_0$. At fixed $N=3$ and 1.3 m, the realistic-dispersion/HC model gives 2.2308 nJ at 80 fs versus 1.8779 nJ at 100 fs; the wider-window comparison is clean and has strong spectral support. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit`; `conv_wide_measured_N3_T80_fixed130cm`, `measured_hc_s1_N3_T100_fixed130cm` | 2026-10-16 |
| Independent known limits | Exact sech/chirped-sech ZS calibration, fundamental NLSE propagation, and the Gordon moment sign and factor pass. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit`; `calibration.json`, `physics_calibration.json` | 2026-10-16 |
| Independent core and held-out checks | Peak-location fit and peak-share trend reproduce. Own $N=4.5$ held-out point passes; $N=12,16$ and HC verifier intervals pass at the resolved candidate points. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit`; `summary.json`, `frozen_checks.json` | 2026-10-16 |
| Independent weak-Raman exponent | Predicted exponent 1; $N=2$: 1.00648 using clean checkpoints, 1.00733 with late saturation diagnostics. $N=4$: approximately 1.16 over the extended finite range; a controlled pointwise remainder is not established. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit`; `asym_diagnostics.json`, `summary.json` | 2026-10-16 |
| Independent convergence and extraction | Separate grid, window, step and shooting-mesh checks; retained aliasing failures. Matched-response second-solver full-field relative difference $2.13\times10^{-7}$. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit`; `quality_metrics.json`, `extraction_checks.json`, `library_comparison.json` | 2026-10-16 |
| Independent physical efficient point | Published full dispersion, HC, shock and loss preserve a weakly N-dependent efficient-point scale, about 1.44-1.46 nJ in the specified model. Shorter fixed-N inputs give more energy. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit`; `regime_metrics.json`, `summary.json` | 2026-10-16 |
| Independent shock observable | The card's unscaled ZS proxy reproduces its 0.25% tolerance. Direct gated photon fractions change by 0.46% and 0.60% at the two peak cases; the physical sub-1% statement survives. | gpt-c (gpt) | `2026-10-16-gpt-c-raman-audit`; `shock_measurement.json` | 2026-10-16 |
| Independent sharpening, all integer orders 3–16 | Bracketed local peaks show scaled-share drift; the original 1.29 coefficient is a useful small-order approximation. Frozen BW heldouts and their resolution envelopes are scored separately from descriptive post-test fits. Every response/shape peak has neighbors on both sides. | gpt-c (gpt; gpt-6-astra) | `2026-10-17-gpt-c-raman-sharpening`; `tables.md`, `final_metrics.json`, `final_position.json` | 2026-10-17 |
| Independent overlap-selection attack | Proposed exit-width equality fails, including the converged BW near-optimum case and high-order response cases. The isolated-sech overlap expansion has a cubic remainder; this is not the fission-law remainder. Phase 2 records the failed null and a separate material extrapolation on new proposer card C-20261017-gpt-c-01. | gpt-c (gpt; gpt-6-astra) | `2026-10-17-gpt-c-raman-sharpening`; `overlap.json`, `accuracy.json`, `derivation.md` | 2026-10-17 |
| Independent physical objectives | Share, energy at the share optimum, fixed-resource best-found energy and integrated photon fractions are distinct. Refined efficient-energy resolution intervals lie inside the frozen 1.35–1.55 nJ test interval. The constrained continuous maximum remains unproved. | gpt-c (gpt; gpt-6-astra) | `2026-10-17-gpt-c-raman-sharpening`; `tables.md`, `final_metrics.json` | 2026-10-17 |
| Independent numerical controls | Fixed-step field convergence approaches order four; matched Python/Julia full-field difference is about 5.05e-14. Grid, window, shooting and kernel checks are tabulated independently; failed and unrun cases remain in the execution inventory. These numerical orders do not certify a physical asymptotic remainder. | gpt-c (gpt; gpt-6-astra) | `2026-10-17-gpt-c-raman-sharpening`; `accuracy.json`, `kernel_validation.json`, `inventory.json` | 2026-10-17 |
| Material extrapolation, proposer tests on new card | C-20261017-gpt-c-01 is refuted by its GPT proposer: all four frozen ZBLAN duration predictions fail, physical scaled shares fail at N=5,6, and both exit-width nulls fail at all physical orders. All eight peaks are bracketed and numerical controls pass. This tests a new gain-peak rescaling, not an independently verified extension of the silica law; Claude verification is T-20261017-gpt-c-05. | gpt-c (gpt; gpt-6-astra) | `2026-10-17-gpt-c-zblan-transfer`; `summary.json`, `tables.md`, `accuracy.json` | 2026-10-17 |
| Novelty search, phase 2 | Selection rule, peak share, peak position and efficient-point energy are each **partly published**: high confidence for their known ingredients, medium confidence that the exact fixed-N laws and exit-width equality were **not found**. Closest sources: Kormokar DOI 10.1364/JOSAB.478975 / arXiv:2301.02945 (full text, selected sections); Judge DOI 10.1364/JOSAB.26.002064 and Pant DOI 10.1364/JOSAB.27.001894 (abstract only here; gpt-b full-text findings attributed); Al-kadry DOI 10.1364/JOSAB.29.001347 (article abstract, associated thesis full text selected chapter). Extended tellurite/fluoride/thesis search and access limits: [review](../docs/review-2026-10-17-gpt-c-raman-peak-novelty.md). No novelty is inferred from a failed prediction. | gpt-c (gpt; gpt-6-astra) | `2026-10-17-gpt-c-zblan-transfer`; `search_log.md`, `SOURCES.md` | 2026-10-17 |

## Outcome

**Current outcome (2026-10-17): refuted.** The narrowed finite peak laws survive the independent tests, but the energy maximum and new exit-width selection hypothesis fail. Phase 2 files C-20261017-gpt-c-01 for a separately frozen measured-response ZBLAN extrapolation and the failed selection null. That new conjunction is refuted by GPT proposer tests; independent Claude verification remains open.

**Submitted intermediate outcome (retained):** Parts refuted on the way: H3b as a global law, H3c, H3e at $(6,800)$, H3g(iii) ($c_4$), H3i(ii), H3k (peak position with $T_R$ alone), H3o at $N=4$ (peak value, by 0.05%), H3p ($c_5$) and H3r (monotone $c_3$, $c_5$). These narrowed the claim to the statement above.

## Audit trail

| Date | Agent / model / family | Change and evidence |
|---|---|---|
| 2026-10-16 | gpt-c / gpt-6-astra / gpt | Cross-family audit: `proposed` → `refuted`. The fixed-N energy-ceiling/duration-scan maximum fails in run `2026-10-16-gpt-c-raman-audit`; the corollary is interpretable only as energy at a specified share-optimal operating point. The submitted regime $N\in[2,10]$, $\tau_R\in[2.3\times10^{-4},5.8\times10^{-2}]$, $x\in[9\times10^{-4},1.05]$ with a controlled relative $O(\tau_R)$ remainder is superseded by the restrictions above. Original regime bullets, Statement and Derivation are retained. Peak-share, peak-location and selected verifier predictions reproduce, but do not rescue the energy maximum or certify a universal physical ceiling. The report records all exclusions, unperformed checks and follow-up work. |
| 2026-10-16 | gpt-c / gpt-6-astra / gpt | After independent verdict commit `143cc58`, read the delegated novelty review in PR #52 and completed further controls in the same independent run. The clean 1.3-m, 80-fs counterexample strengthens spectral support; refined peak brackets preserve the position fit; the extended N=4 coefficient drop survives grid, window, integration and saturation checks. The report separates these later controls and attributed literature findings from the independent verdict. Status remains `refuted`. |
| 2026-10-17 | gpt-c / gpt-6-astra / gpt | Cross-family sharpening in run `2026-10-17-gpt-c-raman-sharpening`: preserved the submitted Statement and Derivation, resolved finite-order peak-share drift through N=16, bracketed peaks and tested frozen heldouts, separated physical energy and photon objectives, and rejected the proposed exit-width selection rule. Status remains `refuted`; the numerical peak fits have no controlled physical remainder. See the dated audit, PI summary and execution inventory. |
| 2026-10-17 | gpt-c / gpt-6-astra / gpt | Phase 2: extended the novelty audit to material optimization and theses; all four broad ingredients are partly published, while exact fixed-N/exit-width laws were not found with medium confidence. New card C-20261017-gpt-c-01 records a frozen measured-response ZBLAN extrapolation, refuted by proposer tests in `2026-10-17-gpt-c-zblan-transfer`. Original status remains `refuted`; Statement and Derivation remain unchanged. |
