# Reproducing R-0003

All commands run from the repository root with the agents' venv (`~/agent-work/venv`: numpy, scipy, mpmath, matplotlib, tomli). Check `memory_pressure | grep 'free percentage'` before each heavy command and run one at a time. The agents' solver is pinned to b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa.

## Figure 1 (`runs/2026-10-16-gpt-d-raman-bound-audit/audit_summary.png`)

It is drawn from committed summaries only, in a few seconds:

```sh
MPLCONFIGDIR=/tmp/mpl ~/agent-work/venv/bin/python runs/2026-10-16-gpt-d-raman-bound-audit/plot_audit.py
```

The script reads `math_summary.json` and `summary.json` in that folder. claude-interactive.15 reran it on a copy in a scratch directory on 2026-10-19, and it produced the figure without error. The script overwrites the committed figure in place.

To regenerate the summaries themselves:
1. Rerun the propagation cases: `python runs/2026-10-16-gpt-d-raman-bound-audit/propagate.py runs/2026-10-16-gpt-d-c02-<case>/config.yaml`, one case at a time. The case configs are committed.
2. Run `math_check.py` and `symmetry.py`.
3. Run `collect.py`, which rebuilds `summary.json`.
4. For the second solver and the adjoint attack, run `julia_core.jl` and `adjoint_bound.jl` with `--project=solver`.

The order of freezes and runs is in that folder's `protocol.md`. Raw output goes to `~/analytical-nl-discovery-data/2026-10-16-gpt-d-*`.

## Figure 2 and the frozen propagation suite

Figure 2 is `runs/2026-10-17-gpt-d-raman-sharpening/fig_summary.png`. It needs the raw output of two runs, so regenerate in this order. The recorded wall times are 426 s for the Python propagation (`meta.yaml` of run `2026-10-17-gpt-d-raman-propagation`) and 38 s and 89 s for the two Julia cases (its `summary.json`):

```sh
~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-sharpening/analyze.py
~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-sharpening/followup.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 ~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-propagation/propagate.py
JULIA_NUM_THREADS=1 julia --heap-size-hint=2G --project=solver runs/2026-10-17-gpt-d-raman-propagation/julia_crosscheck.jl core h6_100
MPLCONFIGDIR=/tmp/mpl ~/agent-work/venv/bin/python runs/2026-10-17-gpt-d-raman-sharpening/report.py
```

`report.py` writes both figures and the summaries of runs `2026-10-17-gpt-d-raman-propagation` and `2026-10-17-gpt-d-raman-conditional`. The run READMEs give the details, including the rule not to overwrite preserved failed evidence.

## Key numbers and their runs

| Number in RESULT.md | Run |
|---|---|
| $\kappa_U=9.31\times10^{-4}$ pJ⁻¹ m⁻¹ (SMF-28), sum rule to $4\times10^{-11}$ | `2026-10-16-claude-interactive.6-c02-heldout` (`summary.json`, `sumrule.json`) |
| $\kappa_U=9.3103132\times10^{-4}$, sum rule to $2.2\times10^{-16}$, analytic passivity | `2026-10-16-gpt-d-raman-bound-audit` (`math_summary.json`) |
| Identity residual $5.59\times10^{-14}$, 36,011 planes, largest $\rho=0.31037732$, core retention 0.95296272 vs 0.63213680, step exponents 4.972 and 4.465, Julia vs Python $1.04\times10^{-10}$ | `2026-10-17-gpt-d-raman-propagation` (`summary.json`, `analysis`) |
| Retention table of section 5 | `2026-10-16-gpt-d-raman-bound-audit` (`summary.json`, `runs`) |
| Adjoint attack 0.86577286 vs 0.86577168 | `2026-10-16-gpt-d-c02-adjoint`, `2026-10-16-gpt-d-c02-mask-*` |
| Formal short pulses, $\rho$ up to 0.95566 | `2026-10-16-gpt-d-c02-short2p0`, `-short1p0`, `-short0p5`, `-short0p5-wide` |
| Frequency-dependent area | `2026-10-16-gpt-d-c02-area` |
| Hollenbeck–Cantrell $k$ | `2026-10-17-claude-interactive.8-hc-relaxed` |
| Blue-edge window photon loss | `2026-10-16-claude-interactive.6-h1-conservation` |
