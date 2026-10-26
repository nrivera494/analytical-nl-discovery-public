# Adversarial audit protocol

The auditor's job is to break the claim.

## Before you start

- You must be a different model family from the proposer.
- Read only: the claim card, the problem file, `evaluator/`, and the solver documentation. Do not read the proposer's log entries, notes or branch history.

## What to attempt

1. **Restate the claim** in your own words and list its assumptions. If you find an assumption the card does not list, record it.
2. **Cheap attacks.** Units. Limits that should reduce to known results. Symmetries the result should respect. Sign and factor-of-two checks.
3. **Edge of regime.** Simulate at and beyond each stated bound. A claim whose stated domain is wider than the domain where it holds fails.
4. **Counterexample search.** Use optimization through the solver to maximize the discrepancy between claim and simulation inside the stated regime.
5. **Artefact checks.** Repeat key runs with doubled window, halved step, more modes. Check for reflections and aliasing.
6. **Relaxed assumptions.** Turn on at least one neglected effect at a realistic strength and report how the result degrades.
7. **Triviality and prior work.** Is the result a known result under a change of variables? Search and report what you searched.
8. **Fine-tuning.** Does the result need a parameter relation that cannot be set in the lab?

## Report

Write `audit-<date>-<agent>.md` with: verdict (`pass`, `pass with reduced regime`, `fail`), each attack with run ids, blockers, non-blocking concerns, and the regime you would sign off on. Then, and only then, you may read the proposer's material and add a short note on anything it changes.
