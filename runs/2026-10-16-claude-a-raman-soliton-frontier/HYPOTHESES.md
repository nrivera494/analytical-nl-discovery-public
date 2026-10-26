# Frozen hypotheses (claude-a, T-20261016-claude-interactive-02)

Frozen 2026-10-16, 11:35 EDT. Nothing below had been computed by me when this was written; the only prior number used is the orchestrator's scratch run `2026-10-16-claude-interactive-zs-bound-check`.

## Conventions

- Normalized NLSE: $iu_\xi+\tfrac12u_{\tau\tau}+|u|^2u=0$, with $\tau=T/T_0$, $\xi=z/L_D$, $u=A/\sqrt{P_0}$ and $N^2=\gamma P_0T_0^2/|\beta_2|$.
- Zakharov–Shabat (ZS) problem: $\psi_1'=-i\zeta\psi_1+q\psi_2$, $\psi_2'=i\zeta\psi_2-\bar q\psi_1$, with $q=u$.
- A bound state $\zeta=\xi_k+i\eta_k$ carries a soliton of energy $4\eta_k$. The laser energy is $E=\int|u|^2$, which is $2N^2$ for $u=N\,\mathrm{sech}\,\tau$.
- $f_1=4\eta_{\max}/E$. The input classes $\mathcal S_\phi\subset\mathcal S_{A\phi}$ are as on the card.

## H1. Zakharov–Shabat bound and its extremality lemmas

**H1a (theorem, proof below).** Every bound state satisfies $\eta\le\|q\|_\infty$.

Proof:
1. $\frac{d}{dt}(|\psi_1|^2-|\psi_2|^2)=2\eta(|\psi_1|^2+|\psi_2|^2)+4\,\mathrm{Re}(q\bar\psi_1\psi_2)$.
2. Integrating over $\mathbb R$ (the bound state decays) gives $\eta\int w=-2\,\mathrm{Re}\int q\bar\psi_1\psi_2$, with $w=|\psi_1|^2+|\psi_2|^2$.
3. Since $2|\psi_1\psi_2|\le w$, $\eta\le\int|q|w/\int w\le\|q\|_\infty$.

Numerical test: no computed eigenvalue in this run violates $\eta\le\|q\|_\infty$ by more than solver accuracy ($10^{-6}$ relative).

**H1b (lemmas, proofs below).** For $q\in\mathcal S_{A\phi}$ built from a laser spectrum $|Q|$:
- $\|q\|_\infty\le\|q_{\rm TL}\|_\infty=\frac1{2\pi}\int|Q|$, by the triangle inequality;
- $\int|q|^4\le\int|q_{\rm TL}|^4$, because $|\widetilde{q^2}|\propto|(mQ)*(mQ)|\le|Q|*|Q|\propto\widetilde{q_{\rm TL}^2}$ pointwise, then Parseval.

Numerical test: no optimized or random mask violates either.

**H1c (conjecture, refutable): a sharper, semiclassical upper bound.**
- Define $\eta_{\rm WKB}[|q|]$ by $\int\big(|q|^2-\eta^2\big)_+^{1/2}\,dt=\pi/2$. It is exact for every $A\,\mathrm{sech}\,t$, giving $A-\tfrac12$.
- Conjecture: $\eta_{\max}(q)\le\eta_{\rm WKB}[|q|]$ for every single-humped $|q|$, chirped or not. Phase in time only lowers the content below that of the real potential $|q|$.
- Prediction: holds within $10^{-3}$ absolute for the following, at peak amplitudes 1–8:
  - transform-limited Gaussians, $\mathrm{sech}^2$, Lorentzian and super-Gaussian ($m=2$) pulses;
  - linearly chirped Gaussians;
  - every phase-shaped Gaussian generated in H2.
- A violation by more than $10^{-3}$, outside the solver's two-grid error, refutes it.

## H2. Integrable-limit headroom (ZS eigenvalues of the shaped input, no propagation)

- **Statement.** For sech and Gaussian lasers, the transform-limited launch maximizes $\eta_{\max}$ over $\mathcal S_\phi$ and over $\mathcal S_{A\phi}$. So $H_{\mathcal S_\phi}=H_{\mathcal S_{A\phi}}=1$, not $2N/(2N-1)$.
- **Prediction.** Multi-start gradient ascent of $\eta_{\max}$ over smooth spectral masks finds no mask with $\eta_{\max}>\eta_{\max}^{\rm TL}(1+10^{-3})$. This is tested at:
  - sech lasers with $N\in\{1.5,2,3,4,6\}$;
  - Gaussian lasers with the same transform-limited peak amplitudes.

  The masks are phase given by up to 24 smooth basis functions, and amplitude by a bounded sigmoid.
- **Supporting reason, not a proof.** Purely imaginary perturbations $\delta q=ir$ of a real even $q$ move a simple imaginary eigenvalue only along the real axis at first order (by the symmetry $q\to\bar q$, $\zeta\to-\bar\zeta$). So the TL pulse is stationary under phase masks. The prediction is that it is a maximum.

## H3. Raman transfer in the GNLSE (output soliton content versus input content)

Model: GNLSE with the Blow–Wood Raman response ($f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs). Launch: TL sech, $N\in\{2,3,4,6,8\}$, $T_0\in\{25,50,100\}$ fs.

- **Measure.** $f_1(L)=4\eta_1(L)/E$: the ZS content of the output's most red-shifted soliton (largest frequency shift), against $f_1(0)=(2N-1)/N^2$.
- **H3a.** For every $N\ge2$, $f_1(L)/f_1(0)-1>0$ once fission is complete.
- **H3b.** The excess is linear in the Raman time at fixed $N$ and $L/L_{\rm fiss}$. The exponent of the excess against $\tau_R=T_R/T_0$ (varying $T_0$) is $1.0\pm0.25$.
- **H3c.** The excess grows monotonically with $N$ over $N=2$–8, at fixed $T_0=50$ fs and $L=4\,L_D/N$.
- **H3d.** The excess saturates once the leading soliton has separated. Between $L=4L_D/N$ and $8L_D/N$ it changes by less than 20% of itself.

## H4. Shaping headroom in the GNLSE

The card's restated conjecture is adopted as frozen. Let $\epsilon^{\rm TL}=f_1^{\rm TL}(L)/f_1^{\rm TL}(0)-1$ be the transform-limited launch's own Raman-transfer excess. Then, for the setting below:

$$\max_{\mathcal S_\phi}f_1(L)<f_1^{\rm TL}(L)\cdot\frac{2N}{2N-1}\cdot(1+\epsilon^{\rm TL}).$$

Setting:
- GNLSE with Raman, and $\delta_3=\beta_3/(6|\beta_2|T_0)\in\{0,0.05\}$;
- $N=2$–6;
- phase masks optimized over a smooth low-dimensional basis, polynomial phase of orders 2–6, with multi-start.

My sharper prediction: the best phase mask found improves $f_1(L)$ over transform-limited by less than 5% at every $N\ge3$.

## H5. Jitter

Not frozen yet. It is posed later only if time allows; otherwise it is left as a loose end.

## Second freeze (12:03 EDT, commit 94bd1ac): H3e, from the shape of the H3 data, before the cases below were computed

**Seen so far** (`h3_main.log`; TL sech, Blow–Wood, $L=4L_D/N$, no $\beta_3$, no self-steepening). The excess $\varepsilon(N,T_0)=f_1(L)/f_1(0)-1$ is:
- $N=2$: 0.095, 0.127, 0.107, 0.042, 0.009 at $T_0=25$, 50, 100, 200, 400 fs;
- $N=3$: 0.121, 0.209, 0.310, 0.266, 0.117;
- $N=4$: 0.107, 0.200, 0.365 at 25, 50, 100 fs;
- $N=6$: 0.366, 0.579, 0.729 at 100, 200, 400 fs.

**H3e.**
- (i) $\varepsilon$ is unimodal in $T_0$ at fixed $N$, and its maximum $\varepsilon^*(N)$ grows with $N$.
- (ii) Held-out predictions, none of them computed yet:
  - $\varepsilon(5,200\,{\rm fs})\in[0.40,0.62]$;
  - $\varepsilon(5,100\,{\rm fs})\in[0.30,0.50]$;
  - $\varepsilon(8,800\,{\rm fs})\in[0.6,1.2]$;
  - $\varepsilon(6,800\,{\rm fs})\ge0.55$, i.e. still near the maximum.

## Third freeze (12:10 EDT, commit d11ec48): H3f, before `h3_ext.py small` and `h3_ext.py dense` were run

**Seen before this freeze.** All of `h3_main.log`. Two observations bear on this freeze:
- At $N=8$, $T_0=400$ fs, $L=4/N$, the measured excess is 0.12 with $\mathrm{Re}\,\zeta_1=-3.17$. A large real part means the window's spectral centroid is not the soliton's frequency: the leading soliton is probably not yet isolated, and the measurement there is suspect.
- $\varepsilon$ is saturated between $L=4/N$ and $8/N$ for $N=3$ and 4 at every $T_0$. It is not saturated for $N=2$ at $T_0=400$ fs.

**H3f.** Here $\varepsilon_\infty(N,T_0)$ is the saturated excess: its value once it changes by less than 5% between consecutive $L\in\{4,8,16,32\}/N$.
- (i) **Perturbative limit.** For $N=3$ and 4, $\varepsilon_\infty\to0$ as $\tau_R=T_R/T_0\to0$. The local exponent $p=d\ln\varepsilon_\infty/d\ln\tau_R$ between $T_0=1600$ and 3200 fs lies in $[0.8,1.4]$. This is H3b restricted to the small-$\tau_R$ regime.
- (ii) **The same for $N=2$**, with $p\in[0.8,1.4]$ between 1600 and 3200 fs. A competing hypothesis gives a finite $\varepsilon_\infty$ as $\tau_R\to0$: a Raman-driven transfer rate of order $\tau_R$, acting for a splitting time of order $1/\tau_R$. I pick the linear law.
- (iii) **Collapse of the peak position.** Take $T_0^*(N)$, the $T_0$ that maximizes $\varepsilon_\infty$ on the grid $\{25,35,50,70,100,140,200,280,400,560\}$ fs. Then $x^*=N^2T_R/T_0^*$ ($T_R=1.462$ fs) is the same for $N=2,3,4,5$ within a factor 1.6 (max/min ≤ 1.6).
- (iv) The peak value grows with $N$: $\varepsilon^*(5)\in[0.50,0.75]$.

## Fourth freeze (12:13 EDT, commit 5628392): H3g. Peak law and small-$\tau_R$ coefficient

Before this freeze I had seen: `h3_main`; `h3_small` for $N=2$ and 3; `h3_dense` for $N=2$–4 and for $N=5$ at $T_0=35$ fs only. I had not seen the excess values of `h3_small` $N=4$, nor any other $N=5$, $N=6$ or $N=8$ results beyond `h3_main`.

**Observed so far** (to be reported with run ids):
- The maximum over $T_0$ of $\varepsilon_\infty$ sits at $x^*=N^2T_R/T_0^*\approx0.11$ for $N=2,3,4$.
- The leading-soliton content at that maximum, $f_1^*=(1+\varepsilon^*)(2N-1)/N^2$, satisfies $f_1^*\sqrt N\approx1.2$ ($N=2$), 1.27 ($N=3$), 1.29 ($N=4$) and 1.30 ($N=6$, $T_0=400$ fs, $L=4/N$).
- At small $\tau_R$, $\varepsilon_\infty\approx c_N\tau_R$, with $c_2\approx5$ and $c_3$ still falling (about 17 at $T_0=3200$ fs).

**H3g (predictions).**
- (i) **Peak position.** For $N=5$, $\varepsilon_\infty(5,T_0)$ is larger at $T_0=340$ fs than at both 200 and 560 fs. Equivalently, $T_0^*(5)\in[250,450]$ fs.
- (ii) **Peak content.** $f_1^*(N)=C/\sqrt N$ with $C=1.30\pm0.09$ for $N=5$, where $f_1^*$ is the maximum over $T_0\in\{200,280,340,400,560\}$ fs. For $N=8$, at the single held-out point $T_0=800$ fs (predicted near the peak $T_0^*\approx850$ fs), $f_1\in[0.40,0.50]$ once saturated in $L$.
- (iii) **Small $\tau_R$.** $c_4=\varepsilon_\infty(4,3200\,{\rm fs})/\tau_R\in[25,60]$.

**Scaling reading of $x$.**
- Over one fission length $\xi_f\sim1/N$, the leading soliton (amplitude $\approx2N$) acquires a Raman frequency shift $\Omega_f\sim\tau_R(2N)^4\xi_f\sim\tau_RN^3$.
- Divided by its bandwidth $\sim2N$, this gives $x\sim\tau_RN^2$.
- The transfer is therefore perturbative, linear in $\tau_R$, for $x\ll x^*$, and Raman-dominated beyond $x^*$.

## Fifth freeze: H3h. Self-steepening changes the excess only through the quantum defect

**Seen before this freeze.** `solver_check.json`, at $(N,T_0)=(3,100)$ and $(4,200)$ fs. For these two cases the numpy model with $s=1/(\omega_0T_0)$ and the solver both gave $f_1^{\rm ph}=4\eta_1/[(1-sW_c)E]$ within $2\times10^{-3}$ (relative) of the $s=0$ value of $f_1$. Here $W_c$ is the window's spectral centroid; positive $W_c$ is red in the numpy convention.

The `h3_relaxed` run had started, and its $N=2$ rows may already exist. I have not looked at any of its output.

**H3h.**
- With self-steepening $s=1/(\omega_0T_0)$ at 1550 nm and $T_0=100$ fs, the leading soliton's photon-number fraction $f_1^{\rm ph}$ equals the $s=0$ energy fraction $f_1$ within 1% (relative) for $N=4$ and $N=6$ (held out).
- The energy fraction $f_1$ is lower by the factor $(1-sW_c)$.

## Sixth freeze: H1c′, the narrowed semiclassical bound, on shapes not used before

H1c is refuted by the Lorentzian; see `h1_tests.json` and `h1c_lorentz_window.json`. It held for every exponentially or faster decaying shape tested: Gaussian, sech², super-Gaussian, chirped and random-phase Gaussians.

**H1c′.**
- $\eta_{\max}\le\eta_{\rm WKB}[|q|]+10^{-3}$ for real, single-humped $q$ whose tails decay at least exponentially.
- Held-out shapes, at peak $A\in\{1,2,3,4\}$:
  - (a) $A\,\mathrm{sech}^{1/2}t$;
  - (b) $A\,\mathrm{sech}^3t$;
  - (c) $Ae^{-|t|^{3/2}}$;
  - (d) the asymmetric $A\,\mathrm{sech}(t)e^{0.4\tanh t}/\max$.
- Algebraic tails, low-confidence guess: $A/(1+t^2)^2$ and $A/(1+t^4)$ also violate the WKB bound at $A=1$.

## Seventh freeze: H2b. TL optimality on two further laser spectra, before computing

H2 was confirmed in 64 optimizations: sech and Gaussian lasers at $A=1.5$–4 (`h2_sech.json`, `h2_gauss.json`). The held-out $A=6$ runs were still running.

**H2b.** For two laser spectra not used before, transform-limited peak $A\in\{2,4\}$, the same optimizer and classes find no mask with $\eta_{\max}>\eta_{\max}^{\rm TL}(1+10^{-3})$. The spectra are:
- the asymmetric spectrum $|Q|\propto\mathrm{sech}(\pi k/2)\,(1+\tfrac12\tanh k)$;
- the flat-top spectrum $|Q|\propto e^{-(k/1.5)^8}$, whose transform-limited pulse has sinc-like side lobes and is not single-humped.

## Eighth freeze: H3i. Held-out N = 7 from the peak-content law, before computing

**Seen before this freeze.** All `h3_*` logs except `h3_heldout` at $N=8$; I have seen no $N=7$ run.

**Fitted so far** (`h3_analysis.py` → `h3_summary.json`):
- the peak position $T_0^*(N)=62,123,195,283$ fs for $N=2$–5, roughly $T_0^*\propto N^{1.65}$;
- the peak content $f_1^*\sqrt N=1.21,1.26,1.29,1.29,1.30$ for $N=2$–6.

**H3i.**
- (i) $N=7$, $T_0=500$ fs (predicted $T_0^*(7)\approx62\cdot3.5^{1.65}\approx490$ fs): the saturated $f_1\in[0.46,0.52]$. That is $1.30/\sqrt7$ within ±6%, equivalently $\varepsilon\in[0.73,0.96]$.
- (ii) $N=6$, $T_0=560$ fs: $\varepsilon\ge0.66$, i.e. still within 10% of the $N=6$ maximum.

## Ninth freeze: H3j and H4b, before computing

**H3j. Non-integer $N$ (held out).**
- For $N=3.5$ the IST leading content is still $f_1^{\rm IST}=(2N-1)/N^2$, and the launch now also sheds radiation.
- Prediction: the maximum over $T_0\in\{110,140,170,200,240\}$ fs of the saturated $f_1$ lies in $1.30/\sqrt{3.5}\,(1\pm0.06)=[0.653,0.737]$.
- The maximizing $T_0$ lies in $[120,200]$ fs. The fit $62\,(N/2)^{1.65}$ gives about 155 fs.

**H4b. Shaping at the Raman-transfer optimum.**
- Setting: $N=4$, $T_0=200$ fs ($x=0.117\approx x^*$).
- Prediction: the best smooth phase mask found (same Powell search as H4) improves $f_1(L=4/N)$ over transform-limited by less than 3%.

## Tenth freeze: H4c. Larger basis and gradient search, before computing

**H4c.**
- Method: L-BFGS-B on forward-difference gradients over 11 Legendre phase coefficients (orders 2–12), from TL and from the best Powell mask.
- Prediction: the improvement over TL stays below 2% for $N=3$ and $N=4$ at $T_0=100$ fs. That is the claim bound in C-20261016-claude-a-03.

## Eleventh freeze: H3k. Does the Raman transfer depend on the response only through $T_R$?

Two single-oscillator responses with the same $f_R=0.18$ and the same $T_R=1.462$ fs as Blow–Wood:
- $(\tau_1,\tau_2)=(10,19.495)$ fs, gain peak near 16 THz, broader;
- $(16,58.676)$ fs, gain peak near 10 THz, narrower.

**H3k (null hypothesis "$T_R$ only").** For $N=3$ and 4, the peak position $T_0^*$ (grid $\{70,100,140,200,280\}$ and $\{100,140,200,280,400\}$ fs) moves by less than 10%, and the peak content $f_1^*$ by less than 3%, relative to Blow–Wood. I hold no strong prior here. A failure would show that the gain-spectrum shape at the solitons' bandwidth matters, so the law's $T_R$ normalization would be specific to silica.

**Disclosure.** While self-testing the new launch option I computed one Gaussian-launch point: $N=4$ peak amplitude, $T_0=200$ fs, $f_1=0.700$, IST content 0.491. The Gaussian-launch scan (`h3_gauss`) is therefore an exploration, not a frozen test.

## Twelfth freeze: H3m. The N = 8 peak, before computing

**Seen before this freeze.** $f_1(8,800\,{\rm fs})=0.4405$ on the 32768-point grid. The fit $T_0^*=20.5\,{\rm fs}\,N^{1.633}$ ($N=2$–6) predicts $T_0^*(8)\approx620$ fs.

**H3m.**
- (i) $f_1(8,600\,{\rm fs})\in[0.43,0.49]$, i.e. $1.29/\sqrt8\pm6\%$.
- (ii) $f_1(8,600)>f_1(8,800)$ and $f_1(8,600)>f_1(8,450)$. Both rows are saturated in $L$ on 32768 points.

## Thirteenth freeze: H5a. Quantum-limited timing jitter of the leading soliton, before N = 4, 5 were computed

**Setup** (`h5_jitter.jl`, solver b9fa957, discrete RK4IP adjoint):
- observable: the temporal centroid of the leading soliton, windowed as in `h3_scan.measure`;
- noise: vacuum noise of the coherent input, plus the symmetrized ($\coth$) Raman phonon bath at 300 K;
- launch: TL sech, $T_0=100$ fs, $L=4L_D/N$, SMF-like parameters.

**Baseline.** An isolated fundamental soliton with the leading soliton's output peak power, over the same physical length, full-pulse centroid. $R_{\rm vac}$, $R_{\rm ram}$ and $R_{\rm tot}$ are the variance ratios, leading over baseline.

**Seen before this freeze.**
- N=1 validation against SPT: vacuum agrees within 1.2%; Raman is 8–9% above the thermal-limit SPT formula.
- $N=2$: $R_{\rm vac}=0.670$, $R_{\rm ram}=0.925$, $R_{\rm tot}=0.734$.
- $N=3$: $R_{\rm vac}=0.494$, $R_{\rm ram}=1.193$, $R_{\rm tot}=0.576$.

**H5a** (power-law extrapolation, ±25%):
- $R_{\rm vac}(4)\in[0.30,0.50]$ and $R_{\rm vac}(5)\in[0.25,0.43]$;
- $R_{\rm ram}(4)\in[1.07,1.79]$ and $R_{\rm ram}(5)\in[1.22,2.04]$;
- $R_{\rm tot}$ decreases monotonically from $N=3$ to 5.

## Fourteenth freeze: H3n. Launch-shape robustness of the peak law (held-out Gaussian, peak 6), before computing

**Seen before this freeze.** The Gaussian-launch exploration at peak amplitude 4 (`h3_gauss`, not frozen) gave a peak leading-soliton energy $E_1^*=4\eta_1=19.85$. The sech launch of the same peak amplitude gives 20.6, i.e. $1.29/\sqrt N\cdot2N^2=2.58N^{3/2}$.

**H3n.**
- Setting: Gaussian launch $q=6e^{-\tau^2/2}$, $T_0\in\{300,380,460\}$ fs (sech $T_0^*(6)\approx377$ fs), saturated in $L$.
- Prediction: the maximum leading-soliton energy $E_1^*=4\eta_1\in[34.5,39.5]$, i.e. $2.58\cdot6^{3/2}\cdot(0.96\pm0.065)$. Equivalently $f_1^*=E_1^*/(36\sqrt\pi)\in[0.541,0.619]$.

## Fifteenth freeze: H3o and H3p, before computing

**H3o. Universality of the peak value.**
- Response: an As2S3-like single oscillator with $f_R=0.10$, $\tau_1=15.5$ fs, $\tau_2=230.5$ fs (parameters as quoted in Kormokar et al. 2023). Its $T_R$ is 0.21 fs (0.2075 fs), seven times smaller than silica's. *Correction after the freeze commit 995962c: the freeze text first said 0.12 fs, a hand estimate typed before the code printed 0.2075 fs. The predictions below do not use $T_R$.*
- Predictions, for $N=3$ and 4:
  - the maximum over $T_0$ of the saturated $f_1$ is within 4% of the Blow–Wood values, 0.731 and 0.644;
  - the maximizing $T_0$ lies within a factor 1.5 of $1.7\tau_1N^{1.62}$, i.e. 156 and 249 fs.
- The $T_0$ grids are $\{40,80,160,320,640\}$ fs ($N=3$) and $\{60,120,240,480,960\}$ fs ($N=4$).

**H3p. $c_5$**, already frozen in C-20261016-claude-a-02 (commit ec14071). $\varepsilon_\infty(5,T_0)/\tau_R\in[150,600]$ at $T_0=3200$ fs.

## Sixteenth freeze: H5b. Jitter at fixed red shift, before N = 4, 5 were printed

**Setup.** As H5a, but the isolated fundamental soliton (same peak power as the leading soliton) is propagated until its spectral centroid reaches the leading soliton's red shift (`h5_jitter_fixedshift.jl`).

**Seen before this freeze.**
- $N=2$: $R_{\rm vac}=0.170$, $R_{\rm ram}=0.300$, $R_{\rm tot}=0.197$.
- $N=3$: $R_{\rm vac}=0.130$, $R_{\rm ram}=0.401$, $R_{\rm tot}=0.156$.

**H5b** (power-law extrapolation, ±30%):
- $R_{\rm tot}(4)\in[0.09,0.17]$ and $R_{\rm tot}(5)\in[0.08,0.15]$;
- $R_{\rm vac}(4)\in[0.076,0.14]$ and $R_{\rm vac}(5)\in[0.065,0.12]$;
- $R_{\rm ram}(4)\in[0.35,0.64]$ and $R_{\rm ram}(5)\in[0.40,0.75]$;
- qualitatively, at fixed shift and peak power the fission source stays at least 4× quieter ($R_{\rm tot}<0.25$) for $N=4$ and 5.

## Seventeenth freeze: H3q. Self-steepening at the transfer maximum, before computing

H3h, the photon fraction under self-steepening within 1% of the $s=0$ value, was tested at $T_0=100$ fs only.

**H3q.** With $s=1/(\omega_0T_0)$ at 1550 nm, $f_1/(1-sW_c)$ equals the $s=0$ value of $f_1$ within 1.5%:
- at $(N,T_0)=(4,200)$ fs;
- at $(6,400)$ fs.

The red shift there is larger, so the quantum defect $sW_c$ is larger.

## Eighteenth freeze: H5c. Fixed-shift jitter at the Raman-transfer maximum, before computing

**Seen before this freeze.** H5b outcome: $R_{\rm tot}=0.197$, 0.156, 0.049, 0.023 for $N=2$–5 at $T_0=100$ fs.

**H5c.** At the transfer maximum, $(N,T_0)=(3,140)$ and $(4,200)$ fs, with the same fixed-shift baseline, the fission source is also at least 4× quieter: $R_{\rm tot}<0.25$.

## Nineteenth freeze: H2c. Sharp-featured masks, before computing

**H2c.** For sech and Gaussian lasers at $A=3$ and 4, none of 600 random sharp-featured masks gives $\eta_{\max}>\eta_{\max}^{\rm TL}(1+10^{-6})$. The masks are drawn from three families:
- binary $0/\pi$ phase on 2–8 random spectral segments;
- random spectral holes, i.e. zero amplitude on 1–4 random intervals, combined with random smooth phase;
- pulse-splitting masks with piecewise-linear phase of random slopes on 2–4 segments.

## Twentieth freeze: H4d. Robustness of the found masks, before computing

**Seen.**
- The 11-parameter forward-difference L-BFGS at $N=4$, $T_0=100$ fs found $f_1/f_1^{\rm TL}=1.062$ (verified saturated and clean, step-converged).
- The 15-parameter adjoint L-BFGS at $N=4$, $T_0=200$ fs found 1.070 (ZS content, re-measured in numpy). It was not converged.
- These refute H4c at $N=4$, H4b, and the frozen "$<5\%$ for $N\ge3$".

**H4d (held-out robustness of the two masks, same coefficients).**
- (i) With self-steepening on ($s=1/(\omega_0T_0)$), each mask still raises the photon-number content $f_1/(1-sW_c)$ by at least 4% over TL.
- (ii) Detuning $T_0$ by $\pm10\%$ (90 and 110 fs for the first mask, 180 and 220 fs for the second, mask fixed in units of the spectral support) still gives at least 4% over TL at the same $T_0$.

## Twenty-first freeze: H4e. Large-basis headroom at N = 3, before computing

**Seen.** At $N=4$ the large-basis searches found $+6.2\%$ (100 fs) and $+7.0\%$ (200 fs). At $N=3$, 100 fs, the 11-parameter search found $+1.13\%$ (converged).

**H4e.** At $N=3$ near its transfer maximum ($T_0=140$ fs), the same 11-parameter forward-difference L-BFGS from TL finds a gain of at least 3%.

## Twenty-second freeze: H3r. The drift of c_3 and c_5 at smaller tau_R, before computing

**Seen.**
- $c_3=24.2$, 18.6, 16.7 at $T_0=800$, 1600, 3200 fs.
- $c_5=149.3$, 139.7 at 1600, 3200 fs.
- $c_2$ ($4.89\pm0.02$) and $c_4$ ($76\pm3$) are already flat.

**H3r** (saturated in $L$, at $T_0=6400$ fs):
- $c_3\in[14.0,16.5]$, i.e. it continues to fall, towards $\approx15$;
- $c_5\in[118,140]$.

A value of $c_N$ outside its window means the extrapolations in C-20261016-claude-a-02 (a) are wrong.

## Twenty-third freeze: H4f and H4g, before computing

**H4f. Self-steepening robustness of the best masks.** With $s=1/(\omega_0T_0)$, the photon-number content gain over TL (same $s$) is:
- at least 5% for mask A2 ($N=4$, 100 fs; $+9.0\%$ at $s=0$);
- at least 5% for mask B2 ($N=4$, 200 fs; $+8.0\%$ at $s=0$).

**H4g. Headroom at $N=5$ near the transfer maximum ($T_0=280$ fs).** A reduced forward-difference L-BFGS from TL (orders 2–8, at most 12 iterations) finds a gain of at least 3%. This is a lower-effort search than at $N=4$, so a smaller value would not by itself mean a smaller headroom.

## Twenty-fourth freeze: H3s. Multi-component Raman response (Lin–Agrawal), before computing

**Response.**
- $h=(1-f_b)h_a+f_bh_b$, with $h_a$ Blow–Wood (12.2 fs, 32 fs), $h_b(t)=\frac{2\tau_b-t}{\tau_b^2}e^{-t/\tau_b}$, $f_b=0.21$, $\tau_b=96$ fs, and $f_R=0.245$.
- Transfer function $H_b=\frac{2}{\tau_ba}-\frac1{\tau_b^2a^2}$, $a=1/\tau_b-i\omega$.

**H3s.** For $N=3$ and 4, the maximum over $T_0$ (grids $\{70,100,140,200,280\}$ and $\{100,140,200,280,400\}$ fs) of the saturated $f_1$ satisfies $f_1^*\sqrt N\in[1.20,1.38]$. This is the verifier prediction of C-20261016-claude-a-02 for multi-peak silica responses, applied here to Lin–Agrawal.

## Twenty-fifth freeze: H4h. Pulse-duration robustness of masks A2 and B2, before computing

**H4h.** With the mask fixed in units of the spectral support:
- mask A2 at $T_0=90$ and 110 fs, and mask B2 at 180 and 220 fs, each still give at least 4% over TL at the same $T_0$;
- or, if not all four, at least three of the four (mask A failed at $-10\%$ in H4d).
