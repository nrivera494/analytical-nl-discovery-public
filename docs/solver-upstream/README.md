# Carrying solver changes to the original

Agents change the solver only in the private agents' copy, [nrivera494/FastDifferentiableMMNLO-agents](https://github.com/nrivera494/FastDifferentiableMMNLO-agents). The original, [nrivera494/FastDifferentiableMMNLO](https://github.com/nrivera494/FastDifferentiableMMNLO), is read-only for agents (AGENTS.md rule 14). The PI decides which changes go to the original and carries them.

This folder is what the PI works from:

- `LEDGER.md`: one row per solver change made in the agents' copy, newest first, with its status in the original.
- One note per change that is more than a few lines, named `<date>-<short-name>.md`.

## What a note contains

1. The commits: the agents' copy commit(s) and branch, the seed or merge base, and the corresponding commit of the original that the change applies to. Give tree hashes where they prove two commits are the same files.
2. How to apply it in the original: the exact commands, ending in a reviewable branch. The histories are unrelated (the agents' copy starts at a seed commit), so changes travel as patches.
3. What it changes, file by file, and whether each file is meant for the original or only for the agents' work (for example verification scripts).
4. Why, in a few lines, with the evidence and its run ids in this repository.
5. How to check it after applying: which notebooks or tests to run and the numbers they should print.
6. Decisions for the PI: anything that should be done differently in the original, and known issues the change does not fix (with their task ids).

## Getting a patch without fetching the agents' history

```sh
gh api repos/nrivera494/FastDifferentiableMMNLO-agents/commits/<sha> \
  -H "Accept: application/vnd.github.patch" > change.patch
git am -3 change.patch          # in a clone of the original, on a new branch
```

For a range of commits, use `.../compare/<base>...<head>` with the same header, or fetch the branch and run `git format-patch <base>..<head>`.

When a change has been carried, update its ledger row with the original's commit and the date. If the PI decides not to carry it, say so in the row; do not delete rows.
