---
auditor: gpt-b
model: gpt-6-astra
family: gpt
date: 2026-10-18
verdict: pass-reduced-regime
report_type: cross-family verification, not a clean-context adversarial audit (gate G5 open)
---

# Cross-family verification of C-20261018-claude-interactive.7-02 (pointer)

The full report is [`claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md`](../../../../claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md). The PI summary is [`docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md`](../../../../docs/summary-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md). Both are kept with the claim; this file records the verdict for result R-0009.

- **Verdict.** Pass with reduced regime, for the covariance identity and approximation and for the independently tested early weak-disorder squeezing. The proposer's family is claude (claude-interactive.7); the verifier's family is gpt.
- **Not signed off:**
  - Gaussianity;
  - the unique attribution of $V_{P|X}$ to cross-phase noise of the excited modes;
  - a universal mean and spread;
  - the strong-disorder statistics, which fail step-resolution gates at $z=20$;
  - distances beyond $20L_{\rm NL}$.
- **Task.** The verify task T-20261018-claude-interactive.7-03.
- **Why it is a verification and not a G5 audit:**
  - gpt-b read the proposer's run config, meta and summary files as well as the cards and the evaluator;
  - no optimization-based counterexample search was run;
  - gpt-b kept blockers open in T-20261018-gpt-b-02 and did not mark the claim `audited`.

  gpt-b read no proposer scripts, notes, logs or PR descriptions.
- **What was done:**
  - the exact identity and its error bound;
  - 12-path tangent ensembles with step refinement to $h=0.000625L_{\rm NL}$;
  - frozen nonlinear-Wigner ensembles, including a held-out launch;
  - antithetic curvature scaling with held-out occupations;
  - a self-phase reference and a number-diagonal mechanism model;
  - distributed loss and detection.
- **Runs.** `2026-10-18-gpt-b-condensate-squeezing`, `2026-10-18-gpt-b-grin-squeezing`, `2026-10-18-gpt-b-kerr-exact`.
