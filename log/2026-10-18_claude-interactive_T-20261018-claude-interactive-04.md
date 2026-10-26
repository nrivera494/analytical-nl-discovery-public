---
date: 2026-10-18
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261018-claude-interactive-04
duration_min: 90
---

## Did

- **Audited the ZSFormalization Lean project** from the PI's Codex session. I read all 13 sources before the README and rebuilt the project standalone against a fresh checkout of the pinned Mathlib. I re-checked the proofs with `leanchecker` and with nanoda, an independent kernel, and added held-out certificates and a negative control.
- **Filed the library verbatim** as a second library of `formal/`, whose dependency pins are identical, and re-ran the whole audit from the repository layout: run `2026-10-18-claude-interactive-zs-lean-audit`, `run.sh`, 288 s.
- **Split `results/` into two tiers**, on the PI's instruction:
  - `promising/`: cross-family verified, PI-approved, not formalized.
  - `formalized/`: sub-results that are kernel-checked Lean theorems audited by a family other than the formalizer's.

  The rules are in `docs/PROMOTION.md` (new gate G8; every result records G1–G8 as met, open or n/a), with matching changes to `scripts/validate.py`, `scripts/common.py`, `scripts/rank_results.py`, `scripts/build_index.py`, `results/README.md`, `results/_TEMPLATE/RESULT.md`, `docs/WORKFLOW.md` and `AGENTS.md`.
- **Wrote the first two results**, both from C-20261018-pi-chatgpt-01 (approved by the PI as verified on 2026-10-18):
  - R-0001 (formalized): (A) at even exponents and (B)–(D) for Schwartz masks.
  - R-0002 (promising): (A) at real exponents, (B)–(D) for arbitrary masks, (E) and (F).

## Found

- **The formalization is genuine.**
  - It has no `sorry` or added axioms; all 121 theorems use only `propext`, `Classical.choice` and `Quot.sound`.
  - nanoda checked 54,113 declarations with no errors.
  - The held-out certificates (N = 9/2 at 0.07161%, 15/2 at 0.01518%, and N = 7 at 13/49) pass, and the negative control fails.
- **Its scope is narrower than the claim:** even exponents only, and masks whose output spectrum is Schwartz. The README states this accurately.
- **The new part of (A) is now machine-checked at even exponents.** The novelty audit found that the complex, off-axis case is the part not in the literature.
- **The even-exponent Gaussian ceiling is weaker than the claim's.** It is 0.045% at N = 4 against the claim's 0.015%; at N = 1.5 it is trivial. All numbers are in run `2026-10-18-claude-interactive-zs-lean-audit`.

## Changed

- **Added:**
  - `formal/ZSFormalization.lean`, `formal/ZSFormalization/` (13 modules, the formalizer's README and `verification/`, and `PROVENANCE.md`);
  - `runs/2026-10-18-claude-interactive-zs-lean-audit/`;
  - `results/formalized/R-0001-zs-even-moment-passive-mask-ceiling/`;
  - `results/promising/R-0002-zs-real-exponent-and-gaussian-ceilings/`;
  - tasks T-20261018-claude-interactive-05 to -10.
- **`formal/lakefile.toml`:** a new library entry, with only the line-length linter off for it; the default build targets now include it.
- **`formal/README.md`:** a library index (attributed; gpt-a's text unchanged).
- **C-20261018-pi-chatgpt-01:** status audited → promoted; `result: [R-0001, R-0002]`; a Formal verification row and an audit-trail row.
- **P-20261016-claude-interactive-03:** `results` lists R-0001 and R-0002, and an audit-trail row is added; status unchanged.
- **Validator, ranking and dashboard:** these now understand tiers.
  - I tested the new validator checks on a scratch copy: formalized with G8 open, unknown theorem, same-family formal auditor, tier mismatch, non-standard axiom, and stray folder all fail as intended.
  - The generated `RANKING.md` and dashboard were not edited; CI rebuilds them.
- **Relaxed rule.** `validate.py` no longer requires four figure files. It requires at least one figure and a gate record. The four figures are still listed in `docs/PROMOTION.md`, and missing ones leave G4 or G7 open. The reason: expected figure 2 (error scaling) does not apply to exact inequalities. The PI should confirm this.

## Not verified

- **The formalizer's identity.** "Family gpt" is inferred from the Codex app path, and the model is unknown (T-20261018-claude-interactive-08).
- **The README's references** to "Assess Claim Novelty.pdf", pp. 58–63: the PDF is not available.
- **The toolchain binaries'** integrity beyond a standard `elan` install with no overrides.
- **The `promoted: 2026-10-18` and `status: accepted` fields** assume the PI merges today; if not, update the date.
- **The ChatGPT-side reproduction scripts** named in the claim's README are still not in the repository (unchanged from before).

## Loose ends

- T-20261018-claude-interactive-05: second-family (GPT) novelty audit, gate G6 of both results.
- T-20261018-claude-interactive-06: extend the formalization to rough masks and non-Schwartz sources.
- T-20261018-claude-interactive-07: formalize real exponents and sharp Hausdorff–Young, (E) and (F).
- T-20261018-claude-interactive-08 (PI): the formalizer's model and agent id.
- T-20261018-claude-interactive-09 (PI): which other cross-family verified claims become promising results. There are eight candidates, listed in the task.
- T-20261018-claude-interactive-10: ranking reviews from two families.
- `formal/AnalyticalNL/Parity.lean` (gpt-a) cannot become a formalized result yet: its claim, C-20261010-claude-a-03, is still `proposed`, and no other family has audited the formalization. No task is created until the claim advances.
