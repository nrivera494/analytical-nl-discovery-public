# Rules for every agent working in this repository

These rules apply to all agents regardless of provider. If a rule here conflicts with a task description, this file wins. If you think a rule is wrong, say so in your log entry and open a task; do not work around it.

## Mission

Find analytical results (exact or asymptotic solutions, reduced models, scaling laws, invariants and symmetry mappings, onset conditions, noise formulas, bounds) in nonlinear ultrafast, multimode and amplifying fiber systems that hold up against simulation and adversarial audit. The bar for interest is a result that is robust, low-dimensional, comes with a usable scaling law, and can be tested in the lab.

## The three layers

- **Problem** (`problems/P-*.md`): a quantity we want a theory of, with the state of the literature. Problems are promoted, demoted and parked as the literature picture changes.
- **Claim** (`claims/C-*.md`): one specific proposed result attached to one problem. Most claims will be refuted. Refuted claims are kept.
- **Result** (`results/formalized/R-*/` or `results/promising/R-*/`): a claim, or part of one, that was verified across families and approved by the PI. **Formalized** results are also kernel-checked Lean theorems audited by another family; **promising** results are not formalized. Gates are in `docs/PROMOTION.md`. Only the PI merges into `results/`.

Lifecycle details are in `docs/WORKFLOW.md`.

## Identity

Every artifact you create records who made it:

- `agent`: the id you were launched with (for example `claude-a`, `gpt-b`). Subagents append a suffix (`claude-a.3`).
- `model`: the exact model name and version you are running as.
- `family`: `claude`, `gpt`, or another provider name. Humans use `human`.

Never write another agent's identity into a field. Never guess your model version; if you do not know it, write `unknown` and say so in the log.

## Session protocol

1. `git fetch && git checkout main && git pull && git submodule sync solver && git submodule update --init --depth 1 solver`.
2. Read `STATUS.md` (PI priorities section), then `automation/policy.yaml`.
3. Pick work: `python scripts/task.py next --family <family>`. Claim it: `python scripts/task.py claim <task-id> --agent <agent>`. Claiming creates the branch `task/<task-id>`; if the claim fails, someone else has it, so pick another.
4. Do the work on that branch. Commit early and often with messages that start with the task id.
5. Before you stop, whether or not you finished:
   - update the files you touched so they are true as of now;
   - create a task for every loose end (`python scripts/task.py new ...`);
   - write a log entry in `log/` from `log/_TEMPLATE.md`;
   - run `python scripts/validate.py` and fix what it reports;
   - push and open a pull request. If the task is finished, set its `status: done` in the same PR.
6. Stop when your time budget ends. An unfinished task with an honest log entry is a good outcome. A finished-looking task with unverified statements is the worst outcome.

## Hard rules

1. **Independence.** A claim may not be marked `sim-verified` or `audited` by an agent of the same family that proposed it. `scripts/validate.py` enforces this.
2. **Clean-context audit.** When auditing, read only the claim card and the evaluator code. Do not read the proposer's derivation notes, log entries or branch history until your audit report is committed. See `docs/AUDIT_PROTOCOL.md`.
3. **Every number traces to a run.** Any numerical statement in a claim or result cites a run id under `runs/`. No run id, no number.
4. **Every literature statement traces to a source.** Give a DOI or arXiv id and say how much you read: `full text`, `abstract only`, or `not accessed`. Never cite a paper you could not locate. "No theory found" must state what was searched.
5. **Assumption ledger.** Every claim lists its assumptions explicitly, including the ones inherited from the model (for example, rate-equation gain, scalar field, no Raman). A verifier checks the claim against a model that relaxes at least one of them.
6. **State the regime.** Every claim and result gives its validity domain as bounds on dimensionless groups. A result that holds "for typical parameters" is not a result.
7. **Keep failures.** Never delete a refuted claim, a demoted problem, or a failed run. Change the status and say why.
8. **Generated files are read-only.** Do not hand-edit `problems/INDEX.md`, `results/RANKING.md`, or the block between the `DASHBOARD` markers in `STATUS.md`.
9. **No raw data in git.** Commit configs, seeds, summary numbers and figures. Raw output goes to the storage location named in `runs/README.md`.
10. **Benchmark hygiene.** During a rediscovery run you may not search the web or the repo for the masked item. The held-out tier is not in this repo; do not ask for it and do not reconstruct it.
11. **No exact-solution mill.** A formally exact solution of a model with no physical realization, or one that exists only on a fine-tuned parameter manifold, is not a claim. Every claim names a physical system and a measurable prediction.
12. **Do not promote your own work.** Only a PR approved by the PI adds a folder to `results/`.
13. **Branches.** Work only on `task/<task-id>` branches. Never push to `main`. Never force-push a branch you did not create, except the stale-claim takeover described in `automation/README.md`.
14. **The original solver is read-only.** Never modify github.com/nrivera494/FastDifferentiableMMNLO in any way: no pushes, branches, tags, pull requests, issues, comments, releases or settings changes. You may clone and read it. Solver changes go to the agents' copy (`docs/SOLVER.md`); only the PI carries them to the original.
15. **No personal data in web requests.** Use a generic User-Agent. Never put an e-mail address, a name or any other personal data in request headers, URLs, query strings or payloads. That includes the "contact" or `mailto` fields that the Crossref, OpenAlex and arXiv APIs ask for: leave them out. When you brief a helper agent, pass this rule on.

## Solver

The solver is FastDifferentiableMMNLO. The submodule `solver/` holds the agents' private copy, github.com/nrivera494/FastDifferentiableMMNLO-agents. You may change that copy when a capability you need does not exist; follow `docs/SOLVER.md`. Every run records the solver commit, and that commit must exist on the agents' copy (runs made before 2026-10-06 cite commits of the original). The original repository is read-only for agents (hard rule 14).

## Evidence standards

- A fit is weak evidence. An error that shrinks with the stated small parameter at the predicted power is strong evidence. Report the measured exponent.
- Score predictions on parameter regions that were not used to build the claim, and say which regions those were.
- Check numerical artefacts before believing a phenomenon: window reflections, aliasing, step-size dependence, mode-basis truncation. Report the convergence test.
- When two solvers are available, use both.

## Writing

Plain, specific, no promotion. Say what was done, what was found, and what is not known. Equations in LaTeX inside `$...$`. Keep problem and claim files current rather than appending history; history goes in the audit trail section and in `log/`.
