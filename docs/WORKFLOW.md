# Workflow

## Problems

One file per candidate problem or system. The file states the concrete quantity to develop a theory of, the governing model, the state of the literature, the sharpest statement of what is open, and how a candidate theory would be checked.

Status values:

| Status | Meaning |
|---|---|
| `candidate` | Proposed. Literature not yet audited by a second family. |
| `audited` | At least two model families have reviewed the literature and agree on what is open. |
| `active` | Audited and selected by the PI for derivation work. |
| `parked` | Open but blocked (missing solver capability, missing lab capability). |
| `demoted` | More prior work than thought, or not physically interesting. Kept, with the reason. |
| `solved` | Has at least one accepted result. May remain active for extensions. |

Changing a problem's status, priority or `literature_state` requires a new row in its audit trail giving the date, the agent, and the evidence.

Adding a problem: copy `problems/_TEMPLATE.md`. New problems start as `candidate`. Use a provisional id of the form `P-<date>-<agent>-NN`; the PI assigns a sequential id on merge.

## Claims

One file per proposed result. Status values:

| Status | Requires |
|---|---|
| `proposed` | Statement, regime, assumptions, predictions. |
| `cheap-checks-passed` | Units, limits, symmetry and symbolic residual checks recorded. |
| `sim-verified` | Simulation checks by a different family; held-out regime; error-scaling exponent measured. |
| `audited` | Adversarial audit by a different family with no unresolved blockers. |
| `promoted` | A result folder exists and was merged by the PI. It needs at least cross-family verification (`sim-verified`); a promising result may precede the clean-context audit, which then fills `audited_by` without changing the status. |
| `refuted` | A check failed. The failing check and run id are recorded. |
| `withdrawn` | Superseded or found to be already published. Cite what supersedes it. |

Claim ids have the form `C-<date>-<agent>-NN` so that parallel agents never collide.

## Results

See `docs/PROMOTION.md` for the gates and `results/_TEMPLATE/` for the layout. A result is a presentation of one verified claim, or of one part of it: the problem, the statement, the derivation, the validation figures, the regime, the audit record. There are two tiers. `results/promising/` holds cross-family verified results the PI approved; `results/formalized/` holds sub-results whose statement is also a kernel-checked Lean theorem in `formal/`, audited by a family other than the formalizer's. A claim's `result` field may list one result in each tier.

## Tasks

The work queue. One file per task in `tasks/`. Types: `registry-review`, `literature`, `derive`, `verify`, `audit`, `explore`, `loose-end`, `rank`, `infra`.

## Explorations

Free exploration produces notes in `explorations/`: an observed phenomenon, the run ids, and why it might have a simple description. A note can be turned into a problem candidate by any agent.
