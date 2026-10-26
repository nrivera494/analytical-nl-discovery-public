# Optional alternate audit configuration

Agent: gpt-a. Model: gpt-6-astra. Family: gpt. Task: T-20261011-gpt-a-01.
All commands below run from the repository root with `PY=~/agent-work/venv/bin/python`; this is a task-local shell variable. Python calculations use Float64/complex128. Each per-case JSON records the actual grid, step count and parameters; scripts contain the deterministic case lists. Raw outputs stay outside git. No tests below are automatically launched by reading this config.

Source card: `claims/C-20261008-claude-b-01-manakov-grin-filtered-noise.md`, commit `6c16dc1a0d8ecc348351dbe56a01d28249e1b8ff`, branch `task/T-20261008-claude-b-01`. Only the packet-named card, problem and scripts were read; no exploration notes.

Independent two-mode XPM split step, anomalous beta=1, no gain/loss/Raman/TOD, zeta=2. Initial field sqrt(p)*sech(t)/sqrt(p^T*C*p). C=all-ones for Manakov; GRIN C=[[1,1],[1,0.5]]. Window40,Nt256,step<=0.002 and linear phase<=0.5; grid/step refinements Nt512,step<=0.001. Masks: centered binary bin radii1..14, all-count, 0.6 transmission within radius5, and asymmetric binary bins[-2,7]. Physical attenuation vacuum is added. Near-Manakov p=[0.7,0.3],Delta22=+/-0.02,+/-0.04,+/-0.08. Relaxations: differential walk-off0.6; modal dispersions[1,1.02]. Deterministic, no random seed needed.

```sh
$PY runs/2026-10-11-gpt-a-highlights-audit-c4/audit.py
$PY runs/2026-10-11-gpt-a-highlights-audit-c4/summarize.py
```

This is a bounded local check, not a verification of global optimized masks, all second-order tensors, or the physical joint regime. All 13 cases are saved. Raw stdout is in the run's raw_location; the small per-case diagnostic values are retained in git. Literature sources and access levels are in the audit report.
