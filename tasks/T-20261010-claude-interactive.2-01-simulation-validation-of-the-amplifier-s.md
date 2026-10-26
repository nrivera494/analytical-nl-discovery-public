---
id: T-20261010-claude-interactive.2-01
title: "Simulation validation of the amplifier-similariton analytical results"
type: verify
status: done
priority: 1
problem: P-001
claim: null
family_required: any
lease_hours: 8
created_by: claude-interactive.2
created: 2026-10-10
---

## Goal

Each analytical statement R1-R10 on the amplifier similariton (attraction rates, phase-sensitive shape amplification, moment noise laws, closed-form noise figures, input-noise share, spectral rank-one, matched LO) is tested against full-NLSE simulation with convergence and measured error exponents, and given a verdict.

## Context

The PI asked on 2026-10-10 for a simulation validation of every analytical result on the NLSE amplifier similariton that the orchestrator (claude-interactive) presented. These are R1-R10: the orchestrator's sketch on P-001, and claims C-20261008-claude-a-01/-02 on branch `origin/task/T-20261008-claude-a-01`. Claude-family work; the validator is Claude family too, so the result is same-family evidence (AGENTS.md hard rule 1).

## Deliverables

- Run folders `runs/2026-10-10-claude-interactive.2-{simval-lib,gain-noise-mc,moment-noise,attraction,shape-modes}/`.
- Note `explorations/2026-10-10-claude-interactive.2-similariton-validation.md`, with a verdict for every item.
- Log `log/2026-10-10_claude-interactive.2_T-20261010-claude-interactive.2-01.md`, with proposed check-table rows.
- Loose-end tasks T-20261010-claude-interactive.2-02 and -03.
