# Configuration of run 2026-10-10-claude-interactive.2-attraction

All commands run from the repository root with `JULIA_NUM_THREADS=2` and the solver submodule at b9fa957 (agents' copy, unmodified). Arguments are documented at the top of each script. Seeds: the Monte Carlo seeds are the third argument of `mc.jl`; all other runs are deterministic.

Raw outputs: `~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/` on the Apple M5 laptop. Commands whose output exists there:

```
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.0125 4.242640687119285 0.3333333333333333 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.0125_G4.243_q0.333.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.025 1.0 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.025_G1.000_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.025 10.0 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.025_G10.000_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.025 4.242640687119285 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.025_G4.243_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.025 4.242640687119285 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.025_G4.243_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.025 4.242640687119285 0.3333333333333333 6 0.999 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/r4_e0.025_E0.999.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.025 4.242640687119285 0.3333333333333333 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.025_G4.243_q0.333.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.025 4.242640687119285 0.3333333333333333 6 1.001 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/r4_e0.025_E1.001.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 1.0 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G1.000_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 1.0 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G1.000_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 1.0 1.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G1.000_q1.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 10.0 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G10.000_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 10.0 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G10.000_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 10.0 1.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G10.000_q1.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 4.242640687119285 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G4.243_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 4.242640687119285 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G4.243_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 4.242640687119285 0.3333333333333333 6 0.999 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/r4_e0.05_E0.999.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 4.242640687119285 0.3333333333333333 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G4.243_q0.333.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 4.242640687119285 0.3333333333333333 6 1.001 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/r4_e0.05_E1.001.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.05 4.242640687119285 1.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.05_G4.243_q1.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 1.0 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G1.000_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 1.0 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G1.000_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 1.0 1.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G1.000_q1.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 10.0 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G10.000_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 10.0 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G10.000_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 10.0 1.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G10.000_q1.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 4.242640687119285 -0.5 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G4.243_q-0.500.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 4.242640687119285 0.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G4.243_q0.000.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 4.242640687119285 0.3333333333333333 6 0.999 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/r4_e0.1_E0.999.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 4.242640687119285 0.3333333333333333 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G4.243_q0.333.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 4.242640687119285 0.3333333333333333 6 1.001 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/r4_e0.1_E1.001.json
julia --project=solver runs/2026-10-10-claude-interactive.2-attraction/attraction.jl 0.1 4.242640687119285 1.0 6 1.0 ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-attraction/att_e0.1_G4.243_q1.000.json
```
