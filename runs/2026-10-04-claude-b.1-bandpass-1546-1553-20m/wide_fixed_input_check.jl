# Extra check for run 2026-10-04-claude-b.1-bandpass-1546-1553-20m (not in the archive).
# The "wide" and "coarse" grids rebuild the input from the measured source spectrum on a different frequency grid,
# so they change the input itself slightly (coupled power changes by about 1e-5 relative). This script separates the
# propagation-window test from that input resampling: it takes the nominal-grid input (8192 samples, 80 ps) and
# zero-pads it in time to 16384 samples over 160 ps at the same 9.765625 fs spacing, then repeats the nominal readout.
#
# Usage: JULIA_NUM_THREADS=2 julia --project=solver wide_fixed_input_check.jl [agarwal|anisotropic]
include(joinpath(@__DIR__, "run_bandpass_point.jl"))

function wide_fixed_input(kind;dz=0.005,zs=0.025)
    p0=filter_problem(kind;nt=8192,window_ps=80.0)
    pw=filter_problem(kind;nt=16384,window_ps=160.0)
    @assert isapprox(pw.grid.dt,p0.grid.dt;rtol=1e-14)
    pad=div(pw.nt-p0.nt,2)
    @assert maximum(abs.(pw.t[pad+1:pad+p0.nt]-p0.t))<1e-12
    a=zeros(ComplexF64,pw.nt,1,1);a[pad+1:pad+p0.nt,:,:].=p0.a
    pr=merge(pw,(;a,pin_mw=p0.pin_mw))
    fwd=@elapsed sol=solve_mmgnlse(pr.a,pr.pars,dz;saveat=zs)
    @printf("FORWARD %s:wide_fixed_input nt=%d window=%.1f dz=%.4g Pin=%.12g seconds=%.1f\n",kind,pr.nt,pr.window_ps,dz,pr.pin_mw,fwd);flush(stdout)
    d=direct_band(pr,sol;label="$(kind)_wide_fixed_input_edge0.5",lo_nm=Float64(SET["lo_nm"]),hi_nm=Float64(SET["hi_nm"]),
        edge_nm=0.5,peak=Float64(SET["peak_transmission"]),dz,zspacing=zs)
    d["forward_seconds"]=fwd
    d["input_note"]="nominal-grid (8192, 80 ps) input zero-padded in time to 16384 samples, 160 ps"
    d["extra_driver_sha256"]=file_sha256(@__FILE__)
    write_toml(joinpath(RAW,"$(kind)_wide_fixed_input_edge0.5.toml"),d)
    d
end

if abspath(PROGRAM_FILE) == @__FILE__
    for kind in (isempty(ARGS) ? ["agarwal"] : ARGS)
        wide_fixed_input(kind)
    end
end
