# lp01_archive_lib.jl -- shared helper for the claude-b.1 LP01 baseline runs (T-20261004-claude-interactive-06).
#
# Adapted by claude-b.1 on 2026-10-04 from the archive's Julia wrappers (read-only source,
# ~/Desktop/fall2026_research/ai driven lab work/research_runs/):
#   2026-09-23_squeezing/common.jl          raman_bath_spectrum, interp1, make_problem, measure
#   2026-09-23_squeezing/analytic_raman.jl  AnalyticRaman (exact Fourier Raman kernels)
#   2026-09-23_squeezing/raman_noise.jl     symmetric_raman_spectrum, scalar_raman_variance
#   2026-09-23_raman_reduction/design_common.jl  physics_at, make_design
#   2026-09-25_stepindex_lp01/common.jl     CATALOG (subset), diagnostics
# The numerical code is copied verbatim. The only changes are:
#   * input files are read from the archive by absolute path (never written);
#   * no results directory is created; drivers write raw output under ~/analytical-nl-discovery-data/<run-id>/;
#   * `physics` (multimode helper) and functions not used by these runs are omitted.
# The pinned solver (solver/ at 9c1288712ea9cd7ef858d4e6dff9dea350e9291a) has src/, ext/ and Manifest.toml
# byte-identical to the archive's `dossier/FastDifferentiableMMNLO for agents` copy, so no API change was needed.
ENV["MPLBACKEND"] = "Agg"
using PulsePropagation, FFTW, LinearAlgebra, DelimitedFiles, Statistics, Printf, TOML, NPZ, SHA
BLAS.set_num_threads(1)
FFTW.set_num_threads(1)
const PP = PulsePropagation
const C_PS = 2.99792458e-4
const H_SI = 6.62607015e-34
const E_SI = 1.602176634e-19
const REP = 80e6
const LAMBDA0 = 1550e-9
const ARCHIVE_RUNS = "~/Desktop/fall2026_research/ai driven lab work/research_runs"
const INPUTS = joinpath(ARCHIVE_RUNS, "2026-09-23_squeezing", "inputs")
const FILTER_DATA = readdlm(joinpath(INPUTS, "filter.csv"), ',', Float64; skipstart=1)

file_sha256(path) = bytes2hex(open(sha256, path))

# ---- 2026-09-23_squeezing/common.jl -------------------------------------------------------------
function raman_bath_spectrum(pr,prefactor;temperature_K=300.0)
    pr.ph.raman isa NoRaman && return zeros(pr.nt)
    kernels=PP._mmgnlse_raman_kernels(pr.pars)
    h=kernels.fraction.*(kernels.ha.+kernels.hb)
    omega=ifftshift(pr.omega).*1e12
    hbar=H_SI/(2pi);kb=1.380649e-23
    C=zeros(pr.nt)
    for k in eachindex(C)
        x=hbar*abs(omega[k])/(2kb*temperature_K)
        C[k]=iszero(x) ? 0.0 : hbar*pr.pars.omega0*1e12/prefactor*abs(imag(h[k]))/tanh(x)
    end
    # Im H ~ omega and coth ~ 1/omega: the thermal DC limit is finite.
    # It drops out of scalar number detection but matters for modal mixing.
    # The nearest bin approximates that limit to O((2pi/window)^2).
    C[1]=C[2]
    C
end

function interp1(x, y, q; outside=0.0)
    result = zeros(Float64, size(q))
    for i in eachindex(q)
        v = q[i]
        if !isfinite(v) || v < first(x) || v > last(x)
            result[i] = outside
        else
            j = clamp(searchsortedlast(x, v), 1, length(x)-1)
            u = (v-x[j])/(x[j+1]-x[j])
            result[i] = (1-u)*y[j]+u*y[j+1]
        end
    end
    result
end

function make_problem(ph; pin_mw=147.192696, nt=4096, window_ps=40.0,
                      length_m=20.0, fwhm_ps=0.2, chirp=0.0, gdd_ps2=0.0,
                      source="gaussian", area_scale=1.0, fractions=nothing, tod_ps3=0.0,
                      frame_ps_m=0.0)
    grid = TimeGrid(nt, window_ps)
    dom = MMGNLSEDomain(degrees_of_freedom(:time, :space), grid)
    beta = copy(hasproperty(ph,:beta_override) ? ph.beta_override : ph.props.beta.coefficients)
    beta[1,:] .-= beta[1,1]
    beta[2,:] .-= beta[2,1] + frame_ps_m
    S = (hasproperty(ph,:S_override) ? ph.S_override : spatial_overlap(ph.props)) ./ area_scale
    pars = MMGNLSEParameters(dom; length=length_m, beta=TaylorBeta(beta),
        S, n2=ph.material.n2, omega0=ph.props.omega0, raman=ph.raman)
    t = time_axis(grid)
    omega = frequency_axis(grid)
    lambda = wavelength_axis(grid, ph.props.omega0)
    weights = photon_weights(grid, ph.props.omega0)
    coeffs = fractions === nothing ? [i==1 ? 1.0 : 0.0 for i in 1:ph.nm] : sqrt.(complex.(fractions))
    coeffs ./= norm(coeffs)
    if source == "gaussian"
        u = exp.(-2log(2).*(t./fwhm_ps).^2 .*(1+im*chirp))
    elseif source == "sech"
        tau=fwhm_ps/(2acosh(sqrt(2)))
        u=sech.(t./tau).*exp.(im*chirp/2 .* (t./tau).^2)
    else
        d = readdlm(joinpath(INPUTS, "source_"*source*".csv"), ',', Float64; skipstart=1)
        # Uniform-lambda OSA bins: multiply by lambda^2 for density per frequency.
        spec = max.(interp1(d[:,1],d[:,2],lambda.*1e9),0.0) .* (lambda./LAMBDA0).^2
        spec[.!isfinite.(spec)] .= 0
        uw = sqrt.(spec) .* exp.(im.*(gdd_ps2/2 .* omega.^2 .+ tod_ps3/6 .* omega.^3))
        u = fftshift(fft(ifftshift(uw)))
    end
    if source in ("gaussian","sech") && (gdd_ps2 != 0 || tod_ps3 != 0)
        uw=fftshift(ifft(u)) .* exp.(im.*(gdd_ps2/2 .* omega.^2 .+ tod_ps3/6 .* omega.^3))
        u=fft(ifftshift(uw))
    end
    a = reshape(u,:,1,1) .* reshape(coeffs,1,:,1)
    energy = pin_mw*1e-3/REP
    a .*= sqrt(energy/(sum(abs2,a)*grid.dt*1e-12))
    T = clamp.(interp1(FILTER_DATA[:,1],FILTER_DATA[:,2],lambda.*1e9),0.0,1.0)
    (; ph, grid, pars, a, t, omega, lambda, weights, T, pin_mw, source,
       fwhm_ps, chirp, gdd_ps2, tod_ps3, area_scale, length_m, nt, window_ps)
end

function measure(pr, sol; calculate_noise=true, dz=0.01, save_adjoint=nothing)
    w=reshape(pr.weights,:,1,1)
    T=reshape(pr.T,:,1,1)
    aw=get_spectral_field(sol)
    n0=sum(w.*abs2.(fftshift(ifft(pr.a,1),1)))
    nf=sum(w.*abs2.(aw))
    obs=SpectralPhotonNumber(filter=vec(pr.T),modes=:all)
    meanN=value(obs,sol)
    partnoise=sum(w.*T.*(1 .- T).*abs2.(aw))
    var_initial=NaN
    adj=nothing
    adjtime=0.0
    if calculate_noise
        terminal=terminal_condition(obs,sol)
        adjtime=@elapsed adj=solve_adjoint(terminal,pr.pars,dz;
            forward_solution=sol,units=:photon,saveat=save_adjoint,
            adjoint_mode=:discrete_rk4ip)
        g=get_spectral_field(adj;units=:photon)
        var_initial=sum(abs2,g)
    end
    F=(var_initial+partnoise)/meanN
    qe=1.2*H_SI*2.99792458e8/(E_SI*LAMBDA0)
    eta3=10.0^(-3/10)*0.95*0.87*qe
    eta10=0.1*0.95*0.87*qe
    F3=1+eta3*(F-1)
    F10=1+eta10*(F-1)
    Epass=sum(abs2.(aw).*T)*pr.nt*pr.grid.dt*1e-12
    Eout=sum(abs2,aw)*pr.nt*pr.grid.dt*1e-12
    at=get_temporal_field(sol)
    edge=round(Int,pr.nt*0.05)
    edgefrac=(sum(abs2,at[1:edge,:,:])+sum(abs2,at[end-edge+1:end,:,:]))/sum(abs2,at)
    input_power=vec(sum(abs2.(pr.a);dims=(2,3)))
    halfmax=findall(input_power .>= maximum(input_power)/2)
    input_fwhm=(last(halfmax)-first(halfmax))*pr.grid.dt
    tbar=sum(pr.t.*input_power)/sum(input_power)
    input_rms=sqrt(sum((pr.t.-tbar).^2 .*input_power)/sum(input_power))
    result=Dict{String,Any}("pin_mw"=>pr.pin_mw,"length_m"=>pr.length_m,
        "source"=>pr.source,"fwhm_ps"=>pr.fwhm_ps,"chirp"=>pr.chirp,
        "gdd_ps2"=>pr.gdd_ps2,"tod_ps3"=>pr.tod_ps3,"area_scale"=>pr.area_scale,
        "nt"=>pr.nt,"window_ps"=>pr.window_ps,"dz"=>dz,
        "mode_count"=>pr.ph.nm,
        "input_fwhm_measured_on_grid_ps"=>input_fwhm,"input_rms_ps"=>input_rms,
        "input_peak_W"=>maximum(input_power),
        "F_filter"=>F,"F_3dB"=>F3,"F_10dB"=>F10,
        "dB_3"=>10log10(F3),"dB_10"=>10log10(F10),
        "spectral_transmission"=>Epass/Eout,
        "detected_power_mw"=>Epass*REP*1e3*0.95*0.87*10.0^(-3/10),
        "photon_drift"=>nf/n0-1,"temporal_edge_fraction"=>edgefrac,
        "initial_variance"=>var_initial,"filter_vacuum_variance"=>partnoise,
        "mean_photons_after_filter"=>meanN,"adjoint_seconds"=>adjtime,
        "quantum_efficiency"=>qe,"eta3_uniform_spatial"=>eta3)
    return result,adj
end

# ---- 2026-09-23_squeezing/analytic_raman.jl ------------------------------------------------------
# Exact Fourier response of the same causal Raman kernels. This extension
# affects only our custom response type and leaves the original package intact.
struct AnalyticRaman{R} <: PP.AbstractRamanResponse
    base::R
    fraction::Float64
end
AnalyticRaman(r)=AnalyticRaman(r,Float64(r.fraction))

function PP._mmgnlse_raman_kernels(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:AnalyticRaman}
    r=p.raman.base
    grid=p.domain.time_grid
    omega=PP.ifft_frequency_grid(grid.nt,grid.dt)
    a=1/r.tau2 .- im.*omega
    oscillator=(1/r.tau1^2+1/r.tau2^2)./(a.^2 .+1/r.tau1^2)
    if r isa AgarwalRaman
        ha=oscillator;hb=zeros(ComplexF64,grid.nt)
    else
        ab=1/r.taub .- im.*omega
        boson=2 ./ (r.taub.*ab) .-1 ./ (r.taub^2 .* ab.^2)
        ha=r.fa.*oscillator
        hb=r.fc.*oscillator.+r.fb.*boson
    end
    # The discrete Nyquist bin is its own conjugate; it must be real.
    if iseven(grid.nt)
        k=grid.nt÷2+1
        ha[k]=real(ha[k]);hb[k]=real(hb[k])
    end
    (;ha=ComplexF64.(ha),hb=ComplexF64.(hb),fraction=p.raman.fraction)
end

analytic_physics(ph)=merge(ph,(raman=AnalyticRaman(ph.raman),))

# ---- 2026-09-23_squeezing/raman_noise.jl ----------------------------------------------------------
# Scalar, linearized Wigner Raman reservoir. See Drummond & Corney,
# JOSA B 18, 139 (2001), Eqs. (6.11),(6.16): 2 Im(H)*(n_th+1/2).
function symmetric_raman_spectrum(pr; temperature_K=300.0)
    gamma=pr.pars.n2*pr.pars.omega0/C_PS*spatial_overlap(pr.ph.props)[1,1,1,1]/pr.area_scale
    return raman_bath_spectrum(pr,gamma;temperature_K),gamma
end

function scalar_raman_variance(pr,sol,adj;temperature_K=300.0)
    pr.ph.nm==1 || error("Scalar Raman contraction requires one spatial mode.")
    C,gamma=symmetric_raman_spectrum(pr;temperature_K)
    z=Float64.(adj.z)
    all(isapprox.(z,sol.z;atol=1e-10)) || error("Forward/adjoint saved planes must match.")
    at=get_temporal_field(sol;z=:all,units=:power)
    lw=get_spectral_field(adj;z=:all,units=:power)
    # Apply the adjoint of the same self-steepening operator as the mean PDE.
    damp=fftshift(PP.damped_freq_window(pr.nt))
    shock=(1 .+ pr.omega./pr.pars.omega0).*damp
    lt=fft(ifftshift(lw.*reshape(shock,:,1,1,1),1),1)
    B=-2 .* imag.(at.*conj.(lt)) ./ pr.nt
    Bw=fft(B,1)
    df=1/(pr.nt*pr.grid.dt)*1e12
    integrand=vec(sum(reshape(C,:,1,1,1).*abs2.(Bw);dims=(1,2,3))).*(gamma^2*df)
    variance=sum(diff(z).*(integrand[1:end-1].+integrand[2:end])./2)
    return variance,integrand
end

# ---- 2026-09-23_raman_reduction/design_common.jl --------------------------------------------------
function physics_at(wavelength_nm;raman_kind="agarwal")
    fiber=GRIN(wavelength_nm*1e-9,31.25e-6,0.275)
    raman=raman_kind=="anisotropic" ? AnisotropicRaman() : AgarwalRaman()
    material=Silica(;n2=2.3e-20,raman)
    props=compute_fiber_properties(fiber,material,1;mode_basis=:LP,beta_order=5,grid_size=65)
    analytic_physics((;fiber,material,props,raman,nm=1))
end

function make_design(ph;wavelength_nm=1550.0,pin_mw=146.0,length_m=20.0,
                     nt=4096,window_ps=40.0,gdd_ps2=-0.015,
                     prefilter_width_nm=Inf,prefilter_center_nm=1550.0,
                     output_width_scale=1.0,output_offset_nm=0.0,
                     power_before_prefilter=false,output_filter_fixed_lab=false,fractions=nothing)
    pr=make_problem(ph;source="100mw",gdd_ps2,pin_mw,length_m,nt,window_ps,fractions)
    # At another carrier retain the same spectral density versus frequency
    # detuning as a controlled comparison, not as a measured OPO spectrum.
    oldomega0=2pi*C_PS/LAMBDA0
    oldlambda=2pi*C_PS./(oldomega0 .+pr.omega).*1e9
    d=readdlm(joinpath(INPUTS,"source_100mw.csv"),',',Float64;skipstart=1)
    spec=max.(interp1(d[:,1],d[:,2],oldlambda),0.0).*(oldlambda./1550.0).^2
    spec[.!isfinite.(spec)].=0
    preT=isfinite(prefilter_width_nm) ? exp.(-4log(2).*((oldlambda.-prefilter_center_nm)./prefilter_width_nm).^2) : ones(nt)
    throughput=sum(spec.*preT)/sum(spec)
    uw=sqrt.(spec.*preT).*exp.(im*gdd_ps2/2 .*pr.omega.^2)
    coeff=fractions===nothing ? ComplexF64[i==1 ? 1.0 : 0.0 for i in 1:ph.nm] : sqrt.(complex.(fractions))
    coeff./=norm(coeff)
    a=reshape(fftshift(fft(ifftshift(uw))),nt,1,1).*reshape(coeff,1,ph.nm,1)
    actual_pin=power_before_prefilter ? pin_mw*throughput : pin_mw
    a .*=sqrt(actual_pin*1e-3/REP/(sum(abs2,a)*pr.grid.dt*1e-12))
    querylambda=output_filter_fixed_lab ? pr.lambda.*1e9 : 1550 .+(oldlambda.-1550 .-output_offset_nm)./output_width_scale
    T=clamp.(interp1(FILTER_DATA[:,1],FILTER_DATA[:,2],querylambda),0.0,1.0)
    merge(pr,(;a,T,pin_mw=actual_pin,wavelength_nm,prefilter_width_nm,prefilter_center_nm,
        prefilter_throughput=throughput,output_width_scale,output_offset_nm,output_filter_fixed_lab,
        coupled_equivalent_power_before_prefilter_mw=actual_pin/throughput))
end

# ---- 2026-09-25_stepindex_lp01/common.jl (subset) -------------------------------------------------
const CATALOG=Dict(
    "FG025LJA"=>(diameter_um=25.,na=.10,min_nm=700.,max_nm=1400.),
    "FG050LGA"=>(diameter_um=50.,na=.22,min_nm=400.,max_nm=2400.),
    "LMA20"=>(diameter_um=20.,na=.08,min_nm=1060.,max_nm=1600.),
    "LMA25"=>(diameter_um=25.,na=.065,min_nm=1060.,max_nm=1600.))

function diagnostics(pr,sol;T=ones(pr.nt))
    aw=get_spectral_field(sol);w=reshape(pr.weights,:,1,1)
    ni=sum(w.*abs2.(fftshift(ifft(pr.a,1),1)));nf=sum(w.*abs2.(aw))
    at=get_temporal_field(sol)
    af=fft(ifftshift(aw.*reshape(sqrt.(T),:,1,1),1),1)
    inp=vec(sum(abs2.(pr.a);dims=(2,3)))
    out=vec(sum(abs2.(at);dims=(2,3)))
    selected=vec(sum(abs2.(af);dims=(2,3)))
    edge=round(Int,pr.nt*.05)
    awpower=vec(sum(abs2.(aw);dims=(2,3)))
    half=findall(inp.>=maximum(inp)/2)
    totalP=sum(awpower)*pr.nt*pr.grid.dt*1e-12*REP*1e3
    passP=sum(awpower.*T)*pr.nt*pr.grid.dt*1e-12*REP*1e3
    spec=get(CATALOG,pr.ph.fiber_name,(min_nm=0.,max_nm=Inf))
    outside=(pr.lambda.*1e9 .< spec.min_nm).|(pr.lambda.*1e9 .> spec.max_nm)
    Dict{String,Any}("pin_mw"=>pr.pin_mw,"wavelength_nm"=>pr.wavelength_nm,
        "length_m"=>pr.length_m,"nt"=>pr.nt,"window_ps"=>pr.window_ps,
        "gdd_ps2"=>pr.gdd_ps2,"mode_count"=>pr.ph.nm,
        "input_peak_W"=>maximum(inp),"fiber_output_peak_W"=>maximum(out),
        "selected_output_peak_W"=>maximum(selected),
        "selected_energy_over_peak_ps"=>sum(selected)*pr.grid.dt/maximum(selected),
        "input_fwhm_ps"=>(last(half)-first(half))*pr.grid.dt,
        "fiber_output_power_mw"=>totalP,"selected_output_power_mw"=>passP,
        "spectral_power_transmission"=>passP/totalP,
        "power_fraction_outside_vendor_range"=>sum(awpower[outside])/sum(awpower),
        "photon_drift"=>nf/ni-1,
        "temporal_edge_fraction"=>(sum(out[1:edge])+sum(out[end-edge+1:end]))/sum(out),
        "spectral_edge_fraction"=>(sum(awpower[1:edge])+sum(awpower[end-edge+1:end]))/sum(awpower),
        "beta2_ps2_km"=>pr.ph.props.beta.coefficients[3,1]*1000,
        "gamma_LP01_W_km"=>pr.pars.n2*pr.pars.omega0/C_PS*spatial_overlap(pr.ph.props)[1,1,1,1]*1000,
        "response"=>string(typeof(pr.ph.raman)),"temperature_K"=>300.0,
        "fiber_name"=>pr.ph.fiber_name,"effective_area_um2"=>1e12/spatial_overlap(pr.ph.props)[1,1,1,1])
end

# ---- run bookkeeping (new) ------------------------------------------------------------------------
function write_toml(path, d)
    mkpath(dirname(path))
    open(path, "w") do io
        TOML.print(io, d)
    end
end
