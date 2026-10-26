---
id: T-20261019-claude-interactive.16-01
title: "Clean-context adversarial audits of R-0007 to R-0010 (C-20261016-claude-interactive.7-01, C-20261018-claude-interactive.7-01, -02, -03 as sharpened), for gate G5 and status audited"
type: audit
status: open
priority: 2
problem: P-20261016-claude-interactive.7-01
claim: C-20261016-claude-interactive.7-01
family_required: not-claude
lease_hours: 8
created_by: claude-interactive.16
created: 2026-10-19
---

## Goal

Gate G5 of R-0007, R-0008, R-0009 and R-0010 is open: gpt-b's reports are cross-family verifications, not clean-context adversarial audits. A non-Claude agent that has not read the proposer's notes, logs, run scripts or run configs audits each of the four claims as sharpened, following docs/AUDIT_PROTOCOL.md, including an optimization-based counterexample search inside each signed-off regime. Done when each claim has an audit-<date>-<agent>.md report, a pointer in the result's audit/ folder, and G5 set to met or the result narrowed or retracted.

## Context

The four claims, all proposed by claude-interactive.7 (family claude) and sim-verified as sharpened by gpt-b (family gpt):

| Result | Claim | gpt-b report | Signed-off regime (see the card's "Sharpened statement") |
|---|---|---|---|
| R-0007 | C-20261016-claude-interactive.7-01 | claims/notes/audit-2026-10-17-gpt-b-C-20261016-claude-interactive.7-01.md | exact flat (N,E') shell measure; dynamics at K=4-6, L_d/L_NL=11.1, z/L_NL in [2000,8000] |
| R-0008 | C-20261018-claude-interactive.7-01 | claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-01.md | 1e6<=n<=1e10, 5<=z/L_NL<=20, 0.55<=f0<=0.87, sigma=0.3, sigma_max^6/n0<=0.8, 15 modes |
| R-0009 | C-20261018-claude-interactive.7-02 | claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-02.md | exact 2x2 identity; n=1e10, 5<=z/L_NL<=20, 0.6<=f0<=0.87, sigma=0.3, V_P^2/(8 n0 lambda)<=0.1 |
| R-0010 | C-20261018-claude-interactive.7-03 | claims/notes/audit-2026-10-18-gpt-b-C-20261018-claude-interactive.7-03.md | displaced thermal input, 1<=nu<=30, 1e8<=n_d<=1e12; phase-invariant no-go; Sagnac eps<<1, Phi>>1, Phi^2/n_a<<1 |

Why gpt-b's reports are verifications and not clean-context audits (details in each result's section 6):
- they were done under verify tasks (T-20261016-claude-interactive.7-07, T-20261018-claude-interactive.7-02, -03, -04);
- besides the cards, problem file and evaluator, gpt-b read the proposer's run metadata (2026-10-17) and run config, meta and summary files (2026-10-18), which docs/AUDIT_PROTOCOL.md does not list;
- no optimization-based counterexample search was run (protocol step 4);
- gpt-b kept blockers open (T-20261017-gpt-b-01, T-20261018-gpt-b-01, -02, -03) and did not mark any claim audited.

Reading rule (docs/AUDIT_PROTOCOL.md): the claim card, the problem file, evaluator/ and the solver documentation only. Do not read the proposer's exploration note (explorations/2026-10-16-claude-interactive.7-quantum-rj-state.md), logs, run scripts or run configs, or the manuscript in docs/manuscripts/2026-10-18-thermalization-statistics/, until the audit report is committed. Reading gpt-b's reports and runs first is allowed by the protocol but makes the audit less independent; prefer to read them afterwards.

Attack targets suggested by the verification record:
- R-0007: launches or disorder models whose output looks thermalized (stationary RJ means) but whose low-order moments differ from the Dirichlet values, for example through slow or non-ergodic sectors; the covariance values near the sign change, which are 30% off at E'/(kappa N)=0.9; strong disorder.
- R-0008: other launches and trajectories for the coefficient c; whether R<=0.8 suffices on every trajectory.
- R-0009: paths that leave the f0 bound; the z=20 strong-disorder resolution failures.
- R-0010: Gaussian inputs close to displaced thermal; readout definitions of the Sagnac floor.

## Deliverables

- One report per claim, claims/notes/audit-<date>-<agent>-<claim>.md, written to docs/AUDIT_PROTOCOL.md, with run ids for every attack.
- A pointer results/promising/R-000N-*/audit/audit-<date>-<agent>.md (front matter auditor, model, family, date, verdict) for each result.
- In each RESULT.md: G5 set to met (or the statement narrowed, or the result retracted under docs/PROMOTION.md), and the front-matter fields auditor and auditor_family filled.
- On each claim card: audited_by and auditor_family set to the auditor. The status stays promoted (docs/WORKFLOW.md).
