---
id: T-20261018-claude-interactive-04
title: "Two-tier results (promising, formalized); file the ZS Lean formalization and its cross-family audit; promote C-20261018-pi-chatgpt-01"
type: infra
status: done
priority: 1
problem: P-20261016-claude-interactive-03
claim: C-20261018-pi-chatgpt-01
family_required: any
lease_hours: 8
created_by: claude-interactive
created: 2026-10-18
---

## Goal

On the PI's instruction (2026-10-18): split results/ into results/promising/ (cross-family verified, PI-approved, not formalized) and results/formalized/ (sub-results kernel-checked in Lean, statement audited by a family other than the formalizer). File the ZSFormalization Lean project under formal/, the orchestrator's audit as a run, and promote C-20261018-pi-chatgpt-01 as one formalized and one promising result.

## Context

## Deliverables
- `results/promising/` and `results/formalized/`, with rules in `docs/PROMOTION.md` (gate G8), checks in `scripts/validate.py`, and tiers in the ranking and dashboard.
- `formal/ZSFormalization/`, copied verbatim and hash-checked, built by `formal/lakefile.toml`.
- Audit run `runs/2026-10-18-claude-interactive-zs-lean-audit/`.
- Results R-0001 (formalized) and R-0002 (promising); C-20261018-pi-chatgpt-01 → promoted.
- Loose ends: T-20261018-claude-interactive-05 to -10.
