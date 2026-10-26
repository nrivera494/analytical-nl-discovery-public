---
auditor: claude-interactive.8
model: claude-opus-5-5
family: claude
date: 2026-10-17
verdict: pass
commit: 6320014
---

# Independent verification and adversarial audit of C-20261017-gpt-d-01 (pointer)

The full report is [`claims/notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md`](../../../../claims/notes/audit-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md). The verifier's summary is [`docs/summary-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md`](../../../../docs/summary-2026-10-17-claude-interactive.8-C-20261017-gpt-d-01.md). This file records the verdict for the result.

- **Verdict:** pass, with no blockers and no narrowing. The closed form, both expansions with their error orders, and the general moment expansion with its remainder bound are correct.
- **Families.** The proposer is gpt (gpt-d, gpt-6-astra); the auditor is claude.
- **Clean context**, from the report's own description. Before the report was committed (6320014), the auditor read only:
  - the two claim cards and the problem card P-20261016-claude-interactive-02;
  - `evaluator/`, and the solver documentation and source;
  - the `config.yaml`, `meta.yaml` and `summary.json` of the four gpt-d runs the cards cite.

  It did not read gpt-d's proof note, audit notes, logs, `docs/summary-*` files, PR description or scripts. All code is its own. The held-out points and tolerances were frozen in f784fed.
- **Attacks:**
  - an independent derivation;
  - two independent quadratures at 48 held-out points;
  - the edge of regime ($r=0.01$, 20);
  - six error exponents, including the cancellation point $r=1$. The $r=1/\sqrt3$ case was checked after the audit commit, in the post-audit note;
  - the general remainder bound;
  - GNLSE launch-plane RHS and real propagation;
  - a sampled kernel;
  - a second solver (agents' solver b9fa957);
  - the Hollenbeck–Cantrell relaxed response;
  - prior work;
  - fine-tuning.
- **Runs:** `2026-10-17-claude-interactive.8-sech-tightness`, `-concentration`, `-hc-relaxed`.
- **Non-blocking concerns:**
  - the closed form is not a calibrated silica prediction (up to a factor of 3 against Hollenbeck–Cantrell);
  - novelty is limited to the trigamma evaluation and the coefficients (arXiv:2603.21734 Eq. 2 has the exact integral);
  - the shortest test points are formal ($\omega_0T_0=1.9$–3.4).
- **Post-audit note.** After the commit, the auditor read the proof note. It changed nothing, and the auditor explained the proposer's retained finite-window failure at $r=0.6$ as a pre-asymptotic window effect.
