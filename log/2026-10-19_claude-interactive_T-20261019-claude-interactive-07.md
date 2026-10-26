---
date: 2026-10-19
agent: claude-interactive
model: claude-opus-5-5
family: claude
task: T-20261019-claude-interactive-07
duration_min: 20
---

## Did

Applied three PI decisions from 2026-10-19:
- **Model name.** The ChatGPT session is recorded as GPT 6 Pro (`gpt-6-pro`) on the four cards and in the review. The run's `meta.yaml` also notes the self-reported "GPT-6 Astra Pro".
- **Promotion.** All cross-family verified claims go to `results/promising/`. I created writer tasks -08, -09 and -10 for R-0003 to R-0013.
- **The promising tier is cross-family verification plus PI approval.** `docs/PROMOTION.md` and `scripts/validate.py` previously also required G5 (a clean-context adversarial audit), which is stricter than the PI's definition. Now:
  - G4 must be met;
  - G5 may be open, with a reason and a task;
  - `audit/` accepts `verification-*.md` reports as well as `audit-*.md`;
  - G5 `met` still requires an `audit-*.md`.

## Found

Eight sim-verified claims had no clean-context audit, so the stricter rule would have blocked all of them, contrary to the PI's decision.

## Changed

- `docs/PROMOTION.md`, `scripts/validate.py`, `results/_TEMPLATE/RESULT.md`, `results/_TEMPLATE/audit/README.md`.
- Model fields on C-20261008-claude-a-02, C-20261010-claude-b-01, C-20261019-pi-chatgpt-01 and -02; the review front matter; the run's `meta.yaml`.
- Tasks -06 and T-20261018-claude-interactive-09 are done, with their decisions recorded.
- Tasks -07 to -10 were created.

## Not verified

Nothing numerical was done in this task.

## Loose ends

- The writer tasks -08, -09, -10, and the verification, audit and literature tasks -02 to -05, have agents launched.
- T-20261018-claude-interactive-08 (the Codex formalizer's model) is still open with the PI.
