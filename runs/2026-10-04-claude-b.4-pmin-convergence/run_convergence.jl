# run_convergence.jl -- claude-b.4, T-20261004-claude-interactive-03, step 5 (convergence).
# Usage: JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no runs/2026-10-04-claude-b.4-pmin-convergence/run_convergence.jl
# For each case in config.toml, evaluates every listed power on the base grid and on three refined grids:
#   dz_half  : propagation step and Raman reservoir spacing halved
#   dt_half  : sample spacing halved (nt doubled, same window); only at the case's dt_half_powers_mw
#   win_x2   : time window doubled at the same sample spacing (nt doubled)
# Writes one TOML per point to ~/analytical-nl-discovery-data/2026-10-04-claude-b.4-pmin-convergence/points/.
include(joinpath(@__DIR__, "pmin_lib.jl"))
const RUN_ID = "2026-10-04-claude-b.4-pmin-convergence"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
const CFG = TOML.parsefile(joinpath(@__DIR__, "config.toml"))
mkpath(joinpath(RAW, "points"))
const PHS = Dict{String,Any}()
@printf("source sha256 %s\n", file_sha256(joinpath(INPUTS, "source_100mw.csv"))); flush(stdout)

for case in CFG["cases"]
    kind = get(case, "kind", "agarwal")
    ph = get!(() -> wavelength_physics(CFG["wavelength_nm"]; kind), PHS, kind)
    L = case["length_m"]
    zs = L <= 1.25 + 1e-9 ? CFG["raman_z_spacing_short_m"] : CFG["raman_z_spacing_long_m"]
    variants = [("base", CFG["nt"], CFG["window_ps"], CFG["dz_m"], zs),
                ("dz_half", CFG["nt"], CFG["window_ps"], CFG["dz_m"] / 2, zs / 2),
                ("dt_half", 2 * CFG["nt"], CFG["window_ps"], CFG["dz_m"], zs),
                ("win_x2", 2 * CFG["nt"], 2 * CFG["window_ps"], CFG["dz_m"], zs)]
    for (tag, nt, win, dz, z) in variants
        plist = tag == "dt_half" ? get(case, "dt_half_powers_mw", case["powers_mw"]) : case["powers_mw"]
        for P in plist
            path = joinpath(RAW, "points", @sprintf("%s_%s_L%.3f_P%.3f_%s.toml", case["tag"], kind, L, P, tag))
            isfile(path) && continue
            d = lp01_point(ph; wl=CFG["wavelength_nm"], P=P, L=L, nt=nt, window_ps=win, dz=dz, zspacing=z,
                lo=CFG["lo_nm"], hi=CFG["hi_nm"], gdd_ps2=CFG["gdd_ps2"], temperature_K=CFG["temperature_K"])
            d["run_id"] = RUN_ID; d["kind"] = kind; d["variant"] = tag; d["case"] = case["tag"]
            write_toml(path, d)
            @printf("CONV %s %s L=%.3f P=%.3f %-7s F=%.10f Fb=%.6f Fs=%.6f FR=%.6f G=%+.6f Pout=%.6f tedge=%.1e sedge=%.1e fwd=%.1fs adj=%.1fs\n",
                case["tag"], kind, L, P, tag, d["F_total"], d["F_bright"], d["F_shape"], d["F_Raman"],
                d["transfer_slope_G"], d["selected_output_power_mw"], d["temporal_edge_fraction"],
                d["spectral_edge_fraction"], d["forward_seconds"], d["adjoint_and_reservoir_seconds"])
            flush(stdout)
        end
    end
end
println("CONVERGENCE DONE")
