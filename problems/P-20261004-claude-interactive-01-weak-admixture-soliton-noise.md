---
id: P-20261004-claude-interactive-01
title: "Noise of an LP01 soliton carrying a weak LP02 or LP11 admixture"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: low
target_quantity: "The first nonzero corrections to fixed-filter (optionally mode-resolved) LP01 and minority Fano factors and their count correlation for a bright weak LP02/LP11 admixture, beyond passive probe capture and known Manakov noise theory: their walk-off dependence at first order in the admixture amplitude (a Manakov linearization with a frequency-offset minority) and the first non-Manakov correction at second order, with explicit walk-off and dispersion-mismatch bounds."
model: "Two-mode (three for the degenerate LP11 pair) GNLSE in a parabolic-index fiber with anomalous dispersion, rotating-wave Kerr overlaps, modal walk-off and causal Raman response; linearized quantum fluctuations about the soliton plus a linear minority field."
oracle_ready: partial
last_audited: 2026-10-04
audited_by: [claude, gpt]
proposed_by: PI
provenance:
  agent: claude-interactive
  model: claude-opus-5-5
  family: claude
updated_by: claude-b
updated_model: claude-opus-5-5
updated_family: claude
claims: []
results: []
---

## Target quantity

**Set-up.** Normalize the LP01 soliton as $iu_\zeta+\tfrac12u_{\tau\tau}+|u|^2u=0$, $u=\operatorname{sech}\tau\,e^{i\zeta/2}$, and launch a minority mode with amplitude $\varepsilon v$. With equal initial sech norms, write $r=\varepsilon^2=E_2/E_1\ll1$; the fraction of total launch energy is $p_2=r/(1+r)$. To first order in $\varepsilon$, with equal anomalous modal GVD, instantaneous Kerr, no gain, and rotating-wave removal of nonresonant coherent terms, the minority obeys a linear equation in the soliton's cross-phase potential:

$$iv_\zeta+i\delta v_\tau+\tfrac12v_{\tau\tau}+\sigma\operatorname{sech}^2\tau\,v=0,\qquad \sigma=2S_{01,m}/S_{01,01},\qquad \delta=\Delta\beta_{1,m}T_0/|\beta_2|.$$

The ideal parabolic profile gives $\sigma=1$ for both LP02 and LP11. Where the text below writes $\varepsilon^2=p_2$, it holds to leading order, since $p_2=r+O(r^2)$ (merge note).

**Derive**, beyond the known baseline (the Claude- and GPT-family review lists, combined):
1. **Walk-off dependence at first order (main target).** For a co-launched sech minority, as functions of $\delta$ at fixed $\zeta$:
   - the filtered Fano factors of the LP01 count and of the minority count, $F_{01}$ and $F_m$;
   - their correlation coefficient $\rho$;
   - the captured minority fraction.
   For $\delta=0$ these are the known sublimit below. For $\delta\neq0$ the problem reduces to a fixed linear one (reduction 2 below), with closed-form bound and continuum states.

   For fixed $\zeta$ and a fixed filter with nonzero transmission, the leading nonzero coefficients in $F_{01}-F_{\rm scalar}=O(p_2)$, $F_m-1=O(p_2)$ and $\rho=O(\sqrt{p_2})$, including their walk-off dependence. A prescribed classical pump gives a passive minority channel, hence $F_m=1$ even after filtering. Pump fluctuations and the coupled Bogoliubov system are essential for a nontrivial answer.
2. **First correction in $\varepsilon^2$.** This is where the GRIN overlaps first differ from the Manakov case. It comes from:
   - the minority's own self-phase ($C_{22}=1/2$ for LP02, $3/4$ for LP11, against 1);
   - for LP11, intragroup coupling between the two orientations (overlap 1/4);
   - phase-matched four-wave mixing into a third mode: 01+03↔02+02 (overlap 1/4), and 02+02↔21+21 (overlap 1/4; LP21 is degenerate with LP02 in the ideal profile). The 01+02↔11+11 overlap is 0.

   Include or bound backreaction, unequal self-overlap, resonant higher-mode generation and LP11 orientation coupling at the order at which they enter. State bounds on $p_2$, $\zeta$, GVD ratio, $\sigma-1$ and retained FWM mismatch. The bright-field noise expansion requires $p_2N\gg1$; an empty mode does not have a defined count Fano factor.
3. Distinguish bound-state projection from finite-window capture. Treat the displayed capture formula as an analytical benchmark already implied by the solvable well.

**Readout.** As in P-20261004-root-03: a fixed bandpass, optionally mode-resolved, and the coherent-reference readout.

## Known sublimit and reductions

claude-b recorded these during the review on 2026-10-04.

**Self-check (same family, not the solver).** Run `2026-10-04-claude-b-reduction-selfcheck` is an independent numpy linearized-noise code, with a hard bandpass at $\zeta=2$ and $F_s=0.635$. It finds:
- $\rho$ matches $\varepsilon(F_s-1)/\sqrt{F_s}$, with a relative correction of 0.0016, 0.0062, 0.025 and 0.097 at $\varepsilon$ = 0.025, 0.05, 0.1 and 0.2, so it scales as $\varepsilon^2$;
- $F_m-1$ and $F_{01}-F_s$ scale as $\varepsilon^2$, with $F_m-1$ about half its Manakov value, so non-Manakov terms enter at that order;
- the walk-off and frequency-offset runs agree to about $10^{-8}$.

The independent check by another family, with the solver, is T-20261004-claude-b-01.

1. **First order at $\delta=0$ is the Manakov linearization.** $\sigma=1$ means the minority's cross-phase coefficient equals LP01's self-phase coefficient, which is the Manakov condition $C_{21}=C_{11}$. To first order in $\varepsilon$, the coupled fluctuation equations are therefore those of a Manakov soliton with polarization angle $\theta=\varepsilon$. This covers the mean fields, the minority's passive vacuum, and both $O(\varepsilon)$ couplings $\varepsilon v(u^*\delta a+u\,\delta a^*)$ and $\varepsilon u(v^*\delta b+v\,\delta b^*)$. For a co-launched sech, the state is a scalar soliton in the rotated mode, with vacuum in the orthogonal mode. For a common filter applied to both modes, this gives:
   - $F_{01}=F_s+O(\varepsilon^2)$;
   - $F_m=1+O(\varepsilon^2)$; the Manakov value is $1-\varepsilon^2(1-F_s)$, and the non-Manakov terms also enter at $O(\varepsilon^2)$;
   - $\rho=\varepsilon\,(F_s-1)/\sqrt{F_s}+O(\varepsilon^2)$;
   - here $F_s$ is the scalar filtered Fano factor at the same $\zeta$.

   So in the limit $\varepsilon\to0$ the minority is shot-noise limited and uncorrelated with LP01. The nontrivial content is the coefficients, which are those of the scalar problem. For example, $F_s=0.4$ and $p_2=0.05$ give $\rho\approx-0.21$. The earlier statement of this item ("all three are finite in this limit") was correct but hid that it adds nothing beyond the scalar soliton.
2. **Walk-off is a frequency offset, also for the noise.** The substitution $v=w\,e^{-i\delta\tau+i\delta^2\zeta/2}$, applied with the same phase to the minority fluctuation $\delta b$, removes the walk-off term. It leaves both first-order couplings unchanged (Sun et al. 2024, Eqs. 40–41, for the mean field). The first-order problem at $\delta\neq0$ is therefore the $\delta=0$ Manakov linearization with:
   - a minority launched as $\operatorname{sech}\tau\,e^{i\delta\tau}$;
   - a minority filter shifted by $\delta/T_0$.

   The captured fraction is the projection onto the single bound state $\operatorname{sech}\tau$: $[\pi\delta/(2\sinh(\pi\delta/2))]^2$, which is 0.466 at $\delta=1$ and 0.074 at $\delta=2$. The remainder radiates without reflection; the continuum states are $(\tanh\tau-ik)e^{ik\tau}$. A natural expectation, still to be derived and not established, is that the captured part behaves as a Manakov component with an effective fraction $\varepsilon^2[\pi\delta/(2\sinh(\pi\delta/2))]^2$, plus a transient from the radiated part.
3. **Minority count conservation.** The cross-phase-only model conserves the photon number in each mode exactly (Sun et al. 2024, Eq. 54), not only at first order. Each mode's unfiltered count therefore has $F=1$ with Raman off. Any squeezing or correlation needs filtering or interference.

## Signal of hidden simplicity

**Independent capture test (gpt-a).** Runs `2026-10-04-gpt-a-material`, `2026-10-04-gpt-a-capture`, `2026-10-04-gpt-a-capture-small` and `2026-10-04-gpt-a-passive` support the ideal overlap ratios and the bound-state projection law. The normalized minority-field error scales as $\varepsilon^2$ (measured exponents 1.99984–2.00018 across the tested walk-offs). The proposed $|\tau|<5$, $\zeta=20$ measurement is **not** an asymptotic captured fraction: a passive probe still contains slow continuum radiation. At $\delta=1$, endpoint-aware integration gives 0.518895 rather than the bound fraction 0.465901 (`2026-10-04-gpt-a-capture-convergence`). The discrepancy persists as $\varepsilon\to0$. Subtracting the prespecified passive finite-distance baseline recovers the nonlinear scaling.

For two Kerr modes at zero walk-off, the bound-projection loss has a vanishing $O(\varepsilon^2)$ coefficient and an observed $O(\varepsilon^4)$ loss. Adding LP03 restores an $O(\varepsilon^2)$ minority-relative correction: its absolute energy has exponents 3.99062 and 4.00025 at $\delta=0$ and 1 (`2026-10-04-gpt-a-three-scaling`). The archive's nonzero carrier mismatch strongly suppresses generation compared with the ideal resonant model (`2026-10-04-gpt-a-capture-convergence`); the comparison also changes the modal group delays and dispersion.

The fixed-filter noise sweep and extension down to $r=10^{-4}$ support finite Fano limits and vanishing intermodal correlation (`2026-10-04-gpt-a-noise`, `2026-10-04-gpt-a-noise-small`). The Kerr minority approaches $F=1$; both Raman models retain excess noise. The reservoir and adjoint pass count-conservation, directional-derivative, direct-space Gram and thermal quantum-channel checks (`2026-10-04-gpt-a-noise-controls`, `2026-10-04-gpt-a-noise-cw`). Sharp spectral filters retain a visible frequency-grid uncertainty, tracked in `T-20261004-gpt-a-02`. Full details, assumptions and frozen predictions are in [the exploration](../explorations/2026-10-04-gpt-a-weak-admixture.md).

The archive GIF625 setup uses ideal analytical GRIN mode fields, so it also gives $\sigma=1$ to numerical precision; a measured-profile deviation has not been tested. Follow-up: `T-20261004-gpt-a-01`.

**Structural facts.** These were derived by claude-interactive on 2026-10-04 from exact Laguerre–Gauss and Hermite–Gauss overlap integrals for an ideal, infinite parabolic profile. They were independently re-derived by gpt-b for the same profile in the [GPT review](../docs/review-2026-10-04-gpt-b-soliton-noise.md), with symbolic/quadrature record [2026-10-04-gpt-b-overlap-capture](../runs/2026-10-04-gpt-b-overlap-capture/summary.json). claude-b re-derived them by exact symbolic integration on the same day (script in the review log). Neither re-derivation is verification in the propagation solver.

- **The potential is the soliton's own.** $S_{01,02}/S_{01,01}=S_{01,11}/S_{01,01}=1/2$, so $\sigma=1$ for both LP02 and LP11. The minority sees exactly the LP01 self-phase potential. With $\sigma=1$ this is the reflectionless Pöschl–Teller well with $\nu=1$, whose only bound state is $\operatorname{sech}\tau$ itself (Steiglitz & Rand 2009: degree $\nu$ with $\nu(\nu+1)$ equal to twice the ratio of cross- to self-nonlinearity). Its continuum states, $(\tanh\tau-ik)e^{ik\tau}$, are explicit, so the first-order Green function is closed form.
- **Walk-off is removable in this model.** It drops out under $v=w\,e^{-i\delta\tau+i\delta^2\zeta/2}$. A same-carrier, same-width sech launch has bound fraction $[\pi\delta/(2\sinh(\pi\delta/2))]^2$. This requires equal modal GVD, a fixed pump and no Raman. It gives no finite capture threshold and is not a finite-distance time-gate fraction. For unequal GVD the well index and projection change.
- **The passive minority remains coherent.** Its fixed-filter count has $F=1$, with loss-port vacuum included. In an XPM-only quantum model the unfiltered count of each mode is conserved at all orders, so independent coherent launch counts remain Poissonian and uncorrelated. Nontrivial filtered squeezing needs the coupled fluctuation dynamics beyond the prescribed-pump limit.
- **Second-order coefficients**, same method:
  - self-overlaps $S_{02,02}/S_{01,01}=1/2$ and $S_{11a,11a}/S_{01,01}=3/4$;
  - intragroup $S_{11a,11b}/S_{01,01}=1/4$, phase-matched within the degenerate LP11 group;
  - 01+03↔02+02 overlap 1/4, phase-matched in an ideal parabolic profile because the mode spacing is equal;
  - 02+02↔21+21 overlap 1/4;
  - 01+02↔11+11 overlap 0.

**Archive context** (`~/Desktop/fall2026_research/ai driven lab work/research_runs/2026-09-26_analytics/report.md`). The overlap-only rescaling failed at 1400 nm for an 85/15 LP01/LP02 launch whose walk-off was comparable to the pulse width. That is the regime of the walk-off item (Derive item 1).

## Literature state

Reviewed by claude-b on 2026-10-04 (T-20261004-root-02).

**Mean field (trapped probe, soliton trapping):**
- Steiglitz & Rand, "Photon trapping and transfer with solitons," PRA 79, 021802(R) (2009), DOI [10.1103/PhysRevA.79.021802](https://doi.org/10.1103/PhysRevA.79.021802). **Full text** (author copy, cs.princeton.edu/~ken).
  - Content: a classical linear probe in a soliton's cross-phase potential. The eigenstates are associated Legendre functions, with degree set by the cross/self ratio; integer degree means a reflectionless potential. Probe transfer and beam splitting in soliton collisions are shown numerically.
  - Not covered: **the walk-off term is explicitly set to zero**, and there is no capture-versus-walk-off formula and no quantum noise.
  - Their 2017 book chapter "Soliton-guided quantum information processing" (author copy) adds no noise analysis.
- Sun, Parra-Rivas, Agrawal, Hansson, Antonelli & Mecozzi, Photonics Res. 12, 2581 (2024), DOI [10.1364/PRJ.531393](https://doi.org/10.1364/PRJ.531393). **Full text**, sections 3–4. Walk-off is removed by a gauge transformation and is equivalent to an initial relative frequency shift (Eqs. 40–41). The power in each mode is conserved (Eq. 54).
- Buch & Agrawal, OL 40, 225 (2015), DOI [10.1364/OL.40.000225](https://doi.org/10.1364/OL.40.000225): two-mode soliton trapping in few-mode fiber by spectral shifts. **Abstract only.**
- Menyuk, JOSA B 5, 392 (1988), DOI [10.1364/JOSAB.5.000392](https://doi.org/10.1364/JOSAB.5.000392): soliton trapping in birefringent fiber. **Not accessed.**
- Dikandé, PRA 81, 013821 (2010), DOI [10.1103/PhysRevA.81.013821](https://doi.org/10.1103/PhysRevA.81.013821): probe modes trapped by pulse trains. With walk-off, the modes carry finite momentum and none is fully transparent. **Abstract only.**
- Babushkin, Melchert, Morgner & Demircan, Nat. Commun. (2026), DOI [10.1038/s41467-026-77059-1](https://doi.org/10.1038/s41467-026-77059-1): trapping of weak waves by a refractive-index step moving at the speed of light ("time cavity"). **Abstract only.**

**Quantum noise with a trapped component or two components:**
- Hirosawa, Kannari, Takeoka & Sasaki, PRA 76, 043817 (2007), DOI [10.1103/PhysRevA.76.043817](https://doi.org/10.1103/PhysRevA.76.043817). **Abstract only** (found by helper claude-b.3 and checked by claude-b).
  - Content: a soliton and a pulse trapped across the zero-dispersion wavelength, in a single spatial mode. Cross-phase modulation produces strong negative photon-number correlation between parts of the trapped pulse and the soliton, enough for sub-shot-noise conditional measurement of the soliton.
  - This is the closest prior quantum treatment of a trapped probe, but with a different trapping mechanism and no walk-off parameter.
- Rand, Steiglitz & Prucnal, PRA 71, 053805 (2005), DOI [10.1103/PhysRevA.71.053805](https://doi.org/10.1103/PhysRevA.71.053805). **Full text.** Quantum theory of Manakov solitons; the partition variance is independent of $z$; optimal homodyne squeezing is scalar. Filtered detection is not treated. Their linearization excludes polarization angles below 1°, which is the weak-admixture limit; the rotation argument in reduction 1 does not need that restriction.
- Lee, Lai & Malomed, PRA 71, 013816 (2005), DOI [10.1103/PhysRevA.71.013816](https://doi.org/10.1103/PhysRevA.71.013816), [arXiv:quant-ph/0405138](https://arxiv.org/abs/quant-ph/0405138): negative photon-number correlation between the x and y components of interacting vector solitons (circular basis, cross/self ratio 2, no walk-off). **Full text.**
- König, Zielonka & Sizmann, PRA 66, 013812 (2002), DOI [10.1103/PhysRevA.66.013812](https://doi.org/10.1103/PhysRevA.66.013812): transient spectral photon-number correlations between colliding solitons with different group velocities, erased after separation. **Abstract only.**
- Konyukhov, PRA 111, 013508 (2025), [arXiv:2412.09208](https://arxiv.org/abs/2412.09208). **Full text, keyword-scanned.** Linearized quantum theory of vector solitons, using Manakov and coupled-NLS models with differential group delay and birefringence. Readout is polarization-diversity homodyne and photon-number correlation maps of pulse pairs from soliton splitting. No spectral filtering and no trapped-probe capture.
- Lantz et al., [arXiv:quant-ph/0311088](https://arxiv.org/abs/quant-ph/0311088): spatial vector soliton, components anticorrelated (see P-20261004-root-03). **Full text.**
- Single-mode soliton noise and filtering baselines: see P-20261004-root-03.
- Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482): multimode-fiber noise via relative modal phases, near-CW. **Full text** of the main paper.

**GPT review and later access updates**, kept as written (gpt-b's review and gpt-a's access updates; the access levels are those of each reader):

Searches by claude-interactive on 2026-10-04. GPT review by gpt-b on 2026-10-04, with the complete search/access ledger in the [review note](../docs/review-2026-10-04-gpt-b-soliton-noise.md). The two trapping-paper access records were updated by gpt-a during T-20261004-claude-interactive-07; see [the access details](../explorations/2026-10-04-gpt-a-next-order-capture.md).

- Steiglitz & Rand, "Photon trapping and transfer with solitons," PRA 79, 021802(R) (2009), DOI [10.1103/PhysRevA.79.021802](https://doi.org/10.1103/PhysRevA.79.021802). Cross-phase trapping in a soliton-induced sech-squared potential is prior mean-field work: weak-probe bound states and soliton-collision transfer, with pump-probe walk-off set to zero in the simulations. The capture expression above was not printed there but follows from the known eigenproblem. **Full text**, read by gpt-b, and by gpt-a from the author PDF for the next-order task.
- Menyuk, "Stability of solitons in birefringent optical fibers. II. Arbitrary amplitudes," JOSA B 5, 392 (1988), DOI [10.1364/JOSAB.5.000392](https://doi.org/10.1364/JOSAB.5.000392): polarization-component trapping with walk-off and compensating component frequency shifts. **Full text**, public paper OCR read by gpt-a; equation-rendering limitations and the inaccessible author PDF are recorded in the linked note. gpt-b had the **abstract only** (author full-text link failed).
- Rand et al., [10.1103/PhysRevA.71.053805](https://doi.org/10.1103/PhysRevA.71.053805), **full text** (gpt-b): Manakov vacuum covariance, dual modes and a scalar-equivalent optimized homodyne limit. A necessary prior baseline.
- Lantz et al., [arXiv:quant-ph/0311088](https://arxiv.org/abs/quant-ph/0311088): squeezing and anticorrelation in incoherently coupled vector spatial solitons (bulk Kerr, no walk-off), with a different XPM matrix and an unstable bound state. The spatial/temporal coordinate distinction alone does not establish novelty. **Full text** (gpt-b); claude-interactive had the abstract only.
- Single-mode soliton noise and filtering baselines: Haus & Lai (1990), Kärtner & Boivin (1996), Levandovsky et al. (1999). Scalar source identifiers and access levels are listed on P-20261004-root-03 and in the review.
- Sloan et al., [arXiv:2509.03482](https://arxiv.org/abs/2509.03482): multimode-fiber quantum-noise theory, including general multimode noise and relative-phase noise conversion. **Full text of the main paper** (gpt-b); supplementary information **not accessed**.

**Searches.** claude-b used OpenAlex forward citations of Steiglitz & Rand 2009 (28 citing works) and Rand et al. 2005 (21), screened by title, and scans of the two 2024 multimode-soliton reviews. Helper claude-b.3 ran web, arXiv-API and OpenAlex searches on vector-soliton squeezing, soliton trapping with quantum noise, and multimode-fiber squeezing; the strings are listed in the review log.

## Sharpest statement of the gap

**Known or reducible to known results:**
- the mean-field capture problem: the reflectionless potential (Steiglitz & Rand) plus the walk-off gauge (Sun et al.);
- the $\delta=0$ first-order noise: the Manakov rotation of the scalar filtered soliton result (reduction 1).

**Not found:**
- the first-order noise at $\delta\neq0$: $F_{01}(\delta)$, $F_m(\delta)$ and $\rho(\delta)$, with the minority partly captured and partly radiated;
- the $O(\varepsilon^2)$ corrections in which the GRIN overlaps ($C_{22}\neq1$, intragroup LP11 coupling, degenerate-group four-wave mixing) first appear.

Reductions 1–2 make the first-order problem a fixed linear one with known bound and continuum states, so a closed form is likely. The remaining interest is whether the $\delta$-dependence of $\rho$ and of the captured fraction is large and clean enough to measure.

**GPT review's statement** (gpt-b, 2026-10-04):

Capture, passive-probe shot noise and integrable vector-soliton noise are baselines. The searched sources did not supply the first nonzero fixed-readout quantum correction for unequal-overlap GRIN spatial modes with walk-off and controlled deviations from the fixed-pump limit. This is a narrowed search-limited question, not a claim that vector quantum soliton theory is absent. Full-text loose ends are T-20261004-gpt-b-01; a second family must complete its review before derivation is authorized.

Note added when the two reviews were merged (claude-interactive, 2026-10-06): with T-20261004-root-02 merged, the Claude-family review is also complete and `audited_by` is `[claude, gpt]`. Status, and whether derivation may begin, were not changed here.

## Conjectures

None registered.

## Oracle

The full two-mode GNLSE with linearized noise, in `solver/`, is the check. The archive covers LP02 (axisymmetric). LP11 needs non-axisymmetric modes; see T-20261004-root-03.

Cheap tests:
- At $\delta=0$, the bound fraction is 1.
- At $\delta=0$, $\rho$ and $F_m$ follow reduction 1, with the measured exponents in $\varepsilon$ (T-20261004-claude-b-01).
- The capture formula agrees with a two-mode run at $\varepsilon^2=0.01$.
- A walk-off run equals the frequency-offset run with a shifted filter (reduction 2).
- The minority's photon number is conserved; its unfiltered $F=1$ with Raman off.
- The error of the first-order theory scales as $\varepsilon^2$; report the measured exponent between $p_2=0.01$ and 0.15.

A nonparabolic measured GIF625 profile may shift $\sigma$ away from 1. The supplied archive uses ideal analytic modes and cannot quantify that shift. Compute it from sourced measured profile data before using $\sigma-1$ as a measured small parameter. (T-20261004-claude-b-03, T-20261004-gpt-a-01)

## Lab test

GIF625 at 1550 nm with the prepared sech from the archive's soliton work.
- Launch 1–15% LP02 or LP11 with a phase plate or SLM.
- Vary $\delta$, by changing wavelength or fiber, and the relative launch delay.
- Measure mode-resolved output spectra and counts with a mode sorter or photonic lantern: captured fraction, the two filtered Fano factors, and $\rho$.

Expected sizes: $\rho$ is of order $\varepsilon(F_s-1)/\sqrt{F_s}$, for example $-0.21$ at $p_2=0.05$ and $F_s=0.4$, and smaller at $\delta\neq0$. So the correlation needs well-squeezed filtered LP01 light and mode-resolved detection with low loss. The naive expectation, a $\gamma_{\rm eff}$ rescaling of the LP01 result, predicts no dependence on $\delta$.

**Walk-off of the proposed launch.** These numbers are from the solver's nominal GIF625 model (run `2026-10-04-claude-b-gif625-walkoff`). For the 0.4 ps sech at 1550 nm:
- LP11: $\delta=0.59$, captured fraction 0.76;
- LP02: $\delta=1.22$, captured fraction 0.33.

So $\delta$ can be scanned through the interesting range by changing the pulse width, with no change of fiber: LP02 has $\delta=1$ at 0.33 ps and $\delta=0.5$ at 0.16 ps. A measured index profile can shift these values (T-20261004-claude-b-03).

## Risks and must-reads

- The capture identity is a straightforward known-well projection; reproducing it alone would not support novelty.
- Linear weak-probe trapping is established prior work; novelty of any next-order or quantum-noise claim needs its own audit.
- **Prior work that could already contain the answer:**
  - Hirosawa et al. 2007 (full text not accessed) may already contain the trapped-probe correlation structure in a form that maps onto item 1.
  - Menyuk 1988 and the soliton-trapping literature may contain the mean-field capture formula.

  These are in T-20261004-claude-b-02.
- **The problem may be small.** With reductions 1–2 the first-order problem may be a short calculation; whether it deserves a card of its own, rather than serving as the first section of P-20261004-root-03, is for the PI.
- **Effects outside the first-order model:**
  - Raman self-frequency shift moves the soliton relative to the minority and adds an effective time-dependent $\delta$. Raman exchange terms between modes break reduction 2.
  - Random mode coupling can transfer the admixture between LP11 orientations.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-04 | claude-interactive (claude; claude-opus-5-5) | Created as candidate on PI instruction, as the weak-admixture subcase of P-20261004-root-03 | PI's four-problem set in chat, 2026-10-04; overlap and capture calculations in this session; targeted literature search |
| 2026-10-04 | claude-b (claude; claude-opus-5-5) | Claude-family full-text review (T-20261004-root-02). Derive item 1 (the $\delta=0$, $\varepsilon\to0$ noise) recognized as the Manakov rotation of the scalar result and moved to "Known sublimit"; walk-off at first order made the main target; second-order list extended (02+02↔21+21; 01+02↔11+11 vanishes); novelty_confidence medium → low because the remaining first-order problem reduces to known machinery; literature_state stays partial | Full texts: Steiglitz & Rand 2009; Rand et al. 2005; Lee, Lai & Malomed 2005; Konyukhov 2025; Sun et al. 2024; Lantz et al. Exact overlap integrals (sympy, script in log). Log `log/2026-10-04_claude-b_T-20261004-root-02.md` |
| 2026-10-04 | gpt-b (gpt; gpt-6-astra) | Completed independent scope review; added gpt; retained candidate, lowered novelty confidence and narrowed target to nonzero quantum corrections | Independent overlap/capture derivation and run 2026-10-04-gpt-b-overlap-capture; full-text Steiglitz, Rand and Lantz; source ledger in docs/review-2026-10-04-gpt-b-soliton-noise.md |
| 2026-10-04 | gpt-a (gpt; gpt-6-astra) | Independent exploration: bound capture law and quadratic field error supported; finite time gate fails as an asymptotic capture estimator; LP03, unequal dispersion and fixed-filter noise checked. Continuous-frequency noise precision and measured profile remain open. | `2026-10-04-gpt-a-capture`, `2026-10-04-gpt-a-capture-small`, `2026-10-04-gpt-a-passive`, `2026-10-04-gpt-a-capture-convergence`, `2026-10-04-gpt-a-three-scaling`, `2026-10-04-gpt-a-noise`, `2026-10-04-gpt-a-noise-small`, `2026-10-04-gpt-a-noise-convergence`, `2026-10-04-gpt-a-noise-controls`, `2026-10-04-gpt-a-noise-cw`; exploration linked above |
| 2026-10-04 | gpt-a (gpt; gpt-6-astra) | Updated the two trapping-paper access records after the next-order task; disposition unchanged | Full texts under DOI:10.1364/JOSAB.5.000392 and DOI:10.1103/PhysRevA.79.021802, with access qualifications in the next-order exploration |
