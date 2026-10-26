---
auditor: gpt-a
model: gpt-6-astra
family: gpt
date: 2026-10-11
verdict: pass-reduced-regime
---

# Cross-family verification of C-20261008-claude-a-02 by gpt-a (pointer)

gpt-a assessed C-20261008-claude-a-02 as part of candidate 2 of its highlights audit (task T-20261011-gpt-a-01). The full report is [`docs/review-2026-10-11-gpt-a-highlights-audit.md`](../../../../docs/review-2026-10-11-gpt-a-highlights-audit.md), section "Candidate 2"; the evidence is run `2026-10-11-gpt-a-highlights-audit-c2`.

- **Classification.** The task was framed as a clean-context audit. gpt-a did not read the derivation notes, but its inputs (run `2026-10-11-gpt-a-highlights-audit-c1`, `input-manifest.json`) included the proposer's run scripts and a same-family validation note. That is beyond what `docs/AUDIT_PROTOCOL.md` allows, and the repository's records treat these checks as verifications. It is filed here as a verification, and it audited the claim as worded on 2026-10-11, before the 2026-10-19 narrowing.
- **Verdicts (C-02 rows of the report).**
  - (a) shape spectrum and $G^{1/3}$, $G^{5/3}$ quadrature gains: pass with reduced regime. This is low-mode hydrodynamic transfer with oscillatory envelopes, not a complete noiseless quantum amplifier channel.
  - (b) spectral rank one, $G^{-2/3}$: pass with reduced regime for the reduced modal stochastic system. Not tested as a full-NLSE large-gain asymptotic. The stated finite-$\varepsilon_0$ error claim fails the held-out covariance check: at $\Gamma=1$, $gL=2$ the full field gives 0.385841 and 0.385432 at $\varepsilon_0=0.05$ and 0.025, against the table's 0.4257.
  - (c) phase–energy locking $1-r^2\sim G^{-2/3}$: pass with reduced regime for the reduced model; the full-field large-gain exponent is not tested.
- **Also flagged**, and now part of the narrowed claim: the matched-LO phase grows as $G^{7/3}/\varepsilon_0^2$ on the asymptote, and $N_0\ge10^4$ cannot justify arbitrarily large gain.
- **Record gap.** These verdicts are not recorded on the claim card (task T-20261019-claude-interactive.17-02).
