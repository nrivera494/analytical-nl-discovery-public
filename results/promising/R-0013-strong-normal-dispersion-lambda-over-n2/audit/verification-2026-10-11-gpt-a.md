---
auditor: gpt-a
model: gpt-6-astra
family: gpt
date: 2026-10-11
verdict: pass-reduced-regime
---

# Cross-family verification of C-20261010-claude-b-01 by gpt-a (pointer)

gpt-a assessed C-20261010-claude-b-01 (a) and (b) as part of candidate 1 of its highlights audit (task T-20261011-gpt-a-01). The full report is [`docs/review-2026-10-11-gpt-a-highlights-audit.md`](../../../../docs/review-2026-10-11-gpt-a-highlights-audit.md), section "Candidate 1", and the regime it signed off is under "Assumptions, limiting checks, and the regime signed off". The evidence is run `2026-10-11-gpt-a-highlights-audit-c1`: gpt-a's own symmetric Fourier split step with an exact transpose, and a reduced map on the full input grid without Hermite truncation.

- **Classification.** The task was framed as a clean-context audit. gpt-a did not read the derivation notes, but its inputs (`input-manifest.json` in run c1) included the proposer's run scripts. It is filed as a verification, consistent with how the repository records the companion check of C-20261010-claude-a-01. It assessed the claim as worded on 2026-10-11.
- **Verdicts.**
  - (a) $\Lambda(Z)/N^2$: pass with reduced regime. gpt-a signs off the formal smooth pre-breaking limit at fixed $Z$, with bounded hydrodynamic blocks.
    - Numerical evidence at $Z=0.5$ ($N=12$–48): exponent −1.98768, $\Lambda=1.5702278$.
    - Numerical evidence at $Z=1.5$ ($N=12$, 20): exponent −1.78370; −1.43626 with four values of $N$, referenced to the finite $N=200$ map.
    - It does not sign off a uniform bound on $c$ for every $Z$, or a global classical map after breaking.
  - (b) small-$Z$ coefficients: pass as a formal asymptotic. Richardson extrapolation from $N=400$ and 800 gives 0.816658 and 2.449844, against $2/\sqrt6$ and $\sqrt6$. This is the same finding as the weak-dispersion result and must not be counted twice.
- **Not rerun:** the full oracle grids, $\lambda_{\rm pass}$ achievability, and full delayed Raman with self-steepening.
- **Record gap.** These verdicts are not recorded on the claim card (task T-20261019-claude-interactive.17-02).
