---
id: C-YYYYMMDD-agent-NN
problem: P-000
title: "Short statement"
type: scaling-law          # exact-solution | asymptotic-solution | reduced-model | scaling-law | invariant | symmetry-mapping | threshold | noise-formula | distribution | bound
status: proposed           # proposed | cheap-checks-passed | sim-verified | audited | promoted | refuted | withdrawn
proposed_by: agent-id
proposer_model: model-name
proposer_family: claude
verified_by: null
verifier_family: null
audited_by: null
auditor_family: null
created: YYYY-MM-DD
updated: YYYY-MM-DD
solver_commit: null
result: null
---

## Statement

The claim, as equations. One claim per file.

## Regime

Bounds on dimensionless groups within which the claim is asserted. Name the small parameter and the predicted order of the error.

## Assumptions

Every assumption, including those inherited from the model.

## Predictions

Numbers or functional forms the simulation should reproduce, including at least one in a region not used to construct the claim. Fix these before running the verification.

## Derivation

Sketch here; full derivation in a linked note or CAS script. Auditors do not read this section until their report is committed.

## Checks

| Check | Result | By (family) | Run ids | Date |
|---|---|---|---|---|
| Units | | | | |
| Known limits | | | | |
| Symmetries | | | | |
| Symbolic residual | | | | |
| Simulation, core regime | | | | |
| Error-scaling exponent | | | | |
| Held-out region | | | | |
| Convergence and artefacts | | | | |
| Second solver or relaxed assumption | | | | |
| Adversarial audit | | | | |
| Novelty search | | | | |

## Outcome

If refuted or withdrawn: which check failed, the run id, and what was learned.
