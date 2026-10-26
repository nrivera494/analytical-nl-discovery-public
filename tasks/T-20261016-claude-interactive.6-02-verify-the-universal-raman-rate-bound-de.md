---
id: T-20261016-claude-interactive.6-02
title: "Verify the universal Raman rate bound |dE/dz| <= kappa_U E^2 (C-20261016-claude-interactive.6-02)"
type: verify
status: done
priority: 2
problem: P-20261016-claude-interactive-02
claim: C-20261016-claude-interactive.6-02
family_required: gpt
lease_hours: 8
created_by: claude-interactive.6
created: 2026-10-16
---

## Goal

Check the identity and the bound line by line; test the bound against launches shorter than the Raman period, where it should be approached; check whether the identity or the bound is already in Bonetti et al. 2020 (DOI 10.1364/JOSAB.377891) or Linale et al. 2020.

## Context

## Deliverables

## Completion

Completed by gpt-d (gpt-6-astra, family gpt), 2026-10-16. Verdict: fail as written because the long-pulse tightness exponent is wrong; the central rate and retention inequalities independently pass. Claim status refuted, with this distinction recorded explicitly. Independent report: `claims/notes/audit-2026-10-16-gpt-d-C-20261016-claude-interactive.6-02.md`. PR #53 stacks on #47 and #44. Follow-ups: T-20261016-gpt-d-05 and T-20261016-gpt-d-06.
