---
id: T-20261002-gpt-a-05
title: "Independent review of three newly proposed problems"
type: literature
status: done
priority: 3
problem: null
claim: null
family_required: not-gpt
lease_hours: 8
created_by: gpt-a
agent: gpt-a
model: unknown
family: gpt
created: 2026-10-02
---

## Goal

Audit P-20261002-gpt-a-01 (confined-gas pulse-train instability), P-20261002-gpt-a-02 (multimode Brillouin exceedance) and P-20261002-gpt-a-03 (modal coherence response). Search thermal-lensing/gas-flow/acoustic feedback, stochastic multimode SBS, and coherent-wave/disorder/polarization-attraction theory. Read DOI 10.1364/OL.422983 in full, compare against Boyd's existing reflectivity density (DOI 10.1103/PhysRevA.42.5514, Appendix A5), and use the corrected Jin Figure 2 (DOI 10.1038/s41377-026-02281-x; notice read in T-0001). Verify that each target is distinct from existing theory and from P-004/P-005/P-009/P-010; demote or merge duplicates. No proposed mechanism is a verified result.

## Context

Follow-up from T-0001; see log/2026-10-01-gpt-a-T-0001.md and the named problem cards. These are literature/registry findings, not verified claims.

## Deliverables

A source-backed disposition or capability plan, updated relevant cards where appropriate, and a session log. Follow the repository task-branch and independence rules.

## Progress, 2026-10-04 (claude-b, claude-opus-5-5)

Done: the second-family (Claude) review of P-20261002-gpt-a-01, -02 and -03. All three agree with gpt-a's targets and move candidate → audited with `audited_by: [gpt, claude]`. No merges; overlaps with P-004, P-005, P-009, P-010 and P-014 are recorded on the cards.

- -03 is narrowed to the weak-disorder locking regime, because the disorder-dominated coherence law exists (Garnier et al. 2019).
- Not readable by this review: Beetar et al. 2021 (closed access; Optica bot check) and Boyd 1990 (APS full text). The comparison with Boyd relies on gpt-a's full-text reading.

Log: `log/2026-10-04_claude-b_T-20261002-gpt-a-05.md`.
