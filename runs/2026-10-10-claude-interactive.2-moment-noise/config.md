# Configuration of run 2026-10-10-claude-interactive.2-moment-noise

All commands run from the repository root with `JULIA_NUM_THREADS=2` and the solver submodule at b9fa957 (agents' copy, unmodified). Arguments are documented at the top of each script. Seeds: the Monte Carlo seeds are the third argument of `mc.jl`; all other runs are deterministic.

Raw outputs: `~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/` on the Apple M5 laptop. Commands whose output exists there:

```
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.0125 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.0125_g4_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.025 2 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.025_g2_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.025 2 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.025_g2_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.025 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.025_g4_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.025 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.025_g4_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.025 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.025_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.025 6 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.025_g6_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.05 2 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.05_g2_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.05 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.05_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.05 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.05_g4_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.05 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.05_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.05 6 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.05_g6_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.1 2 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.1_g2_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.1 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.1_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.1 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.1_g4_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.1 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.1_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.1 6 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.1_g6_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.1 6 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/gbw_asym_e0.1_g6_all_b0.05.json 1.0 1.0 e23 0.05
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl asym 0.1 8 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/asym_e0.1_g8_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.0125 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.0125_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.025 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.025_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.025 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.025_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.025 6 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.025_g6_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.05 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/core_heldout_e0.05_g2_all_chirp.json 1.0 1.0 e23 0.0 chirp
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.05 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.05_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.05 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.05_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.05 6 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.05_g6_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.1 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.1_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.1 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.1_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl heldout 0.1 6 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/heldout_e0.1_g6_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.0125 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.0125_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.0125 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.0125_g4_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.025 2 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.025_g2_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.025 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.025_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.025 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.025_g4_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.025 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.025_g4_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.025 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.025_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.025 6 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.025_g6_TW.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.05 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/core_main_e0.05_g2_all_chirp.json 1.0 1.0 e23 0.0 chirp
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.05 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.05_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.05 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.05_g4_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.05 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/conv_main_e0.05_g4_all_grid1.5.json 1.0 1.5
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.05 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/conv_main_e0.05_g4_all_n2.json 2.0 1.0
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.05 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.05_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.05 6 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.05_g6_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.1 2 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.1_g2_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.1 4 TW ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.1_g4_TW_d1.json 1.0 1.0 e1
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.1 4 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.1_g4_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl main 0.1 6 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/main_e0.1_g6_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl p8 0 0 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/p8_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl p8_lin 0 0 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/p8_lin_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/contract.jl p8_ss 0 0 all ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/p8_ss_all.json
julia --project=solver runs/2026-10-10-claude-interactive.2-moment-noise/fd_check.jl ~/analytical-nl-discovery-data/2026-10-10-claude-interactive.2-moment-noise/fd_check.json
```
