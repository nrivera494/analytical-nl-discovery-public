---
id: P-20261012-claude-interactive.5-02
title: "Pump-to-comb conversion efficiency of a Kerr microresonator: the energy-balance bound over all stationary states and its tightness"
status: candidate
priority: 1
literature_state: partial
novelty_confidence: medium
target_quantity: "The supremum over all stationary (and time-averaged breathing) states of the CW-pumped Lugiato–Lefever equation of the conversion efficiency eta = (output power in all comb lines other than the pump line)/(input pump power), as a function of the coupling ratio eta_c and the normalized pump and detuning; in particular whether the energy-balance bound eta <= eta_c^2 is tight, by which states, and how the bound changes for pulsed pumps and coupled resonators."
model: "Single-mode-family Lugiato–Lefever equation with CW pump f, detuning zeta, dispersion d_2 (either sign) and optional higher-order dispersion, Raman and self-steepening; one input/output port with coupling ratio eta_c = kappa_ext/(kappa_ext+kappa_int); extensions: pulsed pump, two-port and coupled-ring (photonic-molecule) configurations, chi(2) resonators."
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

**Definitions.** Normalized LLE $\partial_\tau\psi=-(1+i\zeta)\psi+i|\psi|^2\psi+i\tfrac{d_2}{2}\partial_\theta^2\psi+f$ with $\psi=\sum_\mu a_\mu e^{i\mu\theta}$, amplitude decay rate 1, external coupling fraction $\eta_c$. Input-output: the pump drive is $f=\sqrt{2\eta_c}\,s_{\rm in}$ and the output pump line is $s_{\rm out}=s_{\rm in}-\sqrt{2\eta_c}\,a_0$; every other line leaves with power $2\eta_c|a_\mu|^2$. The conversion efficiency is
$$\eta=\frac{2\eta_c\sum_{\mu\neq0}|a_\mu|^2}{|s_{\rm in}|^2}=\frac{4\eta_c^2}{f^2}\Big(E-|a_0|^2\Big),\qquad E=\sum_\mu|a_\mu|^2 .$$

**Anchor (to be proved as a claim; sketched here, not checked by anyone else).** Multiplying the stationary LLE by $\psi^*$, integrating over $\theta$ and taking the real part kills the detuning, Kerr and dispersion terms and leaves the power balance $E=f\,\mathrm{Re}\,a_0$. Hence
$$\eta=\frac{4\eta_c^2}{f^2}\big(f\,\mathrm{Re}\,a_0-|a_0|^2\big)\le\eta_c^2,$$
with equality if and only if $a_0=f/2$, which also fixes the pump-mode energy fraction at exactly one half and the pump-line transmission at $|1-\eta_c|^2$. Sharper, with $t=s_{\rm out}/s_{\rm in}$ the complex pump transmission: $\eta=\eta_c^2-|t-(1-\eta_c)|^2$ exactly, so the efficiency of any stationary state is fixed by the complex transmission of the pump line alone. The same algebra holds for time-averaged breathers (where $\langle|a_0|^2\rangle\ge|\langle a_0\rangle|^2$ only adds slack), for any conservative addition to the LLE (higher-order dispersion, Raman with a real response, self-steepening alone, several mode families coupled linearly, thermal shifts), and for any term that only removes energy (two-photon absorption; Raman combined with the shock operator, which conserves photon number but not energy), since a sink can only lower $\eta$. At critical coupling ($\eta_c=1/2$) no CW-pumped single-ring Kerr comb converts more than one quarter of the pump into new lines.

**Assumptions that matter.** One bus port; one CW pump in one mode; the same coupling fraction for every line. If the coupling is mode dependent the same argument gives $\eta\le\eta_{c,0}\max_{\mu\ne0}\eta_{c,\mu}$, which is how wavelength-selective couplers and coupled rings evade $\eta_{c,0}^2$; that is the content of target 3, not a violation. Photon-energy bookkeeping across lines is at the percent level. An independent derivation by a second agent of the same family (claude-interactive.5.4, reasoning only, no tools) confirmed the bound, the equality condition and the lossless-case power conservation; it has not been checked by another family.

**Targets.**
1. **Tightness.** $\eta^\star(f,\zeta,d_2)=\sup\eta/\eta_c^2$ over all stationary states (CW, Turing rolls, bright solitons and multi-solitons, dark pulses and platicons) and over the detuning range where each exists. Which state family approaches $a_0=f/2$, and at what $f$? The dark-pulse duty-cycle estimate of Yang et al. (2024) reaches $\eta_c^2$ at 50% duty cycle in a box-profile approximation, and the single-soliton result of Kondratiev et al. (2023) reaches unity at $\eta_c=1$ with few line pairs. Neither is a maximization over states. Answer form: $\eta^\star$ as a function of $f$ and $d_2$, with the gap $1-\eta^\star$ as a scaling law in $1/f$ or in the number of comb lines.
2. **Pulsed pumping.** With a pump pulse train the balance applies line by line in the pump's own comb. Target: the analogue of the bound when the pump occupies $M$ lines and the "converted" power is counted outside them; a conjecture is that the bound rises towards $\eta_c$ as the pump duty cycle falls.
3. **More ports or rings.** Coupled-ring (photonic-molecule) combs exceed 50% experimentally. Target: the bound for two coupled rings with one or two ports, which should explain why those devices evade $\eta_c^2$ and give their own ceiling.
4. **$\chi^{(2)}$ resonators.** The same power balance for a doubly resonant SHG or OPO cavity with comb formation: a bound on the comb fraction in terms of the two coupling ratios.

**Answer form.** Rigorous inequalities in $\eta_c$ (and the second ring's coupling and detuning for target 3), with the supremum over states as a function of $f$, $\zeta$ and $d_2$, and the pulsed-pump duty cycle $\tau_p/t_R$ for target 2.

## Signal of hidden simplicity

- The bound needs only the power balance and the one-port input-output relation; it is independent of dispersion, Raman and mode crossings. Published state-specific estimates (single soliton $\propto\eta_c^2/N$; dark pulse $4\eta_c^2\,\mathrm{dc}(1-\mathrm{dc})$) both carry the factor $\eta_c^2$, as the bound requires.
- The equality condition $a_0=f/2$ is a single complex number. Whether a stationary state can sit there is a question about the pump-mode projection of the nonlinear term, ${\rm NL}_0=\langle|\psi|^2\psi\rangle_0$, which must equal $-i f(1-i\zeta)/2\cdot$const at the optimum. That is a low-dimensional condition.
- Reported efficiencies above 50% have so far needed coupled rings or bidirectional pumping, in line with a single-ring ceiling below $\eta_c$.

## Literature state

Search strings (subagent claude-interactive.5.2, 2026-10-12): "Kerr comb" "conversion efficiency" "upper bound"; "Lugiato-Lefever" "conversion efficiency" limit; microcomb "maximum conversion efficiency" theory; "pump depletion" "Kerr comb" "critical coupling"; chi(2) microcomb conversion efficiency; pulse-driven soliton conversion efficiency; exact titles below.

- Y. Bao et al., Opt. Lett. 39, 6126 (2014), DOI 10.1364/OL.39.006126. **Abstract only.** Soliton-comb efficiency scales as the inverse line count and grows with coupling. No bound over states.
- X. Xue, X. Wang, P.-H. Wang, M. Qi & A. M. Weiner, Laser Photon. Rev. 11, 1600276 (2017), DOI 10.1002/lpor.201600276, arXiv:1610.00958. **Full text** (subagent). Defines $\eta$ as above; duty-cycle heuristic; "effective critical coupling" argument; about 30% measured with dark pulses. No bound over states.
- J. K. Jang et al., Opt. Lett. 46, 3657 (2021), DOI 10.1364/OL.423654. **Abstract only.** Single-soliton efficiency regimes versus coupling and loss.
- X. Xue, X. Zheng & B. Zhou, Nat. Photon. 13, 616 (2019), arXiv:1805.11228. **Full text** (subagent). Coupled cavities: simulated 94% lossless, about 80% at $Q_i=10^7$; single ring "a few percent, limited by duty cycle".
- Ó. B. Helgason et al., Nat. Photon. 17, 992 (2023), DOI 10.1038/s41566-023-01280-3. **Full text** (subagent). Coupled rings, more than 50% measured; no single-ring ceiling stated.
- N. M. Kondratiev, V. E. Lobanov, N. Yu. Dmitriev, S. J. Cordette & I. A. Bilenko, Phys. Rev. A 107, 063508 (2023), arXiv:2209.03707. **Full text** (subagent). Single-soliton analytic efficiency; global maximum 100% at $\eta_c=1$ at maximal detuning with $d_2\ge0.45$. Single soliton only.
- D. Gaertner, P. Trocha, R. Mandel, C. Koos, T. Jahnke & W. Reichel, Phys. Rev. A 100, 033819 (2019). **Full text** (subagent). Global bifurcation of LLE states; $\eta_{\rm out}=4\eta_c^2\,P_{\rm FC}/f^2$ (the same normalization as above); numerics, no bound.
- Q.-X. Yang (or Yang, Hu, Torres-Company, Vahala as listed), eLight 4 (2024), DOI 10.1186/s43593-024-00075-5. **Full text** (subagent). Dark-pulse estimate $4\eta_c^2(\tau/t_R)(1-\tau/t_R)$, maximal $\eta_c^2$ at 50% duty cycle; soliton estimate $\propto\eta_c^2/N$.
- E. Gasmi, H. Peng, C. Koos & W. Reichel, arXiv:2210.09760. **Full text** (subagent). Dual-pump efficiency numerically at most one half (intracavity-normalized).
- R. Mandel & W. Reichel, SIAM J. Appl. Math. 77, 315 (2017), arXiv:1603.02206. **Full text** (subagent). A priori bounds on $\|\psi\|_\infty$ for LLE stationary states; nothing on efficiency.
- G. Lihachev et al., Nat. Commun. 13, 1771 (2022), DOI 10.1038/s41467-022-29431-0. **Full text** (subagent). 40% on-chip platicon; Z. Zang et al., arXiv:2401.16740. **Abstract only.** 65% with bidirectional pumping. Both are checks for the bound given their coupling ratios.
- Y. Zhao, J. K. Jang, Y. Okawachi & A. L. Gaeta, arXiv:2104.12905. **Full text** (subagent). SHG resonator efficiency bound under nonlinear critical coupling with comb formation suppressed; starting point for target 4.
- F. Leo et al., Phys. Rev. Lett. 116, 033901 (2016), arXiv:1510.04261. **Abstract only.** Mean-field model of $\chi^{(2)}$ cavity combs.

What is settled: state-specific efficiency formulas and coupled-ring demonstrations. What was not found: any bound over all stationary states, any statement of $\eta\le\eta_c^2$, and any pulsed-pump or coupled-ring ceiling.

## Sharpest statement of the gap

The one-port power balance gives $\eta\le\eta_c^2$ for every stationary state of the CW-pumped LLE, apparently unpublished. Not known: whether the supremum over states reaches $\eta_c^2$, which states approach it and how fast in $f$; the corresponding bounds for pulsed pumping, for two-port and coupled-ring resonators, and for $\chi^{(2)}$ comb resonators.

## Conjectures

No claim files yet. First claim to register: the identity $\eta=\eta_c^2-|t-(1-\eta_c)|^2$ and the bound above, with a proof. A crude scratch integration of the LLE in this session (not converged to stationarity for two of three states, not a registered run) gave $\eta/\eta_c^2$ well below one for a soliton, a Turing roll and a dark pulse; a registered run with Newton-converged states is required. The refutable conjecture to test by simulation: **$\eta^\star(f,\zeta,d_2)<1$ strictly for every finite $f$, with $1-\eta^\star\propto1/f$ at large $f$, attained by dark-pulse states in normal dispersion.** A refutation is any converged stationary state with $\eta>\eta_c^2$ (which would refute the bound itself) or a bright-soliton or Turing state with a larger $\eta/\eta_c^2$ than the best dark pulse at the same $f$.

## Oracle

**Missing in the repository, cheap to add.** A one-dimensional LLE integrator (split-step, periodic in $\theta$) and a Newton continuation for stationary states are a few hundred lines. For each converged state compute $a_0$, $E$ and $\eta$ and check the balance $E=f\,\mathrm{Re}\,a_0$ to machine precision as a correctness test. Sweep $f$, $\zeta$ and $d_2$ with continuation to map $\eta^\star$. Add Raman and third-order dispersion as perturbations to confirm the bound is unaffected. The coupled-ring extension needs two coupled LLEs.

**Refutation engine.** Random initial conditions plus continuation, maximizing $\eta$ over $\zeta$ for each state branch; any state with $\eta>\eta_c^2$ refutes the anchor.

## Lab test

In a single-port ring of measured intrinsic and external coupling rates, measure the total power in all lines other than the pump against input power for the best achievable state. The bound fails if $\eta>\eta_c^2$ after correcting for the facet and filter losses. The strongest published checks are the 40% platicon and the 65% bidirectional results, whose coupling ratios set whether they sit inside the bound; a coupled-ring device above $\eta_c^2$ of its bus coupling does not violate it but tests target 3.

## Risks and must-reads

- **The anchor is an elementary energy argument and may be in a paper not located**, for example in Bao et al. 2014 or Jang et al. 2021 (abstracts only), in Helgason et al. 2023 (full text was read by a subagent for the efficiency definition only), or in a thesis. Must-reads: those full texts; Chembo & Menyuk, Phys. Rev. A 87, 053852 (2013) for normalization (not accessed); a 2022 Physical Review Applied paper by Stone et al. on comb efficiency was named by the checking subagent and has not been located.
- **The definition of efficiency matters.** Some experiments count the pump line's own modulated part or use a different normalization; the card fixes the definition above.
- **Two-port rings (add–drop)** change the input-output relation; the bound for them is target 3, not a violation.
- **Fit.** No fibre content; the LLE is close to the repository's split-step machinery but is not in the solver.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched with one subagent (claude-interactive.5.2); power-balance bound derived in the session and checked by derivation by subagent claude-interactive.5.4 (same family); crude LLE scratch check, not a run | Searches listed above; subagent report in the session |
