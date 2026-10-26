# Promotion gates

A claim becomes a result when the PI merges the pull request that adds its folder under `results/`. Results come in two tiers, and the tier is the folder.

| Tier | Folder | What it takes |
|---|---|---|
| **Formalized** | `results/formalized/R-NNNN-name/` | Everything a promising result needs, plus gate G8: the result's mathematical statement is a Lean theorem that is kernel-checked and audited by a family other than the formalizer's. |
| **Promising** | `results/promising/R-NNNN-name/` | Cross-family verification and PI approval. The claim was verified by a family other than the proposer's (claim status `sim-verified` or `audited`; `scripts/validate.py` enforces the families), gate G4 is met, and the PI merges the pull request. It is not formalized. A clean-context adversarial audit (G5) is recorded but may still be open. |

**A formalized result is a sub-result.** It states exactly what the Lean theorems prove, with their hypotheses, and nothing more. The rest of the claim either becomes its own promising result, if the PI approves it, or stays a claim. One claim can therefore give one formalized result and one promising result; the claim's `result` field lists both.

**Moving between tiers.** If a promising result is later formalized in full, the pull request moves its folder from `promising/` to `formalized/` with `git mv` and keeps its id. If only part of it is formalized, add a new formalized result for that part and narrow the promising one.

Result ids `R-NNNN` are sequential across both tiers.

## Gates

Every `RESULT.md` records each gate in its front matter as `met`, `open` or `n/a` (field `gates`). The body says why each open or n/a gate is so, and each open gate has a task. G4 must be met in both tiers. G5 may be open in the promising tier. G8 must be met in the formalized tier and is not met in the promising tier.

The `audit/` folder holds the cross-family reports:
- `audit-*.md` for clean-context adversarial audits (G5);
- `verification-*.md` for cross-family verifications that are not clean-context audits.

Each has front matter with the reporting family, and a result needs at least one such report.

| Gate | Requirement | Evidence in the result folder |
|---|---|---|
| G1 Statement | Result stated with explicit regime bounds in dimensionless groups, assumption ledger, and stated small parameter. | `RESULT.md` sections 2–3 |
| G2 Derivation | Complete derivation that an independent agent re-derived or checked line by line. Symbolic steps reproducible with the CAS script. | `RESULT.md` section 4, `repro/derivation.*` |
| G3 Cheap checks | Units, known limits, symmetries, symbolic residual. | `audit/cheap-checks.md` or the claim's Checks table |
| G4 Simulation | Agreement on held-out regions; measured error-scaling exponent consistent with the prediction; convergence tests; second solver or relaxed-assumption model where available. Run by a different family from the proposer. | `figures/`, `repro/`, run ids |
| G5 Adversarial audit | Clean-context audit by a different family that tried to break the claim: counterexample search, edge of regime, artefact checks. No unresolved blockers. | `audit/audit-*.md` |
| G6 Novelty | Literature check by two families; closest prior work named and the difference stated. | `RESULT.md` section 7 |
| G7 Reproducibility | One command regenerates every figure from committed configs. | `repro/README.md` |
| G8 Formal (formalized tier) | The statement is one or more Lean theorems in a project under `formal/`, pinned to a toolchain and Mathlib commit. They compile with no `sorry` and depend only on `propext`, `Classical.choice` and `Quot.sound`. A family other than the formalizer's rebuilt the project from the committed pins, re-checked it with an independent kernel where available, and audited the translation: that the definitions model the physics, that no hypothesis assumes the conclusion, that every hypothesis is satisfiable, and that the result claims no more than Lean proves. The audit includes at least one held-out instance the formalizer did not prepare and a negative control that must fail. | `RESULT.md` "Formal verification" section and `formal` front-matter block, `audit/formal-audit-*.md`, the audit run under `runs/` |

`scripts/validate.py` checks the tier, the gate record, the families, and, for formalized results, that the named theorems exist in the named library and that the declared axioms are the standard three. It cannot check that a Lean statement means what the result says; that is the formal audit's job.

## Expected figures

1. Theory against simulation in the core of the regime.
2. Error against the small parameter on log axes, with the predicted slope. For exact identities and inequalities this is n/a; show the tightness of the bound instead.
3. Regime map: where the result holds and where it fails, in dimensionless groups.
4. A held-out prediction: a parameter region chosen before the simulation was run.

Each figure caption gives the run ids and the solver commit. A result needs at least one figure. Missing figures leave G4 or G7 open.

## Notification

Opening a pull request that touches `results/` requests review from the code owner and triggers `.github/workflows/notify-result.yml`, which labels the PR `result-candidate`, mentions the PI, and posts to a webhook if one is configured.

## Retraction

If a merged result is later found wrong, set `status: retracted` in its `RESULT.md`, add a retraction note at the top, and leave everything else in place. A formalized result whose Lean proof stays valid can still be retracted if the formal audit missed a mismatch between the Lean statement and the physics; say which.
