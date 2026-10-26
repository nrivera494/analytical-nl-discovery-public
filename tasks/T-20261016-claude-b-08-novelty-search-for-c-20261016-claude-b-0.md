---
id: T-20261016-claude-b-08
title: "Novelty search for C-20261016-claude-b-01: exponential asymptotics and complex-singularity methods for Cherenkov/DW radiation (Karpman 1993, Pomeau-Ramani-Grammaticos 1988, Grimshaw, Sulem-Sulem-Frisch 1983)"
type: literature
status: done
priority: 1
problem: P-20261016-claude-interactive-01
claim: C-20261016-claude-b-01
family_required: gpt
lease_hours: 8
created_by: claude-b
created: 2026-10-16
---

## Goal

A novelty audit for C-20261016-claude-b-01. Has the exponential-asymptotics or complex-singularity description of Cherenkov/DW emission been applied to the fission or compression transient of higher-order solitons, with an exponent set by the breather's strip width instead of the soliton's?

## Context

Candidates:
- Karpman, PRE 47, 2073 (1993);
- Pomeau, Ramani & Grammaticos, Physica D 31, 127 (1988);
- the Grimshaw and Boyd literature on exponentially small radiation;
- Sulem, Sulem & Frisch (1983), singularity tracking;
- Roy et al. 2009–2010 and Akhmediev–Karlsson 1995;
- McCue et al., arXiv:2509.07397 (KdV, complex singularities, dispersive waves; abstract only in this session).

## Deliverables

A ledger with access levels and a verdict for the claim's novelty row.

## Completion

Completed by gpt-b (model gpt-6-astra, family gpt) on 2026-10-16.
Report: `docs/review-2026-10-16-gpt-b-dw-singularity-novelty.md`.
Verdict: **partly published**; the precise evolving-strip integrated-yield
limit was **not found**, at medium confidence. The report was committed in
`fe1397c` before closing the task. The proposer’s derivations, logs, run
outputs, evaluator code, and branch history were not read. A literature row
was added to the claim without changing its status. Remaining work is
recorded in T-20261016-gpt-b-06 and T-20261016-gpt-b-07; independent simulation
verification remains T-20261016-claude-b-01.
