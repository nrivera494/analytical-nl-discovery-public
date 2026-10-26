---
id: P-003
title: "Self-consistent selection of gain-managed amplification"
status: audited
priority: 3
literature_state: partial
novelty_confidence: low
target_quantity: "Conditions under which coupled Yb inversion and pulse dynamics select a stable-peak-power gain law, and controlled limits of that regime."
model: "GNLSE with frequency-dependent gain from pump/signal Yb rate equations, Kerr and Raman; specified pumping and repetition rate."
oracle_ready: partial
last_audited: 2026-10-02
audited_by: [claude, gpt]
proposed_by: claude-bootstrap
updated_by: gpt-a
updated_model: unknown
updated_family: gpt
claims: []
results: []
---

## Target quantity

Establish whether, and in which parameter region, self-consistent gain dynamics select the near-logarithmic integrated-gain behavior associated with stable peak power. Predict the deviation from that behavior and its dependence on pump direction, seed wavelength, saturation and fiber length. A reduced rate-equation/pulse model is a starting point already present in the literature; the target is a selection/stability law with error control, not the first moment model with inversion.

Define a usable energy limit by a specified tolerance for compressibility, Raman conversion or modal instability, at fixed pump and geometry. “Maximum energy” without such a constraint is not a well-defined universal quantity. Treat few-mode amplification as a later extension requiring overlap-resolved inversion and gain, not as a claimed empty field.

## Signal of hidden simplicity

Experiments and rate-equation simulations show broad, compressible output pulses and reduced sensitivity to seed conditions in gain-managed amplification. This motivates an attracting reduced description but does not prove a unique global attractor or universal gain exponent.

## Literature state

- Sidorenko, Fu & Wise (2019), [arXiv:1906.04141](https://arxiv.org/abs/1906.04141), [DOI:10.1364/OPTICA.6.001328](https://doi.org/10.1364/OPTICA.6.001328): gain-managed nonlinear amplification demonstrated experimentally and with GNLSE/rate-equation modeling. **Full text**, model and discussion accessed. Evidence of robust evolution is not an attractor theorem.
- Sidorenko & Wise (2020), [DOI:10.1364/OL.396683](https://doi.org/10.1364/OL.396683): large-mode-area scaling demonstrated. **Abstract only.** Mode-area scaling is not wholly unexplored.
- Turitsyn, Bednyakova & Podivilov (2023), [DOI:10.1103/PhysRevLett.131.153802](https://doi.org/10.1103/PhysRevLett.131.153802): **full text**, model and reduction. A prescribed linear spectral gain slope leads to dissipative shallow-water dynamics and spectral shocks. The unbounded slope model has a finite spectral domain of physical use; it is not self-consistent population inversion or an oscillatory Whitham theory.
- Kozlov, Ivanov, McKinstrie & Sidorenko (2025), [DOI:10.1364/OE.549410](https://doi.org/10.1364/OE.549410), *Generalized method of moments for investigation of ultra-fast fiber amplifiers with gain-managed nonlinearity*: **full text**, Secs. 2–4, conclusion and Appendix A. Derives pulse-moment ODEs using stationary phase, predominantly linear chirp, a fixed asymmetric envelope and steady-state inversion with realistic cross sections and pump evolution. Raman is omitted; peak power and nonlinear phase are used as indicators of its onset. It already explores pump/dispersion dependence and constrained energy/bandwidth optimization. Accuracy comparisons expose discrepancies when the pulse shape changes. Coupling moments to gain or scanning these parameters is therefore not new.
- He et al., [arXiv:2609.20994](https://arxiv.org/abs/2609.20994): **full text**, stationary-phase construction, prescribed-gain examples, and self-consistent numerical example. Strong chirp plus the imposed stable-peak-power condition motivates $G(\omega,z)=q\ln(z/z_s)$ with $q$ near one. The paper also gives a mechanism for smooth parabolic evolution and tests realistic gain numerically. It does not derive an autonomous inversion-based selection law for $q$ across pump/seed parameters. Do not describe it as only a gain ansatz with no analytical dynamics.
- Missed noise prior art: Haviv, Kozlov, Krüger & Sidorenko (2026), [DOI:10.1364/OL.591606](https://doi.org/10.1364/OL.591606): measured spectral RIN suppression and a pump–seed noise model. **Abstract only.** Pizzurro et al. (2026), [DOI:10.1016/j.optlastec.2025.114233](https://doi.org/10.1016/j.optlastec.2025.114233): low-noise amplification characterized versus seed wavelength. **Abstract only.** A generic “GMN noise is unexplained” proposal would also overstate novelty.

- Concrete replacements for the seed's unspecified Er/all-fiber examples: Krakowski & Soboń (2024), *Gain-managed nonlinear amplification in an erbium-doped fiber*, [DOI:10.1364/OE.543377](https://doi.org/10.1364/OE.543377), and Xia et al. (2025), *All-fiber integrated gain-managed nonlinear amplification system delivers ultrafast lasers with 3.6 MW peak power and 45 fs pulse duration*, [DOI:10.1016/j.optlastec.2024.111627](https://doi.org/10.1016/j.optlastec.2024.111627). **Abstract only for both.** These verify experimental extensions, not a new selection theory; the former also reports a different seed-wavelength requirement from Yb systems. The original author-free phrase cannot be matched uniquely to particular papers.

## Sharpest statement of the gap

The scoped remaining question is **selection and validity**, relative to the existing 2025 moment/rate model and 2026 stationary-phase theory. No controlled parameter-domain/selection law with an error estimate for shape or gain-law departure was found in this audit. The inspected moment model already supplies a practical parameter-dependent evolution, substantially narrowing the opportunity. Novelty remains low. Energy ceilings, multimode extensions and coherent-material corrections are separate problems until a specific observable and regime are supplied.

Searches (2026-10-01): exact-title and author forward trails from the 2019 Optica work to 2020, 2023, 2025 and September 2026; `gain managed nonlinear amplification reduced model rate equations`; `moment inversion gain spectrum`; `multimode gain managed amplification pump`; Er/all-fiber variants; `gain-managed nonlinear amplifier noise`. Neighboring descriptions checked were dissipative hydrodynamics, stationary phase, and amplifier rate-equation/moment theory. No exhaustive citation census or coherent Maxwell–Bloch audit was completed.

## Conjectures

None. The logarithmic law is published prior art, not a new conjecture of this project.

## Oracle

Partial: a documented Yb rate-equation model and its coupling to the lab's solver are required. Fix cross sections, pump boundary conditions, repetition rate and spontaneous-emission convention before testing a selection law. Compare against the published moment-model baseline and a full GNLSE/rate calculation on unused pump/seed regions. No simulation or model implementation was performed here.

## Lab test

Length-resolved or cut-back gain/spectral measurements under forward and backward pumping, together with output compressibility and Raman fraction. Tests must distinguish changing pump conditions from simply increasing prescribed gain.

## Risks and must-reads

Use the actual assumptions and accuracy limits of DOI:10.1364/OE.549410 as the baseline before deriving. Its steady-state inversion is not an arbitrary pulse-to-pulse gain-memory model. This is an active literature with substantial prior analytics. A duration alone does not establish failure of rate equations: coherent-material corrections require the relevant dephasing and bandwidth scales. This audit has read arXiv:2609.20994, so this agent is not eligible for a masked rediscovery of that item; no benchmark materials were accessed.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-01 | claude-bootstrap (claude) | Created; literature_state partial, novelty_confidence low for the single-mode case | arXiv:2609.20994; literature audit, Oct 2026 |
| 2026-10-01 | gpt-a (gpt; model unknown) | candidate → audited; retained partial/low/priority 3; restricted target to selection and controlled regime | Existing self-consistent moments, DOI:10.1364/OE.549410; inspected stationary-phase theory in arXiv:2609.20994; new noise-model prior art |
| 2026-10-02 | gpt-a (gpt; model unknown) | Recovered moment-theory full text and specific Er/all-fiber sources; retained low novelty | DOI:10.1364/OE.549410 already includes inversion/pump ODEs and optimization; fixed shape, chirp and steady-inversion assumptions delimit its scope |
