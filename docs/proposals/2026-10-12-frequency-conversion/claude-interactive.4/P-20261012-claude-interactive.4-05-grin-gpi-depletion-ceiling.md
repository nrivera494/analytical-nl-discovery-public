---
id: P-20261012-claude-interactive.4-05
title: "Depletion ceiling of geometric-parametric-instability sideband conversion in GRIN fibre"
status: candidate
priority: 4
literature_state: partial
novelty_confidence: low
target_quantity: "The maximum photon fraction that quasi-continuous-wave geometric parametric instability in graded-index multimode fibre can convert into the h-th sideband pair, over launch beam width, power and length, as a closed form in the residual phase mismatch (including the power-dependent self-imaging period and self- and cross-phase modulation), the Floquet coupling of order h, and the sideband–pump walk-off; with the measured first-sideband fraction as the achievable point."
model: "Reduced 1+1D GNLSE with a periodically modulated nonlinear coefficient γ(z) set by the Kerr-modified self-imaging of the beam (Conforti et al. 2017), with β2 at the pump; checked against the full 3D GRIN multimode GNLSE (many-mode CP backend); quasi-continuous pumps, optional Raman, noise-seeded sidebands."
oracle_ready: available
last_audited: null
audited_by: [claude]
proposed_by: claude-interactive.4
provenance:
  agent: claude-interactive.4
  model: claude-fable-5-1
  family: claude
claims: []
results: []
---

## Target quantity

In graded-index fibre a launched beam self-images with period $\xi$, and the Kerr nonlinearity it experiences oscillates with $z$. The oscillation quasi-phase-matches sideband pairs at detunings $f_h\simeq\sqrt h\,f_1$ with $f_1$ of order 100 THz (Longhi 2003; Krupa et al. 2016). The linear Floquet gain is solved. What is not solved is how much of the pump can end up in a given pair once the pump depletes, the self-imaging period shifts with power, and the sidebands walk off.

**Target.** $\eta_h^{\max}=\max_{w_0,P,L}\,E_h/E_{\rm in}$, the maximal photon fraction in the $h$-th pair over launch width $w_0$, power $P$ and length $L$, for a fibre with given core radius, index contrast and $\beta_2$.

**Answer form.** Truncating the reduced model to the pump and one pair gives a three-wave Hamiltonian system with coupling $\gamma_h$ (the $h$-th Fourier coefficient of $\gamma(z)$) and residual mismatch $\kappa_h=\Delta\beta_h-2\pi h/\xi(P)+(\text{SPM/XPM terms})$. The conjecture is that its exact depleted solution (elliptic functions, as in Cappellini & Trillo 1991) gives $\eta_h^{\max}=F(\kappa_h/\gamma_hP)$ in closed form, that $F$ is reached at an optimal length, and that pulsed operation lowers it by a walk-off factor in $L_{\rm conv}\Delta\beta_1/T_0$. The regime is stated as bounds on the modulation depth, $\gamma_hP/\kappa_h$, the number of competing orders and the walk-off group.

## Signal of hidden simplicity

- **The sideband positions are a one-line law** with a Kerr correction from the path-averaged intensity (Krupa et al. 2016, full text; Conforti et al. 2017, full text): the complicated multimode dynamics reduces to a periodic scalar coefficient.
- **The measured conversion is large.** In 0.4 m of GRIN fibre with 9 ps, 50 kW pulses the first anti-Stokes sideband was only 2 dB below the residual pump (Krupa et al. 2016, full text), so depletion matters and a ceiling is a practical question.
- **The depleted three-wave ceiling is one line.** For gas-filled multipass cells the pump-depleted coupled-mode model gives $u_{\max}=1-|D_h|/2$ in the normalized residual mismatch $D_h$ (Mei et al. 2026, full text). The same reduction applies to the periodic-coefficient fibre model with $D_h\to\kappa_h/\gamma_hP$, so the fibre ceiling has a candidate closed form before any derivation. What that formula leaves out is exactly the fibre physics: the self-imaging period and the SPM/XPM mismatch move as the pump depletes, the sidebands walk off, and several orders compete.
- No registered run yet; see Oracle.

## Literature state

Searched 2026-10-12 (claude-interactive.4 with helper claude-interactive.4.4): "geometric parametric instability graded-index multimode fiber conversion efficiency saturation depletion"; "geometric parametric instability sidebands pump depletion Floquet Hill equation"; "GPI graded-index fiber sideband conversion efficiency percent measured"; "quasi-phase-matched four-wave mixing self-imaging depletion"; "intermodal four-wave mixing conversion efficiency limit walk-off pulsed pump few-mode fiber"; author and title searches. DOIs checked against Crossref.

- Longhi, Opt. Lett. 28, 2363 (2003), DOI [10.1364/OL.28.002363](https://doi.org/10.1364/OL.28.002363). **Not accessed.** Modulational instability in parabolic-index fibre.
- Krupa et al., Phys. Rev. Lett. 116, 183901 (2016), DOI [10.1103/PhysRevLett.116.183901](https://doi.org/10.1103/PhysRevLett.116.183901). **Full text.** Quasi-phase-matching condition $2k_P-k_S-k_A=-2\pi h/\xi$ with the Kerr shift of the sideband frequencies; experiment with 0.4 m fibre (core radius 26 µm), 9 ps, 50 kW: $f_1\simeq123.5$ THz, first anti-Stokes 2 dB below the residual pump; simulated Kerr shift about 2 THz for a fourfold power increase. Linear Floquet analysis only.
- Wright, Wabnitz, Christodoulides & Wise, Phys. Rev. Lett. 115, 223902 (2015), DOI [10.1103/PhysRevLett.115.223902](https://doi.org/10.1103/PhysRevLett.115.223902). **Not accessed.**
- Conforti, Mas Arabi, Mussot & Kudlinski, Opt. Lett. 42, 4004 (2017), DOI [10.1364/OL.42.004004](https://doi.org/10.1364/OL.42.004004), arXiv:1707.09223. **Full text.** 1+1D GNLSE with $\gamma(z)=\omega_0n_2/(2\pi c\,a^2(z))$; $f_m\approx\sqrt{m/(2\pi z_{\rm SI}\beta_2)}$; phase matching with the $\gamma_{\rm av}P/2$ term. No depletion, saturation or walk-off.
- Mas Arabí, Kudlinski, Mussot & Conforti, arXiv:1711.05703. **Full text.** Floquet gain of periodically modulated GRIN fibre; no depletion.
- Teğin & Ortaç, Frontiers in Optics 2017, JTu3A.72, DOI [10.1364/FIO.2017.JTu3A.72](https://doi.org/10.1364/FIO.2017.JTu3A.72). **Abstract only.** Femtosecond GPI; no efficiency numbers.
- Mei et al., "Geometric parametric instability in nonlinear multipass cells", arXiv:2608.13288 (2026). **Full text (arXiv HTML), read by claude-interactive.4.** Floquet quasi-phase-matching from the discrete Gouy-phase imbalance per pass. Their pump-depleted three-wave model reduces to $(du/dz')^2=4u^2(1-u)^2-D_h^2u^2$ (their Eq. 21) with $u$ the converted fraction and $D_h=\delta k_{\rm in}/\kappa_{\rm in}$ the residual mismatch normalized by the coupling, giving $u_{\max}=1-|D_h|/2$ for $|D_h|\le2$ (their Eq. 22). The SPM and XPM contributions to the mismatch are evaluated at the input pump power and held fixed during depletion; the Gouy phase is geometric, not power dependent; walk-off and pulsed pumps are not treated analytically; no converted fractions are tabulated from their multimode simulations. They state that GRIN-fibre GPI, with its continuous self-imaging modulation, is a different mechanism and do not claim transfer.
- Cappellini & Trillo, JOSA B 8, 824 (1991), DOI [10.1364/JOSAB.8.000824](https://doi.org/10.1364/JOSAB.8.000824). **Abstract only.** Exact depleted solutions of pump plus two sidebands in single-mode fibre; spatially unstable eigensolutions control the power exchange.
- Nazemosadat, Pourbeyram & Mafi, JOSA B 33, 144 (2016), DOI [10.1364/JOSAB.33.000144](https://doi.org/10.1364/JOSAB.33.000144); Dupiol et al., Opt. Lett. 42, 1293 (2017), DOI [10.1364/OL.42.001293](https://doi.org/10.1364/OL.42.001293). **Not accessed.** Intermodal phase matching and far-detuned cascades in GRIN fibre.
- Random coupling in long fibres (regime boundary, not a target): Xiao, Essiambre, Desgroseilliers, Tulino, Ryf, Mumtaz & Agrawal, Opt. Express 22, 32039 (2014), DOI [10.1364/OE.22.032039](https://doi.org/10.1364/OE.22.032039), **abstract only** (about 3 dB penalty with few coupled modes, above 40 dB when all couple); Guasoni, Parmigiani, Horak, Fatome & Richardson, J. Lightwave Technol. 35, 5296 (2017), DOI [10.1109/JLT.2017.2767103](https://doi.org/10.1109/JLT.2017.2767103), arXiv:1705.09106, **abstract only**.

**What is solved.** Sideband frequencies with the Kerr shift; linear gain and bandwidth; the depleted single-mode three-wave solution; a depleted model in a cognate geometry. **Not found:** a depleted conversion ceiling for GRIN fibre as a function of mismatch, coupling order and walk-off, or any optimization over launch conditions.

## Sharpest statement of the gap

The fixed-mismatch ceiling $u_{\max}=1-|D_h|/2$ is now in print for a cognate system (Mei et al. 2026) and transfers to the reduced fibre model without new work, so it is not a result for this card. What is open for GRIN fibre: (i) the ceiling when the mismatch itself depends on the depleted pump power, through the Kerr shift of the self-imaging period (Krupa et al. 2016) and the SPM/XPM terms, which Mei et al. freeze at the input power; (ii) the walk-off reduction for pulsed pumps; (iii) whether the single-pair truncation survives when several orders have comparable gain; and (iv) a check of all of these against the 3D multimode dynamics, where the sidebands occupy different mode sets than the pump.

## Conjectures

No claim files yet. The refutable conjecture to register first:

**C1.** For quasi-continuous pumping ($T_0\ge10$ ps), $h=1$, and launch widths within 30% of the fundamental-mode width, the first-pair photon fraction over power and length satisfies $\eta_1\le1-|D_1(P_{\rm in})|/2$ with $D_1=\kappa_1/\gamma_1P_{\rm in}$ evaluated at the input power (the Mei et al. form), within 20%, for modulation depths below 0.5, and the power dependence of the self-imaging period lowers the reachable fraction below it by a computable amount; the 3D multimode solver does not exceed the fixed-mismatch ceiling for any launch in that set. Refuted by any 3D run above the ceiling.

## Oracle

**Available.** The solver's GRIN multimode GNLSE (dense and CP-decomposed many-mode backends) for the 3D check; the scalar GNLSE with a $z$-dependent coefficient for the reduced model (if $\gamma(z)$ is not an option, it is a small opt-in change under `docs/SOLVER.md`); adjoint gradients with respect to the launch field.

Cheap test: 62.5 µm-core GRIN parameters at 1064 nm, 10–50 kW quasi-continuous pump, $L$ up to 1 m; reduced model sweep of $P$ and $L$ at fixed $w_0$ to map $\eta_1$ and the optimum length; 3D runs at five launch widths; adjoint optimization of the launch over width, curvature and power.

Convergence: mode-basis truncation (report the mode count at which $\eta_1$ changes by less than 2%), step size against the self-imaging period, time window for the sidebands' walk-off.

Missing: nothing beyond a possible $\gamma(z)$ option.

## Lab test

Graded-index fibre with a picosecond or nanosecond 1064 nm pump. Measure the first-pair photon fraction versus power and length at a fixed launch; compare with the ceiling at the fibre's $\kappa_1$. Changing the launch width changes the modulation depth and moves the ceiling in a predicted way. A fraction above the ceiling at any power refutes it.

## Risks and must-reads

- **Low novelty, confirmed.** Mei et al. (2026, full text) give the fixed-mismatch ceiling for a cognate system and it transfers to the reduced fibre model without change; the fibre card is a result only if the depletion-dependent mismatch, walk-off or order competition changes the ceiling by more than the numerical uncertainty.
- **The single-pair truncation may fail** at the powers used in experiments, where many orders and Raman cascades compete; the ceiling would then be an upper envelope only.
- **Noise seeding** makes the sideband fraction a random variable; the ceiling should be stated for the mean and the regime where seeding statistics do not matter.
- **Must-reads not accessed:** Longhi (2003); Wright et al. (2015); Nazemosadat et al. (2016); Dupiol et al. (2017).
- Overlap: P-010 (pulsed Kerr self-cleaning) shares the GRIN model; none of the existing cards targets GPI conversion.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.4 (claude; claude-fable-5-1) | Created as candidate for the PI's frequency-conversion call; literature searched by helper claude-interactive.4.4 and checked against Crossref; no runs yet | Search strings and sources above; task T-20261012-claude-interactive.4-01 |
| 2026-10-12 | claude-interactive.4 (claude; claude-fable-5-1) | Mei et al. (2026) read in full: fixed-mismatch ceiling $u_{\max}=1-|D_h|/2$ already in print for a cognate system; gap narrowed to the depletion-dependent mismatch, walk-off and order competition; novelty stays low | arXiv:2608.13288, Eqs. 21–22 and Appendix A |
