---
id: T-20261019-claude-interactive.15-01
title: "Clean-context GPT audit of C-20261016-claude-a-04 as narrowed (published masks A2 and B), for gate G5 of R-0006"
type: audit
status: open
priority: 3
problem: P-20261016-claude-interactive-03
claim: C-20261016-claude-a-04
family_required: gpt
lease_hours: 8
created_by: claude-interactive.15
created: 2026-10-19
---

## Goal

Audit the narrowed statement of C-20261016-claude-a-04 (H >= 1.09016 for mask A2 at N=4, T0=100 fs; H >= 1.06974 for mask B at 200 fs; ZS readout f1 = 2 Im zeta1 / N^2 at L = 4 L_D/N) under docs/AUDIT_PROTOCOL.md. Try to break it: an independent readout of the leading soliton (identification, gate, carrier removal, ZS root), edge of regime in N^2 tau1/T0 and output length, artefacts, and a relaxed model. A pass makes gate G5 of R-0006 met (auditor and auditor_family on the claim card and in RESULT.md, an audit-*.md pointer in its audit/ folder; status stays promoted).

## Context

R-0006 (results/promising/R-0006-phase-mask-headroom-leading-raman-soliton/) was promoted on the PI's 2026-10-19 decision with G5 open. Its only cross-family report is gpt-a's verification (claims/notes/audit-2026-10-17-gpt-a-C-20261016-claude-a-04.md, run 2026-10-17-gpt-a-phase-headroom). It was clean-context by its own description, but gpt-a classed it as verification and requested no audited status.

The auditor should be a GPT agent other than gpt-a. Under docs/AUDIT_PROTOCOL.md it reads only:
- the claim card, including the gpt-a sharpened statement;
- the problem card;
- evaluator/ and the solver documentation;
- the mask coefficient files named on the card.

It must not read the proposer's notes, logs or scripts, or gpt-a's report or scripts, before committing its report.

## Deliverables

- `audit-<date>-<agent>.md` in claims/notes/, with a verdict and the regime signed off.
- On a pass: a pointer `audit-<date>-<agent>.md` in the R-0006 audit/ folder, G5 set to met with the reason, and `audited_by`/`auditor_family` filled on the card. The PI merges.
