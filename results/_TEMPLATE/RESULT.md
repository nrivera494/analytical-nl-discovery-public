---
id: R-0000
title: "One-line statement of the result"
claim: C-0000
problem: P-000
tier: promising             # promising | formalized; must match the folder (docs/PROMOTION.md)
status: under-review        # under-review | accepted | retracted
type: scaling-law
proposer_family: claude
verifier_family: gpt
auditor_family: gpt
solver_commit: abcdef0
promoted: null              # date of PI merge
pi_score: null              # optional, 1-5, set by the PI
gates:                      # met | open | n/a; the body says why for each open or n/a gate
  G1: open
  G2: open
  G3: open
  G4: met                   # required in both tiers (cross-family verification)
  G5: open                  # clean-context adversarial audit; may be open (record why and give a task)
  G6: open
  G7: open
  G8: open                  # met only in the formalized tier
# formal:                   # formalized tier only
#   project: formal
#   library: LibraryName
#   theorems: [Namespace.theorem_name]
#   toolchain: leanprover/lean4:v4.35.0-rc4
#   mathlib_commit: 1f414401f69059aa7eead47b53ee40bd38455eeb
#   axioms: [propext, Classical.choice, Quot.sound]
#   formalizer: agent-id
#   formalizer_family: gpt
#   auditor: agent-id
#   auditor_family: claude
#   audit_run: <run id under runs/>
---

# Title

## 1. Problem

What quantity, in what physical system, and why it matters. Two or three sentences. Link to the problem file.

## 2. Result

The statement as equations, boxed or displayed, with every symbol defined.

## 3. Regime of validity

| Dimensionless group | Definition | Lower bound | Upper bound | What fails outside |
|---|---|---|---|---|

Small parameter and predicted error order. Assumption ledger.

## 4. Derivation

Complete, in steps a specialist can follow. Reference `repro/derivation.*` for the symbolic computation.

## 5. Validation against numerics

![Theory against simulation](figures/fig1-theory-vs-sim.png)
*Caption: what is plotted, parameter values, run ids, solver commit.*

![Error scaling](figures/fig2-error-scaling.png)
*Caption: measured exponent with uncertainty against predicted exponent.*

![Regime map](figures/fig3-regime-map.png)
*Caption: region of validity in dimensionless groups; where and how the result fails.*

![Held-out prediction](figures/fig4-heldout.png)
*Caption: the prediction was fixed in commit <hash> before the run.*

Convergence tests and second-solver comparison, with run ids.

## 6. Adversarial audit

Summary of each audit in `audit/`: who, verdict, attacks attempted, regime signed off, open non-blocking concerns.

## 7. Novelty

Closest prior work, with DOIs, and the precise difference. What was searched, by whom.

## 8. Experimental test

The measurement, the required equipment, expected signal size, and what outcome would falsify the result.

## 9. Open questions

Loose ends, each with a task id.

## 10. Formal verification

Formalized tier only. A table mapping each part of section 2 to its Lean theorem, the Lean definitions that carry the physics, every hypothesis, what is not formalized, the checks the formal auditor ran (with run id), and what still has to be trusted.
