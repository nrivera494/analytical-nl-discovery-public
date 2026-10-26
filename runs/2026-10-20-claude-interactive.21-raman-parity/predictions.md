# Pre-registered predictions (frozen before any simulation in this folder)

Agent claude-interactive.21 (claude-opus-5-5), 2026-10-20, task T-20261020-claude-interactive-02. Model and
units: `mmfield.py`, `config.json`. Closed-form numbers below come from `python run_tests.py predict`
(`predictions.json`), which evaluates the formula of §2 of the exploration note on the discrete grid; no
field propagation had been run when this file was committed.

Notation. $\tilde N_p=\sum_k|B_{p,k}|^2/w_k$ is the modal photon-number invariant ($w=1+s\Omega/\omega_0$).
$\lambda$ scales the odd part of the Raman response ($\lambda=1$ physical, $\lambda=-1$ time-mirrored). The
time-reversal map $R:A(t)\to A(-t)$ sends the model $(\lambda,s,b_1)$ to $(-\lambda,-s,-b_1)$.
"Odd part" $O_p(\lambda)=[\langle\tilde N_p\rangle(\lambda)-\langle\tilde N_p\rangle(-\lambda)]/2$;
"even part" $E_p(\lambda)=[\langle\tilde N_p\rangle(\lambda)+\langle\tilde N_p\rangle(-\lambda)]/2-\langle\tilde N_p\rangle(0)$.

## P1. Exact time-reversal identity (cheap check)

For every realization, the mirrored launch $RB_0$ propagated with $(-\lambda,-s,-b_1)$ equals $R$ applied to
the propagation of $B_0$ with $(\lambda,s,b_1)$. Cases: $(\lambda,s,b_1)=(1,0,0),(1,1,0),(1,1,0.05\,{\rm ps/m}),
(0.5,1,0.05)$, with Kerr, Raman, $\beta_2$ and intra-group random coupling (same coupling path for both runs).

- **P1:** maximum relative field deviation $<10^{-10}$ after 300 steps in all four cases.

## P2. First-order (z → 0) Raman modal photon transfer of a stationary Gaussian field

Initial slope of $O_p(1)$, from $[\tilde N_p(z_1;+1)-\tilde N_p(z_1;-1)]/(2z_1)$ at $z_1=10^{-3}$ m $=0.01L_{\rm NL}$,
same realizations for $\pm1$, disorder off. Closed form:
$d\tilde N_p/dz=-2\gamma f_R\sum_qS_{pqpq}\sum_{l,k}b_{p,l}b_{q,k}\,{\rm Im}H(\Omega_l-\Omega_k)$, a functional of the
**energy** spectral densities $b$ only.

- **P2a** (co-centred symmetric energy spectra, $\sigma=(40,15,15)$ rad/ps, shock on): all three slopes zero;
  the measured means lie within 3 standard errors of 0.
- **P2b** (symmetric **photon** spectra, i.e. the shock-tilted energy spectra $b=w\times$Gaussian, same widths,
  shock on): $d\tilde N_0/dz=-44.4$ W/m, $d\tilde N_{1,2}/dz=+22.2$ W/m (the spectrally broader mode loses
  photons). Pass: each mean within 3 SE of the prediction, and the SE of mode 0 below 25% of 44.4 (otherwise
  inconclusive). Linear-gain approximation for comparison: $-27.3$ W/m.
- **P2c** (energy-centroid offset $c=(-5,+5,+5)$ rad/ps, $\sigma=20$, shock off): $+544$, $-272$, $-272$ W/m
  (photons flow to the redder mode). Pass: within 3 SE. Linear-gain approximation: $+702$ W/m.

## P3. Finite distance, z up to 0.2 m = 2 L_NL (beyond perturbation theory in Kerr)

Launch: co-centred symmetric energy spectra, $\sigma=20$ rad/ps ($t_c=50$ fs), powers $(4,3,3)$ kW; Kerr, Raman,
$\beta_2$ ($W_t=0.25$), disorder $D_d=30$ /m. 16 base realizations plus their 16 mirrors.

- **P3.1** ($s=0$, mirror-paired ensemble): $O_p(\lambda)$ for $\lambda=0.5,1$ vanishes to $<10^{-9}$ relative at every
  saved $z$.
- **P3.2** ($s=0$, base realizations only): $O_0(1)$ at $z=0.2$ m within 3 SE of 0.
- **P3.3** ($s=0$): $E_0(1)>0$ (the fundamental gains at second order in the Raman gain, because its Raman
  overlap with the populated modes is largest: $\sum_qS_{0q0q}P_q=7$ kW against 5 kW for modes 1, 2). Magnitude:
  within a factor 3 of the Langmuir second-order estimate $+1.6$ W (relative $4\times10^{-4}$) at $z=0.2$ m.
  $E_0(1)/E_0(0.5)=4.0\pm0.4$.
- **P3.4** ($s=1$): $|O_0(1)|>3$ SE at $z=0.2$ m (a shock × Raman cross term exists). It is linear in $s$:
  $O_0(1)|_{s=0.5}/O_0(1)|_{s=1}=0.5\pm0.1$. Sign: **no firm prediction**; my unverified guess is negative.
- **P3.5** ($s=1$): $|E_0(1)|_{s=1}-E_0(1)|_{s=0}|<0.2\,|E_0(1)|_{s=0}|$.

## Convergence (pre-registered tolerances)

For $s=1$, $\lambda\in\{-1,0,1\}$: halving $dz$ (Brownian-refined coupling path) and halving $dt$ (same window,
zero-padded spectrum) each change $O_0(1)$ and $E_0(1)$ at $z=0.2$ m by less than 5% of their values, or by less
than 1 SE of the base run if that is larger.

## P4. Second solver (added 2026-10-20 13:4x, before any solver propagation)

Script `solver_check.jl` with the repository solver (agents' copy, commit `b9fa957`, unmodified). The solver's model
is the one above with $s=1$; its sampled Raman kernel is not renormalized ($\sum h\,dt=0.9897$). Closed form
evaluated with the solver's own kernel (`predictions_solver.txt`), in W/m:

| case | mode 0 | mode 1 | mode 2 |
|---|---|---|---|
| b (shock-tilted photon-symmetric spectra, as P2b) | −43.98 | +21.99 | +21.99 |
| c (energy-centroid offsets, as P2c) | +538.49 | −269.25 | −269.25 |
| d (**held-out**: powers 5/2.5/2.5 kW, $\sigma=12,25,18$ rad/ps, centroids $+3,-2,0$ rad/ps) | −210.69 | +152.37 | +58.32 |

Estimator: 512 mirror pairs per case, $[\Delta\tilde N_p(A_0)-\Delta\tilde N_p(RA_0)]/(2z_1)$ at $z_1=1$ mm, which cancels
the Kerr first-order fluctuations exactly (§3.1 of the note) and doubles the Raman transfer (odd in the centroids).
For case b the mirror pair maps the tilt to its opposite, so the estimator measures the same closed form.

- **P4:** every mean within 3 SE of the closed form; SE of mode 0 below 10% of its value in cases c and d.
