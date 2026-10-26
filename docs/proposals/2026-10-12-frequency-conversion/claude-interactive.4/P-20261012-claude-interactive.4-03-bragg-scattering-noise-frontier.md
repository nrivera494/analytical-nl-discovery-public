---
id: P-20261012-claude-interactive.4-03
title: "Raman-set noise–efficiency frontier of Bragg-scattering frequency translation in fibre"
status: candidate
priority: 3
literature_state: partial
novelty_confidence: low
target_quantity: "The minimum number of added noise photons per output spectral–temporal mode of a χ(3) Bragg-scattering frequency translator at translation efficiency η, minimized over pump powers (including unequal powers), detunings, polarizations, length and pump pulse shapes, with the Raman response, nonlinear coefficient and temperature fixed, counting spontaneous Raman scattering and pump–pump spontaneous four-wave mixing; as a closed form in g_R(Ω)/γ, n_th(Ω) and η, with its gap to the best measured translators."
model: "Two strong pumps at ω1, ω2 and a weak signal at ωs in the scalar or vector GNLSE with the silica Raman response and its symmetrized quantum-thermal reservoir, dispersion to the orders needed for phase matching, loss optional; undepleted pumps; linearized Gaussian noise; idler at ωs + ω2 − ω1."
oracle_ready: partial
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

Bragg-scattering four-wave mixing translates a signal to an idler without parametric gain, so in a Raman-free medium it adds no noise and reaches unit efficiency at coupling $\kappa L=\pi/2$, $\kappa=2\gamma\sqrt{P_1P_2}$. In silica the two pumps also scatter spontaneously into the signal and idler bands. Define $n_{\rm add}$ as the mean number of noise photons per output mode (one spectral bin of width $1/T$ over time $T$ for continuous pumps; one Schmidt mode for pulsed pumps) at the idler frequency with no signal present, and $\eta$ as the signal-to-idler photon efficiency.

**Target.** The frontier $n^{\min}_{\rm add}(\eta)=\min_{\rm config}n_{\rm add}$ over pump powers $P_1,P_2$, length, pump–signal detunings consistent with phase matching, pump polarizations and, for pulsed operation, pump shapes, at fixed $g_R(\Omega)$ (the co- and cross-polarized Raman gain spectra), $\gamma$ and $T$.

**Answer form.** For continuous co-polarized pumps and weak noise gain, the conjectured closed form is

$$n_{\rm add}(\eta)\ \ge\ \frac{\sqrt{\rho_1\rho_2}}{\gamma}\,\arcsin\sqrt\eta,\qquad \rho_j=g_R(|\Omega_j|)\,[n_{\rm th}(|\Omega_j|)+\vartheta_j],$$

with $\Omega_j$ the detuning from pump $j$ to the idler, $\vartheta_j=1$ when the idler lies on the Stokes side of pump $j$ and $0$ on the anti-Stokes side, attained at $P_1\rho_1=P_2\rho_2$. The full answer adds the noise generated in the signal band and translated with efficiency $\eta$, stimulated Raman gain or depletion of the noise, the pump–pump spontaneous four-wave-mixing term (quadratic in pump power and phase-mismatch dependent), the cross-polarized configuration, and the pulsed per-mode statement; its regime is stated as bounds on $g_RP L$, $\gamma P L$, detuning relative to the Raman band, and pump walk-off.

## Signal of hidden simplicity

- **Both quantities scale with the same product.** Conversion is a function of $\gamma\sqrt{P_1P_2}L$; spontaneous Raman noise is linear in $P_jL$ (Friis, Mejling & Rottwitt 2017, Eqs. 27–28 in the small-gain limit; Korsgaard, Koefoed & Rottwitt 2024, Eq. 23). Eliminating length between them gives a noise-versus-efficiency curve with no free parameter but the ratio $g_R/\gamma$, which for silica is a material constant times a known line shape.
- **Unequal pump powers are a free knob.** Coupling depends on $\sqrt{P_1P_2}$ while noise depends on $P_1\rho_1+P_2\rho_2$; the geometric-mean bound above follows. Raghunathan et al. (2025) used a 90 mW / 4 mW imbalance empirically to cut idler noise.
- **Published floors exist for the amplifier analogue** (Voss & Kumar 2004: Raman-limited noise figure of phase-insensitive χ(3) amplifiers) and for fixed translator configurations (Friis 2017: 2.1 dB Stokes, 2.6 dB anti-Stokes at 300 K, about 0.4 dB at 77 K). The translator frontier minimized over configuration is the missing envelope.

## Literature state

Searched 2026-10-12 (claude-interactive.4 with helper claude-interactive.4.1): "Bragg scattering four-wave mixing frequency conversion Raman noise theory"; "quantum frequency conversion fiber Raman noise photons per mode efficiency Bragg scattering"; "Raman-noise-induced noise-figure limit parametric amplifiers"; "frequency conversion single photon fiber cooled Raman noise Bragg scattering"; "spontaneous Raman scattering quantum frequency conversion silicon nitride four-wave mixing noise photons"; "noise figure frequency translation Bragg scattering fiber quantum noise"; author searches (Rottwitt, Koefoed, Korsgaard 2024–2025). DOIs checked against Crossref.

Theory on point:
- Korsgaard, Koefoed & Rottwitt, Phys. Rev. A 110, 033508 (2024), DOI [10.1103/PhysRevA.110.033508](https://doi.org/10.1103/PhysRevA.110.033508), arXiv:2406.03484. **Full text (arXiv).** Quantum model with classical pumps and a Raman phonon bath; continuous-wave closed forms; their Eq. 23 gives the heralded $g^{(2)}$ as (Raman spectrum) × $n_{\rm th}$ × $f_R\gamma P_0\ell$ while the efficiency is $\sin^2$ of the same product; they note the optimal $g^{(2)}$ is not at the optimal length because Raman noise grows linearly; Stokes/anti-Stokes asymmetry; cross-polarized pumps reduce the Raman response about tenfold; temperatures for $g^{(2)}<0.05$ at 13 THz detuning: about 135 K co-polarized, 253 K cross-polarized. No pump–pump spontaneous four-wave mixing (pumps classical); nonlinear phase modulation enters deterministically.
- Friis, Mejling & Rottwitt, Opt. Express 25, 7324 (2017), DOI [10.1364/OE.25.007324](https://doi.org/10.1364/OE.25.007324), arXiv:1701.00940. **Full text.** Semiclassical noise figures with Raman gain and loss: $NF_S=1/G+2(G-1)(n_T+1)/G$, $G=e^{g_R(P_p+P_q)z}$ (Stokes); $NF_{aS}=1/D+2(1-D)n_T/D$, $D=e^{-g_R(P_p+P_q)z}$ (anti-Stokes); efficiency with loss and Raman (their Eq. 16). Minimum 300 K noise figures 2.1 dB (Stokes) and 2.6 dB (anti-Stokes); about 0.4 dB at 77 K. No optimization over pump configuration.
- Friis et al., CLEO 2014, STu2I.2, DOI [10.1364/CLEO_SI.2014.STu2I.2](https://doi.org/10.1364/CLEO_SI.2014.STu2I.2); Rottwitt, Korsgaard & Koefoed, ICTON 2025, DOI [10.1109/ICTON67126.2025.11125181](https://doi.org/10.1109/ICTON67126.2025.11125181). **Not accessed.**
- McKinstrie, Harvey, Radic & Raymer, Opt. Express 13, 9131 (2005), DOI [10.1364/OPEX.13.009131](https://doi.org/10.1364/OPEX.13.009131). **Abstract only.** Bragg scattering translates quantum states with reduced Raman pollution if frequencies and polarizations are chosen well. Must-read for whether a detuning-dependent noise estimate is given.
- McKinstrie, Yu, Raymer & Radic, Opt. Express 13, 4986 (2005), DOI [10.1364/OPEX.13.004986](https://doi.org/10.1364/OPEX.13.004986). **Abstract only.** Multi-mode quantum noise of parametric processes including frequency conversion; no Raman in the abstract.
- Mejling, McKinstrie, Raymer & Rottwitt, Opt. Express 20, 8367 (2012), DOI [10.1364/OE.20.008367](https://doi.org/10.1364/OE.20.008367); Mejling, Cargill, McKinstrie, Rottwitt & Moore, Opt. Express 20, 27454 (2012), DOI [10.1364/OE.20.027454](https://doi.org/10.1364/OE.20.027454). **Not accessed.** Low-conversion Green-function theory; deterministic nonlinear phase modulation.
- Voss & Kumar, Opt. Lett. 29, 445 (2004), DOI [10.1364/OL.29.000445](https://doi.org/10.1364/OL.29.000445). **Abstract only.** Raman-limited noise figure of χ(3) parametric amplifiers. Voss, Köprülü & Kumar, JOSA B 23, 598 (2006), DOI [10.1364/JOSAB.23.000598](https://doi.org/10.1364/JOSAB.23.000598), arXiv:quant-ph/0410214. **Full text.** Phase-sensitive and phase-insensitive noise figures in terms of the real and imaginary nonlinear response and $n_{\rm th}$ (their Eq. 93); no Bragg scattering.
- Lefrancois, Clark & Eggleton, Phys. Rev. A 91, 013837 (2015), DOI [10.1103/PhysRevA.91.013837](https://doi.org/10.1103/PhysRevA.91.013837), arXiv:1412.3511. **Abstract only.** Optimization against spurious four-wave mixing and modulation instability; Raman not in the abstract.
- Known selectivity limits (solved, not a target): Reddy, Raymer, McKinstrie, Mejling & Rottwitt, Opt. Express 21, 13840 (2013), DOI [10.1364/OE.21.013840](https://doi.org/10.1364/OE.21.013840); Reddy, Raymer & McKinstrie, Opt. Lett. 39, 2924 (2014), DOI [10.1364/OL.39.002924](https://doi.org/10.1364/OL.39.002924); Quesada & Sipe, Opt. Lett. 41, 364 (2016), DOI [10.1364/OL.41.000364](https://doi.org/10.1364/OL.41.000364). **Not accessed** (DOIs verified).

Experiments (achievable points):
- McGuinness, Raymer, McKinstrie & Radic, Phys. Rev. Lett. 105, 093604 (2010), DOI [10.1103/PhysRevLett.105.093604](https://doi.org/10.1103/PhysRevLett.105.093604), arXiv:1006.4350. **Full text.** Photonic-crystal fibre, 683 to 659 nm, 20 m, pumps about 20 and 30 mW at 808 and 845 nm; efficiency 28.6 ± 2.2%; about 24% of the counts in the 659 nm channel and 11% at 683 nm were pump-induced noise, mostly from the 808 nm pump; $g^{(2)}(0)=0.19\pm0.05$ after translation.
- Clark, Shahnia, Collins, Xiong & Eggleton, Opt. Lett. 38, 947 (2013), DOI [10.1364/OL.38.000947](https://doi.org/10.1364/OL.38.000947). **Abstract only.** 750 m highly nonlinear fibre; 99.1 ± 4.9% down- and 98.0 ± 5.0% up-conversion by 12 nm; noise not in the abstract.
- Krupa et al., Opt. Express 20, 27220 (2012), DOI [10.1364/OE.20.027220](https://doi.org/10.1364/OE.20.027220), arXiv:1211.4950. **Abstract only.** Highly nonlinear fibre, photon counting, polarization-dependent noise.
- Agha, Davanço, Thurston & Srinivasan, Opt. Lett. 37, 2997 (2012), DOI [10.1364/OL.37.002997](https://doi.org/10.1364/OL.37.002997); Li, Davanço & Srinivasan, Nat. Photon. 10, 406 (2016), DOI [10.1038/nphoton.2016.64](https://doi.org/10.1038/nphoton.2016.64); Singh et al., Optica 6, 563 (2019), DOI [10.1364/OPTICA.6.000563](https://doi.org/10.1364/OPTICA.6.000563). **Abstract only.** Silicon-nitride waveguides and microrings: about 5%; 25% to above 60% with femtowatt-to-picowatt noise; about 12% on chip with $g^{(2)}(0)$ from 0.080 to 0.290.
- Raghunathan et al., Optica Quantum 3, 329 (2025), DOI [10.1364/OPTICAQ.563123](https://doi.org/10.1364/OPTICAQ.563123), arXiv:2505.10338. **Full text.** Silicon-nitride chip, 1260 to 698 nm, 40 THz pump–signal separation; 5% on-chip efficiency; idler noise 220 kHz on chip from the 780 nm pump, below 3 kHz after an etalon and pump imbalance; noise channels identified as fluorescence (linear, unpolarized), spontaneous four-wave mixing (quadratic, co-polarized) and Raman (linear, co-polarized).

**What is solved.** Noise scalings with pump power, length, detuning, polarization and temperature for fixed configurations (Friis 2017; Korsgaard 2024); the amplifier noise-figure floor (Voss & Kumar); temporal-mode selectivity limits. **Not found:** the frontier minimized over configuration, the pump-asymmetry law, the combined Raman plus spontaneous-four-wave-mixing floor at large detuning, and a per-temporal-mode statement for pulsed pumps.

## Sharpest statement of the gap

For a single pump configuration the bound above is a corollary of the DTU results and would not be a new result. What is open is the envelope: (i) the minimum over $P_1/P_2$, detunings and polarizations at fixed $\eta$, including the Stokes/anti-Stokes placement of both pumps; (ii) where the spontaneous four-wave-mixing channel takes over from Raman as the detuning leaves the Raman band (the regime of the 40 THz silicon-nitride translator), and the resulting minimum over detuning; (iii) the pulsed-pump statement per Schmidt mode, where Raman noise generated within the pump envelope competes with mode-selective conversion; (iv) whether the pump's own quantum noise, through cross-phase modulation, adds a channel at any practical photon number (an estimate gives a phase variance of order $\gamma P L\times2/N_{\rm pump}$, negligible, but no source treats it).

## Conjectures

No claim files yet. The refutable conjecture to register first:

**C1.** For continuous co-polarized pumps, phase-matched, $g_R(P_1+P_2)L\le0.2$ and loss neglected, the idler noise per mode satisfies $n_{\rm add}\ge(\sqrt{\rho_1\rho_2}/\gamma)\arcsin\sqrt\eta$ for every $P_1/P_2$, with equality within 10% at $P_1\rho_1=P_2\rho_2$ and $\eta\le0.5$. Refuted by any linearized-noise run with a lower value.

## Oracle

**Partial.** The solver's linearized covariance with the Raman reservoir computes the idler-band noise for any pump field (two long pulses plus vacuum), including spontaneous four-wave mixing automatically, since pump–pump parametric processes act on the input vacuum. Caveats: the Raman Langevin spectrum must be symmetrized (T-20261004-gpt-b-02), the sampled Raman kernel needs time steps of 3 fs or less (T-20261006-claude-interactive-02), and continuous pumps need long windows, so use pulses of 100 ps or more and read the noise per spectral bin in the flat-top region.

Cheap test: silica fibre at 1550 nm, pumps 10 THz apart, signal 5–20 THz from the nearer pump; sweep $P_1/P_2$ at fixed $P_1P_2$ and $L$; compare the idler-band noise per bin with the bound. Then sweep detuning through the 13 THz Raman peak and beyond 30 THz to locate the Raman-to-spontaneous-four-wave-mixing crossover.

Missing: a two-polarization Raman reservoir is in the model but its multimode noise path is single-mode only in the stochastic solver (fine here, since the linearized path is used).

## Lab test

A highly nonlinear fibre translator with photon counting at the idler and no input signal. At fixed efficiency (fixed $P_1P_2L$) vary $P_1/P_2$ and record the noise rate; the minimum should occur at $P_1\rho_1=P_2\rho_2$ and equal the bound within the detector calibration. Cooling to 77 K and rotating one pump's polarization test $n_{\rm th}$ and the cross-polarized $\rho$. A noise rate below the bound at any setting refutes it.

## Risks and must-reads

- **Novelty is the main risk.** The fixed-configuration bound is already implied by Korsgaard et al. (2024); the card stands or falls on the envelope over configurations and the pulsed statement. The orchestrator should weigh this against the other cards.
- **McKinstrie et al. (2005) full text** may contain a detuning-dependent Raman-noise estimate; read before deriving.
- **At large detuning the dominant noise is not Raman** (fluorescence and spontaneous four-wave mixing in silicon nitride, Raghunathan 2025); the silica Raman tail beyond 30 THz needs a measured spectrum, not the single-Lorentzian model.
- **Must-reads not accessed:** McKinstrie 2005 (both); Mejling 2012 (both); Lefrancois 2015 full text; Clark 2013 full text for the noise numbers.
- Not in scope: χ(2) converters (other proposer); temporal-mode selectivity (solved).

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.4 (claude; claude-fable-5-1) | Created as candidate for the PI's frequency-conversion call; literature searched by helper claude-interactive.4.1 and checked against Crossref; no runs yet | Search strings and sources above; task T-20261012-claude-interactive.4-01 |
