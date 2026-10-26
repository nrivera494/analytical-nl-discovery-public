# Frozen hypotheses for T-20261016-claude-interactive-04 (P-20261016-claude-interactive-02)

Agent claude-interactive.6 (family claude, model claude-opus-5-5). Written 2026-10-16, about 12:15 EDT, **before any production run.**

**Pilot runs seen before freezing.** These were used to choose regimes and are not tests:
- a 2 m numpy run of a transform-limited (TL) sech launch, $N=3$, $T_0=56.7$ fs, in the SMF-28 model: photon drift, the dissipation identity, monotone mean;
- the same launch at $L=0.5$ and 1 m, for photon fractions beyond 1.65–1.90 µm;
- reduced-model runs for isolated solitons in SMF-28, InF₃ and ZrF₄.

The reduced-model predictions below are in `runs/2026-10-16-claude-interactive.6-lwir-predictions/predictions.json`, produced by `predict.py` in the same folder, committed with this file.

## Common model and fibres (assumption ledger, shared by every hypothesis)

**Model.**
- Scalar single-mode GNLSE in a retarded frame, with the full $\beta(\omega)$ of the LP01 mode.
- Kerr term with the shock (self-steepening) factor $\omega/\omega_0$.
- Raman: a single damped oscillator, $h(t)\propto e^{-t/\tau_2}\sin(t/\tau_1)$.
- Loss: power loss $\alpha(\omega)$.
- Input: deterministic. No noise, no polarization, no higher-order modes.
- The nonlinearity has three forms:
  - `const`: constant $A_{\rm eff}$, as in the agents' Julia solver;
  - `naive`: $\gamma(\omega)=n_2\omega/(cA_{\rm eff}(\omega))$ as a plain prefactor;
  - `pc`: the photon-conserving form with $A_{\rm eff}(\omega)^{-1/4}$ on the field and on the prefactor (Laegsgaard's form).

**Fibres.** Step-index LP01, weakly guiding (scalar), with core index $n_1^2=n_2^2+{\rm NA}^2$.
- Cladding glasses use the two-term Sellmeier fits of Boilard, Vallée & Bernier, arXiv:2109.13366, Table 2 (full text).
- **S28 (silica).** Core 8.2 µm, NA 0.14 (SMF-28 as listed in Boilard Table 1).
  - Model values: $\beta_2(1.55)=-21.9$ ps²/km, ZDW 1.302 µm, $A_{\rm eff}(1.55)=64.5$ µm².
  - $n_2=2.6\times10^{-20}$ m²/W.
  - Raman: $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs, as used by Kormokar, Shamim & Rochette, JOSA B 40, 412 (2023), DOI 10.1364/JOSAB.478975, arXiv:2301.02945 (full text). The model's own $T_R=f_R\int t\,h=1.46$ fs.
  - IR edge: $\alpha=7.81\times10^{11}e^{-48.48/\lambda}$ dB/km. This is a secondary source (a course note); the primary source was not located.
- **Z75 (ZrF₄).** Core 7.5 µm, NA 0.30.
  - $n_2=2.1\times10^{-20}$ m²/W, assumed (a typical ZBLAN value, **not sourced** this session).
  - Raman: a single-oscillator stand-in, $f_R=0.20$, $\tau_1=20.9$ fs, $\tau_2=53$ fs. It is built from the broad 7.63 THz, 5.98 THz-wide component of the InF₃ fit in Gauthier et al., Sci. Rep. 12, 15898 (2022), DOI 10.1038/s41598-022-19658-8 (full text via PMC; $f_R=0.20$ from the same source). This is an approximation.
  - Edge: $\alpha=A e^{-B/\lambda}$, with 1 dB/m at 4.2 µm for ZrF₄ fibre (Gauthier 2022). The slope $B=92$ µm is **assumed**, scaled from silica's $B$ by the phonon-energy ratio.
- Pump wavelengths: 1.55 µm for S28, 2.8 µm for Z75.

**Definitions.**
- $\mathcal N$ is the photon number $\sum_k|\tilde A_k|^2 n_t\,dt/(\hbar\omega_k)$, and $\bar\omega$ the photon mean frequency.
- $\eta(\lambda_c)$ is the photon fraction at $\lambda>\lambda_c$, relative to the input photon number of the unmasked laser.
- The leading soliton is the highest-peak pulse, isolated in time with a window of $\pm8$ times its FWHM/1.763. $N_1$ is its photon number; $\omega_1$ is its photon mean frequency.

## H1. Conservation structure of the forward model

**Statement.** In the `const` form with shock, Raman and arbitrary $\beta(\omega)$, and lossless:
- $\mathcal N$ is conserved;
- $\bar\omega$ is non-increasing;
- the energy obeys the exact dissipation identity
$$\frac{dE}{dz}=-\frac{n_2f_R}{cA_{\rm eff}}\int\frac{d\Omega}{2\pi}\,\Omega\,{\rm Im}\,\tilde h(\Omega)\,|\tilde I(\Omega)|^2,$$
with $\tilde I$ the Fourier transform of $|A|^2$ (independent of $\beta(\omega)$);
- it obeys the universal bound $|dE/dz|\le\frac{n_2f_R}{cA_{\rm eff}}\,\frac{h'(0^+)}{2}\,E^2$, from $|\tilde I(\Omega)|\le E$ and $\int\frac{d\Omega}{2\pi}\Omega\,{\rm Im}\tilde h=h'(0^+)/2$.

**Test case.** S28; TL sech launch with $N=3$, $T_0=56.7$ fs ($E=4.25$ nJ); $L=1$ m; $n_t=2^{13}$, $dt=3$ fs; lossless; no window.

**Predictions.**
- (a) $|\Delta\mathcal N/\mathcal N|$ at $L$ scales as $dz^p$ with $p=4\pm0.5$ over $dz\in[0.125,1]$ mm, and is $\le10^{-6}$ at $dz=0.25$ mm.
- (b) $E(L)-E(0)=-\int_0^L(\text{identity})\,dz$ to a relative mismatch $\le10^{-3}$, using trapezoid quadrature over 200 saved planes.
- (c) $\bar\omega$ is non-increasing between every pair of successive saved planes, to within $10^{-6}$ rad/ps.
- (d) The universal bound holds at every plane, and the slack ratio $\max_z({\rm rate}/{\rm bound})<0.1$.
- (e) Same launch, $A_{\rm eff}(\omega)$ from the LP01 model:
  - `naive`: $|\Delta\mathcal N/\mathcal N|\ge10^{-3}$ at 1 m;
  - `pc`: $|\Delta\mathcal N/\mathcal N|\le10^{-6}$ at $dz=0.25$ mm.
- (f) Without the shock factor (constant $\gamma$): $|\Delta E/E|\le10^{-6}$, and photons are created, with $\Delta\mathcal N/\mathcal N\in[+0.05,+0.20]$ at 1 m.
- (g) The agents' Julia solver on case (a) at $dz=0.25$ mm:
  - $|\Delta\mathcal N/\mathcal N|\le10^{-5}$;
  - $\eta(1.75\,\mu{\rm m})$ within 2% (relative) of the numpy value.

## H2. The red reach: what caps it, and the reach law

- **H2.1 (expected refutation of card sketch 3's premise).** For TL sech launches in S28, the leading soliton's photon fraction $N_1/\mathcal N$, measured after separation, exceeds the input-content cap $2/N$ of card P-…-03 sketch 1 when $N\ge4$. The cases are $T_{\rm FWHM}=100$ and 300 fs. The excess is at least 10% of the cap.
  - It also exceeds the IST value $(2N-1)/N^2$ by at least 0.05 in every case with $N\in\{3,4,6\}$.
  - So no input-content bound caps the propagated reach.
  - N=3 at 100 fs was seen in a pilot, about 0.71 against the cap 0.667, and does not count as a test.
- **H2.2 (Gordon's law is not an upper bound for an isolated soliton).** Fundamental sech solitons launched at 1.55 µm in S28, lossless, `const`:
  - (a) The GNLSE photon-mean shift agrees with the exact-overlap reduced model (predictions.json, key `H2.2_fundamental_SMF28`) within 5% for $T_0\in\{20,30,50,80\}$ fs. For $T_0=15$ fs the tolerance is 10%.
  - (b) Gordon's law underestimates the GNLSE shift by at least 20% at $T_0=20$ and 30 fs.
  - (c) The relative error of Gordon's law against the GNLSE scales as $T_0^{-q}$ with $q=2\pm0.4$, over $T_0\in\{50,80,120,200\}$ fs. Lengths are chosen so that $T_s$ changes by less than 10%.
- **H2.3 (reach law given the soliton's photon number).**
  - Take the leading soliton of the H2.1 runs from the plane where it has separated. Start the exact-overlap reduced model from the GNLSE values ($z_s$, $\omega_1$, $N_1$).
  - It predicts $\omega_1$ at the final plane to within 10% of the shift accumulated after $z_s$.
  - The regime is $N\le4$. For $N=6$ the tolerance is 20%.
  - A larger excess means extra acceleration (trapped radiation or collisions), and its size is then the measured allowance.

## H3. Loss-edge photon budget and optimal length (Z75, edge-limited case)

**Derivation (reduced model).** With $\dot\omega=-K(\omega)N^4$ (Gordon) and $\dot N=-\alpha N$:
$$N(\omega)^4=N_0^4-\Lambda(\omega),\qquad \Lambda(\omega)=4\int_\omega^{\omega_0}\frac{\alpha}{K}d\omega',\qquad z(\omega)=\int_\omega^{\omega_0}\frac{d\omega'}{K(N_0^4-\Lambda)}.$$
- The photon number is a fixed function of how far the soliton has shifted, independent of $z$.
- If $\alpha$ and $K$ are locally exponential, with $\alpha\propto e^{-\omega/w}$ and $K\propto e^{\kappa\omega}$:
$$N/N_0\simeq\left[1-e^{-(\omega-\omega_\infty)/w_{\rm eff}}\right]^{1/4},\qquad w_{\rm eff}=(1/w+\kappa)^{-1}.$$
- The terminal frequency obeys $\alpha(\omega_\infty)=K(\omega_\infty)N_0^4/(4w_{\rm eff})$.
- The best photon fraction beyond $\lambda_c$ is $\eta^*\approx N(\omega_c)/N_0$, less a crossing correction of order $(\varepsilon/a)\ln(a/\varepsilon)$, with $\varepsilon=\alpha/|\dot\omega|$ and $a=\pi T_s/2$.
- The production test uses the exact-overlap rate, where the law is not exactly $N^4$-separable. The Gordon closed form is checked against it as well.

**Test case.** Z75, `const`; fundamental soliton at 2.8 µm with $T_0=20$ fs ($E=9.13$ nJ); $L=8$ m. Predictions, from predictions.json `H3_ZrF4.const_aeff`:
- (a) Soliton photon fraction $N_1/N_0$ at $z=2,4,6,8$ m: 0.995, 0.975, 0.941, 0.894, each $\pm0.02$. Centre wavelength 3.589, 3.718, 3.787, 3.830 µm, each $\pm0.03$ µm.
- (b) Maximum over $L\le8$ m of $\eta(\lambda_c)$:
  - 0.986 at $L^*=2.83$ m for $\lambda_c=3.5$ µm;
  - 0.967 at $L^*=4.12$ m for $\lambda_c=3.6$ µm;
  - 0.921 at $L^*=6.19$ m for $\lambda_c=3.7$ µm.
  - Tolerances: $\eta^*$ to $\pm0.03$, $L^*$ to $\pm20\%$.
- (c) **Relaxed assumption (`pc` with $A_{\rm eff}(\omega)$).** The same structure holds against the `aeff_w` model column of predictions.json, with the same tolerances, at $\lambda_c=3.5$ µm ($L^*=6.81$ m, $\eta^*=0.973$). The run is to 8 m.

## H4. Shaping headroom (adjoint-optimized masks)

**Case.** S28, `const`, laser = the TL sech spectrum of $N=3$, $T_0=56.7$ fs, $L=1$ m. The objective is $\eta(\lambda_c)$.
- (a) $\lambda_c=1.75$ µm, where TL already reaches $\lambda_c$ (pilot $\eta_{\rm TL}\approx0.71$). Phase-only optimization gives $H_\phi=\eta_\phi^{\rm opt}/\eta_{\rm TL}\in[1.00,1.30]$. This is consistent with the card's conjectured cap $2N/(2N-1)\times1.5=1.8$.
- (b) Passive masks ($|m|\le1$, photons counted against the unmasked laser): $H_{A\phi}\le H_\phi+0.05$.
- (c) $\lambda_c=1.85$ µm, the marginal case (pilot $\eta_{\rm TL}\approx0.30$): $H_\phi>1.3$.

**Method.** The optimizer works on pixels of the spectral phase inside the laser band. Gradients come from the Julia solver's `solve_adjoint(...; adjoint_mode=:discrete_rk4ip)`, with a fixed step equal to the forward step. The method is gradient ascent with Adam steps, starting from TL and from two random smooth phases, run one start at a time. An optimized value is a lower bound on the class maximum.

## What would change the plan
- If H1(a) fails, every photon-budget number needs the window or step diagnosis first.
- If H2.2(a) fails, the reduced model is wrong and H3 is not tested on it.
