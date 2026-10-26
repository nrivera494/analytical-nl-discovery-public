---
id: T-20261012-gpt-a-11
title: "Apply parity card scope corrections after review"
type: loose-end
status: open
priority: 1
problem: P-20261010-claude-interactive-01
claim: null
family_required: any
lease_hours: 8
created_by: gpt-a
created: 2026-10-12
agent: gpt-a
model: gpt-6-astra
family: gpt
---

## Goal

After PI review and availability of the claim branch, update C-20261010-claude-a-03 using the proposed wording in docs/lean/2026-10-13-gpt-a-parity-pilot.md: retain both sector orderings, distinguish electronic weighting from physical attenuation, and link the compiled conditional proofs without treating them as numerical or physical-model certification.

## Context

The card lives on PR #29, which was read but not edited by the parity pilot.
The corrected mathematical and attenuation statements are compiled in
`formal/AnalyticalNL/Parity.lean`; the detailed proposed changes are in the
pilot note. The claim frontmatter reference is intentionally null until that
card is available on the task's eventual base branch.

## Deliverables

- Card title, statement, proof, assumptions, and check-table wording aligned
  with the piecewise bound and vacuum-corrected physical attenuation.
- Links to the independent audit and pinned Lean proof.
- Existing numerical claims and run provenance preserved; no automatic status
  promotion based on formal algebra alone.
