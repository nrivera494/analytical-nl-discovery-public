---
id: P-20261012-claude-interactive.5-03
title: "A proven ceiling on single-stage temporal-mode selectivity in pulsed quantum frequency conversion"
status: candidate
priority: 2
literature_state: partial
novelty_confidence: medium
target_quantity: "The supremum of the temporal-mode selectivity S of a single-pass pulsed sum-frequency converter over all pump pulse shapes, strengths and group-velocity-mismatch configurations, as a closed-form bound in the dimensionless walk-off groups, together with the efficiency–purity frontier (eta_1, purity) of the best Schmidt mode; the numerically observed ceiling near 0.8–0.85 turned into a theorem or refuted."
model: "Undepleted classical pump pulse, linear coupled-wave equations for signal and converted fields with first-order group-velocity mismatch among pump, signal and converted waves, no dispersion, no loss; Green function G(t,t') and its Schmidt (singular-value) decomposition; extensions: second-order dispersion, loss, cavity-assisted and cascaded stages."
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

**Setting.** A pump pulse of duration $\tau_p$ and peak coupling $\gamma$ drives signal-to-converted-wave sum-frequency generation in a waveguide of length $L$. With group delays per unit length $\beta'_p,\beta'_s,\beta'_r$ for pump, signal and converted wave, the dimensionless groups are the conversion strength $\bar\gamma$ (so that a CW analogue converts $\sin^2\bar\gamma$), $\zeta=(\beta'_r-\beta'_s)L/\tau_p$ (signal–converted walk-off over the pump duration) and $\xi=(\beta'_p-\beta'_r)/(\beta'_p-\beta'_s)$ (where the pump sits between or outside the other two velocities), plus the pump's shape and chirp. The linear input-output map has singular values $\sqrt{\eta_n}$ and Schmidt modes; following Reddy, Raymer and McKinstrie the selectivity is
$$S=\eta_1\cdot\frac{\eta_1}{\sum_n\eta_n},$$
the efficiency of the dominant mode times its purity. A perfect pulse gate has $S=1$.

**Targets.**
1. $S^\star=\sup S$ over all pump shapes, chirps, $\bar\gamma$, $\zeta$ and $\xi$ for a single pass, as a closed form or a rigorous bound with a stated gap. The numerical ceiling reported in the literature is about 0.81–0.85, with the best regime being the pump matched in group velocity to the signal while the converted wave walks off ($\xi\to\infty$, $\zeta\gg1$).
2. The frontier $\max\{\text{purity}:\eta_1=p\}$ for $p\in[0,1]$, which tells a user what purity is available at a given efficiency.
3. The dependence on the groups near the optimum: $S^\star(\zeta,\xi)$ for finite walk-off, as an expansion in $1/\zeta$ and $1/\xi$.
4. What breaks the ceiling: a proof that cascading two stages (temporal-mode interferometry), a dispersion-engineered second-order term, or a cavity is necessary to exceed $S^\star$, or a single-stage construction that does.

**Answer form.** $S^\star$ as a number with a derivation, or as a function of $(\zeta,\xi)$ with asymptotic error order; the frontier of target 2 as a curve with its two endpoints ($\eta_1\to0$ gives purity 1 since the first-order Green function is separable; $\eta_1\to1$ gives the ceiling).

## Signal of hidden simplicity

- In the best regime the Green function is known exactly: a Bessel-$J_0$ kernel in $\sqrt{\text{product of the two shifted times}}$ on a triangular support (Reddy et al. 2013). Its Schmidt problem is a finite Hankel-transform eigenproblem, whose eigenfunctions are Slepian's generalized prolate spheroidal functions. The ceiling is therefore a property of a classical integral operator, which suggests a closed form.
- Quesada and Sipe showed that time ordering enters through Magnus terms of definite order and that the first-order term is exactly separable when $\mu^2=\tau^2+(s_p-s_a)(s_p-s_b)=0$; the ceiling arises from the interference of the first- and third-order terms. That is a two-term structure, not a numerical accident.
- The ceiling is reported as roughly the same number (0.8–0.85) in several configurations and by several groups, which points to a universal constant.

## Literature state

Search strings (subagent claude-interactive.5.3, 2026-10-12): "Reddy Raymer McKinstrie selectivity"; "quantum pulse gate" selectivity limit time ordering; "temporal mode" "frequency conversion" "upper bound"; "Quesada Sipe mode-selective"; "time ordering" "mode selectivity" Magnus Schmidt; exact titles below.

- D. V. Reddy, M. G. Raymer, C. J. McKinstrie, L. Mejling & K. Rottwitt, Opt. Express 21, 13840 (2013), arXiv:1305.2165. **Full text** (subagent). Defines $S$; five walk-off regimes; exact $J_0$ Green function in the matched regime; numerical Schmidt decomposition gives $S\approx0.81$ at $\bar\gamma\approx1$, about 0.83 at best, tending to about 0.85 as the pump shortens; symmetric counter-propagating case about 0.70; low-conversion $S\approx0.967\bar\gamma^2$. Analytic result: pump chirp cannot help in that regime.
- D. V. Reddy, M. G. Raymer & C. J. McKinstrie, Opt. Lett. 39, 2924 (2014), DOI 10.1364/OL.39.002924. **Abstract only.** Temporal-mode interferometry (two stages) to beat the ceiling.
- D. V. Reddy, M. G. Raymer & C. J. McKinstrie, Phys. Rev. A 91, 012323 (2015), arXiv:1501.03216. **Full text** (subagent). States the single-stage ceiling "no greater than about 0.8"; mechanism: pulses convecting through each other; two 50% stages give $S\to1$; no analytic bound.
- D. V. Reddy & M. G. Raymer, Opt. Express 25 (2017), arXiv:1702.05687. **Full text** (subagent). The limit is "determined through exhaustive numerical exploration"; the groups $\bar\gamma,\zeta,\xi$ and the optimum $\xi\gg\zeta\gg1$.
- N. Quesada & J. E. Sipe, Opt. Lett. 41, 364 (2016), arXiv:1508.03361, and Phys. Rev. A 90, 063840 (2014), arXiv:1407.6976. **Full text** (subagent). Time-ordering corrections to third Magnus order; separability condition $\mu^2=0$; unit conversion possible but with two Schmidt modes; cascading $N$ stages suppresses order-$n$ corrections by $N^{-n}$. No closed-form $S$.
- A. Christ, B. Brecht, W. Mauerer & C. Silberhorn, New J. Phys. 15, 053038 (2013). **Full text** (subagent). Numerical Heisenberg solution; states that whether single-mode pulse gates with time ordering are possible remains open.
- B. Brecht, D. V. Reddy, C. Silberhorn & M. G. Raymer, Phys. Rev. X 5, 041017 (2015). **Full text** (subagent). Quotes the 0.85 ceiling as numerical.
- V. Ansari, J. M. Donohue, B. Brecht & C. Silberhorn, Optica 5, 534 (2018). **Full text** (subagent). $S\approx0.83$ single stage; cascaded above 0.98.
- D. V. Reddy & M. G. Raymer, Opt. Express 26, 28091 (2018), arXiv:1708.01705. **Abstract only.** Dichroic cavity gives nearly perfect selectivity.
- L. Babel et al., arXiv:2608.09346 (2026). **Abstract only.** $S=96.8\%$ at $\eta=89.6\%$ with a different metric; must be read to see whether it is a single pass and which $S$ it uses.

What is settled: the definition, the regimes, the exact kernel in the best regime, the qualitative time-ordering explanation, and that cascading or cavities beat the ceiling. What was not found: any proof or closed form for the single-stage ceiling, or any frontier of purity against efficiency.

## Sharpest statement of the gap

The single-stage selectivity ceiling of about 0.8–0.85 is a numerical observation on an analytically known kernel. No theorem bounds $S$ for a single pass over all pump shapes and walk-off configurations, no closed form is known for the matched-regime optimum, and the purity-versus-efficiency frontier has not been stated.

## Conjectures

No claim files yet. The refutable conjecture: **for a single pass with first-order walk-off only, $S\le S^\star$ with $S^\star$ equal to the matched-regime, short-pump limit (reported near 0.85), and $S^\star$ is given by the leading eigenvalues of the finite Hankel transform on the triangular support.** A refutation is any single-pass simulation (any pump shape, chirp, $\zeta$, $\xi$) with converged Schmidt decomposition giving $S>S^\star$. The 2026 preprint claiming $S=96.8\%$ is the first thing to test against this, once its metric and geometry are known.

## Oracle

**Missing in the repository, cheap to add.** The model is a linear $1+1$D coupled-wave PDE with three walk-off terms; the Green function is built column by column (or by propagating a basis of signal modes), and the SVD gives $\eta_n$. A few hundred lines. The repository's $\chi^{(3)}$ solver does not apply, but the adjoint machinery pattern does: parametrize the pump shape and maximize $S$ by gradient ascent to search for violations. Convergence checks: time-grid resolution against the walk-off, and the support truncation.

## Lab test

A pulse-gate experiment in PPLN or thin-film lithium niobate with a shaped pump: measure $\eta_1$ and the purity by sending the Schmidt-mode basis (or by tomography of the output) and compute $S$. The bound fails if a single-pass device, with no cavity and no second stage, shows $S>S^\star$ beyond its error bar.

## Risks and must-reads

- **A derivation may exist in a thesis or talk.** Reddy's 2017 NIST talk abstract promises a derivation of the selectivity limit; Reddy's Oregon thesis (2017) was not accessed. Must-reads: that thesis; Babel et al. 2026 in full; Brecht et al., Phys. Rev. A 90, 030302(R) (2014) (abstract only, quotes "around 87%").
- **The ceiling might not be universal**: with second-order dispersion or a non-stationary pump the kernel changes, and a single-pass device may exceed it; then the card's answer is a frontier rather than a number.
- **Fit.** Quantum-optics flavour, linear model; the repository's strengths in noise do not enter.

## Audit trail

| Date | Agent (family) | Change | Evidence |
|---|---|---|---|
| 2026-10-12 | claude-interactive.5 (claude; claude-fable-5-1) | Created as candidate; literature searched with one subagent (claude-interactive.5.3) | Searches listed above |
