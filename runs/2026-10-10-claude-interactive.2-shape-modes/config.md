# Configuration of run 2026-10-10-claude-interactive.2-shape-modes

All commands run from the repository root with `JULIA_NUM_THREADS=2` and the solver submodule at b9fa957 (agents' copy, unmodified). Arguments are documented at the top of each script. Seeds: the Monte Carlo seeds are the third argument of `mc.jl`; all other runs are deterministic.

Raw outputs: `~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/` on the Apple M5 laptop. Commands whose output exists there:

```
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.025 6 1e-4 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_asym_e0.025_g6_eta1e-4.json
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.05 6 1e-3 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_asym_e0.05_g6.json
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.05 6 1e-4 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_asym_e0.05_g6_eta1e-4.json
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.05 6 1e-4 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_main_e0.05_g6_eta1e-4.json 1.0 main
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.1 6 1e-3 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_asym_e0.1_g6.json
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.1 6 1e-4 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/conv_sm_asym_e0.1_g6_eta1e-4_n2.json 2.0
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.1 6 1e-4 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_asym_e0.1_g6_eta1e-4.json
julia --project=solver runs/2026-10-10-claude-interactive.2-shape-modes/shapemodes.jl 0.1 6 1e-4 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-shape-modes/sm_main_e0.1_g6_eta1e-4.json 1.0 main
```
