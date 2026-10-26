# Solver

The solver is FastDifferentiableMMNLO, a Julia package (`PulsePropagation`) for differentiable single-mode and multimode pulse propagation. It includes adjoint gradients, stochastic (Langevin) propagation, CP-decomposed many-mode backends and an optional CUDA extension.

There are two repositories:

- **The agents' copy**, [nrivera494/FastDifferentiableMMNLO-agents](https://github.com/nrivera494/FastDifferentiableMMNLO-agents) (private). This repository holds it as the git submodule `solver/`, pinned to one commit. Agents read, run and change this copy.
- **The original**, [nrivera494/FastDifferentiableMMNLO](https://github.com/nrivera494/FastDifferentiableMMNLO) (public). Agents may clone and read it. Agents never modify it in any way: no pushes, branches, tags, pull requests, issues, comments, releases or settings changes. Solver changes reach the original only through the PI (see "Carrying a change to the original" below).

The agents' copy starts at a seed commit whose tree is identical to a commit of the original. The history before the seed is not carried over (it is 16.5 GiB, over GitHub's push limit).

| Agents' copy | Original | Tree | Note |
|---|---|---|---|
| `b9fa957` | `9c12887` | `ce25a00760964a362767daf5799b6611904c1502` | seed, 2026-10-06 |

## Getting it

```sh
git submodule sync solver
git submodule update --init --depth 1 solver
julia --project=solver -e 'using Pkg; Pkg.instantiate()'
```

`git submodule sync` makes an existing checkout follow the URL in `.gitmodules`; without it, a checkout made before 2026-10-06 still points at the original. The checked-out tree is about 330 MB, almost all of it example notebooks and benchmark data; the source is about 1 MB. The launcher fetches the submodule at the start of every session.

Check the remote before you commit anything in `solver/`:

```sh
git -C solver remote -v      # must show FastDifferentiableMMNLO-agents for push
```

If you add the original as a second remote (for example to compare with it), disable pushing to it at once: `git -C solver remote set-url --push <name> DISABLED`.

Start with `solver/docs/index.md`, `solver/test/README.md` and the notebooks in `solver/example_notebooks/`. The notebooks are the best reference for how the API is called.

## Using it in a run

Every `runs/*/meta.yaml` records:

- `solver_commit`: the output of `git -C solver rev-parse HEAD`;
- `solver_dirty`: `true` if `git -C solver status --porcelain` printed anything.

**Adjoint mode.** For noise contractions and gradients use the discrete adjoint, `solve_adjoint(...; adjoint_mode=:discrete_rk4ip)`, the exact derivative of the fixed-step RK4IP forward map; it requires the adjoint step to equal the forward step. It is the default in the agents' copy once [PR #2](https://github.com/nrivera494/FastDifferentiableMMNLO-agents/pull/2) is merged and the pin is moved; until then pass it explicitly. The continuous adjoint interpolates the forward field and was off by 5–14% for a squeezing observable at dz = 1 mm (run `2026-10-05-claude-interactive-raman-stochastic`). The problem-API backend adjoint used by `gradients.jl` and `variance_objectives.jl` has no discrete mode.

A run on a dirty solver tree, or on a commit that does not exist on the agents' copy, cannot be cited in a claim (AGENTS.md rule 3). Commit and push the solver change first. Runs made before 2026-10-06 cite commits of the original; those remain citable, and the table above maps them to the agents' copy.

## Changing it

Agents may change the solver when a capability they need does not exist. The PI confirmed this on 2026-10-02.

1. Work inside `solver/` on a branch named after your task: `git -C solver checkout -b task/<task-id>`.
2. Add capabilities as opt-in options that leave existing behaviour unchanged. The solver's own history follows this pattern; see the checkpointed-adjoint commits.
3. Every new capability comes with a test in `solver/test/` that checks it against a known analytical limit or an independent calculation, for example the fundamental soliton or energy conservation without gain. Run the CPU suite with `julia --project=solver solver/test/runtests.jl`. If CUDA code changed and no GPU is available, say so in the pull request.
4. Push the branch to the agents' copy and open a pull request there. Its description names the task id and the claim or exploration that needs the change.
5. Add one row to `docs/solver-upstream/LEDGER.md` in the same pull request in this repository that uses or records the change. Fill in what the PI needs to carry it to the original; `docs/solver-upstream/README.md` says what that is.
6. Runs may use the pushed branch commit before it is merged. Moving the pin in this repository (`git add solver` after checking out the new commit) is a separate pull request here. That pull request needs PI review (`.github/CODEOWNERS`).

Do not commit simulation output or large data into the solver repository either.

**Independence.** A solver change that a verification depends on must not be written by an agent of the claim proposer's family. If it was, the verifier says so in the claim's checks table, and the change is reviewed by another family before the claim moves past `cheap-checks-passed`.

## Carrying a change to the original

Only the PI does this. Agents prepare it: each solver change has a ledger row and, when it is more than a few lines, a note in `docs/solver-upstream/` with the commits, the patch command, the evidence and anything the PI may want to do differently in the original. The histories are unrelated, so changes travel as patches (`git format-patch` in the agents' copy, `git am` in the original); they apply cleanly while the touched files are unchanged in the original since the seed.
