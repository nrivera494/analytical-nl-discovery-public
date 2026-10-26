# agent: gpt-a; model: gpt-6-astra; family: gpt
# T-20261008-gpt-a-01. Independent Fourier Strang solver of the exact lens
# transformation of the gain NLSE. No PulsePropagation integration stages used.
include("similariton_gain.jl")

function refine_periodic_field(f,n)
    n0=length(f); n>=n0 && iseven(n) && iseven(n0) || error("Only even-grid spectral refinement is supported")
    n==n0 && return copy(f)
    fw=ifft(f); out=zeros(ComplexF64,n); nh=div(n0,2)
    out[1:nh].=fw[1:nh]; out[end-nh+1:end].=fw[nh+1:end]
    fft(out)
end

function lens_measure(f,x,omega,t,Nstar)
    dx=x[2]-x[1]; R=abs2.(f); E=sum(R)*dx
    D=1/(sqrt(18)*Nstar); a=D*exp(-2t/3)
    eps=exp(-2t/3)/Nstar
    fw=ifft(f); fx=fft((-1im.*omega).*fw)
    current=-a.*imag.(conj.(f).*fx)
    target=max.(1 .-x.^2,0.)
    center=sum(x.*R)*dx/E; xx=x.-center
    variance=sum(xx.^2 .*R)*dx/E
    q=1/3+sum(xx.*current)*dx/(E*variance)
    core=(abs.(x).<.8).&(R.>1e-12)
    urms=sqrt(sum(current.^2 ./(R.+1e-30))*dx/E)
    ucore=sqrt(sum(current[core].^2 ./R[core])*dx/E)
    overlap=abs(dot(sqrt.(target),f))*dx/sqrt(E*sum(target)*dx)
    kinetic=eps^2/2*sum(abs2,fx)*dx
    energy=kinetic+sum(.5R.^2+x.^2 .*R)*dx
    Dict{String,Any}("gain_length"=>t,"mass_relative_error"=>E/(4/3)-1,
        "width_ratio"=>sqrt(5variance),"chirp_ratio"=>3q,
        "density_l1"=>sum(abs.(R.-target))*dx/E,
        "density_l2_relative"=>sqrt(sum((R.-target).^2)/sum(target.^2)),
        "centroid_scaled"=>center,"scaled_velocity_rms"=>urms,
        "core_scaled_velocity_rms"=>ucore,"wing_mass_fraction"=>sum(R[abs.(x).>1])*dx/E,
        "time_guard_fraction"=>sum(R[abs.(x).>.85maximum(abs,x)])*dx/E,
        "frequency_guard_fraction"=>sum(abs2,fw[abs.(omega).>.8maximum(abs,omega)])/sum(abs2,fw),
        "even_parabolic_field_overlap"=>overlap,"peak_scaled_density"=>maximum(R),
        "central_scaled_density"=>R[argmin(abs.(x))],"lens_energy"=>energy,
        "lens_kinetic_energy"=>kinetic,"epsilon_eff"=>eps)
end

function run_lens(c,defaults,raw)
    getc(key,fallback)=get(c,key,get(defaults,key,fallback))
    label=c["label"]; Nstar=Float64(getc("Nstar",10.))
    D=1/(sqrt(18)*Nstar); H=Nstar/sqrt(18)
    nt=Int(getc("nt",8192)); window=Float64(getc("window",12.))
    length=Float64(getc("length",12.)); step=Float64(getc("step",.001))
    linear_cap=Float64(getc("linear_phase_cap",Inf))
    nonlinear_cap=Float64(getc("nonlinear_phase_cap",Inf))
    save_interval=Float64(getc("save_interval",.05))
    shape=getc("shape","parabola"); width=Float64(getc("width",1.))
    chirp=Float64(getc("chirp",1/3)); order=Int(getc("order",4))
    smooth=Float64(getc("smooth",.02))
    grid=TimeGrid(nt,window); x=collect(time_axis(grid))
    omega=2pi.*collect(FFTW.fftfreq(nt,1/grid.dt))
    initial=initial_pulse(x,shape,width,chirp,D;order,smooth)
    f=initial.field.*exp.(1im.*x.^2/(6D))
    z=0.; restart_file=getc("restart_file",""); restart_gain=Float64(getc("restart_gain_length",0.))
    if !isempty(restart_file)
        source=npzread(restart_file); source_meta=TOML.parsefile(replace(restart_file,".npz"=>".toml"))
        source_meta["Nstar"]==Nstar || error("Restart Nstar mismatch")
        source_meta["shape"]==shape && source_meta["width"]==width && source_meta["chirp"]==chirp || error("Restart input mismatch")
        iz=argmin(abs.(source["z"].-restart_gain)); abs(source["z"][iz]-restart_gain)<1e-9 || error("Restart time absent")
        old_window=Float64(source_meta["window"]); ratio=window/old_window
        ratio>=1 && abs(ratio-round(ratio))<1e-9 || error("Restart window must be an integer expansion")
        inner_nt=Int(round(nt/ratio)); inner=refine_periodic_field(source["fields"][:,iz],inner_nt)
        f=zeros(ComplexF64,nt);offset=div(nt-inner_nt,2);f[offset+1:offset+inner_nt].=inner
        z=restart_gain
    end
    steps=0; rows=[lens_measure(f,x,omega,z,Nstar)]
    snapshots=Vector{ComplexF64}[copy(f)];snapz=[z]
    save=collect(z:save_interval:length)
    last(save)<length-1e-10 && push!(save,length)
    elapsed=@elapsed begin
        for target in save[2:end]
            while z<target-1e-12
                # Keep all represented linear frequencies below the split-step
                # resonance threshold and bound the nonlinear phase separately.
                h=min(step,target-z,linear_cap/(D*exp(-2z/3)*maximum(abs2,omega)),
                      nonlinear_cap/(H*exp(2z/3)*maximum(abs2,f)))
                # Time-ordered linear half steps and the exactly integrated
                # time-dependent nonlinear/potential substep.
                a1=1.5D*exp(-2z/3)*(-expm1(-h/3))
                a2=1.5D*exp(-2(z+h/2)/3)*(-expm1(-h/3))
                b=1.5H*exp(2z/3)*expm1(2h/3)
                f=fft(exp.(0.5im*a1.*omega.^2).*ifft(f))
                f .*= exp.(1im*b .* (abs2.(f) .+ x.^2 .- 1))
                f=fft(exp.(0.5im*a2.*omega.^2).*ifft(f))
                z+=h;steps+=1
            end
            push!(rows,lens_measure(f,x,omega,target,Nstar))
            if abs(target/2-round(target/2))<1e-8 || target==length
                push!(snapshots,copy(f));push!(snapz,target)
            end
        end
    end
    result=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
       "label"=>label,"method"=>"independent exact-lens Strang",
       "shape"=>shape,"width"=>width,"chirp"=>chirp,"order"=>order,"smooth"=>smooth,
       "Nstar"=>Nstar,"N0"=>sqrt(H*initial.peak*initial.scale^2/D),
       "nt"=>nt,"window"=>window,"length"=>length,"step"=>step,
       "linear_phase_cap"=>linear_cap,"nonlinear_phase_cap"=>nonlinear_cap,
       "restart_file"=>restart_file,"restart_gain_length"=>restart_gain,
       "steps"=>steps,"elapsed_seconds"=>elapsed,"rows"=>rows)
    mkpath(raw)
    open(joinpath(raw,label*".toml"),"w") do io;TOML.print(io,result);end
    npzwrite(joinpath(raw,label*".npz"),Dict("x"=>x,"z"=>snapz,"fields"=>hcat(snapshots...)))
    final=last(rows)
    @printf("%s lens: seconds=%.2f L1=%.5g width=%.8f chirp=%.8f guard=(%.2g,%.2g)\n",
       label,elapsed,final["density_l1"],final["width_ratio"],final["chirp_ratio"],
       final["time_guard_fraction"],final["frequency_guard_fraction"]);flush(stdout)
    GC.gc()
end

function lens_main()
    config=TOML.parsefile(ARGS[1]); defaults=get(config,"defaults",Dict{String,Any}())
    for c in config["cases"];run_lens(c,defaults,config["raw_location"]);end
end
abspath(PROGRAM_FILE)==(@__FILE__) && lens_main()
