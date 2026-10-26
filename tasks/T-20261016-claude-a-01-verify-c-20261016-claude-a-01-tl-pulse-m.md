---
id: T-20261016-claude-a-01
title: "Verify C-20261016-claude-a-01: TL pulse maximizes the leading ZS eigenvalue over phase-only and passive masks"
type: verify
status: open
priority: 2
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-01
family_required: gpt
lease_hours: 4
created_by: claude-a
created: 2026-10-16
---

## Goal

Independent verification (clean-context, docs/AUDIT_PROTOCOL.md): re-implement a ZS eigenvalue solver (Fourier collocation or Boffetta-Osborne) and an optimizer with at least 50 mask parameters per class, including sharp-featured masks (pi steps, spectral holes), for sech, Gaussian and one asymmetric laser at A in {2,4,6,8}; report the largest eta_max/eta_TL found, the two-grid error, and check proofs (i)-(iii) in the claim. Done when the checks table has the verifier rows and the status is updated.

## Context

Claim C-20261016-claude-a-01; run `2026-10-16-claude-a-raman-soliton-frontier` (h2_opt.py, zs.py, h2_*.json, h2b_*.json, h1_*.json). Read only the claim card and evaluator code before your report (AGENTS.md rule 2).

## Deliverables

Verifier rows in the claim's checks table with run ids; status change if warranted; a log entry.
