---
id: P-20261012-claude-interactive.5-05
title: "Structural upper bound on the nonlinear overlap of doubly resonant chi(2) cavities, and the minimum critical power for complete second-harmonic conversion"
status: candidate
priority: 3
literature_state: partial
novelty_confidence: medium
target_quantity: "An upper bound, over all dielectric geometries made of a given material pair inside a given volume, on the normalized nonlinear overlap beta-bar of a doubly resonant chi(2) cavity, equivalently a lower bound on the critical pump power at which temporal-coupled-mode theory predicts complete second-harmonic conversion, P_crit proportional to 1/(beta-bar^2 Q_1^2 Q_2), with the best inverse-designed cavities as the achievable point."
model: "Temporal coupled-mode theory for a two-mode (omega, 2 omega) chi(2) cavity with quality factors Q_1, Q_2 and overlap beta (Rodriguez et al. 2007); Maxwell's equations for the linear modes in a design region with two local lossless or lossy dielectrics; the chi(2) tensor of the nonlinear material; extensions: material sum rules on chi(2), pump depletion and bandwidth, chi(3) four-wave mixing analogue."
oracle_ready: missing
last_audited: null
audited_by: [claude]
proposed_by: claude-interactive.5
provenance:
  agent: claude-interactive.5
  model: claude-fable-5-1
  family: claude
claims: []
results: []
---

## Target quantity

**Setting.** In temporal coupled-mode theory a doubly resonant cavity with modes at $\omega_1$ and $\omega_2=2\omega_1$, quality factors $Q_1,Q_2$ and a nonlinear overlap $\beta=\int\epsilon_0\chi^{(2)}E_1^2E_2^*\,dV/\big(\int\epsilon|E_1|^2dV\sqrt{\int\epsilon|E_2|^2dV}\big)$ converts 100% of the pump at a critical input power $P_{\rm crit}\propto\omega_1/(|\beta|^2Q_2Q_1^2)$ (Rodriguez et al. 2007). Lin et al. (2016) write $P_{\rm crit}=2\omega_1\epsilon_0\lambda_1^3/[(\chi_{\rm eff})^2|\bar\beta|^2Q_1^2Q_2]$ with a dimensionless $\bar\beta$ that absorbs the material susceptibility and $\lambda_1^3$, and report inverse-designed values $\bar\beta\approx0.018$–$0.030$, about ten times earlier hand designs. They state that no upper bound on $\bar\beta$ is known.

**Targets.**
1. $\bar\beta_{\max}(\epsilon_{\rm hi}/\epsilon_{\rm lo},\,V/\lambda_1^3)$: the supremum of $|\bar\beta|$ over all two-material geometries in a design volume $V$, with modal confinement expressed through $V$. Answer form: a closed-form or semi-analytic bound in the index contrast and $V/\lambda_1^3$, with the ratio to the best inverse design stated.
2. The joint bound on $\bar\beta^2Q_1^2Q_2$ at fixed total footprint, since $Q$ and overlap compete for the same volume, and so the minimum $P_{\rm crit}$.
3. Material sum rules: does the Kuzyk-type bound on $\chi^{(2)}$ (or the Bassani–Scandolo superconvergence rules) combine with the structural bound into a single material-and-geometry limit on $P_{\rm crit}$?
4. Beyond the two-mode model: the effect of pump depletion, self- and cross-phase modulation and a finite pump bandwidth on the achievable efficiency, as corrections to the two-mode optimum.

**Answer form.** Inequalities in the groups $\epsilon_{\rm hi}/\epsilon_{\rm lo}$, $V/\lambda_1^3$, $Q_1$, $Q_2$ and the material figure $(\chi^{(2)})^2/\epsilon^3$, with tightness measured against the published inverse designs.

## Signal of hidden simplicity

- The overlap is a trilinear functional of modal fields, each constrained by Maxwell's equations and normalized; local power-conservation (T-operator, QCQP) bounds already give rigorous limits for linear objectives and for the related quartic $\int|E|^4$ objective with reported tightness.
- The two-mode model reduces the whole nonlinear problem to one number, $\bar\beta$, so a bound on $\bar\beta$ immediately bounds the complete-conversion power without any nonlinear simulation.
- The only existing structural SHG bound (Mohajan et al. 2023, undepleted, 2D) sits one to two orders of magnitude above designs; the two-mode cavity formulation may give a far tighter one because the modes are discrete.

## Literature state

Search strings (subagent claude-interactive.5.3, 2026-10-12): "T-operator bounds second harmonic generation"; "bounds nonlinear frequency conversion arbitrary structure duality"; "fundamental limits upper bound nonlinear nanophotonics four-wave mixing QCQP"; Kuzyk limits; Bassani Scandolo sum rules; Rodriguez 2007 critical power; Lin 2016 nonlinear overlap; "limits to second-harmonic generation efficiency".

- J. Mohajan, P. Chao, W. Jin, S. Molesky & A. W. Rodriguez, "Fundamental limits on radiative χ(2) second harmonic generation," Opt. Express 31, 44212 (2023), DOI 10.1364/OE.513565, arXiv:2307.06414. **Full text** (subagent). Lagrange-dual QCQP bound on radiated SH power in a design region; undepleted pump, two frequencies, 2D TM, lossy material; bounds one to two orders of magnitude above inverse designs.
- P. Chao, B. Strekha, R. Kuate Defo, S. Molesky & A. W. Rodriguez, Nat. Rev. Phys. 4, 543 (2022), DOI 10.1038/s42254-022-00468-w. **Not accessed.** Review of electromagnetic bounds; nonlinear section unverified.
- Z. Kuang, PhD thesis, arXiv:2308.08698 (2023). **Partial** (subagent). An appendix on power-conservation laws in nonlinear nanophotonics and possible bounds; exploratory.
- P. Chao, A. M. Hammond & S. G. Johnson, arXiv:2502.09821 (2025). **Abstract only.** Sum-of-squares bounds on $\int|E|^4$ (Raman-type objective), reported tight against inverse designs; the closest tight bound of nonlinear type.
- A. Rodriguez, M. Soljačić, J. D. Joannopoulos & S. G. Johnson, Opt. Express 15, 7303 (2007), arXiv:0705.3652. **Full text** (subagent). Two-mode theory, 100% conversion at the critical power; $\beta\propto V^{-1/2}$ for $\chi^{(2)}$; no bound on $\beta$.
- Z. Lin, X. Liang, M. Lončar, S. G. Johnson & A. W. Rodriguez, Optica 3, 233 (2016), arXiv:1505.02880. **Full text** (subagent). Topology-optimized overlaps $\bar\beta\approx0.018$–$0.030$; explicitly no upper bound stated.
- M. G. Kuzyk, Phys. Rev. Lett. 85, 1218 (2000), DOI 10.1103/PhysRevLett.85.1218. **Abstract only**; the formula and the gap to best molecules taken from Kuzyk, arXiv:physics/0510199 (**full text**, subagent). Quantum limit on hyperpolarizabilities.
- F. Bassani & S. Scandolo, Phys. Rev. B 44, 8446 (1991), DOI 10.1103/PhysRevB.44.8446. **Abstract only.** Kramers–Kronig relations and sum rules for nonlinear susceptibilities.
- L. Z. Tan & A. M. Rappe, Phys. Rev. B 100, 085102 (2019), arXiv:1708.05433. **Abstract only.** Bound on $\chi^{(2)}$ from gap, bandwidth and geometry.
- H. Li, T. Koutserimpas, F. Monticone & O. D. Miller, arXiv:2409.20351 (2024). **Abstract only.** Unified resonant $\chi^{(2)}/\chi^{(3)}$ material bounds; SHG bounds near designs.
- T. Koutserimpas et al., arXiv:2410.02002 (2024). **Abstract only.** Causality versus quantum sum rules for SHG; notes difficulty in turning them into limits.
- D. Wang et al., Sci. Adv. (2025), DOI 10.1126/sciadv.adu7605, arXiv:2412.11111. **Abstract only.** Microresonator SHG efficiency limit under nonlinear critical coupling; 61% measured. A model-level, not structural, limit.

What is settled: the two-mode critical-power theory, the best designs, the undepleted 2D duality bound, and material-level limits on $\chi^{(2)}$. What was not found: any bound on $\bar\beta$ or on $\bar\beta^2Q_1^2Q_2$, and any joining of material and structural limits.

## Sharpest statement of the gap

No upper bound on the normalized overlap $\bar\beta$ of a doubly resonant $\chi^{(2)}$ cavity is known, so the minimum pump power for complete second-harmonic conversion at given $Q$'s and volume is unknown; the one structural SHG bound that exists is undepleted, two-dimensional and loose by one to two orders of magnitude.

## Conjectures

No claim files yet. The refutable conjecture: **$|\bar\beta|\le c\,(\epsilon_{\rm hi}-\epsilon_{\rm lo})/\epsilon_{\rm hi}\cdot(\lambda_1^3/V_{\rm eff})^{1/2}$ with a universal $c$ of order one, where $V_{\rm eff}$ is the smaller of the two mode volumes**, that is, the scaling of Rodriguez et al. with a contrast factor. A refutation is any computed cavity whose $\bar\beta$ exceeds this at its measured mode volumes.

## Oracle

**Missing.** Needs a frequency-domain Maxwell solver (2D first) to compute modes and overlaps, and a QCQP or sum-of-squares bound code over the design region. None of it exists in the repository, and it does not use the $\chi^{(3)}$ fibre solver. The cheap first test is the conjecture above against the published designs and against random and optimized 2D cavities.

## Lab test

Fabricate the best-known doubly resonant cavity in a given platform (for example thin-film lithium niobate or gallium phosphide), measure $Q_1,Q_2$ and the SHG efficiency curve against pump power, and extract $\bar\beta$. The bound fails if any device gives $\bar\beta$ above it after correcting for the measured $Q$'s.

## Risks and must-reads

- **The 2022 review may already contain a bound** on cavity overlaps; must-read in full. Also the full text of Chao, Hammond & Johnson 2025 (the method likely transfers) and Li et al. 2024.
- **The two-mode model may be the wrong level**: at the volumes of interest other modes and the finite pump bandwidth matter, and a bound on $\bar\beta$ may say little about a real device's efficiency.
- **Low repository fit** (no fibre, heavy new tooling). Priority 3 for that reason, not for lack of interest.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched with one subagent (claude-interactive.5.3) | Searches listed above |
