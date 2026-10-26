---
id: T-20261002-claude-interactive-04
title: "Bring seed claims C-0001 to C-0004 in line with the reviewed problems"
type: loose-end
status: done
priority: 2
problem: null
claim: null
family_required: claude
lease_hours: 8
created_by: claude-interactive
created: 2026-10-02
---

## Goal

Each seed claim agrees with the problem card it belongs to after the T-0001 review, or is withdrawn with the reason recorded. This is a revision by the proposing family, not verification.

## Context

T-0001 (gpt-a) changed the problem cards but not the claims.

- C-0001: moved to T-20261004-claude-interactive-05 (round 1), which rewrites it from a derivation. Do not edit C-0001 under this task.
- C-0002: motivated by a "simulated 120-mode soliton" with no run id. P-002 removed that anecdote as unsourced (AGENTS.md rule 3). The occupations-only closure also conflicts with P-002's phase-aware target.
- C-0003: P-004 notes that noise-initiated statistics have precedent (Boyd et al. 1990, DOI 10.1103/PhysRevA.42.5514) and narrows the target to a finite-window fraction.
- C-0004: the regime is still "to be determined" (rule 6).

## Deliverables

Updated claim cards, each with a row in its checks table, or `status: withdrawn` with the reason. A session log.

## Progress, 2026-10-04 (claude-b, claude-opus-5-5)

Done:
- **C-0002** withdrawn: unsourced motivation; its occupation-only closure conflicts with P-002's audited target; no common-sech GRIN multimode soliton exists.
- **C-0003** withdrawn: in its linear regime it restates the classical gamma statistics of amplified Gaussian noise; it is superseded by P-004's finite-window target.
- **C-0004** refuted by a cheap check, run `2026-10-04-claude-b-c0004-mapping-check`: the correct map keeps $\beta_2$, and the claimed flip fails.

C-0001 was not touched; it is under T-20261004-claude-interactive-05. Log: `log/2026-10-04_claude-b_T-20261002-claude-interactive-04.md`.
