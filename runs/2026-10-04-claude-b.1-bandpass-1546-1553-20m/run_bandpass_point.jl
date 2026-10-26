# Driver for run 2026-10-04-claude-b.1-bandpass-1546-1553-20m.
# Adapted from archive research_runs/2026-09-23_arbitrary_bandpass/filter_common.jl
# (sha256 a8d2066f9cf13779db19a3caea452fce391a069742b480df935c1a6d6e2c2aef; functions filter_problem, bandpass,
# direct_band) and validate_selected.jl (sha256 f6ccd58bac5a29f1bf68fc544f9c5c7d537ab803a6c38b4da49b0683f4bf6b64).
# Numerical steps are unchanged. Changes: settings come from config.toml; only the "long" condition is built; output
# goes to the raw-data folder; a total-photon (all-wavelength) readout is added on the same propagation as a check.
#
# Usage: JULIA_NUM_THREADS=2 julia --project=solver run_bandpass_point.jl [kind:tag ...]
#        (no arguments: all grids in config.toml, in order)
include(joinpath(@__DIR__, "lp01_archive_lib.jl"))
const RUN_ID = "2026-10-04-claude-b.1-bandpass-1546-1553-20m"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
const CONFIG = joinpath(@__DIR__, "config.toml")
const CFG = TOML.parsefile(CONFIG)
const SET = CFG["setting"]

for (k, f) in (("source_spectrum", joinpath(INPUTS, "source_100mw.csv")), ("filter_csv", joinpath(INPUTS, "filter.csv")))
    got = file_sha256(f)
    got == SET[k*"_sha256"] || error("sha256 mismatch for $f: $got")
end

function filter_problem(kind;nt=2048,window_ps=20.0,power_scale=1.0,gdd_ps2=Float64(SET["gdd_ps2"]))
    ph=physics_at(1550.0;raman_kind=kind)
    SET["condition"]=="long" || error("only the long condition is configured")
    options=(;pin_mw=Float64(SET["pin_before_prefilter_mW"])*power_scale,length_m=Float64(SET["length_m"]),
        prefilter_width_nm=Float64(SET["prefilter_width_nm"]),power_before_prefilter=true)
    make_design(ph;options...,nt,window_ps,gdd_ps2)
end

function bandpass(pr,lo,hi;edge_nm=0.0,peak=1.0)
    lambda=pr.lambda.*1e9
    if edge_nm==0
        return peak.*Float64.((lambda.>=lo).&(lambda.<hi))
    end
    # edge_nm is the 10%-90% width of each logistic power-transmission edge.
    scale=edge_nm/(2log(9))
    rise=1 ./ (1 .+exp.(clamp.((lo.-lambda)./scale,-700.0,700.0)))
    fall=1 ./ (1 .+exp.(clamp.((lambda.-hi)./scale,-700.0,700.0)))
    peak.*rise.*fall
end

function finish!(d,pr,sol,adj,label;zspacing)
    vr,_=scalar_raman_variance(pr,sol,adj;temperature_K=Float64(SET["temperature_K"]))
    d["F_without_reservoir"]=d["F_filter"]
    d["raman_F_increment"]=vr/d["mean_photons_after_filter"]
    d["F_filter"]+=d["raman_F_increment"]
    d["dB_intrinsic"]=10log10(d["F_filter"])
    d["power_after_ideal_bandpass_mw"]=d["detected_power_mw"]/(.95*.87*10.0^(-0.3))
    d["raman_z_spacing"]=zspacing;d["response"]=string(typeof(pr.ph.raman));d["label"]=label
    d["prefilter_width_nm"]=pr.prefilter_width_nm
    d["power_before_input_filter_equivalent_mw"]=pr.coupled_equivalent_power_before_prefilter_mw
    d["run_id"]=RUN_ID
    d["config_sha256"]=file_sha256(CONFIG)
    d["lib_sha256"]=file_sha256(joinpath(@__DIR__,"lp01_archive_lib.jl"))
    d["driver_sha256"]=file_sha256(@__FILE__)
    d["julia_threads"]=Threads.nthreads()
    d
end

function direct_band(pr,sol;label,lo_nm,hi_nm,edge_nm=0.0,peak=1.0,dz=0.01,zspacing=0.1)
    pr=merge(pr,(;T=bandpass(pr,lo_nm,hi_nm;edge_nm,peak)))
    d,adj=measure(pr,sol;dz,save_adjoint=zspacing)
    finish!(d,pr,sol,adj,label;zspacing)
    d["lo_nm"]=lo_nm;d["hi_nm"]=hi_nm;d["edge_10_90_nm"]=edge_nm;d["filter_peak_transmission"]=peak
    write_toml(joinpath(RAW,label*".toml"),d)
    @printf("BAND %s [%.3f,%.3f] edge=%.3f Pin=%.6f F=%.12g FR=%.9g F0=%.12g Pband=%.9g drift=%.2g edge_frac=%.2g adj=%.1fs\n",
        label,lo_nm,hi_nm,edge_nm,pr.pin_mw,d["F_filter"],d["raman_F_increment"],d["F_without_reservoir"],
        d["power_after_ideal_bandpass_mw"],d["photon_drift"],d["temporal_edge_fraction"],d["adjoint_seconds"])
    flush(stdout)
    d
end

# Check added for this run: all wavelengths (T = 1) on the same propagation. Kerr and Raman conserve the
# all-band photon number, so F must be 1 with a negligible Raman part.
function total_photon(pr,sol;label,dz,zspacing)
    pr=merge(pr,(;T=ones(pr.nt)))
    d,adj=measure(pr,sol;dz,save_adjoint=zspacing)
    finish!(d,pr,sol,adj,label;zspacing)
    write_toml(joinpath(RAW,label*".toml"),d)
    @printf("TOTAL %s F=%.15g FR=%.3g F0=%.15g\n",label,d["F_filter"],d["raman_F_increment"],d["F_without_reservoir"])
    flush(stdout)
    d
end

function run_all(selection)
    println("BANDPASS_RUN_STARTED");flush(stdout)
    for g in CFG["grids"]
        key=g["kind"]*":"*g["tag"]
        (isempty(selection) || key in selection) || continue
        kind=g["kind"];tag=g["tag"];dz=Float64(g["dz_m"]);zs=Float64(g["raman_z_spacing_m"])
        pr=filter_problem(kind;nt=g["nt"],window_ps=Float64(g["window_ps"]))
        fwd=@elapsed sol=solve_mmgnlse(pr.a,pr.pars,dz;saveat=zs)
        @printf("FORWARD %s nt=%d window=%.1f dz=%.4g Pin=%.12g seconds=%.1f\n",key,pr.nt,pr.window_ps,dz,pr.pin_mw,fwd);flush(stdout)
        for edge in Float64.(g["edges_nm"])
            d=direct_band(pr,sol;label="$(kind)_$(tag)_edge$(edge)",lo_nm=Float64(SET["lo_nm"]),hi_nm=Float64(SET["hi_nm"]),
                edge_nm=edge,peak=Float64(SET["peak_transmission"]),dz,zspacing=zs)
            d["forward_seconds"]=fwd
            write_toml(joinpath(RAW,"$(kind)_$(tag)_edge$(edge).toml"),d)
        end
        if g["total_photon_check"]
            total_photon(pr,sol;label="$(kind)_$(tag)_total",dz,zspacing=zs)
        end
        sol=nothing;GC.gc()
    end
    println("BANDPASS_RUN_COMPLETE");flush(stdout)
end

if abspath(PROGRAM_FILE) == @__FILE__
    run_all(ARGS)
end
