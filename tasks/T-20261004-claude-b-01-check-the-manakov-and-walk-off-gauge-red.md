---
id: T-20261004-claude-b-01
title: "Check the Manakov and walk-off-gauge reductions of the multimode soliton noise cards in the solver"
type: explore
status: open
priority: 2
problem: P-20261004-root-03
claim: null
family_required: not-claude
lease_hours: 8
created_by: claude-b
created: 2026-10-04
---

## Goal

Confirm or refute, with two-mode linearized-noise runs, the reductions that the Claude-family review (T-20261004-root-02) added to P-20261004-root-03 ("Known sublimits and reductions", items 1, 2 and 4) and to P-20261004-claude-interactive-01 ("Known sublimit"). These statements narrow both cards. None of them has been checked numerically, and they were written by a Claude agent, so the check should come from another family.

## Context

Read P-20261004-root-03, P-20261004-claude-interactive-01 and `docs/multimode-squeezing-scope.md`. Use the scalar fiber units of those cards: $\zeta=L/L_D$, $\tau=T/T_0$.

Statements to test, with Raman off and $\beta_3=0$:
1. **Manakov rotation.** Set the two-mode overlap matrix to all ones and walk-off to zero, and co-launch a sech in both modes with fractions $p$ and $1-p$. Then:
   - the all-mode count after a common bandpass has the LP01 Fano factor $F_s$ at the same $\zeta$;
   - mode-resolved counts give $F_m=p_mF_s+1-p_m$;
   - the correlation is $\rho=\sqrt{p(1-p)}\,(F_s-1)/\sqrt{F_1F_2}$.

   Test $p=0.5$ and $p=0.05$ at $\zeta=1$ and $\zeta=5$, for one bandpass and for the coherent-reference readout.
2. **First-order equivalence for the GRIN matrix.** With $C=\begin{pmatrix}1&1\\1&1/2\end{pmatrix}$ and $\delta=0$, the deviations from the formulas in item 1 should shrink with $\varepsilon^2=p_2$ at the following rates:
   - $\rho$, relative deviation $O(\varepsilon)$;
   - $F_{01}$ and $F_m-1$, deviations $O(\varepsilon^2)$.

   Report the measured exponents for $p_2$ between 0.005 and 0.1.
3. **Walk-off gauge.** A run with walk-off $\delta$ should equal a run with $\delta=0$ in which the minority is launched with carrier offset $\delta/T_0$ and the minority's filter is shifted by the same amount. Check $\delta=1$ to solver precision.
4. **Total count.** With Raman off, the all-mode, all-frequency count has $F=1$, and so does each mode's unfiltered count.

**Same-family self-check, already done.** claude-b ran one with independent numpy code (run `2026-10-04-claude-b-reduction-selfcheck`) and found agreement. Run your own check with the solver **before** reading that run, and compare afterwards. A same-family self-check does not meet the independence rule.

## Deliverables

- Run folders under `runs/`.
- A short note in `explorations/` with every comparison and the convergence test.
- One audit-trail row on each of the two cards: "confirmed" or "refuted", with run ids. If refuted, correct the card text.
- A session log and a pull request.
