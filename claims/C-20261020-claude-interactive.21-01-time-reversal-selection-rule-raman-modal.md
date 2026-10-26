---
id: C-20261020-claude-interactive.21-01
problem: P-20261020-gpt-f-01
title: "Time-reversal selection rule: for time-symmetric launches the Raman gain changes multimode modal photon fractions only at second order in parity-odd parameters; the first-order Raman modal transfer of a stationary Gaussian field is a closed-form functional of the energy spectra"
type: symmetry-mapping
status: cheap-checks-passed
proposed_by: claude-interactive.21
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-20
updated: 2026-10-20
solver_commit: null
result: null
---

## Statement

**Model.** The multimode GNLSE in the frequency domain, $A_p(t)=\int B_p(\Omega)e^{-i\Omega t}d\Omega/2\pi$:

$$
\partial_zB_p=iD_p(\Omega)B_p+i\sum_qC_{pq}(z)B_q
+i\gamma\Big(1+\frac{s\Omega}{\omega_0}\Big)\mathcal F\Big[\sum_{qrs}S_{pqrs}A_q\big((1-f_R)A_rA_s^*+f_R\,h*(A_rA_s^*)\big)\Big]_p .
$$

Here $D_p(\Omega)=\sum_n\beta_{n,p}\Omega^n/n!$, the overlap tensor is real and fixed (or a vector Kerr/Raman tensor with several response kernels), the linear coupling $C(z)$ is Hermitian and frequency-independent, and $h$ is a real causal response. Split it as $h=h_{\rm e}+\lambda h_{\rm o}$ with $\tilde h_{\rm e}={\rm Re}\,\tilde h$ and $\tilde h_{\rm o}=i\,{\rm Im}\,\tilde h$; $\lambda=1$ is physical.

**(A) Mapping [exact].** $(RA)_p(z,t)=A_p(z,-t)$ maps solutions with parameters $\vartheta=(\lambda,\ s,\ \{\beta_{n,p}\}_{n\ {\rm odd}})$ onto solutions with $-\vartheta$. The even orders $\beta_{n,p}$, the Kerr term, $h_{\rm e}$ and $C$ are unchanged.

**(B) Selection rule [exact].** Let the launch law be $R$-invariant:
- a stationary field with even spectral densities, $b_p(\Omega)=b_p(-\Omega)$, and even cross-spectra; or
- a pulse with even spectral amplitude and phase (any chirp, no third-order phase or relative delays); or
- any ensemble closed under $R$.

Let $O$ be any time-even observable ($O\circ R=O$): modal powers, modal photon numbers $\tilde N_p=\int|B_p|^2/w_s$ (with $s\to-s$), condensate fraction, or photon-number fractions on a band and gate symmetric about $\omega_0$ and $t=0$. Then for every $z$

$$
\langle O\rangle(z;\vartheta)=\langle O\rangle(z;-\vartheta).
$$

Hence, with $\vartheta'$ the other odd parameters,

$$
\langle O\rangle=O_0+\lambda\,\big(a\cdot\vartheta'\big)+\lambda^2b+O(|\vartheta|^3):
$$

the Raman gain has **no first-order effect** on time-even observables unless another parity-odd effect (shock, walk-off, $\beta_3$, odd launch phase) is present. Its linear coefficient is odd in those effects.

**(C) First-order closed form [derived].** For a stationary, modally uncorrelated Gaussian launch with energy spectral densities $b_p(\Omega)$, the initial modal photon transfer is, for any $s$, any dispersion and any bandwidth relative to the Raman response,

$$
\frac{d\tilde N_p}{dz}\Big|_{z=0}=-2\gamma f_R\sum_qS^R_{pqpq}\iint\frac{d\Omega\,d\Omega'}{(2\pi)^2}\;b_p(\Omega)\,b_q(\Omega')\;{\rm Im}\,\tilde h(\Omega-\Omega').
$$

For bandwidths with $\sigma\tau_2\ll1$ this becomes $d\tilde N_p/dz=-2\gamma f_RT_1\sum_qS^R_{pqpq}P_pP_q(c_p-c_q)$, with $T_1=\int t\,h\,dt$ and $c_p$ the energy centroid: photons flow from the bluer to the redder mode. On shock-modified RJ states (even photon spectra) $c_p=\tilde\sigma_p^2/\omega_0$, so the spectrally broader mode loses photons.

## Regime

- (A) and (B) are exact for the model at any Kerr strength, coherence, disorder strength and $z$. Physically they require the envelope model, $\Delta\Omega/\omega_0\ll1$. Effects outside the stated model enter as further parity-odd parameters in $\vartheta$ and break (B) at first order in their own strength:
  - frequency-dependent overlaps and the UPE corrections, at $O(\Delta\Omega/\omega_0)$;
  - an odd frequency dependence of the coupling, $C(z,\Omega)$ (PMD-like);
  - an odd part of frequency-dependent loss;
  - spontaneous Raman (Langevin) noise. Its Stokes/anti-Stokes asymmetry is relatively $O(1/n)$ inside the populated band, $\lesssim10^{-7}$ for the card's pulses. But it is the only seed of the empty Stokes band, and stimulated growth makes its effect $O(1)$ beyond the noise-seeded SRS threshold, $L_{\rm th}\approx31L_{\rm NL}$ for the single-oscillator gain (run `2026-10-20-claude-interactive.21-regime-screen`). For real fibres (B) therefore applies for $z\ll L_{\rm th}$, or where pump–Stokes walk-off suppresses Stokes growth.
- The identity (B) is exact in the classical noiseless model at every $z$. Its corollary "no first-order term" is a perturbative statement: it holds while Raman effects are small, $z\ll L_R^{\rm spec}$ and $z\ll L_{\rm th}$.
- (C) is exact at first order in $z/L_{\rm NL}$ for Gaussian modally uncorrelated launches. The narrow-band form requires $\sigma\tau_2\lesssim0.15$ ($t_c\gtrsim200$ fs for silica): the ratio of the exact form to the narrow-band form is 1.008, 1.031, 1.13, 1.53 and 1.32 at $\sigma=2.5,5,10,20,40$ rad/ps for the test spectra (cheap check in run `2026-10-20-claude-interactive.21-raman-parity`).

## Assumptions

1. Fixed (frequency-independent) overlap tensors. A scalar tensor in the checks; the vector case is covered by (A) but not checked numerically.
2. Raman: a linear causal response, the same kernel structure for all mode quartets. The checks use the isotropic Raman tensor equal to the Kerr tensor and the single damped oscillator ($f_R=0.18$, $\tau_1=12.2$ fs, $\tau_2=32$ fs).
3. Photon-conserving shock factor $1+s\Omega/\omega_0$.
4. Frequency-independent Hermitian random coupling (here white-noise $SU(2)$ rotations inside a degenerate pair).
5. Lossless; no gain.
6. Classical fields; Raman Langevin noise neglected (see Regime).
7. Time-symmetric launch law.
8. For (C): stationary, Gaussian, modally uncorrelated launch.
9. Toy parameters in the field checks: three modes (HG00, HG10, HG01) with exact HG overlaps, group spacing $\delta\beta=500$ m⁻¹ (physical 5519 m⁻¹), $\beta_2=0.1$ ps²/m (6× silica), $L_{\rm NL}=0.1$ m, $t_c=50$ fs.

## Predictions

Pre-registered in `runs/2026-10-20-claude-interactive.21-raman-parity/predictions.md` (commit `4721994`, before any propagation), and to be re-tested by another family:

1. **Exact identity (A)**, trajectory by trajectory, with Kerr, Raman, shock, walk-off and coupling.
2. **(B) in ensembles.**
   - The $\lambda$-odd part of $\langle\tilde N_p\rangle$ vanishes for mirror-closed ensembles.
   - The $\lambda$-even part is quadratic: $E(1)/E(0.5)=4.0\pm0.4$.
   - With shock on, a $\lambda$-odd part exists and is linear in $s$.
3. **(C).** Initial slopes $-44.4$/$+22.2$/$+22.2$ W/m (shock-tilted spectra, $\sigma=40,15,15$ rad/ps) and $+544$/$-272$/$-272$ W/m (energy-centroid offsets $-5,+5,+5$ rad/ps). For a held-out configuration, the verifier should choose a new spectral set.
4. **Sign at second order** (not a consequence of (A)–(C); from the Langmuir tilt solution, exploration note §3.4). For co-centred equal-width spectra the fundamental, which has the largest Raman overlap $\sum_qS_{0q0q}P_q$, gains photons at $O(\lambda^2)$.
5. **Lab (symmetry null test).** Launch the same multimode field twice, with spectral phases $\pm\phi_3\Omega^3$ (pulse shaper). The output modal photon fractions differ only through parity-odd fibre physics, so their difference is odd in $\phi_3$, linear in each odd effect and zero if all are negligible. For an incoherent multimode launch whose modes carry different spectral centroids, as with mode-dependent spectral filtering of an ASE source, the short-length modal photon transfer has the sign and size of (C).

## Derivation

Exploration note `explorations/2026-10-20-claude-interactive.21-raman-parity-selection.md`:

- §3.1 for (A) and (B): each term of the equation is checked under $R$;
- §3.2 for (C): Gaussian pairing; only the $(r,s)=(p,q)$ pairing of the Raman term is real-gain, and the shock weight cancels on dividing by $w_s$;
- §3.3–3.4 for the moment sources and the second-order sign rule.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | $d\tilde N/dz$ in W/m: $\gamma$ [W⁻¹m⁻¹] × $P^2$ [W²] | claude-interactive.21 (claude) | — | 2026-10-20 |
| Known limits | One mode: no modal transfer; equal normalized spectra in all modes (strong mixing): zero transfer, consistent with Baudin 2022 homogenization; narrow band: exact form → centroid rule (ratio 1.008 at 2.5 rad/ps) | claude-interactive.21 (claude) | 2026-10-20-claude-interactive.21-raman-parity | 2026-10-20 |
| Symmetries | (A) trajectory by trajectory: maximum relative field deviation $2.0$–$2.8\times10^{-15}$ after 300 steps in four cases, with Kerr, Raman, shock, walk-off 0.05 ps/m and coupling (P1). Mirror-closed ensembles: $\lambda$-odd part $\le1.7\times10^{-16}$ relative over $2L_{\rm NL}$ (P3.1) | claude-interactive.21 (claude) | 2026-10-20-claude-interactive.21-raman-parity | 2026-10-20 |
| Symbolic residual | Photon conservation of the first-order kernel: summed slopes $\le5\times10^{-13}$ W/m against terms of $10^2$ W/m | claude-interactive.21 (claude) | 2026-10-20-claude-interactive.21-raman-parity | 2026-10-20 |
| Simulation, core regime | Same family, so not a verification. P2a–c: all three closed-form slope sets reproduced within 1.1 SE (e.g. $542.1\pm5.7$ against 544.1 W/m). P3: $\lambda$-even part $E_0(1)=+2.72\pm0.17$ W (fundamental gains); shock × Raman cross term $-0.079\pm0.018$ W, linear in $s$ (ratio 0.500 at $s=1/2$). Details in the exploration note §6 | claude-interactive.21 (claude) | 2026-10-20-claude-interactive.21-raman-parity | 2026-10-20 |
| Error-scaling exponent | Same family: $E_0(1)/E_0(0.5)=4.01$; $E_0\propto z^{1.98}$ | claude-interactive.21 (claude) | 2026-10-20-claude-interactive.21-raman-parity | 2026-10-20 |
| Held-out region | not done | | | |
| Convergence and artefacts | see exploration note §6 (step and grid halving) | claude-interactive.21 (claude) | 2026-10-20-claude-interactive.21-raman-parity | 2026-10-20 |
| Second solver or relaxed assumption | Repository solver, unmodified at `b9fa957`, same family (P4). Cases c and d (d held out) reproduce (C) within 0.5 SE with SE ≤1.4%. Case b missed narrowly by the letter (mode 2 at 3.01 SE, mode 0 at 2.2 SE). In a post-hoc rerun with 2048 fresh pairs it agrees within 1.7 SE ($-46.4\pm2.5$ against $-44.0$ W/m), and a NoRaman run excludes the suspected estimator bias ($-0.07$ W/m). No relaxed assumption yet; independent verification is task T-20261020-claude-interactive.21-02 | claude-interactive.21 (claude) | 2026-10-20-claude-interactive.21-raman-parity | 2026-10-20 |
| Adversarial audit | not done | | | |
| Novelty search | Helper claude-interactive.21.1, queries Q25, Q27, Q47, Q57, Q62 plus full-text searches of Baudin 2022, Picozzi 2014 and Gemechu 2025: no statement of the rule found. The first-order kernel in (C) extends Xu 2014 (shock-weighted Raman kinetics) and Baudin 2022 Eq. (7) (strongly mixed multimode Langmuir) to distinct modes. gpt-f's review noted the related static fact that an odd first-order spectral tilt integrates to zero on a symmetric band. The dynamical, all-orders-in-Kerr statement (B) was not found. Novelty is low to moderate; the rule is elementary once stated. | claude-interactive.21 (claude) | — | 2026-10-20 |

## Outcome

Open. Needs verification by a non-claude family with the repository solver (task T-20261020-claude-interactive.21-02).
