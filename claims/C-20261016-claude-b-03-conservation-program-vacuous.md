---
id: C-20261016-claude-b-03
problem: P-20261016-claude-interactive-01
title: "No conservation-law ceiling on dispersive-wave band yield with third-order dispersion: the photon-number/momentum/Hamiltonian program (sharp Gagliardo-Nirenberg Kerr control) has value 1 on the whole line and 0.74-0.95 on simulation windows; with pure beta2 normal dispersion it reduces exactly to the Cantelli bound"
type: bound
status: cheap-checks-passed
proposed_by: claude-b
proposer_model: claude-opus-5-5
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: 2026-10-16
updated: 2026-10-16
solver_commit: null
result: null
---

## Statement

**Model.** $iu_\xi+\frac12u_{\tau\tau}+N^2|u|^2u=i\delta_3u_{\tau\tau\tau}$ (Kerr, cubic dispersion, no Raman, no self-steepening, lossless), with $K(w)=-D(w)=w^2/2-\delta_3w^3$.

**Invariants.** For a launch $u_{\rm in}$, every output photon spectrum $n(w)\ge0$ satisfies:
- $\int n=\mathcal N$;
- $\int wn=\mathcal P$;
- $\mathcal H_{\rm in}\le\int Kn\le\mathcal H_{\rm in}+\frac{N^2}{2\sqrt3}\mathcal N^{3/2}V^{1/2}$, where $V=\int(w-\mathcal P/\mathcal N)^2n$.

The lower Hamiltonian bound holds because the Kerr energy is non-negative. The upper bound is the sharp one-dimensional Gagliardo–Nirenberg inequality $\|u\|_4^4\le\frac1{\sqrt3}\|u\|_2^3\|u'\|_2$: equality holds for sech, and the inequality is applied to $ue^{i\bar w\tau}$.

The **program** maximises $\int_{w\ge w_z}n/\mathcal N$ over these constraints. It is card P-20261016-claude-interactive-01's sketch 1, with the lower Hamiltonian bound added.

1. **(Vacuity on the line.)** For every $\delta_3>0$, every $N$ and every launch, the supremum of the program is 1.
   - Witness: a three-point spectrum with mass $1-r-\varepsilon$ in the band, recoil mass $r$ at $-w_r$, and mass $\varepsilon=m/w_\infty$ at $w_\infty$ (also in the band).
   - Momentum fixes $w_r$. As $w_\infty$ increases, $\langle K\rangle$ decreases continuously and without bound, because $K\sim-\delta_3w^3$. So $w_\infty$ can be chosen to make $\langle K\rangle=\mathcal H_{\rm in}/\mathcal N$ exactly. Then both Hamiltonian bounds hold and the band fraction is $1-r$ for any $r>0$.
   - The same holds for any dispersion with $K(w)/w\to-\infty$ on the band side. That includes normal-dispersion pumping with $\beta_3\ne0$: there $K=-w^2/2-\delta_3w^3$ is unbounded below on the $\mathrm{sgn}(\delta_3)$ side, so any band on that side has supremum 1.
2. **(Finite windows.)** With $n$ supported on $|w|\le W$, the value for transform-limited Gaussian launches ($N=3$–10, $\delta_3=0.01$–0.05) is:
   - 0.57–0.85 at $W=2w_{\rm DW}$;
   - 0.70–0.90 at $W=3w_{\rm DW}$;
   - 0.74–0.95 on the windows of the simulations. That is between 2.9 and 837 times the simulated transform-limited band yield, and 2.9 times or more everywhere.
3. **(Normal dispersion, pure $\beta_2$.)** With $K=-w^2/2$, the constraint that binds is the lower Hamiltonian bound, $\langle w^2\rangle\le2|\mathcal H_{\rm in}|/\mathcal N$; the Gagliardo–Nirenberg side is irrelevant. For a one-sided band $w\ge w_B$ at zero momentum, the program value equals the Cantelli bound
$$\eta\le\frac{\sigma^2}{\sigma^2+w_B^2},\qquad\sigma^2=\frac{2|\mathcal H_{\rm in}|}{\mathcal N}.$$
   This is never larger than the Hamiltonian–Markov ceiling $\sigma^2/w_B^2$, which follows from Castelló-Lurbe, Andrés and Silvestre (2013) and is noted on the card. The Cantelli form is attained by a two-point measure; whether that measure is dynamically attainable is not known.

## Regime

- Item 1: all $\delta_3>0$ (exact statement).
- Item 2: the stated grids and windows only.
- Item 3: all launches with finite $\mathcal H$ and $\mathcal P=0$, for one-sided bands.

## Assumptions

1. The invariants are those of M0. Self-steepening changes the conserved quantity to photon number weighted by $1/\omega$. Raman breaks momentum conservation; the momentum constraint becomes one-sided ($\mathcal P$ non-increasing in the photon-conserving model), which only enlarges the feasible set. Loss is excluded.
2. Spectra are treated as arbitrary non-negative measures. A real output also satisfies dynamical constraints, which the program ignores; that is why it is loose.
3. The Gagliardo–Nirenberg constant $1/\sqrt3$ was checked numerically: sech gives 0.5773503, a Gaussian 0.5642, and 200 random profiles at most 0.535.

## Predictions

Frozen as H1a–H1c in commit d1b7f71.
- H1a: vacuous on the line. **Confirmed** (three-point witness at band fraction 0.99 for all 20 grid points).
- H1b: at least 0.5 at $W\ge2w_{\rm DW}$ (**confirmed**, minimum 0.571); at least 0.9 on the simulation windows (**refuted**: 9 of 20 points are 0.9 or more, range 0.74–0.95).
- H1c: Cantelli reduction (**confirmed** to LP precision at 9 points).
- Measurable consequence: no measured or simulated DW band fraction can be bounded by these invariants alone. The card's conjecture that the ceiling lies within a factor 3 of the optimised yield fails wherever the optimised yield is below about 0.25–0.3.

## Derivation

The construction is in item 1. The LP formulation is in `runs/2026-10-16-claude-b-dw-program/program.py`: linear programs at fixed variance $v$, maximised over $v$ on a geometric grid.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | Per-photon normalisation, $a=N^2\mathcal N/(2\sqrt3)$, $h=\mathcal H/\mathcal N$; Gaussian $h=\frac14-N^2/(2\sqrt2)$; sech $N=1$ gives $h=-1/6$ with Gagliardo–Nirenberg equality | claude-b (claude) | 2026-10-16-claude-b-dw-program | 2026-10-16 |
| Known limits | Gagliardo–Nirenberg constant: sech 0.57735 equals $1/\sqrt3$; Gaussian 0.5642 | claude-b (claude) | 2026-10-16-claude-b-dw-program | 2026-10-16 |
| Simulation, core regime | LP values at windows 1.2, 1.5, 2 and 3 $w_{\rm DW}$, and at simulation windows | claude-b (claude) | 2026-10-16-claude-b-dw-program | 2026-10-16 |
| Second solver or relaxed assumption | Raman relaxes momentum conservation, which can only loosen the program | claude-b (claude) | — | 2026-10-16 |
| Adversarial audit | not done | | | |
| Novelty search | The vacuity is elementary; the card's literature review found no rigorous GNLSE band bound. The Cantelli sharpening of the Markov ceiling is a small refinement of Castelló-Lurbe et al. (2013), DOI 10.1364/OE.21.028550 (card: full text, gpt-a) | claude-b (claude) | — | 2026-10-16 |

## Outcome

Proposed as a negative result. It refutes card sketch 1 as a usable ceiling in anomalous dispersion with $\beta_3>0$. A useful ceiling needs dynamical information beyond $\mathcal N$, $\mathcal P$ and $\mathcal H$. Candidates are a priori lower bounds on the analyticity-strip width $d(\xi)$ (see C-20261016-claude-b-01), or Zakharov–Shabat soliton content.
