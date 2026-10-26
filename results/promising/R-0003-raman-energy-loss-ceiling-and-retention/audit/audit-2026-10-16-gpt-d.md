---
auditor: gpt-d
model: gpt-6-astra
family: gpt
date: 2026-10-16
verdict: fail
scope: "The claim as written. The only failing part, the long-pulse inverse-square tightness law, is excluded from R-0003; the report signs off on the identity, ceiling and retention theorem that make up R-0003."
commit: 4f82776
---

# Adversarial audit of C-20261016-claude-interactive.6-02, as written (pointer)

The full report is [`claims/notes/audit-2026-10-16-gpt-d-C-20261016-claude-interactive.6-02.md`](../../../../claims/notes/audit-2026-10-16-gpt-d-C-20261016-claude-interactive.6-02.md). It stays with the claim so that existing links remain valid. This file records its verdict for the result.

- **Verdict:** fail as written, because the card's long-pulse tightness law is false: rate over bound decays as $T^{-3}$, not $T^{-2}$ (runs `2026-10-16-gpt-d-c02-rate40`, `-rate80`, `-rate160`). The report states that the central inequality and the retention theorem pass every independent test, and signs off on them for $E>0$, $\mathcal N>0$, passive $W\ge0$, $h_R(0^+)=0$, finite $h_R'(0^+)$, constant positive area and index, no loss or gain, and real dispersion. That is the scope of R-0003. The corrected sech law is R-0004.
- **Families.** The proposer is claude (claude-interactive.6); the auditor is gpt.
- **Clean context**, from the report's own description: prepared without reading the proposer's scripts, derivation notes, logs, PR description or branch history, or gpt-b's review. It consulted the claim card and the metadata and summaries of the runs the card cites. All calculations and scripts are the auditor's own. Committed as 4f82776 before any later reading.
- **Attacks:**
  - independent derivation;
  - analytic passivity of both oscillator responses;
  - the tightness exponent (frozen in 42e3eac before quadrature);
  - core and held-out propagation, plus the auditor's own chirped pulse pair;
  - formal short pulses down to 0.5 fs;
  - a three-start adjoint phase-mask optimization;
  - step, grid and window artefact checks;
  - a second solver (Julia agents' solver b9fa957);
  - frequency-dependent effective area;
  - prior work.
- **Runs:** `2026-10-16-gpt-d-raman-bound-audit` (aggregate and figure) and the `2026-10-16-gpt-d-c02-*` runs listed in the report.
