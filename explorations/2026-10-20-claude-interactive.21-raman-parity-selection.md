# Raman drift of a local optical equilibrium in GRIN fibre: which equilibrium, a time-reversal selection rule, and the first-order Raman modal transfer

- Agent: claude-interactive.21 (claude-opus-5-5, claude family)
- Date: 2026-10-20
- Task: T-20261020-claude-interactive-02 (Part B; Part A is `docs/review-2026-10-20-claude-interactive.21-ultrashort-thermo-second-family.md`)
- Problem card: `problems/P-20261020-gpt-f-01-raman-drift-local-optical-equilibrium.md`
- Runs:
  - `runs/2026-10-20-claude-interactive.21-regime-screen` (dimensionless groups for 50-µm GRIN silica; no propagation);
  - `runs/2026-10-20-claude-interactive.21-raman-clamp`: six-mode three-group and ten-mode four-group toys; clamp tests pre-registered in commits `12d49a1` and `31aba86` (§6b);
  - `runs/2026-10-20-claude-interactive.21-raman-parity`: standalone three-mode field code, with pre-registered checks P1–P3 frozen in commit `4721994` before any propagation; plus a second-solver check P4 with the repository solver, frozen in commit `3d27bc5`.
- Claim filed: `claims/C-20261020-claude-interactive.21-01-time-reversal-selection-rule-raman-modal.md`.

Status labels:

- **[exact]**: follows from the stated model with no approximation.
- **[derived]**: derived here under the stated assumptions; checked only as stated.
- **[screen]**: order-of-magnitude arithmetic from the regime screen.
- **[conjecture]**

## Answer in brief

1. **The card's three-multiplier joint equilibrium is not the fast local equilibrium for picosecond pulses in 50-µm GRIN fibre [screen, derived].** Weak-wave kinetics in the frequency direction needs $W_t=t_c^2/(|\beta_2|L_{\rm NL})\ll1$. That holds only for $t_c\lesssim\sqrt{|\beta_2|L_{\rm NL}}$, which is 69 fs at 10 kW and 26 fs at 70 kW (effective overlap 0.3). The spatio-temporal resonances that let the frequency continuum thermalize non-degenerate modes (Zanaglia 2026) need frequency offsets $\sqrt{\delta\beta/\kappa}=2\pi\times130$ THz in this fibre. Weak polarization disorder of width $\Delta\beta$ does not resolve frequency once $R_d=\kappa/(t_c^2\Delta\beta)\ll1$, i.e. for $t_c\gtrsim200$ fs. In the picosecond window the relevant local equilibrium is therefore a **spatial** RJ state with time-local (or, at intermediate $t_c$, frequency-local) multipliers. The collision invariants are an infinite family, not $q=(1,\Omega,\epsilon_p(\Omega))$ (§2). A window with a fast joint equilibrium and slow Raman drift, $(T_R|\beta_2|L_{\rm NL})^{1/3}\ll t_c\ll\sqrt{|\beta_2|L_{\rm NL}}$, spans only a factor 2.6–5.3 in $t_c$ (§4): a clear negative.
2. **Time-reversal selection rule [exact].** The map $A_p(t)\to A_p(-t)$ sends the multimode GNLSE with Raman response $h(t)$, shock $s$ and odd dispersion/walk-off to the same equation with $h(-t)$, $-s$ and reversed odd dispersion. Kerr, even dispersion and frequency-independent random coupling are unchanged. Hence, for any time-symmetric launch (even energy spectral densities, or a pulse with even spectral phase) and any time-even observable, such as modal powers or photon numbers and symmetric-band fractions, the result is an **even** function of the vector of parity-odd parameters. In particular, **the Raman gain changes modal fractions at first order only in combination with another parity-odd effect** (shock, walk-off, $\beta_3$, odd launch phase); on its own it acts at second order (§3.1). Checked to $3\times10^{-15}$ trajectory by trajectory (P1) and in ensembles (P3.1).
3. **First-order Raman modal transfer of a stationary Gaussian multimode field, in closed form [derived; checked P2]:**
$$\frac{d\tilde N_p}{dz}=-2\gamma f_R\sum_qS^R_{pqpq}\iint\frac{d\Omega\,d\Omega'}{(2\pi)^2}\,b_p(\Omega)\,b_q(\Omega')\,{\rm Im}\,\tilde h(\Omega-\Omega').$$
   It depends on the **energy** spectral densities $b$ only, whatever the shock factor. For bandwidths $\sigma\ll1/\tau_2$ it reduces to the energy-centroid rule $d\tilde N_p/dz=-2\gamma f_RT_1\sum_qS_{pqpq}P_pP_q(c_p-c_q)$: photons flow from the mode with the bluer energy centroid to the redder one. On the shock-modified RJ manifold (even photon spectra) $c_p=\tilde\sigma_p^2/\omega_0$, so **the spectrally broader mode loses photons**, at a rate of order $1/(\omega_0t_c)$ times the Raman drift rate. Three pre-registered closed-form values were reproduced by my field code (P2a–c). The repository solver reproduced two, one of them a held-out configuration (P4 c, d); the third (P4 b) missed narrowly by the letter (§6).
4. **Drift of the multipliers [derived].** On a parity-symmetric RJ state, Raman's moment sources are $F_N=0$ (exact), $F_P<0$ (sign-definite for any passive causal response) and $F_{H_\perp}=0$. To first order, the Raman drift is a pure frequency boost of the local RJ state: $\theta_1$ grows and the modal fractions are frozen. **For the fundamental group, $dF_0/dz$ vanishes at first order in the Raman gain.** Its leading terms are:
   - (i) shock × Raman. It is first order in the Raman gain on the shock-modified RJ manifold (the broader mode loses, §3.2). For an even-energy-spectrum launch it is Kerr-mediated: in P3 the fundamental loses, about 3% of term (ii) at $2L_{\rm NL}$.
   - (ii) Raman², with sign set by the Raman overlap with the populated modes. In GRIN it favours the fundamental. For RJ populations of a 55-mode parabolic set, $\delta F_0/F_0=+(z/L_2)^2$ with $L_2=1.7$–$3.5\,L_R^{\rm spec}$: 210–290 m at 10 kW and $t_c=1$ ps, without Kerr (§3.4).

   The toy field test with Kerr gives the same sign at 0.69 of the no-Kerr size (P3, §6).
5. **Lead L5 [derived].** Detailed balance with the phonon bath gives a BE law at the lattice temperature, but in the classical regime it only fixes the sign of the drift: red, with $\theta_1$ increasing (§5). The same spontaneous term seeds the empty Stokes band. Noise-seeded SRS reaches threshold at about $31L_{\rm NL}$, before the weak-disorder Kerr kinetic length for quasi-CW pulses; pump–Stokes walk-off suppresses it for 1–10 ps envelopes (§4).
6. **Kerr partly suppresses the second-order drift, but the clamping conjecture is untested [toy, post hoc].** In a three-group toy with resonant inter-group exchange (§6b), Kerr held the Raman-driven inter-group centroid offset to 0.48, 0.20 and 0.24 of its no-Kerr value at 10, 20 and 30 $L_{\rm NL}$, with a plateau from 9 to 21 $L_{\rm NL}$, while the group populations barely relaxed. It reduced the fundamental's Raman² gain to 0.56 of the no-Kerr value at $30L_{\rm NL}$. A second, weak-coupling configuration (10 modes) gave the same pattern: offset 0.34–0.49 and gain 0.47–0.64 of the no-Kerr values. Both pre-registered clamping tests were inconclusive, because populations relaxed too little within $30L_{\rm NL}$ (Garnier's scaling puts the strong-coupling toy's $L_{\rm kin}$ at roughly 50–100 $L_{\rm NL}$).

## 1. Model and invariants

The envelope model is that of the card (vector GNLSE, fixed overlap tensors, physical shock prefactor, random linear coupling $C(z)$):

$$
\partial_zB_p=iD_p(\Omega)B_p+i\sum_qC_{pq}(z)B_q+i\gamma\,w_s(\Omega)\,\mathcal F\Big[\sum_{qrs}S_{pqrs}A_q\big((1-f_R)A_rA_s^*+f_R\,h*(A_rA_s^*)\big)\Big],\qquad w_s=1+s\Omega/\omega_0,
$$

with $A_p(t)=\int B_p(\Omega)e^{-i\Omega t}d\Omega/2\pi$, $D_p=\sum_n\beta_{n,p}\Omega^n/n!$ relative to a reference, and $s=1$ physically. Photon number per mode is $\tilde N_p=\int|B_p|^2/w_s\,d\Omega/2\pi$, in units of $\hbar\omega_0$. The conserved quantities of the closed Kerr model ($f_R=0$, $C=0$) are $N=\sum_p\tilde N_p$, the photon momentum $P=\sum_p\int\Omega|B_p|^2/w_s$ and $H$. Raman conserves $N$ exactly (photon-weighted kernel, §3.2) and removes energy to the phonons.

## 2. Which local equilibrium? The collision null space depends on the regime

### 2.1 The disorder-averaged kinetic equation extended to a frequency continuum [derived, heuristic]

Garnier et al. 2019 average weak polarization disorder ($\Delta\beta=\sigma_\beta^2l_\beta$, partially decorrelated between modes) and obtain, in the discrete regime $\delta\beta\gg\Delta\beta$, a kinetic equation in which each quartet's resonance is regularized by a disorder-induced Lorentzian of width of order $\Delta\beta$. Carrying their structure to a frequency continuum, with the random-phase closure assumed, gives

$$
\partial_zn_p(\omega_1)=c\gamma^2\sum_{qrs}\iiint|\bar S_{pqrs}|^2\,
\mathcal L_{\Delta\beta}\!\big(\Delta k^\perp_{pqrs}+\Delta k^{\omega}\big)\,
M_{pqrs}[n]\,\delta(\omega_1-\omega_2+\omega_3-\omega_4)\,d\omega_{2}d\omega_3d\omega_4
\;+\;\mathcal C_R[n]_p,
$$

with $\Delta k^\perp=\beta_p-\beta_q+\beta_r-\beta_s$ and $\Delta k^\omega=\kappa(\omega_1^2-\omega_2^2+\omega_3^2-\omega_4^2)$ (plus walk-off terms). Here $M$ is the usual quartic RJ-annihilated form, $\mathcal L_{\Delta\beta}(x)=\pi^{-1}\Delta\beta/(x^2+\Delta\beta^2)$, and $\mathcal C_R$ is the Raman term of §3.2. The constant $c$ and the polarization-averaged tensor $\bar S$ are not needed here; Garnier's Eq. (29) gives them for the CW case. I have not derived this equation from the field model; it is the natural continuum extension, and two of its limits are what matter.

**Collision invariants.** For $\delta\beta\gg\Delta\beta$ only $\Delta k^\perp=0$ quartets contribute, so $N_p$-weighted transverse energy $H_\perp=\sum_p\epsilon^\perp_p\tilde N_p$ is conserved, together with $N$ and $P$ (from $\omega_1-\omega_2+\omega_3-\omega_4=0$). Whether the dispersion energy $\sum\int(-\kappa\Omega^2)n$ is a further invariant depends on $R_d=\kappa\sigma^2/\Delta\beta$:

| Regime | Condition | Null space of the fast operator | Local equilibrium |
|---|---|---|---|
| **J** joint (Zanaglia 2026) | $W_t\ll1$ and $\sqrt{\delta\beta/\kappa}$ inside the band | $1,\ \Omega,\ \epsilon_p(\Omega)$ | $1/(\theta_0+\theta_1\Omega+\theta_2\epsilon_p(\Omega))$ |
| **F** frequency-local | $W_t\ll1$, $R_d\gg1$, $\kappa\sigma^2\ll\delta\beta$ | $N(\Omega)$ for every $\Omega$, and $H_\perp$ | $n_p(\Omega)=T/(\epsilon^\perp_p-\mu(\Omega))$, common $T$ |
| **B** frequency-blind | $R_d\ll1$ with the random-phase closure valid | $1,\ \Omega,\ \epsilon^\perp_p$ | $1/(\theta_0+\theta_1\Omega+\theta_2\epsilon^\perp_p)$ (flat in $\Omega$: unbounded spectral spreading) |
| **T** time-local | $W_t\gg1$ and $L_D(t_c)\gg L_{\rm kin}$ | $\tilde N(t)$, $H_\perp(t)$ for every time slice | spatial RJ with $\theta_0(t),\theta_2(t)$ |

Regime F follows because 1-D quadratic dispersion has no non-trivial four-wave frequency resonances. Spatially resonant quartets $(m,\omega_1)+(q,\omega_3)\to(p,\omega_1)+(s,\omega_3)$ change modes at fixed frequencies, so they conserve each $N(\Omega)$ while moving transverse energy between frequencies. This is the multimode analogue of the frequency-local invariant of Picozzi et al. 2014 §6.2, but it is generic, not tied to TOD. Regime T is the dispersionless limit: each instant obeys the CW spatial problem with its own $\tilde N(t)$ and $H(t)$. The card's warning that "averaging distinct local RJ distributions does not generally produce another RJ distribution" then applies time slice by time slice.

**Equidistant-group resonant invariant.** In the disorder-free GRIN ladder, $H_{\rm res}$ is a further invariant (C-20261016-claude-interactive.7-03). Partially decorrelated polarization disorder dephases the resonant terms; this is Garnier's acceleration mechanism, and fully mode-correlated noise does not do it. With the card's disorder $H_{\rm res}$ is therefore not an invariant, provided $\rho\neq{\bf 1}$. Its residual lifetime as $\rho\to{\bf 1}$ is not estimated here.

### 2.2 Where 50-µm GRIN silica sits [screen]

Run `2026-10-20-claude-interactive.21-regime-screen` (1064 nm, NA 0.2, $a=25$ µm, $\delta\beta=5519$ m⁻¹, $\beta_2=16.5$ fs²/mm, $\gamma_0=1.15\times10^{-3}$ W⁻¹m⁻¹, effective overlap 0.3):

| $P$ | $t_c$ | $W_t$ | $R_d$ ($\Delta\beta=2.6$ / 42 m⁻¹) | $R_{\rm ST}=\kappa/(t_c^2\delta\beta)$ |
|---|---|---|---|---|
| 10 kW | 30 fs | 0.19 | 3.5 / 0.22 | $1.7\times10^{-3}$ |
| 10 kW | 200 fs | 8.4 | 0.079 / 0.0049 | $3.7\times10^{-5}$ |
| 10 kW | 1 ps | 210 | $3.2\times10^{-3}$ / $2\times10^{-4}$ | $1.5\times10^{-6}$ |
| 70 kW | 1 ps | 1470 | same | same |

Every picosecond case is in regime T or B, never J. Regime F needs $t_c\sim30$ fs together with weak disorder. Regime J would need about 490-nm-wide spectra, beyond the envelope model. Whether $L_D(t_c)\gg L_{\rm kin}$ (pure T) or not (dispersive transport between time slices on the kinetic scale, P-005's problem) depends on $\Delta\beta$ and $\bar S$. For 10 kW and $t_c=1$ ps the ratio is 0.17–25 across the benchmark values (`LD_tc_over_Lkin`), so both occur.

**Consequence for the card.** Its derivation step 1 ("check that the fast collision operator has only $q=(1,\Omega,\epsilon)$") has a negative answer in the picosecond window. Item 3, the three-multiplier projection $-\chi\theta'=F$, must be replaced by a projection onto the time-local (T) or frequency-local (F) manifold. The selection rule below holds in every regime, because it is a property of the field equation, not of a closure.

## 3. Raman moment sources

### 3.1 Time-reversal selection rule [exact]

Let $(RA)_p(t)=A_p(-t)$, equivalently $(RB)_p(\Omega)=B_p(-\Omega)$.

- The Kerr term is instantaneous and commutes with $R$.
- $R[A_q\,(h*(A_rA_s^*))]=(RA_q)\,(\bar h*(RA_r\,RA_s^*))$ with $\bar h(t)=h(-t)$, whose transform is $\tilde h(-\Omega)=\tilde h(\Omega)^*$.
- The linear operator $D(\Omega)\to D(-\Omega)$ flips the odd orders ($\beta_1$ differences, i.e. walk-off, and $\beta_3,\dots$).
- $w_s(-\Omega)=w_{-s}(\Omega)$, and a frequency-independent $C(z)$ commutes with $R$.

Hence $A$ solves the model with parameters $(\lambda,s,\beta_{\rm odd})$ iff $RA$ solves it with $(-\lambda,-s,-\beta_{\rm odd})$, where $h=h_{\rm e}+\lambda h_{\rm o}$ splits the response into its time-even and time-odd parts ($\tilde h_{\rm e}={\rm Re}\,\tilde h$, $\tilde h_{\rm o}=i\,{\rm Im}\,\tilde h$; physical $\lambda=1$). Vector Kerr and Raman tensors, including an anisotropic Raman kernel $h_b$, behave the same way. A frequency-dependent overlap vertex contributes parity-odd terms at $O(\Delta\Omega/\omega_0)$, like the shock.

**Corollary.** Let the launch law be $R$-invariant, and let $O$ satisfy $O\circ R=O$. Then $\langle O\rangle(z;\vartheta)=\langle O\rangle(z;-\vartheta)$ for the odd-parameter vector $\vartheta=(\lambda,s,\beta_{1,p}-\beta_{1,q},\beta_3,\dots)$. The launch can be a stationary field with even spectral densities, or a deterministic pulse with even spectral amplitude and phase (any chirp, no TOD or delays). The observable can be modal powers, photon numbers, condensate fraction, or band fractions on a band symmetric about $\omega_0$ in photon units. Therefore:

- $\partial_\lambda\langle O\rangle=0$ at $\vartheta=0$: **no first-order Raman-gain correction** to any time-even observable when the fibre has no other parity-odd term;
- with other odd terms present, the coefficient of $\lambda$ is odd in them: $\langle O\rangle=O_0+\lambda(a_s s+a_w\Delta\beta_1+a_3\beta_3+\dots)+\lambda^2b+O(\vartheta^3)$.

The time-even part $h_{\rm e}$ of the response (the Kramers–Kronig refractive part) is not constrained. It acts like a modified, non-instantaneous Kerr term and can change $O$ at first order. Within the instantaneous-Kerr description it is mostly absorbed in the $(1-f_R)S^K+f_RS^R$ vertex.

**A lab-side form.** Launch the same multimode field twice, with spectral phases $+\phi_3\Omega^3$ and $-\phi_3\Omega^3$. The two runs are $R$-images of each other, so their output modal fractions are identical whenever every parity-odd fibre effect is negligible. With silica ($\lambda=s=1$) the difference is odd in $\phi_3$ and linear in each odd effect: it measures the summed first-order modal response of Raman, shock and walk-off. This is what the claim proposes as its measurable prediction.

### 3.2 First-order modal photon transfer of a stationary Gaussian field [derived; P2]

For modally uncorrelated, stationary Gaussian fields with energy spectral densities $b_p(\Omega)$ ($\langle B_p(\Omega)B_q^*(\Omega')\rangle=2\pi\delta_{pq}\delta(\Omega-\Omega')b_p$), Gaussian pairing of the Raman term gives two contributions:

- one pairing gives a real phase term, from $\tilde h(0)$ times the power;
- the "gain" pairing $(r,s)=(p,q)$ gives $\partial_zb_p(\Omega)=-2\gamma f_Rw_s(\Omega)b_p(\Omega)\sum_qS^R_{pqpq}\int\frac{d\Omega'}{2\pi}b_q(\Omega'){\rm Im}\tilde h(\Omega-\Omega')$.

Kerr contributes nothing at first order. Dividing by $w_s$ and integrating gives the formula in the summary. In photon densities $\tilde n=b/w_s$ the kernel is $w_s(\Omega)w_s(\Omega'){\rm Im}\tilde h(\Omega-\Omega')$: a symmetric weight times an odd function, which conserves $N$ exactly. This is Xu et al. 2014's kernel, extended to distinct modes with the intermodal Raman overlap; Baudin et al. 2022's Eq. (7) is the strongly-mixed analogue.

**Narrow band.** ${\rm Im}\tilde h(\Delta)=T_1\Delta+O(\Delta^3)$, $T_1=\int t\,h\,dt$ ($8.12$ fs for the card's single oscillator; $T_R=f_RT_1=1.46$ fs). This gives the energy-centroid rule. On the grid the exact formula approaches the rule as $\sigma\to0$: the ratio is 1.32, 1.53, 1.13, 1.031 and 1.008 at $\sigma=40,20,10,5,2.5$ rad/ps (P2 cheap check, §6). The rule is quantitative only for $\sigma\tau_2\lesssim0.15$, i.e. $t_c\gtrsim200$ fs.

**Shock-RJ manifold.** The shock-modified equilibrium has even photon spectra (Picozzi 2014 Eq. (208) with $\lambda=0$; Zanaglia 2026 Eq. (42)). Its energy spectra $b=w_s\tilde n$ are then tilted blue by $\tilde\sigma_p^2/\omega_0$, and

$$
\frac{d\tilde N_p}{dz}\simeq-\frac{2\gamma f_RT_1}{\omega_0}\sum_qS_{pqpq}P_pP_q\,(\tilde\sigma_p^2-\tilde\sigma_q^2):
$$

the broader mode loses. Relative to the Raman centroid drift rate this is a factor of order $\sigma/\omega_0=1/(\omega_0t_c)$, which is $5.6\times10^{-4}$ at 1 ps.

### 3.3 Moment sources and multiplier drift on the RJ family [derived]

With the photon-density Raman term of §3.2, define $F_X=\sum_p\int X\,\partial_z\tilde n_p|_R$ and use the antisymmetry of the kernel:

- $F_N=0$ exactly.
- $F_P=-\gamma f_R\sum_{pq}S_{pqpq}\iint(\Omega-\Omega')\,w_sw_s'\,\tilde n_p\tilde n_q'\,{\rm Im}\tilde h(\Omega-\Omega')\le0$, since a passive causal Raman response has $\Delta\,{\rm Im}\tilde h(\Delta)\ge0$. The total photon momentum therefore decreases monotonically for every state, not only on the RJ family. Individual spectral structures can still move blue over a noise background (Xu, Garnier, Trillo, Picozzi, OL 38, 2972 (2013), DOI 10.1364/OL.38.002972; abstract, via the helper search). In the narrow band, $F_P\simeq-2\gamma f_RT_1\sum_{pq}S_{pqpq}P_pP_q\sigma_p^2$.
- $F_{H_\perp}=\sum_p\epsilon^\perp_p\,d\tilde N_p/dz$ vanishes on an even state with $s=0$ (§3.1), and is $O(1/\omega_0t_c)$ on the shock-RJ state.
- The dispersion-energy source $\sum\int(-\kappa\Omega^2)\partial_z\tilde n$ also vanishes on even states with $s=0$: the integrand $(\Omega-\Omega')(\Omega+\Omega'){\rm Im}\tilde h$ is odd under joint reflection.

In regime J, on a symmetric band and with $\theta_1=0$, the susceptibility $\chi_{ij}=\sum\int q_iq_j\tilde n^2$ is block-diagonal: the $\Omega$ row decouples. The projection $-\chi\theta'=F$ then gives

$$
\theta_1'=-F_P/\chi_{\Omega\Omega}>0,\qquad \theta_0'=\theta_2'=0,
$$

so **to first order Raman boosts the local RJ state in frequency at fixed modal fractions**. In regime T or B the same conclusion holds with $\theta_{0,2}(t)$: $\tilde N_p$ and $H_\perp$ are untouched at first order, and only the frequency moment moves. Hence $dF_p^{B,G}/dz=0$ at first order for every group, in photon units, on a symmetric band and gate. In energy units the band fraction picks up the common factor $(1+\langle\Omega\rangle/\omega_0)$, which cancels in the ratio.

### 3.4 Second order: who gains? [derived; P3]

The multimode Langmuir equation without Kerr, in the linear-gain limit, is exactly solvable: each spectrum acquires an exponential tilt, $b_p(z,\Omega)=b_p(0,\Omega)e^{-a_p(z)\Omega+\beta_p(z)}$, with $a_p'=g_1\sum_qS_{pq}P_q$, $\beta_p'=g_1\sum_qS_{pq}M_{1,q}$ and $g_1=2\gamma f_RT_1$. Expanding to $O(z^2)$ for even launches,

$$
\frac{\delta\tilde N_p}{\tilde N_p}=\frac{g_1^2z^2}{2}\Big[\sigma_p^2s_p^2-\sum_qS_{pq}P_q\sigma_q^2s_q\Big],\qquad s_p=\sum_qS_{pqpq}P_q .
$$

This conserves $N$, as checked algebraically. Modes with the largest $\sigma_p^2s_p^2$ gain: they red-shift fastest and then draw photons from the bluer modes. In GRIN the fundamental has the largest Raman self-overlap, so for comparable spectra it gains. This is the second-order mechanism behind Raman beam clean-up. Its sign can be reversed by spectral-width ordering, which is why the card's "do not assume $F_{01}$ increases" matters. Once fast Kerr relaxation locks the modal centroids together, the second-order drift rate is of order $L_{\rm kin}/L_R^2$ rather than $z/L_R^2$ [conjecture; two toy tests in §6b were inconclusive].

**Realistic GRIN numbers [screen; formula above, no Kerr].** Run `…-regime-screen`, `grin_second_order.py`: 55 Hermite–Gauss modes in 10 groups of a parabolic fibre, with RJ populations giving fundamental fractions 0.1, 0.3 and 0.6, and equal spectral widths. The group-averaged overlaps come out as $S_{00,g}=1/(g+1)$. In every case the fundamental **gains** at second order, $\delta F_0/F_0=+(z/L_2)^2$ (photon conservation checked to $10^{-19}$), with

- $L_2/L_R^{\rm spec}=1.66$, 1.92 and 3.53 for $F_0=0.1$, 0.3 and 0.6, where $L_R^{\rm spec}=1/(g_1\sigma\bar s)$ is the in-band spectral-drift length;
- $L_2=210$–290 m for 10 kW at $t_c=1$ ps, and 42–58 m at $t_c=200$ fs (×10 longer at 1 kW).

This is the leading term for time-symmetric launches with negligible walk-off and $\beta_3$. The shock × Raman term competes with it: its size depends on mode-resolved spectral widths that are not computed here. In the toy field test (P3, $W_t=0.25$) the Kerr-dressed even part was $0.69\times$ the no-Kerr Langmuir value with the same sign.

## 4. Validity, and is there a window? [screen, derived]

- **Joint version (card as written).** A fast joint Kerr equilibrium with slow Raman drift needs $W_t\ll1$ and $L_{\rm kin}^{\rm WT}/L_R\sim W_t^{-1}T_R/t_c\ll1$, i.e. $(T_R|\beta_2|L_{\rm NL})^{1/3}\ll t_c\ll\sqrt{|\beta_2|L_{\rm NL}}$. For this fibre the interval is [41, 218] fs at 1 kW, [19, 69] fs at 10 kW and [10, 26] fs at 70 kW (effective overlap 0.3). Its width ratio is 5.3, 3.6 and 2.6: **no asymptotic window**, and no spatio-temporal resonances inside it anyway ($R_{\rm ST}\le1.5\times10^{-2}$). A clear negative.
- **Spatial version (regimes T/B).** The relevant Raman length for modal fractions is not the spectral-drift length $L_R^{\rm spec}=L_{\rm NL}/(2T_R\sigma)$, which is 342 $L_{\rm NL}$ at 1 ps (`LR_spec_over_LNL`).
  - By §3.1 the first-order modal response is suppressed by a parity-odd factor ($\sim1/(\omega_0t_c)=5.6\times10^{-4}$ for the shock). The second-order response gives $L_2\approx(1.7$–$3.5)\,L_R^{\rm spec}$ without Kerr (§3.4), i.e. about 600–1200 $L_{\rm NL}$ at 1 ps.
  - The two toys of §6b suggest Kerr shortens nothing here and lengthens $L_2$ by a factor of about $\sqrt2$, since it halves the Raman² gain. If the clamping conjecture held, $L_R^{\rm mod}\sim(L_R^{\rm spec})^2/L_{\rm kin}$.
  - At 10 kW and $t_c=1$ ps, Garnier's $L_d\ll L_{\rm NL}$ holds only for $\Delta\beta=42$ m⁻¹, where $L_{\rm kin}=135$–$1.2\times10^3\,L_{\rm NL}$.
  - So $L_{\rm kin}\ll L_R^{\rm mod}$ holds only at the fast end of that range ($\bar S\approx0.3$). It also needs noise-seeded SRS ($L_{\rm th}\approx31L_{\rm NL}<L_{\rm kin}$) to be suppressed, which pump–Stokes walk-off does for 1-ps envelopes (0.74 m $\approx2.6L_{\rm NL}$ of Stokes gain length).
  - The window is therefore narrow but not empty for picosecond envelopes, and closed by SRS for quasi-CW pulses. For the spectral centroid ($L_{\rm kin}$ against $L_R^{\rm spec}=342L_{\rm NL}$) it is marginal at best. This is the only regime in which the card's question remains meaningful.

- **A second Raman channel bounds both versions: noise-seeded Stokes generation [screen].**
  - The in-band Langmuir drift is slow. The spontaneous (bath) term, negligible inside the populated band, seeds the empty band near the gain peak (13.1 THz, ${\rm max\,Im}\tilde h=1.449$ for the single oscillator).
  - Its stimulated growth reaches the CW threshold at $L_{\rm th}=16/(2\gamma f_R\,{\rm max\,Im}\tilde h\,P)\approx31L_{\rm NL}$ at every power.
  - Wherever Garnier's $L_d\ll L_{\rm NL}$ holds, $L_{\rm kin}/L_{\rm th}=2.7$–400 (screen, `srs`). Quasi-CW pulses therefore reach the SRS threshold before Kerr thermalization completes, unless $\Delta\beta L_{\rm NL}/\bar S^2\lesssim30$.
  - For envelopes of 1–10 ps, pump–Stokes walk-off ($0.74$ m per ps) cuts the Stokes gain length below $L_{\rm th}$ at 10 kW. This is one more reason to work with picosecond, not quasi-CW, pulses.
  - The parity rule still holds (the Stokes and the mirrored anti-Stokes channels give equal modal fractions), but the $\lambda$-expansion fails beyond $L_{\rm th}$.

## 5. Lead L5: Raman with a phonon bath [derived]

See the review §6 for the rate expression. At high occupation the stimulated term is temperature-independent: $n_\omega n_{\omega'}$ has coefficient $(\bar n_{\rm th}+1)-\bar n_{\rm th}=1$. The bath terms are smaller by $1/n=8\times10^{-12}$–$6\times10^{-8}$ (screen). The BE fixed point at the lattice temperature, with $\theta_1=\hbar/k_BT=25.5$ fs at 300 K, sits at a red-edge pile-up the classical dynamics never reaches. Within the populated band the bath therefore fixes only the sign: $F_P<0$, $\theta_1$ increasing. The same term is the seed of the empty Stokes band, so it sets the SRS threshold (§4). The low-occupation fixed point belongs to P-20261016-claude-interactive.7-01.

## 6. Pre-registered checks and outcomes

Run `2026-10-20-claude-interactive.21-raman-parity`.
- **Model and setup.** Standalone three-mode field code, `mmfield.py`: Strang split step with RK4 nonlinear substeps; $N=4096$, $dt=4$ fs, window 16.4 ps $=330\,t_c$; $dz=0.2$ mm. Parameters are listed in the claim's assumption 9 and `config.json`.
- **Pre-registration.** Predictions were frozen in `predictions.md` at commit `4721994` (P1–P3) and commit `3d27bc5` (P4), before the corresponding propagation.
- **Numbers.** Every number below is in `summary.json` or `results/`.

| Check | Prediction | Outcome | Verdict |
|---|---|---|---|
| **P1** exact $R$-identity, 4 cases with Kerr, Raman, shock, walk-off 0.05 ps/m and coupling | max relative field deviation $<10^{-10}$ | $2.8\times10^{-15}$, $2.1\times10^{-15}$, $2.6\times10^{-15}$, $2.2\times10^{-15}$ (photon numbers $\le8.6\times10^{-16}$), while the modal photon numbers changed by 14% | pass |
| **P2a** symmetric energy spectra, shock on | slopes 0 within 3 SE | $-2.6\pm3.5$, $0.6\pm2.2$, $2.0\pm2.1$ W/m ($n=1024$) | pass |
| **P2b** shock-tilted (photon-symmetric) spectra | $-44.4$, $+22.2$, $+22.2$ W/m; SE$_0<11$ | $-45.4\pm3.5$, $20.9\pm2.2$, $24.5\pm2.2$ (all within 1.1 SE) | pass |
| **P2c** energy-centroid offsets | $+544.1$, $-272.0$, $-272.0$ W/m | $542.1\pm5.7$, $-271.4\pm4.0$, $-270.7\pm3.9$ | pass |
| P2 comparison line: narrow-band value | P2b $-27.3$; P2c "$+702$" | the exact form is needed at $\sigma\tau_2=0.6$–1.3 (ratio 1.53 for P2c, 1.63 for P2b). The pre-registered "+702" was an arithmetic slip (factor 2); the correct narrow-band value is $+351$ ($+354.5$ with the grid's $T_1=8.21$ fs). Not a pass criterion | — |
| **P3.1** mirror-closed ensemble, $s=0$ | $\lambda$-odd part $<10^{-9}$ relative | $\le1.7\times10^{-16}$ relative at all $z$ | pass |
| **P3.2** base realizations only, $s=0$ | $O_0(1)$ within 3 SE of 0 | $-2.6\pm2.8$ W | pass |
| **P3.3** sign and size of the even part, $s=0$ | $E_0(1)>0$; within factor 3 of $+1.6$ W; $E_0(1)/E_0(0.5)=4.0\pm0.4$ | $E_0(1)=+2.72\pm0.17$ W (modes 1, 2: $-1.35$, $-1.36$); ratio 4.01; $E_0\propto z^{1.98}$ between 0.1 and 0.2 m | pass |
| P3.3 post hoc | — | exact-kernel Langmuir without Kerr: $+3.92$ W; the field value is $0.62$–$0.70$ of it at every $z$ | — |
| **P3.4** shock × Raman cross term | $\lvert O_0(1)\rvert>3$ SE at $s=1$; $O_0\vert_{s=0.5}/O_0\vert_{s=1}=0.5\pm0.1$; sign: no firm prediction (guess negative) | $O_0(1)=-0.079\pm0.018$ W (4.4 SE); ratio $0.500$; sign negative (the fundamental loses). It grows about linearly in $z$ for $z\ge0.2L_{\rm NL}$, slope $\approx-0.5$ W/m, whereas the no-Kerr Langmuir model gives a $z^3$ term ($-0.024$ W at 0.2 m): the cross term is Kerr-mediated | pass |
| **P3.5** shock does not change the even part | $<20\%$ | $2.7155$ against $2.7151$ W (0.01%) | pass |
| **Convergence, $dz/2$** (Brownian-refined coupling) | $<5\%$ change | $O_0(1)$: $-2.5\%$; $E_0(1)$: $-0.17\%$ | pass |
| **Convergence, $dt/2$** (zero-padded spectrum, same window) | $<5\%$ change | $O_0(1)$: $-1.1\%$; $E_0(1)$: $-1.5\%$, consistent with the sampled $T_1$ moving from 8.21 fs toward the continuum 8.12 fs ($E\propto T_1^2$) | pass |
| Window $\times2$ (post hoc, not pre-registered; fresh realizations, so statistical) | — | $O_0(1)=-0.0758\pm0.0090$ against $-0.0787\pm0.0180$ (0.14 combined SE); $E_0(1)=2.59\pm0.14$ against $2.72\pm0.17$ (0.57 combined SE) | consistent |
| **P4** second solver (repository solver, unmodified, commit `b9fa957`), mirror-pair estimator, 512 pairs, closed form with the solver's own kernel ($\sum h\,dt=0.9897$) | all means within 3 SE; SE$_0<10\%$ in c, d | c: $537.1\pm4.0$, $-268.5\pm2.8$, $-268.6\pm2.7$ (pred. $538.5$, $-269.2$, $-269.2$). **d (held-out)**: $-209.8\pm3.0$, $151.3\pm2.4$, $58.6\pm2.0$ (pred. $-210.7$, $152.4$, $58.3$). b: $-33.6\pm4.7$, $20.7\pm3.0$, $12.9\pm3.0$ (pred. $-44.0$, $22.0$, $22.0$; mode 0 at 2.2 SE, **mode 2 at 3.01 SE**) | c, d pass; **b fails narrowly by the letter** |
| P4 post hoc diagnostics for b | — | The NoRaman run on the same realizations shows that the shock-odd Kerr bias of the mirror estimator is negligible ($-0.07\pm0.015$ W/m). Rerun of b with 2048 fresh pairs (new seed): $-46.4\pm2.5$, $24.6\pm1.6$, $21.8\pm1.6$ W/m against $-44.0$, $22.0$, $22.0$ (within 1.7 SE). The 512-pair miss was most likely a fluctuation; the pre-registered verdict for b stays "fail by the letter" | — |


## 6b. Does fast Kerr relaxation clamp the second-order Raman drift? (three- and four-group toys)

Run `2026-10-20-claude-interactive.21-raman-clamp`; predictions frozen in `predictions.md`, commit `12d49a1`, before any propagation.
- **Model.** Six Hermite–Gauss modes in groups of 1, 2 and 3, with resonant inter-group Kerr exchange $g_0+g_2\leftrightarrow g_1+g_1$ and white-noise $su(n)$ coupling inside groups 1 and 2.
- **Launch.** Group populations 0.3/0.1/0.6; the RJ target with the same $N$ and $H_\perp$ is 0.180/0.339/0.480.
- **Ensemble and length.** $z\le30L_{\rm NL}$; mirror-closed ensembles of 8 pairs; $\lambda=-1,0,+1$.

| Check | Prediction | Outcome | Verdict |
|---|---|---|---|
| **C0** exact, $\lambda=0$ centroids and $\lambda$-odd photon numbers | $<10^{-9}$ | $2.4\times10^{-14}$ rad/ps and $3.4\times10^{-16}$ relative | pass |
| **C1** relaxation exists | group-1 fraction $>0.25$ at 3 m | 0.117: fractions 0.2905/0.1044/0.6051 → 0.2803/0.1169/0.6028, against RJ 0.180/0.339/0.480 | **fail** |
| **C2** sign of the Raman² term | $E_0>0$ at 0.2, 0.3, 3 m | $2.06\pm0.28$, $4.72\pm0.62$, $396\pm37$ W | pass |
| **C3** clamping | only if $L_{\rm kin}\le1$ m | operational $L_{\rm kin}=1.9$ m, meaningless here because C1 failed | **inconclusive** (pre-registered rule) |

**Why there was no relaxation.** The toy is far slower than intended: $L_{\rm kin}\gg30L_{\rm NL}$. Garnier's scaling, $L_{\rm kin}/L_{\rm NL}\sim\Delta\beta L_{\rm NL}/\bar S^2$, gives 50–100 here ($\Delta\beta L_{\rm NL}=3$; resonant overlaps $\bar S\approx0.18$–0.25). Even at the optimum, $\Delta\beta L_{\rm NL}\sim1$, it gives at least $1/\bar S^2\approx20$–30. A test of clamping therefore needs $\gtrsim100\,L_{\rm NL}$ or a toy with larger resonant overlaps. I dropped a staged fallback with $D_d=10$ m⁻¹ because the same scaling predicts at least 20–30 $L_{\rm NL}$ for it. Instead I pre-registered and ran a weak-coupling configuration, `g4_weak` (below).

**Post-hoc observations** (not pre-registered; figure `fig_clamp_main.png`):
- **Kerr locks the Raman-driven inter-group centroid offset long before the populations relax.** The $\lambda$-odd offset $\Delta c_{01}$ follows the no-Kerr Langmuir line for about $3L_{\rm NL}$. It then plateaus near $-1.3$ to $-1.5$ rad/ps from 9 to 21 $L_{\rm NL}$, and reaches $-2.6\pm0.7$ at $30L_{\rm NL}$, against $-11.1$ without Kerr: the field-to-Langmuir ratio is 0.75, 0.48, 0.20 and 0.24 at 3, 10, 20 and 30 $L_{\rm NL}$. Meanwhile the group populations moved by about 0.01. This looks like the "velocity locking" of incoherent wave packets: Pitois, Lagrange, Jauslin, Picozzi, PRL 97, 033902 (2006), DOI 10.1103/PhysRevLett.97.033902. **Not accessed**: I located the Crossref record, and a search snippet of a related HAL conference record describes irreversible evolution of incoherent wave packets to a common group velocity, of thermodynamic origin. The identification is a hypothesis. In the card's language, the inter-group $\theta_1$ equalization is a fast constraint, while $\theta_{0,2}$ relax slowly.
- **The fundamental's Raman² gain** $E_0$ keeps a local exponent of about 1.7–2.4 out to $30L_{\rm NL}$. It falls to 0.84 (2 $L_{\rm NL}$), 0.65 (18 $L_{\rm NL}$) and 0.56 (30 $L_{\rm NL}$) of the no-Kerr value. So Kerr reduces the second-order modal drift even without population relaxation, but by less than it reduces the centroid offset (time-integrated ratio about 0.26). The energy-centroid rule alone therefore does not account for the modal transfer once Kerr correlations build up. Group 2 is the main loser ($-486\pm39$ W at 3 m), not group 1.
- **The selection rule held exactly throughout** (C0), with 6 modes, resonant inter-group exchange and $su(3)$ coupling.

**Second configuration `g4_weak`** (pre-registered as an addendum in commit `31aba86`, after the `main` outcome and before its own propagation): 10 modes in 4 groups, weak coupling $D_d=1$ m⁻¹ ($L_d=10L_{\rm NL}$), $N=1024$, 6 mirror pairs; launch 0.3/0.1/0.5/0.1, RJ 0.291/0.246/0.234/0.229. Figure `fig_clamp_g4_weak.png`.

| Check | Prediction | Outcome | Verdict |
|---|---|---|---|
| C0 | $<10^{-9}$ | $3.6\times10^{-14}$ rad/ps; $9.0\times10^{-16}$ | pass |
| C1 | group-2 fraction $<0.40$ at 3 m | 0.423 (from 0.504; fractions at 3 m 0.289/0.154/0.423/0.134): relaxing, but only 30% of the way | **fail** (narrowly) |
| C2 | $E_0>0$ at 0.2, 0.3, 3 m | $1.55\pm0.26$, $3.57\pm0.51$, $329\pm46$ W | pass |
| C3 | needs $L_{\rm kin}\le1$ m | operational $L_{\rm kin}$ not reached by 3 m | **inconclusive** |

**Post hoc, same pattern as `main`.** The $\lambda$-odd centroid offset $\Delta c_{01}$ is 0.49, 0.34, 0.38 and 0.47 of the no-Kerr value at 3, 10, 20 and 30 $L_{\rm NL}$. $E_0$ is 0.64, 0.58, 0.50 and 0.47 of the no-Kerr value, with a local exponent of 1.7–2.5. Across both toys, Kerr reduces the Raman-driven inter-group frequency offsets by a factor of 2–5 within a few $L_{\rm NL}$ and roughly halves the fundamental's Raman² gain, without yet changing its $z^2$ growth. This holds whether the coupling is strong or weak and before the populations relax. Whether full relaxation turns the growth linear (the conjecture) remains open: it needs $\gtrsim100L_{\rm NL}$.

## 7. What is not known

- The continuum kinetic equation of §2.1 is a heuristic extension of Garnier 2019, not a derivation. Its constant, polarization tensor and partially correlated noise factor $(1-\rho)$ for a frequency continuum are not computed.
- The second-order Raman modal drift with fast Kerr relaxation ($L_{\rm kin}/L_R^2$ scaling) is a conjecture. P3 tests only $z\le2L_{\rm NL}$, without inter-group Kerr exchange. Both clamp tests (§6b; three and four groups) were inconclusive because populations did not relax enough in $30L_{\rm NL}$. The fast centroid locking seen there is post hoc and its mechanism is not derived.
- In regime T the observable is a mixture of time-local RJ states. How Raman, which couples neighbouring time slices on the scale $T_R\ll t_c$, moves $\theta(t)$ is not derived, beyond the first-order selection rule.
- The coherent femtosecond regime (most experiments) is not addressed beyond the selection rule; see the scope task.
- The main field code is standalone, scalar and three-mode. It uses the isotropic Raman tensor and a toy group spacing, and has no frequency-dependent overlaps. The repository solver was used only for the first-order check P4, without disorder, because it has no random-coupling operator.
- The mechanism of the Kerr-mediated shock × Raman cross term (P3.4: about linear in $z$ beyond $0.2L_{\rm NL}$, about 3% of the Raman² term at $2L_{\rm NL}$) is not derived.
- The SRS-threshold comparison (§4) is a screen estimate (CW Smith criterion, single-oscillator gain), not a simulation. Whether pump–Stokes walk-off fully suppresses noise-seeded Stokes growth for 1–10 ps envelopes is not computed.
