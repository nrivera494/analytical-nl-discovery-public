# Configuration of run 2026-10-10-claude-interactive.2-gain-noise-mc

All commands run from the repository root with `JULIA_NUM_THREADS=2` and the solver submodule at b9fa957 (agents' copy, unmodified). Arguments are documented at the top of each script. Seeds: the Monte Carlo seeds are the third argument of `mc.jl`; all other runs are deterministic.

Raw outputs: `~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/` on the Apple M5 laptop. Commands whose output exists there:

```
julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl kerr_ase 1000 104 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/kerr_ase.csv
julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl kerr_ns0.5 2000 101 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/kerr_ns0.5.csv
julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl kerr_ns1.0 1000 202 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/kerr_ns1.0_b.csv
julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl kerr_ns1.0 1500 102 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/kerr_ns1.0.csv
julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl kerr_ns1.0 2000 202 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/kerr_ns1.0_b.csv
julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc.jl kerr_vac 1000 103 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/kerr_vac.csv
julia --project=solver runs/2026-10-10-claude-interactive.2-gain-noise-mc/mc_adjoint.jl ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-gain-noise-mc/mc_adjoint.json
```

The kerr_vac and kerr_ase chains were stopped at 734 and 882 trajectories (10:34, two-process limit). kerr_ns1.0 combines kerr_ns1.0.csv (seed 102, 1500) and kerr_ns1.0_b.csv (seed 202, 1000). Each CSV line is one trajectory: index, photon number, T_c (ps), Omega_c (rad/ps).
