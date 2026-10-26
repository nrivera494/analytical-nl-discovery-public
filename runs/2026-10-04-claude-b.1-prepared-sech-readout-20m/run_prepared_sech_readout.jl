# Driver for run 2026-10-04-claude-b.1-prepared-sech-readout-20m.
# Adapted from archive research_runs/2026-09-26_analytics/simulations/validate_prepared_sech_readout.jl
# (sha256 f4cbbf737f0eafc1bbff14d22c706c8e4672148e5ae2afc3316f5928e5cc2f22) and run_prepared_sech_validation.jl
# (sha256 ac94b0d40e549d6f3be3d012b450795f334e7e712d36438c6b77b35981ed80e3).
# Numerical steps are unchanged. Changes: settings come from config.toml; the frozen-forecast manifest check is
# dropped (it only hashed an archive file); output goes to the raw-data folder; a "wide" case zero-pads the input in
# time to an 80 ps window at the same sample spacing.
#
# Usage: JULIA_NUM_THREADS=2 julia --project=solver run_prepared_sech_readout.jl [kind:tag ...]
#        (no arguments: all cases in config.toml, in order)
include(joinpath(@__DIR__, "lp01_archive_lib.jl"))
const RUN_ID = "2026-10-04-claude-b.1-prepared-sech-readout-20m"
const RAW = joinpath(homedir(), "analytical-nl-discovery-data", RUN_ID)
const CONFIG = joinpath(@__DIR__, "config.toml")
const CFG = TOML.parsefile(CONFIG)
const SET = CFG["setting"]
const PIN = Float64(SET["signal_input_power_mW"])
const LENGTH = Float64(SET["length_m"])
const ETA = Float64(SET["eta"])
const R = Float64(SET["reference_amplitude_ratio"])
const PHI = Float64(SET["reference_phase_rad"])
const KEYS = ["a_w_sqrtW_per_sqrt_mW", "a_t_sqrtW_per_sqrt_mW", "t_ps", "dt_ps", "passive_throughput", "fidelity"]

function load_prepared()
    f = CFG["input_field"]
    prep = try
        npzread(f["path"], KEYS)
    catch e
        @warn "Could not read the results/ npz with NPZ.jl; using the archive's numeric copy" exception=e
        nothing
    end
    if prep === nothing
        path = f["fallback_path"]; expected = f["fallback_sha256"]
        prep = npzread(path, KEYS)
    else
        path = f["path"]; expected = f["sha256"]
    end
    got = file_sha256(path)
    got == expected || error("Input field sha256 mismatch: $got != $expected")
    prep, path
end
const PREP, PREP_PATH = load_prepared()

function power_mw(p,aw)
    p.nt*p.grid.dt*1e-12*REP*1e3*sum(abs2,aw)
end

function problem(kind;nt=4096,window=40.,pin=PIN)
    ph=merge(physics_at(1550.;raman_kind=kind),(fiber_name="GIF625",))
    p=make_design(ph;wavelength_nm=1550.,pin_mw=pin,length_m=LENGTH,
        nt,window_ps=window,gdd_ps2=0.)
    awbase=PREP["a_w_sqrtW_per_sqrt_mW"]
    ntbase=length(awbase);dtbase=Float64(PREP["dt_ps"])
    if window == ntbase*dtbase
        # Archive path: resample the exact frozen periodic field by preserving its spectral
        # amplitudes at matching detunings. Nt increases extend the zero tail.
        @assert nt>=ntbase && iseven(nt-ntbase)
        aw=zeros(ComplexF64,nt);pad=div(nt-ntbase,2)
        aw[pad+1:pad+ntbase].=awbase
        a=reshape(fft(ifftshift(aw)),nt,1,1).*sqrt(pin)
        @assert isapprox(power_mw(p,aw.*sqrt(pin)),pin;rtol=2e-13)
        if nt==ntbase
            @assert norm(vec(a)./sqrt(pin)-PREP["a_t_sqrtW_per_sqrt_mW"])/norm(PREP["a_t_sqrtW_per_sqrt_mW"])<1e-13
            @assert maximum(abs.(p.t-PREP["t_ps"]))<1e-12
        end
    else
        # New "wide" path: same time samples, zero-padded window (same dt).
        @assert isapprox(window/nt, dtbase; rtol=1e-14) && iseven(nt-ntbase)
        pad=div(nt-ntbase,2)
        @assert maximum(abs.(p.t[pad+1:pad+ntbase]-PREP["t_ps"]))<1e-12
        at=zeros(ComplexF64,nt);at[pad+1:pad+ntbase].=PREP["a_t_sqrtW_per_sqrt_mW"]
        a=reshape(at,nt,1,1).*sqrt(pin)
        aw=vec(fftshift(ifft(a,1),1))
        @assert isapprox(power_mw(p,aw),pin;rtol=1e-12)
    end
    merge(p,(a=a,T=ones(nt),source="frozen_passive_sech_preparation",fwhm_ps=.4))
end

function mean_detected(p,aw,rw)
    cw=sqrt(ETA).*aw.+sqrt(1-ETA).*rw
    cw,sum(p.weights.*abs2.(cw))
end

function run_case(kind;nt=4096,window=40.,dz=.01,zspacing=.05,tag="standard",validate_derivative=true,
    reference_blocked_check=(tag=="standard"),pin=PIN)
    p=problem(kind;nt,window,pin)
    aw0=vec(fftshift(ifft(p.a,1),1))
    rw=R*exp(im*PHI).*aw0
    nin=sum(p.weights.*abs2.(aw0));nref=sum(p.weights.*abs2.(rw))
    elapsed=@elapsed begin
        sol=solve_mmgnlse(p.a,p.pars,dz;saveat=zspacing)
        aw=vec(get_spectral_field(sol))
        cw,nout=mean_detected(p,aw,rw)
        terminal=reshape(sqrt(ETA).*p.weights.*cw,p.nt,1,1)
        adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,
            saveat=zspacing,adjoint_mode=:discrete_rk4ip)
        g=vec(get_spectral_field(adj;units=:photon))
        vin=sum(abs2,g)
        vr,integrand=scalar_raman_variance(p,sol,adj;temperature_K=Float64(SET["temperature_K"]))
    end
    vref=(1-ETA)*nout
    b=sqrt.(p.weights).*aw0
    amplitude=real(dot(g,b./sqrt(nin)))
    phaseamplitude=real(dot(g,im.*b./sqrt(nin)))
    exact_dndn=amplitude/sqrt(nin)
    fd=NaN
    if validate_derivative
        epsilon=.0005;vals=Float64[]
        for scale in (1-epsilon,1+epsilon)
            ss=solve_mmgnlse(p.a.*sqrt(scale),p.pars,dz)
            _,nn=mean_detected(p,vec(get_spectral_field(ss)),rw)
            push!(vals,nn)
        end
        fd=(vals[2]-vals[1])/(2epsilon*nin)
    end
    d=diagnostics(p,sol;T=p.T)
    if reference_blocked_check
        # The same nonlinear signal with a blocked coherent reference must give
        # Poisson total-number statistics: Kerr/Raman conserve all-band photons.
        cn=sqrt(ETA).*aw;nn=sum(p.weights.*abs2.(cn))
        tn=reshape(sqrt(ETA).*p.weights.*cn,p.nt,1,1)
        an=solve_adjoint(tn,p.pars,dz;forward_solution=sol,units=:power,
            saveat=zspacing,adjoint_mode=:discrete_rk4ip)
        vn=sum(abs2,get_spectral_field(an;units=:photon))
        vrn,_=scalar_raman_variance(p,sol,an;temperature_K=Float64(SET["temperature_K"]))
        d["reference_blocked_F_total"]=(vn+vrn)/nn+(1-ETA)
        d["reference_blocked_F_Raman"]=vrn/nn
    end
    throughput=Float64(PREP["passive_throughput"])
    merge!(d,Dict{String,Any}("run_id"=>RUN_ID,
        "response_kind"=>kind,"tag"=>tag,"signal_input_power_mw"=>pin,
        "reference_power_mw"=>power_mw(p,rw),"source_power_required_both_arms_mw"=>2*(pin+power_mw(p,rw))/throughput,
        "preparation_passive_throughput"=>throughput,"preparation_fidelity"=>Float64(PREP["fidelity"]),
        "signal_beamsplitter_transmission"=>ETA,"reference_amplitude_ratio"=>R,"reference_phase_rad"=>PHI,
        "fiber_length_m"=>LENGTH,"readout_output_power_mw"=>power_mw(p,cw),
        "input_signal_photons"=>nin,"input_reference_photons"=>nref,"readout_output_photons"=>nout,
        "F_signal_input"=>vin/nout,"F_Raman"=>vr/nout,"F_reference_vacuum"=>vref/nout,
        "F_total"=>(vin+vr+vref)/nout,"F_total_dB"=>10log10((vin+vr+vref)/nout),
        "F_signal_bright_amplitude"=>amplitude^2/nout,
        "F_signal_bright_phase"=>phaseamplitude^2/nout,
        "F_signal_orthogonal_both_quadratures"=>(vin-amplitude^2-phaseamplitude^2)/nout,
        "dNout_dNsignal_reference_held_fixed_adjoint"=>exact_dndn,
        "dNout_dNsignal_reference_held_fixed_finite_difference"=>fd,
        "finite_difference_relative_pin_step"=>.0005,
        "dz_m"=>dz,"raman_z_spacing_m"=>zspacing,"elapsed_seconds"=>elapsed,
        "input_field_path"=>PREP_PATH,"input_field_sha256"=>file_sha256(PREP_PATH),
        "julia_threads"=>Threads.nthreads(),
        "config_sha256"=>file_sha256(CONFIG),
        "lib_sha256"=>file_sha256(joinpath(@__DIR__,"lp01_archive_lib.jl")),
        "driver_sha256"=>file_sha256(@__FILE__),
        "terminal_definition"=>"C=sqrt(eta)*Aout+sqrt(1-eta)*r*exp(i*phi)*Ain; gL_power=sqrt(eta)*w*C",
        "reference_definition"=>"Coherent copy of the frozen prepared INPUT waveform, bypassing the fiber, same spectral phase except the fixed scalar phi; independent coherent vacuum, no output-waveform shaping",
        "observable"=>"Total output photon number in one beamsplitter port, all temporal/spectral modes, full spatial LP01 collection, no output bandpass",
        "implementation"=>"Archive mean+discrete adjoint including beta0..5, shock and exact Raman kernels; scalar reservoir contraction with custom terminal"))
    name=kind*"_"*tag
    write_toml(joinpath(RAW,name*".toml"),d)
    npzwrite(joinpath(RAW,name*".npz"),Dict("t_ps"=>p.t,"omega_centered_rad_ps"=>p.omega,
        "photon_weight"=>p.weights,"input_signal_a_w_sqrtW"=>aw0,"input_reference_a_w_sqrtW"=>rw,
        "fiber_output_a_w_sqrtW"=>aw,"readout_output_a_w_sqrtW"=>cw,
        "signal_input_adjoint_g_w_photon"=>g,"terminal_g_w_power"=>vec(terminal),
        "z_m"=>Float64.(sol.z),"Raman_variance_integrand_per_m"=>integrand))
    @printf("SECH_READOUT %s F=%.12g dB=%.7g Fin=%.9g FR=%.9g Fref=%.9g Pout=%.9g Psource=%.9g derivative=%.9g fd=%.9g seconds=%.1f\n",
        name,d["F_total"],d["F_total_dB"],d["F_signal_input"],d["F_Raman"],d["F_reference_vacuum"],
        d["readout_output_power_mw"],d["source_power_required_both_arms_mw"],exact_dndn,fd,elapsed)
    if haskey(d,"reference_blocked_F_total")
        @printf("SECH_READOUT %s reference_blocked_F=%.15g reference_blocked_FR=%.3g\n",name,d["reference_blocked_F_total"],d["reference_blocked_F_Raman"])
    end
    flush(stdout)
    d
end

function linear_control(;nt=4096,window=40.,dz=.01)
    p0=problem("agarwal";nt,window)
    q=p0.pars
    pars=MMGNLSEParameters(q.domain;length=q.length,beta=q.beta,S=q.S,
        n2=0.,omega0=q.omega0,raman=NoRaman())
    p=merge(p0,(pars=pars,))
    elapsed=@elapsed begin
        sol=solve_mmgnlse(p.a,p.pars,dz)
        aw=vec(get_spectral_field(sol));a0=vec(fftshift(ifft(p.a,1),1))
        rw=R*exp(im*PHI).*a0;cw,nout=mean_detected(p,aw,rw)
        terminal=reshape(sqrt(ETA).*p.weights.*cw,p.nt,1,1)
        adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,
            adjoint_mode=:discrete_rk4ip)
        vi=sum(abs2,get_spectral_field(adj;units=:photon))
    end
    result=Dict{String,Any}("run_id"=>RUN_ID,"tag"=>"linear_control","F_signal"=>vi/nout,"F_reference_vacuum"=>1-ETA,
        "F_total"=>vi/nout+1-ETA,"expected_F"=>1.,"elapsed_seconds"=>elapsed,"nt"=>nt,"window_ps"=>window,"dz_m"=>dz,
        "description"=>"Full beta0..5 dispersive mean/adjoint, same two coherent input ports and fixed readout, n2=0; F must equal 1 independent of mismatch/interference")
    write_toml(joinpath(RAW,"agarwal_linear_control.toml"),result)
    @printf("SECH_LINEAR_CONTROL F=%.15g signal=%.15g ref=%.12g\n",result["F_total"],result["F_signal"],1-ETA)
    flush(stdout)
    result
end

function run_all(selection)
    println("SECH_DIRECT_VALIDATION_STARTED input=", PREP_PATH);flush(stdout)
    for c in CFG["cases"]
        key = c["kind"]*":"*c["tag"]
        (isempty(selection) || key in selection) || continue
        if c["tag"] == "linear_control"
            linear_control(;nt=c["nt"],window=Float64(c["window_ps"]),dz=Float64(c["dz_m"]))
        else
            run_case(c["kind"];nt=c["nt"],window=Float64(c["window_ps"]),dz=Float64(c["dz_m"]),
                zspacing=Float64(c["raman_z_spacing_m"]),tag=c["tag"],
                validate_derivative=c["validate_derivative"],reference_blocked_check=c["reference_blocked_check"])
        end
    end
    println("SECH_DIRECT_VALIDATION_COMPLETE");flush(stdout)
end

if abspath(PROGRAM_FILE) == @__FILE__
    run_all(ARGS)
end
