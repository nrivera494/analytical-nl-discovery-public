---
id: P-20261012-claude-interactive.4-04
title: "Raman-budget bound on supercontinuum energy delivered blue of the pump"
status: candidate
priority: 3
literature_state: partial
novelty_confidence: medium
target_quantity: "An upper bound on the fraction of launched photons that a soliton-fission supercontinuum can deliver into a band blue-shifted by Ω_b from the pump in a fibre of length L, in terms of the maximal soliton red-shift reachable in L (the self-frequency-shift reach of the fission products) and the group-velocity-matching relation of trapped dispersive waves, using the monotone decrease of the mean frequency under Raman together with momentum conservation; with its gap to adjoint-optimized input pulses."
model: "Scalar GNLSE with β(ω) to all orders (one zero-dispersion wavelength, pump in anomalous dispersion), Kerr, self-steepening, measured Raman response, loss; coherent input; photon-number-conserving form."
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

Let $\eta_b$ be the fraction of launched photons found at the output above a blue edge $\omega_0+\Omega_b$ (band of any width beyond it), and let $\bar\Omega_r$ be the mean red-shift of the remaining photons. With the mean frequency $\langle\omega\rangle(z)$ of the photon distribution,

$$\eta_b\,\Omega_b-(1-\eta_b)\,\bar\Omega_r=\langle\omega\rangle(L)-\omega_0\le0,$$

the inequality being the Raman dissipation statement (below). So $\eta_b\le\bar\Omega_r/(\Omega_b+\bar\Omega_r)$, and the question becomes how large $\bar\Omega_r$ can be. In a fission supercontinuum the red photons sit in Raman solitons whose shifts are bounded by their self-frequency-shift reach in $L$, and the blue photons are dispersive waves trapped by those solitons, whose frequency is tied to the soliton frequency by group-velocity matching $\beta_1(\omega_0+\Omega_b)=\beta_1(\omega_0-\Omega_r)$ (Gorbach & Skryabin 2007).

**Target.** The bound $\eta_b^{\max}(\Omega_b;L,N,\delta_3,f_R,\beta(\omega))$ obtained by (i) the Raman inequality and momentum balance, (ii) the maximal red-shift $\Omega_r^{\max}(L)$ over the fission products of an input of order $N$ (the shortest soliton, $T_1=T_0/(2N-1)$, shifts fastest), integrated through $\beta_2(\omega)$ and the loss edge, and (iii) the group-velocity link between $\Omega_b$ and $\Omega_r$, which makes $\Omega_b$ a function of $\Omega_r$ and the dispersion profile rather than a free variable.

**Answer form.** A closed-form inequality $\eta_b\le F(\Omega_b;\Omega_r^{\max}(L))$ with $\Omega_r^{\max}$ given by an integrated Gordon law in $T_R/T_1$, $L/L_{D,1}$ and the dispersion slope; its regime as bounds on $N$, $\delta_3$, $T_R/T_1$ and $L/L_{D,1}$; and the gap, in photon fraction, between the bound and the best adjoint-optimized input.

## Signal of hidden simplicity

- **The mean frequency only goes down with Raman.** The Raman term transfers energy from higher to lower frequencies because ${\rm Im}\,\tilde h_R(\Omega)\ge0$ for $\Omega>0$; in the moment method the shift rate is a signed first moment of the Raman gain against the intensity spectrum (Santhanam & Agrawal 2003, **abstract only**). A universal red-shift and a monotonically decreasing energy are asserted for the photon-conserving model (Huang et al. 2026, **abstract only**). This turns the orchestrator's momentum identity into an inequality that works in the direction of a bound.
- **Blue light is paid for by red light at a fixed exchange rate.** Trapped dispersive waves blue-shift as fast as the trapping soliton red-shifts in group velocity (Gorbach & Skryabin 2007; Stone & Knight 2008), so the blue edge of a long supercontinuum tracks the reddest soliton. The exchange rate is $\Omega_b/\Omega_r$ fixed by $\beta_1(\omega)$.
- **The red reach is a known law.** Gordon's $T^{-4}$ rate with the growth of $|\beta_2|$ along the shift gives a reach that saturates with distance (Santhanam & Agrawal 2003), and in silica the loss edge near 2.3–2.5 µm caps it.
- **Shaping experiments report enhancement factors but never an absolute ceiling** (Hary et al. 2023, 2025), which is what a bound would add.
- No registered run yet; see Oracle.

## Literature state

Searched 2026-10-12 (claude-interactive.4 with helper claude-interactive.4.3): "supercontinuum blue edge energy limit trapped dispersive wave Gorbach Skryabin energy budget"; "Raman term GNLSE mean frequency monotonically decreases proof photon number"; "supercontinuum pulse shaping optimization target band energy"; "differentiable simulation supercontinuum optimization adjoint target band energy"; "automatic differentiation gradient optimization supercontinuum GNLSE pulse shape inverse design"; title searches. DOIs checked against Crossref.

Monotone red-shift and photon conservation:
- Santhanam & Agrawal, Opt. Commun. 222, 413 (2003), DOI [10.1016/S0030-4018(03)01561-X](https://doi.org/10.1016/S0030-4018(03)01561-X). **Abstract only.** Moment-method Raman shift for arbitrary pulses in both dispersion regimes; saturation when the pulse broadens. The sign statement for arbitrary pulses was not verified from the text.
- Blow & Wood, IEEE J. Quantum Electron. 25, 2665 (1989), DOI [10.1109/3.40655](https://doi.org/10.1109/3.40655). **Not accessed.** Raman-GNLSE; energy loss by the Raman term.
- Linale, Fierens, Bonetti & Sánchez, Opt. Lett. 45, 4535 (2020), DOI [10.1364/OL.401096](https://doi.org/10.1364/OL.401096). **Not accessed.** Photon-conserving NLSE (the form in which photon number is exactly conserved).
- Huang et al., "Photon-conserving Raman soliton attractors in focusing and defocusing Kerr media", arXiv:2607.05244 (2026). **Abstract only.** Universal spectral red-shift and monotonically decreasing pulse energy regardless of the Kerr sign.

Trapping and the blue edge:
- Gorbach & Skryabin, Nat. Photon. 1, 653 (2007), DOI [10.1038/nphoton.2007.202](https://doi.org/10.1038/nphoton.2007.202); Phys. Rev. A 76, 053803 (2007), DOI [10.1103/PhysRevA.76.053803](https://doi.org/10.1103/PhysRevA.76.053803). **Abstract only.** Gravity-like trapping of dispersive waves by decelerating solitons; the opposing shifts exceed the bare self-frequency-shift rate.
- Skryabin & Gorbach, Rev. Mod. Phys. 82, 1287 (2010), DOI [10.1103/RevModPhys.82.1287](https://doi.org/10.1103/RevModPhys.82.1287). **Not accessed.**
- Stone & Knight, Opt. Express 16, 2670 (2008), DOI [10.1364/OE.16.002670](https://doi.org/10.1364/OE.16.002670). **Not accessed.** Group-velocity matching sets the blue edge.
- Sørensen, Judge, Thomsen & Bang, Opt. Lett. 36, 816 (2011), DOI [10.1364/OL.36.000816](https://doi.org/10.1364/OL.36.000816). **Abstract only.** Tapers: the trapped, blue-shifted fraction grows as the taper gradient decreases; quantified by group-acceleration mismatch.
- Travers, J. Opt. 12, 113001 (2010), DOI [10.1088/2040-8978/12/11/113001](https://doi.org/10.1088/2040-8978/12/11/113001). **Not accessed.** Review of blue extension.
- Dudley, Genty & Coen, Rev. Mod. Phys. 78, 1135 (2006), DOI [10.1103/RevModPhys.78.1135](https://doi.org/10.1103/RevModPhys.78.1135). **Abstract only.**

Pulse-shaping optimization (what the reachable set looks like):
- Wetzel et al., Nat. Commun. 9, 4884 (2018), DOI [10.1038/s41467-018-07141-w](https://doi.org/10.1038/s41467-018-07141-w). **Abstract only.**
- Michaeli & Bahabad, J. Opt. 20, 055501 (2018), DOI [10.1088/2040-8986/aab59c](https://doi.org/10.1088/2040-8986/aab59c). **Abstract only.**
- Hary et al., Opt. Lett. 48, 4512 (2023), DOI [10.1364/OL.492064](https://doi.org/10.1364/OL.492064). **Abstract only.** Genetic-algorithm Fourier-domain shaping in highly nonlinear fibre; enhancement factors 5–20 (1550–1800 nm) and above 160 near 2000 nm.
- Hary, Koivisto, Lukasik, Dudley & Genty, Sci. Rep. 15 (2025), DOI [10.1038/s41598-024-84567-x](https://doi.org/10.1038/s41598-024-84567-x). **Full text.** Genetic, particle-swarm and annealing optimizers; enhancement up to a few hundred near the pump, 2–10 far from it; model-free; simultaneous enhancement of arbitrary channel sets "not always achievable".
- Lee et al., arXiv:2312.10640. **Abstract only.** Inverse design of waveguide geometry for coherent supercontinua.

**What is solved.** The trapping mechanism and the group-velocity-matching rule for the blue edge; the Raman shift of a given pulse; enhancement factors from shaping. **Not found:** any bound on the blue-band photon fraction; any energy-budget statement between soliton red-shift and trapped-wave blue-shift; any gradient-based optimization of the band energy against which a bound could be scored.

## Sharpest statement of the gap

Nobody has written the blue-band yield as an inequality. The three ingredients exist separately: momentum balance (the orchestrator's conservation-law card), the sign of the Raman shift, and the group-velocity link of trapped waves to their solitons. Open: whether their combination gives a tight ceiling (within a factor of two of shaped optima) or a loose one; what sets $\Omega_r^{\max}(L)$ once fission products interact (collisions re-partition energy); and whether the Raman inequality can be strengthened to a rate bound, $-d\langle\omega\rangle/dz\le c\,\gamma f_R\max_\Omega[{\rm Im}\,\tilde h_R(\Omega)\,\Omega]\,P_{\rm peak}$, that holds for any field and caps the budget independently of soliton theory.

## Conjectures

No claim files yet. The refutable conjecture to register first:

**C1.** For an input of order $N\in[3,8]$ in a fibre with one zero-dispersion wavelength, $\delta_3\in[0.02,0.2]$, $f_R=0.18$ and $L\le20L_D$, the photon fraction above any blue edge $\Omega_b$ satisfies $\eta_b\le\Omega_r^{(1)}(L)/(\Omega_b+\Omega_r^{(1)}(L))$, where $\Omega_r^{(1)}(L)$ is the integrated Gordon shift of the first fission soliton ($T_1=T_0/(2N-1)$, energy fraction $(2N-1)/N^2$) through the fibre's $\beta_2(\omega)$; and the ratio of the measured blue edge to the reddest soliton frequency follows $\beta_1$ matching within 5%. Refuted by any run, shaped or not, with $\eta_b$ above the bound.

## Oracle

**Available.** Scalar GNLSE with full $\beta(\omega)$, Raman, self-steepening and loss; adjoint gradients with respect to the input field.

Cheap test: a standard photonic-crystal-fibre dispersion (zero-dispersion wavelength near 780 nm, pump at 800–850 nm), $N=3$–8, $L$ up to $20L_D$; record $\eta_b$ for a set of blue edges, the reddest soliton frequency and the mean frequency along $z$ (check its monotone decrease); compare with the bound. Then run the adjoint optimizer over 20–40 input parameters at fixed energy and duration to maximize $\eta_b$ for one edge; the bound fails if exceeded.

Convergence: the mean frequency must be computed in the photon-number-conserving form (the solver's self-steepening term defines it); report step-size and window checks on $\eta_b$ to 1%.

Missing: nothing for the single-mode case.

## Lab test

A photonic-crystal-fibre supercontinuum pumped by a femtosecond oscillator. Sweep pump energy and fibre length; measure the photon fraction above a chosen blue edge and the wavelength of the reddest soliton with a calibrated spectrometer. Plot $\eta_b$ against $\Omega_r/(\Omega_b+\Omega_r)$; points above the line refute the bound. The group-velocity link is tested by comparing the blue edge with $\beta_1$ matching of the reddest soliton.

## Risks and must-reads

- **Overlap with the orchestrator's conservation-law cards.** Momentum balance is theirs; this card's additions are the Raman inequality, the reach law and the trapping link. If the orchestrator's bound already uses the Raman sign, merge.
- **The bound may be loose** because most red photons sit in solitons that do not trap anything; a tight version needs the trapped fraction, which Sørensen et al. (2011) show is tunable by tapering.
- **The Raman sign statement for arbitrary fields** must be proved, not quoted; the abstracts located assert it for specific models.
- **Must-reads not accessed:** Santhanam & Agrawal (2003) full text; Blow & Wood (1989); Stone & Knight (2008); Skryabin & Gorbach (2010); Travers (2010).
- Overlap: P-20261012-claude-interactive.4-01 (fission dispersive-wave yield) supplies the initial blue photons; P-013 (parked) concerns noise-rejecting observables, not yield.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.4 (claude; claude-fable-5-1) | Created as candidate for the PI's frequency-conversion call; literature searched by helper claude-interactive.4.3 and checked against Crossref; no runs yet | Search strings and sources above; task T-20261012-claude-interactive.4-01 |
