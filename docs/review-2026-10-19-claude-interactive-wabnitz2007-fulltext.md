---
agent: claude-interactive
model: claude-opus-5-5
family: claude
date: 2026-10-19
task: T-20261008-claude-a-05
---

# Full-text check of Wabnitz (2007), "Analytical dynamics of parabolic pulses in nonlinear optical fiber amplifiers"

**Source.** S. Wabnitz, *IEEE Photonics Technology Letters* 19, 507–509 (2007), DOI 10.1109/LPT.2007.893823. Read in **full text**, 3 pages including the equations and figures, from the publisher PDF the PI downloaded on 2026-10-19. It is kept at `~/analytical-nl-discovery-data/wabnitz2007/` and not committed.

**Purpose.** Earlier records had this paper at abstract level only: claude-a.2, gpt-a and GPT 6 Pro (which read the conference version, DOI 10.1109/QELS.2007.4431461). This note checks it against result R-0011 (C-20261008-claude-a-02) and claim C-20261008-gpt-a-01.

## What the paper does

- **Model.** The amplified NLSE in the small-dispersion limit, reduced to the dispersionless hydrodynamic (Whitham) equations with gain, Eq. (3).
- **Ansatz.** A parabolic intensity with linear chirp, Eq. (4), which turns Eq. (3) into three ODEs for peak power $\rho_0$, half-width $T_0$ and chirp $C_0$ (Eq. 5), and a rescaled pair (Eq. 7). Eq. (5) with $\delta=0$ is credited to Anderson et al. (1993), and its extension to $\delta\ne0$ to Kruglov et al. and Boscolo et al.
- **Two regimes.**
  - A "linear" regime: the amplitude grows at the full gain and the width stays fixed.
  - A "nonlinear" regime: the peak grows at the reduced rate $2\delta/3$, and the width grows at the same rate.

  Here $\delta=GL_{NL}/2$ is half the power-gain coefficient in nonlinear-length units, so the width grows as $e^{gz/3}=G^{1/3}$ and the peak power as $G^{2/3}$.
- **Attractor.** The asymptotic self-similar solution, Eq. (8). Phase portraits in the (chirp, scaled width) plane, Fig. 3, show trajectories for every input width at fixed energy spiralling into this fixed point, a "dynamical sink".
- **Applications.** The amplifier length needed to reach the similariton regime (within 5%, Fig. 4a,b), and the compression factor (Fig. 4c,d).
- **Numerics.** Comparison with the full amplified NLSE ($2^{11}$ points), for parabolic and Gaussian inputs.

**Not in the paper:**
- noise of any kind (classical or quantum);
- shape modes beyond the parabola's own width, chirp and amplitude;
- a linearization about the fixed point. The spiral is shown in Fig. 3, but no relaxation rate or oscillation frequency is stated.

## Verdicts

| Statement | Verdict |
|---|---|
| R-0011 (a): photon-normalized shape-mode variance envelopes $G^{1/3}$ (intensity), $G^{5/3}$ (phase) | **Not anticipated.** No noise. |
| R-0011 (a), background: the $l=2$ (width and chirp) relaxation onto the attractor | **Partly anticipated, qualitatively.** The reduced ODE contains this relaxation, and Fig. 3 shows the spiral. The decay rate ($G^{-1/3}$) and the log-gain frequency are not stated; they follow from linearizing the published ODE, as GPT 6 Pro noted. The $l\ge3$ modes are not treated. |
| R-0011 (b): single-shot spectral covariance tends to rank one, $\mu_2/\mu_1=\Theta(G^{-2/3})$ | **Not anticipated** |
| R-0011 (c): matched-LO phase–energy deficit $1-r^2=\Theta(G^{-2/3})$ | **Not anticipated** |
| C-20261008-gpt-a-01: global attraction within parabolas | **Partly anticipated, numerically and graphically.** Fig. 3 shows convergence from every tested input width at fixed energy. No proof or Lyapunov function is given. |

## Effect on the records

- **R-0011, gate G6.** Two families have searched, and the closest prior works are now read in full: Wang et al. (2016), both papers, and Wabnitz (2007). The difference is stated: the background attractor and its classical relaxation are published; the photon-normalized shape-mode noise exponents, the spectral covariance law and the energy–phase locking are not. G6 can be set to met.
- **Task T-20261008-claude-a-05** stays open for its other three papers: McKinstrie, Santhanam & Agrawal (2002); Santhanam & Agrawal (2003); and Kruglov et al. (2002), whose publisher PDF has not been obtained.
