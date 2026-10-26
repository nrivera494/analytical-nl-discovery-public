# Driver for run 2026-10-04-claude-b.1-ideal-sech-kerr-20m.
# Adapted from archive research_runs/2026-09-26_analytics/simulations/validate_ideal_sech_kerr.jl
# (sha256 022530ac4f6e25f7700de75df23e33e57bbb09d32c494bcfbb2c412d4c8f21a2). Numerical steps unchanged;
# changes: parameters come from config.toml, a grid tag selects the grid, the pi offset is stored as Float64
# (the archive's first execution failed to serialize the symbolic pi), output goes to the raw-data folder.
#
# Usage: JULIA_NUM_THREADS=2 julia --project=solver run_ideal_sech_kerr.jl <tag> [<tag> ...]
include(joinpath(@__DIR__, "lp01_archive_lib.jl"))
const RUN_ID = "2026-10-04-claude-b.1-ideal-sech-kerr-20m"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
const CONFIG = joinpath(@__DIR__, "config.toml")

# Canonical beta2 Kerr NLSE: this control type changes only its own solver cache.
# No package file or physical Raman response is modified (verbatim from the archive script).
struct InstantaneousNoShock <: PP.AbstractRamanResponse
    fraction::Float64
end
function PP._mmgnlse_solver_cache(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:InstantaneousNoShock}
    nt,nm,np=PP._mmgnlse_public_shape(p)
    omega=PP._mmgnlse_raw_omega(p)
    beta_operator=PP._mmgnlse_beta_array(p.beta,nt,nm,np,omega)
    nonlinear_prefactor=fill(1im*p.n2*p.omega0/C_PS,nt,1,1)
    nonlinear_active=any(!iszero,nonlinear_prefactor) && !PP._mmgnlse_overlap_iszero(p.S)
    raman=(ha=ComplexF64[],hb=ComplexF64[],fraction=0.)
    (;omega,beta_operator,nonlinear_prefactor,nonlinear_active,raman)
end

function run_control(tag)
    cfg = TOML.parsefile(CONFIG)
    d = cfg["frozen_control_parameters"]
    grid = only(filter(g -> g["tag"] == tag, cfg["grids"]))
    nt = grid["nt"]; window = Float64(grid["window_ps"]); dz = Float64(grid["dz_m"])
    ph=physics_at(1550.;raman_kind="agarwal")
    p0=make_design(ph;wavelength_nm=1550.,pin_mw=d["Pin_mW"],length_m=d["length_m"],nt,window_ps=window,gdd_ps2=0.)
    beta=zeros(size(ph.props.beta.coefficients));beta[3,1]=d["beta2_ps2_per_m"]
    n2=d["gamma_per_W_m"]*C_PS/(p0.pars.omega0*spatial_overlap(ph.props)[1,1,1,1])
    pars=MMGNLSEParameters(p0.pars.domain;length=d["length_m"],beta=TaylorBeta(beta),
        S=p0.pars.S,n2,omega0=p0.pars.omega0,raman=InstantaneousNoShock(0.))
    a=reshape(sqrt(d["Ppeak_W"])./cosh.(p0.t./d["T0_ps"]),nt,1,1)
    p=merge(p0,(pars=pars,a=a,T=ones(nt),))
    hbar=H_SI/(2pi)
    weight=nt*p.grid.dt*1e-12/(hbar*p.pars.omega0*1e12)
    power_scale=nt*p.grid.dt*1e-12*REP*1e3
    a0=vec(fftshift(ifft(a,1),1));nin=weight*sum(abs2,a0)
    started=time()
    forward_seconds=@elapsed sol=solve_mmgnlse(a,pars,dz)
    aw=vec(get_spectral_field(sol));ns=weight*sum(abs2,aw)
    phi=d["length_m"]/(2*d["LD_m"])
    mean_error=norm(aw-a0.*exp(im*phi))/norm(a0)
    G=zeros(ComplexF64,nt,2)
    for (j,phase) in enumerate((1.,1im))
        terminal=reshape(phase*weight.*aw./sqrt(ns),nt,1,1)
        adj=solve_adjoint(terminal,pars,dz;forward_solution=sol,units=:power,
            adjoint_mode=:discrete_rk4ip)
        G[:,j].=vec(get_spectral_field(adj;units=:power))./sqrt(weight)
    end
    Q=real.(G'*G)
    eta=d["eta"];r=d["r"];rows=Dict{String,Any}[]
    for offset in Float64.(cfg["readout"]["phase_offsets_rad"])
        psi=d["psi_rad"]+offset
        rw=r*exp(im*psi).*a0
        cw=sqrt(eta).*aw.+sqrt(1-eta).*rw
        nc=weight*sum(abs2,cw)
        terminal=reshape(sqrt(eta)*weight.*cw,nt,1,1)
        adj=solve_adjoint(terminal,pars,dz;forward_solution=sol,units=:power,
            adjoint_mode=:discrete_rk4ip)
        g=vec(get_spectral_field(adj;units=:power))./sqrt(weight)
        f0=sum(abs2,g)/nc;ft=f0+1-eta
        push!(rows,Dict{String,Any}("phase_offset_rad"=>offset,"phase_rad"=>psi,"F_signal"=>f0,
            "F_reference_vacuum"=>1-eta,"F_total"=>ft,"output_power_mw"=>power_scale*sum(abs2,cw),
            "output_power_ratio"=>sum(abs2,cw)/sum(abs2,a0)))
        @printf("IDEAL_SECH_KERR tag=%s phaseoffset=%.9g F=%.12g Pout=%.12g\n",tag,offset,ft,power_scale*sum(abs2,cw));flush(stdout)
    end
    total_seconds=time()-started
    result=Dict{String,Any}("run_id"=>RUN_ID,"tag"=>tag,"nt"=>nt,"window_ps"=>window,"dz_m"=>dz,
        "dt_ps"=>p.grid.dt,
        "input_power_mw"=>power_scale*sum(abs2,a0),"input_photons"=>nin,
        "gamma_per_W_m"=>n2*p.pars.omega0/C_PS*spatial_overlap(ph.props)[1,1,1,1],
        "exact_soliton_mean_relative_field_error"=>mean_error,"photon_drift"=>ns/nin-1,
        "Q_optical"=>[collect(row) for row in eachrow(Q)],"readout"=>rows,
        "canonical_photon_weight_constant"=>weight,
        "forward_seconds"=>forward_seconds,"forward_plus_4_adjoints_seconds"=>total_seconds,
        "julia_threads"=>Threads.nthreads(),
        "classification"=>"Clean ideal-sech Kerr+beta2 Green-function control; not the prepared pulse and not a physical Raman prediction",
        "config_sha256"=>file_sha256(CONFIG),
        "lib_sha256"=>file_sha256(joinpath(@__DIR__,"lp01_archive_lib.jl")),
        "driver_sha256"=>file_sha256(@__FILE__))
    out=joinpath(RAW,tag)
    write_toml(joinpath(out,"full_control.toml"),result)
    npzwrite(joinpath(out,"full_control.npz"),Dict("t_ps"=>p.t,"omega_centered_rad_ps"=>p.omega,
        "input_a_w_sqrtW"=>a0,"output_a_w_sqrtW"=>aw,"Q_optical"=>Q,
        "photon_quadrature_gradients"=>G,"constant_photon_weight"=>weight))
    @printf("IDEAL_SECH_KERR_COMPLETE tag=%s Q11=%.12g Q12=%.12g Q22=%.12g meanerr=%.3g seconds=%.1f\n",tag,Q[1,1],Q[1,2],Q[2,2],mean_error,total_seconds);flush(stdout)
    result
end

if abspath(PROGRAM_FILE) == @__FILE__
    tags = isempty(ARGS) ? ["nominal"] : ARGS
    for tag in tags
        run_control(tag)
    end
end
