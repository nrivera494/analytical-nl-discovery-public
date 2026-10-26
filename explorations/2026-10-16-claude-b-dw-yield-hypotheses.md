# Frozen hypotheses: dispersive-wave yield ceiling and shaping headroom

Task T-20261016-claude-interactive-03, problem P-20261016-claude-interactive-01. Agent claude-b (family claude, model claude-opus-5-5). Written 2026-10-16 before any production run. Each hypothesis states the prediction, its tolerance and its regime. Changes after the freeze commit are listed at the end with their commit, never edited in place.

## Model, conventions and observables

**Model M0** (Kerr and cubic dispersion; no Raman, no self-steepening, no loss):
$$iu_\xi+\tfrac12u_{\tau\tau}+N^2|u|^2u=i\delta_3u_{\tau\tau\tau},\qquad \delta_3=\frac{\beta_3}{6|\beta_2|T_0},$$
with $\xi=z/L_D$, $\tau=(t-z/v_g)/T_0$, $N^2=\gamma P_0T_0^2/|\beta_2|$. This is Eqs. 1–2 of Roy, Bhadra and Agrawal, PRA 79, 023824 (2009), DOI 10.1103/PhysRevA.79.023824 (**full text**, author copy from the Agrawal group website), including the factor 6.

- Fourier convention: $u(\tau)=\frac1{2\pi}\int\hat u(w)e^{-iw\tau}dw$, so $w>0$ is blue. The linear phase is $\hat u\propto e^{iD(w)\xi}$ with $D(w)=\delta_3w^3-w^2/2$. The zero-dispersion frequency is $w_z=1/(6\delta_3)$. A soliton of amplitude $\eta$ (wavenumber $\eta^2/2$) is linearly phase-matched at $D(w)=\eta^2/2$, so $w_{\rm DW}\approx(1+4\delta_3^2\eta^2)/(2\delta_3)$ (Roy Eq. 5).
- **Launches:** the transform-limited (TL) Gaussian $u_0=e^{-\tau^2/2}$ (the card's laser), and $u_0=\mathrm{sech}\,\tau$ for Roy comparisons and exact anchors.
- **Model M1:** M0 plus the causal Raman response, with self-steepening where stated.
- **Band yield:** $\eta_B(\xi)=\int_{w\ge w_z}|\hat u(\xi,w)|^2dw\big/\int|\hat u_{\rm laser}|^2dw$, where the denominator is the laser before any mask. In M0, $\int|u|^2$ is both the energy and the photon number. With self-steepening, photon and energy fractions are reported separately. The initial leakage $\eta_B(0)$ is always reported.
- **Gated DW yield:** $\eta_{\rm DW}$ is $\eta_B$ evaluated after setting the field to zero within $|\tau-\tau_s|<\tau_g$ of each soliton, so that the solitons' own spectral tails are excluded. It is used for the asymptotic law, where soliton tails beyond $w_z$ can rival an exponentially small DW.

## H1. Conservation-law program (card sketch 1)

**Ingredients, each to be checked.**
- In M0 the conserved quantities are $\mathcal N=\int n\,dw$, $\mathcal P=\int w\,n\,dw$ and $\mathcal H=\int K(w)n\,dw-\frac{N^2}2\int|u|^4d\tau$, where $n=|\hat u|^2/2\pi$ and $K=-D$.
- The sharp one-dimensional Gagliardo–Nirenberg inequality is $\int|u|^4\le\frac1{\sqrt3}\left(\int|u|^2\right)^{3/2}\left(\int|u_\tau|^2\right)^{1/2}$, with equality for sech. Applying it to $u\,e^{-i\bar w\tau}$ allows the centred second moment $V=\int(w-\bar w)^2n$, where $\bar w=\mathcal P/\mathcal N$.
- The program is: maximise $\int_Bn$ subject to $n\ge0$, fixed $\mathcal N$ and $\mathcal P$, and $\int Kn-\frac{N^2}{2\sqrt3}\mathcal N^{3/2}\sqrt V\le\mathcal H_{\rm in}$.

**H1a (prediction: the program is vacuous).** For every $\delta_3>0$, every launch and every $N$, the supremum of the program over spectra on the whole line is 1 for $B=\{w\ge w_z\}$. This holds even with the Kerr credit set to zero. The mechanism is that $K(w)=w^2/2-\delta_3w^3$ falls superlinearly on the blue side. A three-point spectrum (band mass, red recoil mass, and a vanishing mass at $w\to\infty$ carrying fixed momentum) satisfies all constraints with band fraction $\to1$. Test: an analytic construction, checked by exact arithmetic on the constraint values.

**H1b (finite window).** If the spectrum is confined to $|w|\le W$, the program becomes a finite second-order cone program.
- For TL Gaussians, $N=3$–10 and $\delta_3=0.01$–0.05, its value is at least 0.5 whenever $W\ge 2w_{\rm DW}$.
- It is at least 0.9 on the frequency windows used in the simulations here.

The program is therefore loose by more than the card's factor 3 wherever the achieved yield is below 0.3. Test: scipy linear programs on a grid, scanned over the variance level, with the windows stated.

**H1c (normal dispersion).**
- With pure $\beta_2>0$ ($K=-w^2/2$, sign-definite), the program reduces to a moment problem. For a one-sided band $w\ge w_B$ and fixed $\mathcal P$, its value is the Cantelli bound $\sigma^2/(\sigma^2+(w_B-\bar w)^2)$, where $\sigma^2=2|\mathcal H|/\mathcal N-\bar w^2$. This is at most the Hamiltonian–Markov ceiling $2|\mathcal H|/(\mathcal N w_B^2)$ of Castelló-Lurbe et al. (2013).
- With $\beta_3\ne0$ on an unbounded window, the normal-dispersion program is vacuous for the same reason as H1a.

Test: analytic, plus the linear program.

**H1d (invariants in the codes).**
- In M0 the numpy oracle conserves $\mathcal N$ to machine precision.
- $\mathcal P$ and $\mathcal H$ drift by less than $10^{-6}$ relative over the runs, on grids that pass the convergence test.
- The Julia solver (FastDifferentiableMMNLO, fixed-step RK4IP) shows the same, and any larger drift is reported.

## H2. Transform-limited yield

**H2a (reproduce Roy et al. first).**
- Setup: model M0, sech, $N=2$, $\xi=4$. Observable: the NSR spectral-peak level in dB relative to the input spectral peak.
- At $\delta_3=0.02,0.03,0.04,0.06,0.10$ it should lie within ±5 dB of my digitisation of the TOD-only curve of Roy Fig. 3(b): −22, −14, −12, −10 and −6 dB.
- The peak frequency $\Delta\nu_dT_0=\Omega_dT_0/2\pi$ should lie within 6% of Roy Fig. 3(a), which is about 5% above their Eq. 5.
- I expect the measured levels to lie **above** Roy's Eq. 6 by more than 20 dB at $\delta_3=0.02$. That is, Eq. 6 does not describe the TOD-only fission burst (see H2b).

**H2b (singularity law, the main new hypothesis).**
- Statement: for a TL launch in M0, the integrated DW yield of the fission burst obeys
$$\lim_{\delta_3\to0}\delta_3\ln\eta_{\rm DW}=-d_*,$$
where $d_*$ is the minimum over $\xi$ of the width of the analyticity strip (the distance from the real $\tau$ axis to the nearest complex-time singularity) of the **unperturbed** ($\delta_3=0$) NLSE solution from the same launch.
- Reasoning: the TOD source at frequency $w$ is $\delta_3w^3\hat u_0(w,\xi)$, and $|\hat u_0(w,\xi)|\sim e^{-d(\xi)|w|}$. The $\xi$ integral is dominated by the time of minimal $d$, and $w_{\rm DW}=1/(2\delta_3)+O(\delta_3)$.
- **Sech, $N=2$.** For the Satsuma–Yajima breather the poles satisfy $\cosh2\tau=\sqrt3|\sin2\xi|-1$. This gives $d(\xi)=\tfrac12\arccos(\sqrt3|\sin2\xi|-1)$ and
$$d_*(2)=\tfrac12\arccos(\sqrt3-1)=0.37466\quad\text{at }\xi=\pi/4.$$
  Roy's Eq. 6 instead has exponent $\pi/(2(2N-1))=0.5236$.
- **Prediction for sech $N=2$:**
  - the local slope $s(\delta_3)=-d\ln\eta_{\rm DW}/d(1/\delta_3)$ over $\delta_3\in[0.008,0.03]$ lies within 10% of 0.3747;
  - $|s-d_*|$ decreases as $\delta_3$ decreases, and its measured exponent is reported;
  - the Eq. 6 value 0.5236 is excluded.
- **General launches,** including the card's Gaussians: the same law, with $d_*$ computed from the $\delta_3=0$ evolution. It is measured from the exponential decay rate of the spectral tail and minimised over $\xi$, before the corresponding TOD runs; it is recorded below as an amendment before those runs.
  - Prediction: the slope over $\delta_3\in[0.01,0.02]$ is within 15% of that $d_*$ for the Gaussian at $N=3$.
  - Held out: the Gaussian at $N=4$ and the sech at $N=3$ are tested only after the $N=2$ sech and $N=3$ Gaussian results are fixed.

**H2c (card regime, descriptive).**
- For TL Gaussians with $N\in\{3,4,6,8,10\}$ and $\delta_3\in\{0.01,0.02,0.03,0.05\}$, $\eta_B$ at $\xi_f=2$ spans more than six decades.
- It is at most 0.5 everywhere on that grid.
- $\eta_B(\xi)$ has saturated by $\xi=2$, changing by less than 20% between $\xi=1.5$ and 2 wherever $\eta_B>10^{-6}$.

## H3. Shaping headroom (card conjecture)

The objective is $\eta_B(\xi_f=2)$, or $\ln\eta_B$ for conditioning, as a fraction of laser photons. The input is $\hat u_{\rm in}=m(w)\hat u_{\rm laser}(w)$.

- $\mathcal S_\phi$: $m=e^{i\phi}$.
- $\mathcal S_{A\phi}$: $m=a\,e^{i\phi}$ with $a=\sin^2\theta\in[0,1]$, a smooth parametrisation of $|m|\le1$.

Gradients come from the discrete adjoint of the numpy split-step (checked against finite differences) and are optimised by L-BFGS from several starts.

**H3a (refutes the card conjecture in the small-yield regime).** For the Gaussian at $N=3$, $\delta_3=0.02$ (deep in the exponentially small regime), the optimised phase-only mask raises $\eta_B$ above TL by more than a factor 2. I expect a factor of at least 10, because the yield is exponentially sensitive to $d_*$, which phase shaping can lower.

**H3b (large-yield regime).** Where $\eta_B^{\rm TL}\ge0.05$ (e.g. Gaussian $N=8$, $\delta_3=0.05$), the phase-only headroom is at most 2.

**H3c (chirp).**
- The best group-delay-dispersion (GDD) value alone gives headroom of at most 1.5 where $\eta_B^{\rm TL}\ge0.05$, consistent with Petty's about 1.4×.
- In the small-yield regime, GDD alone gives at least 2×.

**H3d (passive versus phase-only).** $H_{A\phi}/H_\phi\le1.2$ at every tested point: the amplitude freedom adds little.

**H3e (ceiling comparison).** Every optimised yield lies below the windowed program value of H1b. This is trivially expected given H1a/H1b. The card's "ceiling within a factor 3" fails wherever the optimised yield is below 0.3.

## H4. Raman

**Model M1:** M0 plus Raman with $f_R=0.18$ and the single-damped-oscillator response, $\tau_1=12.2$ fs, $\tau_2=32$ fs, at $T_0=50$ fs (Roy's $T_0$), with self-steepening off unless stated.

- **H4a.** The windowed program value is not exceeded. This is trivial given H1. The momentum constraint becomes one-sided ($\mathcal P$ non-increasing) and only loosens the program.
- **H4b.** In the small-yield regime, Raman lowers $\eta_B^{\rm TL}$, as in Roy Fig. 3(b) (by more than 10 dB at sech $N=2$, $\delta_3=0.02$).
- **H4c.** Phase masks optimised in M0 keep more than half of their M0 gain factor over TL when evaluated in M1 at the same $\delta_3$ and $N$.

## Amendments after freezing

**A1 (12:50 EDT, before any TOD run of these launches): $d_*$ values and held-out predictions for H2b.**
- Each $d_*$ is computed from the $\delta_3=0$ evolution in `runs/2026-10-16-claude-b-dw-oracle/` (`singularity.py`, `dstar.py`, `dstar2.py`).
  - Validation: the fit reproduces the exact $N=2$ breather $d(\xi)$ to $10^{-4}$.
  - Converged to 0.1% across grids up to $N_t=16384$.

  | Launch | $d_*$ | Attained at | Roy Eq. 6 exponent | Role |
  |---|---|---|---|---|
  | Gaussian, $N=3$ | 0.2015 | $\xi_*=0.3567$ | — | primary |
  | sech, $N=3$ | 0.1997 | $\xi\approx0.372$, and $1.1985$ by the period-$\pi/2$ reflection symmetry | 0.3142 | held out |
  | Gaussian, $N=4$ | 0.1322 | $\xi_*=0.2287$ | — | held out |

- **Procedure, fixed on the $N=2$ sech construction set before the held-out runs.**
  - Fit $\ln\eta_{\rm DW}=c+p\ln\delta_3-d/\delta_3$ to the four smallest-$\delta_3$ points of a sweep in which $d_*/\delta_3$ spans about 34–47.
  - On $N=2$ this gave $d=0.3788$ against the exact 0.37466 (+1.1%).
- **Frozen predictions.**
  - For each of the three launches, the fitted $d$ is within 4% of its $d_*$.
  - The local slope approaches $d_*$ from below as $\delta_3$ decreases.
  - Eq. 6's exponent (where defined) is excluded.
- **Sweeps** (gated yield, $\xi_f=2$ for the Gaussians, $\xi_f=2$ for sech $N=3$):
  - Gaussian $N=3$ and sech $N=3$: $\delta_3\in\{0.0043,0.0047,0.0052,0.0058,0.0066,0.0075,0.009,0.011\}$.
  - Gaussian $N=4$: $\delta_3\in\{0.0028,0.0031,0.0034,0.0038,0.0043,0.005,0.006\}$.

**A2 (12:01 EDT, before the held-out runs).**
- Correction: A1 was committed at 11:59 EDT (commit 85637bb), not 12:50 as its header says.
- For the Gaussian $N=4$ sweep, $\xi_f=1.0$ instead of 2. The reason is cost: at $\xi_f=2$ the grid would need $N_t=131072$.
  - The DW of the $N=4$ burst is emitted near $\xi_*=0.229$. By $\xi=1$ it lies more than 60 time units beyond the gate at every listed $\delta_3$.
  - The yield is expected to be saturated there.
- Gaussian $N=3$ and sech $N=3$ keep $\xi_f=2$.

**A3 (12:16 EDT).** Recorded after the held-out sweeps and the first GDD scans. At that point only the best GDD value of each scan had been seen: for the Gaussian at $N=3$, $\delta_3=0.01$, $C=-0.4$ gives 4.13× TL.

1. **Correction to A1 (post hoc).** The A1 scan for the Gaussian at $N=3$ stopped at $\xi=1.0$, but the frozen H2b definition takes the minimum over the whole propagation.
   - Over $\xi\le\xi_f=2$, the $\delta_3=0$ evolution recompresses at $\xi=1.103$ with $d=0.1923$, below the first-compression value 0.2015 (runs `dscan_full_gauss3.json`, `dstar_gauss3_second_compression.json`).
   - The held-out fit (0.1929) is therefore −4.3% from the A1 number, which fails the 4% tolerance, and +0.3% from the correctly computed definition. Both are reported, and the second is flagged as found after the result.
   - For the Gaussian at $N=4$ ($\xi_f=1$), the global minimum is the first compression (0.1317), so A1 stands.
2. **New frozen prediction (H3f, shaping acts through $d_*$).**
   - Statement: in the exponentially small regime, the yield of a shaped launch is $\eta\propto e^{-d_*[\phi]/\delta_3}$ to leading order, where $d_*[\phi]$ is the minimum over $\xi\le\xi_f$ of the strip width of the $\delta_3=0$ evolution of that launch.
   - Test: for the Gaussian at $N=3$, $\delta_3=0.01$, $\xi_f=2$, the measured GDD curve $\eta(C)/\eta(0)$ should agree with $\exp(-[d_*(C)-d_*(0)]/\delta_3)$ within a factor 2 for $C\in[-1,1]$.
   - Prefactor changes are ignored in the prediction. $d_*(C)$ is computed before the comparison is made.

**A4 (12:31 EDT, before the run): a length test of "minimum over $\xi\le\xi_f$".**
- Setup: Gaussian at $N=3$ with $\xi_f=1.0$, which ends before the second compression ($\xi=1.103$, $d=0.1923$). The first compression is at $\xi=0.357$ with $d=0.2015$.
- The same fit procedure (four points) is applied at $\delta_3\in\{0.0043,0.0047,0.0052,0.0058\}$. At every one of these the DW clears the gate by $\xi=1$.
- Prediction:
  - the fitted $d$ lies within 2% of 0.2015;
  - it exceeds the $\xi_f=2$ fit (0.1929) by at least 2.5%.

**Time-stamp correction.** A3 was committed at 12:13 EDT (f736bd3) and A4 at 12:19 EDT (3a852dc). The "12:16" and "12:31" in their headers were my estimates, not clock readings. The commit times are authoritative.

**A5 (frozen before the run; commit time authoritative): the singularity law with Raman (H4d).**
- Statement: in model M1 (Raman with $f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs at $T_0=50$ fs, no self-steepening), the gated DW exponent equals $d_*^{M1}$. This is the narrowest strip of the **Raman-including, TOD-free** evolution of the same launch (`h4_law.py dstar`, RK4IP, $N_t=16384$, $T_W=64$):
  - sech $N=2$: $d_*^{M1}=0.4410$;
  - Gaussian $N=3$: $d_*^{M1}=0.2346$.
- Observation, not frozen: the sech $N=2$ M1 local slopes (0.390 at $\delta_3\approx0.018$, 0.403 at 0.014 and 0.410 at 0.0115) were partly seen before $d_*^{M1}$ was known.
- **Frozen held-out test.**
  - Setup: Gaussian $N=3$ in M1, $\xi_f=2$, $\delta_3\in\{0.0055,0.006,0.0066,0.0073\}$.
  - Prediction:
    - the four-point fit gives $d$ within 4% of 0.2346;
    - it lies above the M0 fit (0.1929) by more than 10%.

**A6 (frozen before the forward runs): cubic-phase headroom predicted from $d_*$ alone (H3g).**
- Launch: Gaussian $N=3$, spectral phase $C_2w^2/2+C_3w^3/6$ with $(C_2,C_3)=(-0.2,-0.6)$.
- From `dstar_poly.py`, the blue-side $d_*$ over $\xi\le2$ is 0.17535 at $\xi=0.555$, against 0.19197 for TL.
- Prediction:
  - the gated DW headroom $\eta_{\rm DW}^{\rm mask}/\eta_{\rm DW}^{\rm TL}$ at $\xi_f=2$ is $\exp(0.01662/\delta_3)$ within a factor 2, i.e. 5.3 at $\delta_3=0.01$ and 15.9 at $\delta_3=0.006$;
  - the ratio of the two headrooms, $\ln H(0.006)/\ln H(0.01)$, is within 25% of $0.01/0.006=1.67$.

**A7 (commit time authoritative; written after the A6 result at $\delta_3=0.01$, before the A6 result at $\delta_3=0.006$).**
- **The A6 input was a fit artifact.** The value $d_*=0.17535$ at $\xi=0.555$ for $(C_2,C_3)=(-0.2,-0.6)$ is an isolated one-point outlier of the strip-width fit. Direct checks on two grids give $d(0.55)\approx0.455$.
  - The artifact was found by a verification run at about 12:33, before the A6 outcome was seen at 12:34:47.
  - The robust minimum (3-point running median) is $d_*=0.1944$, at the second compression ($\xi\approx1.19$); the first-compression minimum is 0.2071 at $\xi\approx0.39$.
- **A6 as frozen is refuted** at $\delta_3=0.01$: measured $H_{\rm gated}=0.755$, against a prediction of 5.27.
- **Corrected prediction (law unchanged, corrected $d_*$).** $H=\exp(-(0.1944-0.19197)/\delta_3)$, which gives 0.78 at $\delta_3=0.01$ (seen: 0.755) and **0.667 at $\delta_3=0.006$ (not yet seen; frozen here within 30%)**.
- The `dstar_poly.py` scan was rerun with the robust minimum.

**A8 (frozen before `mask_transfer.py` is run on it): transfer of an optimised mask's DW headroom (H3h).**
- The mask is the best phase-only mask from the gated optimisation at Gaussian $N=3$, $\delta_3=0.01$, $\xi_f=2$ (`opt_N3_d0.01_xi2_it100_gated.json`, best of three starts). Seen so far: the TL start reached 2.04× in the gated objective.
- Let $H_{0.01}$ be its gated headroom.
- Predictions:
  1. $d_*[\text{mask}]$, computed from the $\delta_3=0$ evolution, is below $d_*^{\rm TL}=0.19197$ by $0.01\ln H_{0.01}$, within 30% of that decrement.
  2. The gated headroom at $\delta_3=0.006$ is $H_{0.01}^{0.01/0.006}$ within 30%. At $\delta_3=0.0075$ it is $H_{0.01}^{0.01/0.0075}$ within 30%.

**A9 (frozen before the $d_*$ values for these launches were seen; `dstar_card.py` is running): the card-regime collapse (H2d).**
- Statement: the TL band yield $\eta_B(\xi_f=2)$ of Gaussian launches depends on $(N,\delta_3)$ mainly through $x=d_*(N)/\delta_3$, even outside the exponentially small regime.
- Basis: Gaussian $N=3$ and 4 (with $d_*=0.1923$ and $0.1317$), whose curve is $\eta_B(x)$ = 8.9e-4 at $x=19.2$, 0.018 at 13.2, 0.052 at 9.6, 0.107 at 6.6, 0.106 at 6.4, 0.152 at 4.4, 0.164 at 3.84 and 0.210 at 2.64.
- Inverting this curve against the already-seen $N=6$, 8, 10 card yields predicts:
  - $d_*(6)=0.080\pm15\%$;
  - $d_*(8)=0.053\pm15\%$;
  - $d_*(10)=0.037\pm25\%$;
  - and, by interpolation, $d_*(5)\approx0.10\pm20\%$.
- These are to be compared with the robust $d_*$ from the $\delta_3=0$ evolution (`dstar_card_*.json`).

**A10 (frozen before computing): optimised masks in the large-yield regime act through $d_*$ (H3i).**
- Statement: if the card-regime collapse $\eta_B\approx F(d_*/\delta_3)$ (A9) also governs shaped launches, then the band-objective phase optimum should have a smaller $d_*$ (from the $\delta_3=0$ evolution of the shaped launch, minimum over $\xi\le2$).
- The value is predicted by inverting $F$ through the TL card points:
  - $N=3$, $\delta_3=0.02$ mask (`opt_N3_d0.02_xi2_it60.json`, $\eta=0.080$): $d_*=0.153\pm15\%$, against TL 0.1922;
  - $N=3$, $\delta_3=0.05$ mask (`opt_N3_d0.05_xi2_it150.json`, $\eta=0.247$): $d_*=0.095\pm25\%$.

**A11 (frozen before the run): a further held-out launch for H2b.**
- Launch: sech $N=4$, model M0, $\xi_f=2$. From `dstar_card_a.json` (robust minimum over $\xi\le\pi/2$, one breather period), $d_*=0.1342$, attained at $\xi=1.335$ and, by the period reflection, at about 0.236.
- Sweep: $\delta_3\in\{0.0029,0.0032,0.0035,0.0039\}$, so $d_*/\delta_3\approx34$–46.
- Prediction:
  - the A1 four-point fit gives $d$ within 4% of 0.1342;
  - Roy's exponent $\pi/(2\cdot7)=0.2244$ is excluded.
