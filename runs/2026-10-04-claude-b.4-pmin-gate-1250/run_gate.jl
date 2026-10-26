# run_gate.jl -- claude-b.4, T-20261004-claude-interactive-03, step 1.
# Usage: JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no runs/2026-10-04-claude-b.4-pmin-gate-1250/run_gate.jl [sweep-tag ...]
# Writes one TOML per power point to ~/analytical-nl-discovery-data/2026-10-04-claude-b.4-pmin-gate-1250/points/.
include(joinpath(@__DIR__, "pmin_lib.jl"))
const RUN_ID = "2026-10-04-claude-b.4-pmin-gate-1250"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
cfg = TOML.parsefile(joinpath(@__DIR__, "config.toml"))
mkpath(joinpath(RAW, "points"))
@printf("source sha256 %s\n", file_sha256(cfg["source_spectrum"])); flush(stdout)
wanted = isempty(ARGS) ? nothing : Set(ARGS)
phys = Dict{String,Any}()
for sw in cfg["sweeps"]
    (wanted === nothing || sw["tag"] in wanted) || continue
    kind = sw["kind"]
    ph = get!(() -> wavelength_physics(cfg["wavelength_nm"]; kind), phys, kind)
    for P in sw["powers_mw"]
        path = joinpath(RAW, "points", @sprintf("%s_%s_P%.2f.toml", sw["tag"], kind, P))
        isfile(path) && continue
        d = lp01_point(ph; wl=cfg["wavelength_nm"], P=P, L=sw["length_m"], nt=sw["nt"], window_ps=sw["window_ps"],
            dz=sw["dz_m"], zspacing=sw["raman_z_spacing_m"], lo=cfg["lo_nm"], hi=cfg["hi_nm"],
            gdd_ps2=cfg["gdd_ps2"], temperature_K=cfg["temperature_K"])
        d["sweep_tag"] = sw["tag"]; d["kind"] = kind; d["run_id"] = RUN_ID
        write_toml(path, d)
        @printf("GATE %s %s P=%.2f F=%.10g Fb=%.6g Fs=%.6g FR=%.6g G=%.5f Pout=%.6f edge=%.2g fwd=%.1fs adj=%.1fs\n",
            sw["tag"], kind, P, d["F_total"], d["F_bright"], d["F_shape"], d["F_Raman"], d["transfer_slope_G"],
            d["selected_output_power_mw"], d["temporal_edge_fraction"], d["forward_seconds"],
            d["adjoint_and_reservoir_seconds"])
        flush(stdout)
    end
end
println("GATE DONE")
