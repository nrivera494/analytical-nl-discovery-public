# run_map.jl -- claude-b.4, T-20261004-claude-interactive-03, step 3 (map P_min(L)).
# Usage: JULIA_NUM_THREADS=2 julia --project=solver --startup-file=no runs/2026-10-04-claude-b.4-pmin-length-map/run_map.jl [L ...]
# Without arguments, runs every length in config.toml in the listed order. Points already on disk are reused.
# Writes one TOML per point to ~/analytical-nl-discovery-data/2026-10-04-claude-b.4-pmin-length-map/points/.
include(joinpath(@__DIR__, "pmin_lib.jl"))
const RUN_ID = "2026-10-04-claude-b.4-pmin-gdd0-check"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
const CFG = TOML.parsefile(joinpath(@__DIR__, "config.toml"))
mkpath(joinpath(RAW, "points"))
const KIND = get(ENV, "PMIN_KIND", CFG["kind"])
const PH = wavelength_physics(CFG["wavelength_nm"]; kind=KIND)
@printf("source sha256 %s kind %s\n", file_sha256(joinpath(INPUTS, "source_100mw.csv")), KIND); flush(stdout)

zspacing(L) = L <= 1.25 + 1e-9 ? CFG["raman_z_spacing_short_m"] : CFG["raman_z_spacing_long_m"]

function point(L, P)
    P = round(P; digits=3)
    path = joinpath(RAW, "points", @sprintf("%s_L%.3f_P%.3f.toml", KIND, L, P))
    isfile(path) && return TOML.parsefile(path)
    d = lp01_point(PH; wl=CFG["wavelength_nm"], P=P, L=L, nt=CFG["nt"], window_ps=CFG["window_ps"],
        dz=CFG["dz_m"], zspacing=zspacing(L), lo=CFG["lo_nm"], hi=CFG["hi_nm"], gdd_ps2=CFG["gdd_ps2"],
        temperature_K=CFG["temperature_K"])
    d["run_id"] = RUN_ID; d["kind"] = KIND
    write_toml(path, d)
    @printf("MAP L=%.3f P=%9.3f F=%.8f Fb=%.5f Fs=%.5f FR=%.5f G=%+.5f Pout=%9.3f tedge=%.1e sedge=%.1e drift=%.1e fwd=%.1fs adj=%.1fs\n",
        L, P, d["F_total"], d["F_bright"], d["F_shape"], d["F_Raman"], d["transfer_slope_G"],
        d["selected_output_power_mw"], d["temporal_edge_fraction"], d["spectral_edge_fraction"], d["photon_drift"],
        d["forward_seconds"], d["adjoint_and_reservoir_seconds"])
    flush(stdout)
    d
end

grid_ok(d) = d["temporal_edge_fraction"] <= CFG["max_temporal_edge_fraction"] &&
             d["spectral_edge_fraction"] <= CFG["max_spectral_edge_fraction"]

function sorted_F(pts)
    Ps = sort(collect(keys(pts)))
    Ps, [pts[p]["F_total"] for p in Ps]
end

function sweep_length(L)
    pts = Dict{Float64,Any}()
    r = CFG["coarse_ratio"]
    Pg = CFG["P_guess_1m_mw"] * L^(-0.8)
    # 1. coarse upward scan
    # Stop once a dip below F = 0.99 has been passed by two rising points (the weak-power region has wiggles of
    # order 0.005 around F = 1 that must not be mistaken for the minimum), or above 10 P_guess.
    k = 0
    while k < 40
        P = round(CFG["start_factor"] * Pg * r^k; digits=3)
        P > 10 * Pg && (println("WARN no dip below 0.99 found up to 10 P_guess at L=$L"); break)
        d = point(L, P); pts[P] = d
        grid_ok(d) || (println("WARN grid diagnostic failed in coarse scan at P=$P"); break)
        Ps, Fv = sorted_F(pts); i = argmin(Fv)
        if Fv[i] < 0.99 && i <= length(Ps) - 2 && Fv[end] > Fv[i] + CFG["rise_needed"] && Fv[end-1] > Fv[i]
            break
        end
        k += 1
    end
    # extend downward while the minimum (below 0.99) is the lowest sampled power
    for _ in 1:30
        Ps, Fv = sorted_F(pts); i = argmin(Fv)
        (i > 1 || Fv[i] >= 0.99) && break
        P = round(Ps[1] / r; digits=3)
        P < 1.0 && break
        pts[P] = point(L, P)
    end
    Ps, Fv = sorted_F(pts); Pc = Ps[argmin(Fv)]
    # 2. refine around the coarse minimum at 4% spacing, extend until the lowest point is interior
    for f in CFG["refine_factors"]
        P = round(Pc * f; digits=3); pts[P] = point(L, P)
    end
    for _ in 1:10
        Ps, Fv = sorted_F(pts); i = argmin(Fv)
        lo_gap = i > 1 ? Ps[i] / Ps[i-1] - 1 : Inf
        hi_gap = i < length(Ps) ? Ps[i+1] / Ps[i] - 1 : Inf
        if lo_gap > 0.05
            P = round(Ps[i] * 0.96; digits=3); pts[P] = point(L, P)
        elseif hi_gap > 0.05
            P = round(Ps[i] * 1.04; digits=3); pts[P] = point(L, P)
        else
            break
        end
    end
    Ps, Fv = sorted_F(pts); Pm = Ps[argmin(Fv)]
    # 3. plateau search: continue upward until the bright amplitude c changes sign
    Pmax = CFG["plateau_max_factor"] * Pm
    P = maximum(Ps)
    found = false
    while P < Pmax
        P = round(P * CFG["plateau_ratio"]; digits=3)
        d = point(L, P); pts[P] = d
        if !grid_ok(d)
            println("WARN grid diagnostic failed in plateau scan at L=$L P=$P; stopping plateau search")
            break
        end
        if d["bright_amplitude_c"] < 0
            found = true
            break
        end
    end
    if found
        # two bisection steps in ln P on the sign change of c
        for _ in 1:2
            Ps = sort(collect(keys(pts)))
            cs = [pts[p]["bright_amplitude_c"] for p in Ps]
            j = findfirst(k -> cs[k] > 0 && cs[k+1] <= 0, 1:length(Ps)-1)
            j === nothing && break
            P = round(sqrt(Ps[j] * Ps[j+1]); digits=3)
            pts[P] = point(L, P)
        end
    end
    @printf("LENGTH DONE L=%.3f points=%d coarse_min=%.3f plateau_found=%s\n", L, length(pts), Pm, string(found))
    flush(stdout)
end

lengths = isempty(ARGS) ? Float64.(CFG["lengths_m"]) : parse.(Float64, ARGS)
if haskey(ENV, "PMIN_POWERS")
    # Explicit power list (added after the first pass, for the weak-power scans at the shortest lengths):
    # PMIN_POWERS="10,20,30" evaluates exactly these powers at each listed length, with the same grid.
    for L in lengths, P in parse.(Float64, split(ENV["PMIN_POWERS"], ','))
        point(L, P)
    end
    println("LIST DONE")
else
    for L in lengths
        t = @elapsed sweep_length(L)
        @printf("LENGTH TIME L=%.3f %.1f s\n", L, t); flush(stdout)
    end
    println("MAP DONE")
end
