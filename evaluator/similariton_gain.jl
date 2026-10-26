# agent: gpt-a; model: gpt-6-astra; family: gpt
# T-20261008-gpt-a-01. Deterministic scalar gain-NLSE evaluator.
# Uses the pinned solver's actual gain propagator and RK4IP stages. Its cache
# prefactor is explicitly constant i*gamma: no shock and no spectral damping.
# The solver checkout/source is not modified.
using PulsePropagation, FFTW, LinearAlgebra, TOML, NPZ, Printf
const PP = PulsePropagation
BLAS.set_num_threads(1)
FFTW.set_num_threads(1)

function initial_pulse(t, shape, width, chirp, beta; order=4, smooth=0.02)
    # All shapes have mass 4/3. Gaussian/sech/super-Gaussian inputs have
    # sqrt(5)*rms duration = width. For soft-edge parabolic/odd inputs, width
    # is the nominal shape scale; the actual rms width is in the first row.
    if shape == "gaussian"
        a = width * sqrt(2/5)
        f = exp.(-(t./a).^2)
    elseif shape == "sech"
        a = width * sqrt(12/5)/pi
        f = 1 ./ cosh.(t./a).^2
    elseif shape == "supergaussian"
        # Quadrature fixes scale without an extra SpecialFunctions dependency.
        y = collect(range(-4.,4.,length=20001))
        v = exp.(-y.^(2order))
        ratio = sum(y.^2 .*v)/sum(v)
        a = width/sqrt(5ratio)
        f = exp.(-(t./a).^(2order))
    elseif shape == "parabola" || shape == "odd"
        # Smooth physical-vacuum edge, preserving positivity in the wings.
        a = width
        y = 1 .-(t./a).^2
        f = smooth .* (max.(y./smooth,0.) .+ log1p.(exp.(-abs.(y./smooth))))
        shape == "odd" && (f .*= tanh.(t./(0.08width)).^2)
    else
        error("unknown shape $shape")
    end
    dt=t[2]-t[1]
    f .*= (4/3)/(sum(f)*dt)
    field = sqrt.(f).*exp.(-0.5im*chirp.*t.^2/beta)
    shape == "odd" && (field .*= sign.(t))
    # N0 uses the analytic shape scale a and the actual sampled peak power.
    (;field, scale=a, peak=maximum(f))
end

function measure(field,t,omega,z,beta,e0)
    dt=t[2]-t[1]; I=abs2.(field); E=sum(I)*dt
    b=exp(z/3); P=exp(2z/3)
    x=t./b; target=max.(1 .-x.^2,0.)
    center=sum(t.*I)*dt/E
    tc=t.-center
    sigma2=sum(tc.^2 .*I)*dt/E
    spectrum=ifft(field)
    derivative=fft((-1im.*omega).*spectrum)
    current=-beta.*imag.(conj.(field).*derivative)
    meanv=sum(current)*dt/E
    qm=sum(tc.*current)*dt/(E*sigma2)
    relcurrent=current .-I.*t./3
    velocity_error=sqrt(sum(abs2.(relcurrent)./(I.+1e-30))*dt/E)/b
    core=(abs.(x).<0.8).&(I.>1e-12P)
    u=relcurrent[core]./I[core]./b
    core_error=sqrt(sum(I[core].*u.^2)*dt/E)
    ideal=sqrt.(P.*target).*exp.(-1im.*t.^2/(6beta))
    Ei=sum(abs2,ideal)*dt
    overlap=abs(dot(ideal,field))*dt/sqrt(E*Ei)
    Dict{String,Any}(
        "gain_length"=>z,"mass_relative_error"=>E/(e0*exp(z))-1,
        "width_ratio"=>sqrt(5sigma2)/b,"chirp_ratio"=>3qm,
        "centroid_scaled"=>center/b,"mean_velocity"=>meanv,
        "density_l1"=>sum(abs.(I.-P.*target))*dt/E,
        "density_l2_relative"=>sqrt(sum((I./P.-target).^2)/sum(target.^2)),
        "scaled_velocity_rms"=>velocity_error,"core_scaled_velocity_rms"=>core_error,
        "wing_mass_fraction"=>sum(I[abs.(x).>1])*dt/E,
        "time_guard_fraction"=>sum(I[abs.(t).>0.85maximum(abs,t)])*dt/E,
        "frequency_guard_fraction"=>sum(abs2,spectrum[abs.(omega).>0.8maximum(abs,omega)])/sum(abs2,spectrum),
        "even_parabolic_field_overlap"=>overlap,
        "peak_scaled_density"=>maximum(I)/P,
        "central_scaled_density"=>I[argmin(abs.(t))]/P)
end

function run_case(c, defaults, raw)
    getc(key,fallback)=get(c,key,get(defaults,key,fallback))
    label=c["label"]; Nstar=Float64(getc("Nstar",10.))
    beta=1/(sqrt(18)*Nstar); gamma=Nstar/sqrt(18)
    nt=Int(getc("nt",8192)); window=Float64(getc("window",64.))
    length=Float64(getc("length",6.)); dzmax=Float64(getc("dzmax",0.005))
    phase_step=Float64(getc("phase_step",0.04)); save_interval=Float64(getc("save_interval",0.1))
    shape=getc("shape","gaussian"); width=Float64(getc("width",1.))
    chirp=Float64(getc("chirp",0.)); order=Int(getc("order",4))
    smooth=Float64(getc("smooth",0.02))
    gain=Float64(getc("gain",1.)); nonlinear=Bool(getc("nonlinear",true))
    nonlinear || (gamma=0.)
    grid=TimeGrid(nt,window)
    domain=MMGNLSEDomain(degrees_of_freedom(:time),grid)
    t=time_axis(grid)
    initial=initial_pulse(t,shape,width,chirp,beta;order,smooth)
    carrier=1200.; lightspeed=2.99792458e-4
    p=MMGNLSEParameters(domain;length,alpha=0.,gain,
        beta=TaylorBeta([0.,0.,beta]),S=1.,n2=gamma*lightspeed/carrier,
        omega0=carrier,raman=NoRaman())
    base=PP._mmgnlse_solver_cache(p)
    cache=merge(base,(nonlinear_prefactor=fill(ComplexF64(0,gamma),nt,1,1),
                     nonlinear_active=!iszero(gamma)))
    omega=PP._mmgnlse_raw_omega(p)
    field=initial.field; fw=ifft(reshape(field,nt,1,1),1)
    e0=sum(abs2,field)*grid.dt
    rows=Dict{String,Any}[measure(field,t,omega,0.,beta,e0)]
    savez=collect(0.:save_interval:length)
    last(savez)<length-1e-10 && push!(savez,length)
    snapshots=Vector{ComplexF64}[copy(field)]; snapz=[0.]
    z=0.; steps=0; maxmass=0.; mingrid=Inf
    elapsed=@elapsed begin
        for target in savez[2:end]
            while z<target-1e-12
                # The step schedule is explicit and recorded; its coefficient
                # is halved for convergence. No error-estimator claim is made.
                peak=maximum(abs2,field)
                h=min(dzmax,phase_step/max(gamma*peak,1e-30),target-z)
                fw=PP._mmgnlse_rk4ip_step(fw,p,z,z+h,cache)
                z+=h; steps+=1; mingrid=min(mingrid,h)
                field=vec(fft(fw,1))
            end
            row=measure(field,t,omega,target,beta,e0)
            push!(rows,row); maxmass=max(maxmass,abs(row["mass_relative_error"]))
            if abs(target/2-round(target/2))<1e-8 || target==length
                push!(snapshots,copy(field));push!(snapz,target)
            end
        end
    end
    result=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
        "label"=>label,"method"=>"solver RK4IP with constant Kerr cache",
        "shape"=>shape,"width"=>width,"chirp"=>chirp,"order"=>order,"smooth"=>smooth,
        "Nstar"=>Nstar,"N0"=>sqrt(gamma*initial.peak*initial.scale^2/beta),
        "input_peak"=>initial.peak,"input_shape_scale"=>initial.scale,
        "nt"=>nt,"window"=>window,"length"=>length,"dzmax"=>dzmax,
        "phase_step"=>phase_step,"steps"=>steps,"smallest_step"=>mingrid,
        "beta2"=>beta,"gamma"=>gamma,"gain"=>gain,"elapsed_seconds"=>elapsed,
        "maximum_mass_error"=>maxmass,"rows"=>rows)
    mkpath(raw)
    open(joinpath(raw,label*".toml"),"w") do io; TOML.print(io,result);end
    npzwrite(joinpath(raw,label*".npz"),Dict("t"=>collect(t),"z"=>snapz,"fields"=>hcat(snapshots...)))
    final=last(rows)
    @printf("%s: steps=%d seconds=%.2f mass=%.3g L1=%.4g width=%.6f chirp=%.6f guard=(%.2g,%.2g)\n",
       label,steps,elapsed,maxmass,final["density_l1"],final["width_ratio"],final["chirp_ratio"],
       final["time_guard_fraction"],final["frequency_guard_fraction"]);flush(stdout)
    GC.gc()
    result
end

function main()
    config=TOML.parsefile(ARGS[1]); raw=config["raw_location"]
    defaults=get(config,"defaults",Dict{String,Any}())
    for c in config["cases"]
        run_case(c,defaults,raw)
    end
end
abspath(PROGRAM_FILE)==(@__FILE__) && main()
