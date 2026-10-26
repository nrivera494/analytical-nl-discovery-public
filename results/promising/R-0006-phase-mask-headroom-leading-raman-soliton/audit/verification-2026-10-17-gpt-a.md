---
auditor: gpt-a
role: verifier
model: gpt-6-astra
family: gpt
date: 2026-10-17
verdict: pass-reduced-regime
task: T-20261016-claude-a-03
run: 2026-10-17-gpt-a-phase-headroom
---

# Independent verification of C-20261016-claude-a-04 (pointer)

The full report is [`claims/notes/audit-2026-10-17-gpt-a-C-20261016-claude-a-04.md`](../../../../claims/notes/audit-2026-10-17-gpt-a-C-20261016-claude-a-04.md). The verifier's summary is [`docs/summary-2026-10-17-gpt-a-C-20261016-claude-a-04.md`](../../../../docs/summary-2026-10-17-gpt-a-C-20261016-claude-a-04.md). The report's file name starts with `audit-`, but its title and verdict make it a verification, so it is filed here as `verification-*`. It does not count toward gate G5.

- **Verdict:** sim-verified only as narrowed to the independently reproduced published witnesses. Those are A2 ($H=1.090163$, 100 fs), A (1.061806) and B (1.069737, 200 fs), at $N=4$.
  - The literal reading of B's gain as at least 7.000% is refuted (6.974%).
  - The upper bracket, the masks B2 and B3, and any global optimum are unverified.
  - In the report's own words: "No audited status or result promotion is requested."
- **Families.** The proposer is claude (claude-a); the verifier is gpt.
- **Context**, from the report's own description. Before writing the report, the verifier read only:
  - the two assigned claim cards and the problem card;
  - the cited configs, metadata and summaries;
  - the authorized masks;
  - the evaluator code and the solver API examples.

  It consulted no proposer propagation or optimization script, derivation, exploration, log or PR description.
- **Checks:**
  - an independent Python RK4IP and two-sided ZS shooting;
  - the pinned agents' solver (b9fa957) for a second forward solve and its discrete adjoint;
  - step-order tests (3.88–3.97);
  - grid, window, gate and length checks;
  - frozen held-out duration tests (±10% at fixed energy and length);
  - self-steepening, third-order dispersion, loss, and a published SMF-28 dispersion model;
  - a soliton census.

  The primary freeze is commit 04cf1e92059772ef6bda543e933460698acd1ce6.
- **New content.** Stronger masks found by the verifier are filed separately as claim C-20261017-gpt-a-01 and are not part of this result.
