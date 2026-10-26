# agent: gpt-b; model: gpt-6-astra; family: gpt
# Task T-20261004-claude-interactive-08. Run with JULIA_NUM_THREADS=2.
# Full-field propagation uses the pinned PulsePropagation RK4IP implementation.
# The harness specifies the exact NLSE limit, dual projections, and source spectra.
using PulsePropagation, FFTW, LinearAlgebra, Random, Statistics, NPZ, TOML
const PP = PulsePropagation
BLAS.set_num_threads(1)
FFTW.set_num_threads(1)

const HBAR = 1.054571817e-34
const KB = 1.380649e-23

function setup(n, window, h; raman=false, t0=0.5, fraction=0.18)
    dt = window / n
    x = collect(-n÷2:n÷2-1) .* dt
    k = PP.ifft_frequency_grid(n, dt)
    s = sech.(x)
    sim = PP.Simulation{Float64}(lambda0=1.55e-6, dz=h,
        include_Raman=raman, pulse_centering=false)
    fiber = PP.Fiber{Float64}(betas=reshape([0., 0., -1.], 3, 1),
        sr=ones(1,1,1,1), L0=1., fr=fraction)
    sr = PP.calc_srsk(fiber, sim, 1)
    d = reshape(-0.5im .* k.^2, n, 1)
    # The low-level solver accepts both arrays explicitly. Flat prefactor = no shock.
    pref = fill(1.0im, n)
    haw = raman ? raman_transfer(k ./ t0, fraction) : ComplexF64[]
    g = hcat(2s, 1im .* (1 .- x .* tanh.(x)) .* s,
             x .* s, 1im .* s .* tanh.(x))
    tangents = hcat((1 .- x .* tanh.(x)) .* s ./ 2,
                    1im .* s, s .* tanh.(x), 1im .* x .* s)
    (; n, window, h, dt, x, k, s, sim, sr, d, pref, haw, g, tangents, t0, fraction)
end

"Causal Agarwal transfer, including f_R; omega is rad/ps (positive-transform convention)."
function raman_transfer(omega, fraction=0.18)
    a, b = 1/0.032, 1/0.0122
    fraction .* (a*a+b*b) ./ ((a .- 1im .* omega).^2 .+ b*b)
end

"Wigner phase-force PSD divided by q in normalized coordinates; includes its DC limit."
function raman_psd(k, t0, temperature; fraction=0.18)
    h = raman_transfer(k ./ t0, fraction)
    tr_ps = fraction * 2/0.032 / ((1/0.032)^2+(1/0.0122)^2)
    out = zeros(length(k))
    for j in eachindex(k)
        wsi = abs(k[j])/t0*1e12
        if wsi == 0
            out[j] = temperature == 0 ? 0. : 2KB*temperature/HBAR*tr_ps*1e-12
        else
            occupation = temperature == 0 ? 0. : 1/expm1(HBAR*wsi/(KB*temperature))
            out[j] = abs(imag(h[j]))*(2occupation+1)
        end
    end
    out
end

project(u, z, a) = a.dt .* real.(a.g' * vec(u) .* exp(-0.5im*z))

function step(aw, cache, a; method="rk4ip")
    if method == "rk4ip"
        v, c, ok = PP.step_rk4ip_nogain(aw, a.sim, a.pref, a.sr, a.d,
            a.haw, ComplexF64[], nothing, cache)
        ok || error("RK4IP rejected step")
        return v, c
    elseif method == "splitstep"
        half = exp.(a.d .* (a.h/2))
        v = fft(half .* aw, 1)
        intensity = abs2.(v)
        potential = if isempty(a.haw)
            intensity
        else
            (1-a.fraction).*intensity .+
                real.(fft(reshape(a.haw,:,1).*ifft(intensity,1),1))
        end
        v .*= exp.(1im*a.h.*potential)
        return half .* ifft(v, 1), nothing
    end
    error("Unknown integration method $method")
end

function propagate(u0, a, zmax, save_every; method="rk4ip", fields=false)
    nsteps = round(Int, zmax/a.h)
    stride = round(Int, save_every/a.h)
    @assert isapprox(nsteps*a.h,zmax) && isapprox(stride*a.h,save_every)
    z = collect(0:nsteps÷stride).*save_every
    projected = zeros(4,length(z))
    saved = fields ? zeros(ComplexF64,a.n,length(z)) : nothing
    u = reshape(ComplexF64.(u0),a.n,1)
    projected[:,1] = project(u,0.,a)
    fields && (saved[:,1] = vec(u))
    aw, cache = ifft(u,1), nothing
    for j=1:nsteps
        aw,cache = step(aw,cache,a;method)
        if j % stride == 0
            idx = j÷stride+1
            u = fft(aw,1)
            projected[:,idx] = project(u,j*a.h,a)
            fields && (saved[:,idx] = vec(u))
        end
    end
    (;z,projected,fields=saved)
end

function run_trace(cfg, raw)
    a = setup(cfg["n"],cfg["window"],cfg["h"])
    eps = cfg["epsilon"]
    start = time()
    mean = propagate(a.s,a,cfg["zmax"],cfg["save_every"];fields=true)
    response = zeros(length(mean.z),4,2a.n)
    # Complete real orthonormal collocation basis, norm dt*sum(abs2)=1.
    # Central differences suppress even nonlinear orders. No covariance fit.
    for j=1:2a.n
        perturb = zeros(ComplexF64,a.n)
        perturb[mod1(j,a.n)] = (j<=a.n ? 1. : 1im)/sqrt(a.dt)
        plus = propagate(a.s .+ eps.*perturb,a,cfg["zmax"],cfg["save_every"])
        minus = propagate(a.s .- eps.*perturb,a,cfg["zmax"],cfg["save_every"])
        response[:,:,j] = transpose((plus.projected-minus.projected)/(2eps))
        if j % 128 == 0
            println("trace ",cfg["name"]," ",j,"/",2a.n," elapsed=",round(time()-start,digits=1));flush(stdout)
        end
    end
    npzwrite(joinpath(raw,"trace_"*cfg["name"]*".npz"),Dict(
        "z"=>mean.z,"x"=>a.x,"k"=>a.k,"dual"=>a.g,"tangents"=>a.tangents,
        "response"=>response,"mean_fields"=>mean.fields,
        "biorthogonality"=>a.dt.*real.(a.g'*a.tangents),
        "wall_seconds"=>time()-start))
end

function run_drift(cfg, raw)
    output = Dict{String,Any}()
    for t0 in cfg["t0_ps"], method in ["rk4ip","splitstep"]
        h = method=="rk4ip" ? cfg["h"] : cfg["h_splitstep"]
        a = setup(cfg["n"],cfg["window"],h;raman=true,t0)
        out = propagate(a.s,a,cfg["zmax"],cfg["save_every"];method,fields=true)
        e, freq, timing = Float64[],Float64[],Float64[]
        for u in eachcol(out.fields)
            ut = fft((-1im.*a.k).*ifft(u))
            energy = a.dt*sum(abs2,u)
            push!(e,energy)
            push!(freq,a.dt*imag(dot(u,ut))/energy)
            push!(timing,a.dt*sum(a.x.*abs2.(u))/energy)
        end
        key = replace(string(t0),"."=>"p")*"_"*method
        output[key*"_z"] = out.z
        output[key*"_energy"] = e
        output[key*"_frequency"] = freq
        output[key*"_timing"] = timing
        output[key*"_final_field"] = out.fields[:,end]
        # Independent momentum balance for the launch profile.
        intensity = a.s.^2
        di = real.(fft((-1im.*a.k).*ifft(intensity)))
        delayed = real.(fft(a.haw.*ifft(intensity)))
        output[key*"_initial_exact_rate"] = -a.dt*sum(di.*delayed)/2
    end
    npzwrite(joinpath(raw,"drift.npz"),output)
end

function run_source_checks(cfg,raw)
    a = setup(cfg["n"],cfg["window"],0.02;t0=cfg["t0_ps"])
    gamma = cfg["gamma_W_m"]
    f0 = a.sim.f0
    t0 = cfg["t0_ps"]
    beta2 = cfg["beta2_ps2_m"]
    ld = t0^2/abs(beta2)
    p0 = 1/(gamma*ld)
    q = HBAR*2pi*f0*1e12/(p0*t0*1e-12)
    dtps = a.dt*t0
    hR = raman_transfer(a.k./t0)
    out = Dict{String,Any}("x"=>a.x,"k"=>a.k,"q"=>q,"LD_m"=>ld,"P0_W"=>p0)
    rng = MersenneTwister(cfg["seed"])
    # Test samplers without propagation. Each column is a different optical observable.
    b = hcat(a.s.^2 .* tanh.(a.x), (1 .- a.x.*tanh.(a.x)).*a.s.^2)
    for temp in cfg["temperatures_K"]
        legacy = PP.raman_langevin_spectrum(a.n,dtps,f0,hR,gamma;temperature_K=Float64(temp))
        psd = raman_psd(a.k,t0,temp)
        correct = (HBAR*2pi*f0*1e12/gamma).*psd
        for (name,c) in [("legacy",legacy),("wigner",correct)]
            samples = zeros(cfg["n_samples"],2)
            for j=1:cfg["n_samples"]
                eta = PP.sample_real_raman_langevin_noise(c,ld,dtps;rng)
                samples[j,:] = gamma*a.dt.*(transpose(b)*eta)
            end
            key = name*"_"*string(temp)
            out[key*"_C"] = c
            out[key*"_samples"] = samples
        end
    end
    meanw = ifft(reshape(sqrt(p0).*a.s,a.n,1),1)
    for scale in [0.5,inv(sqrt(2.))]
        ens = PP.photon_vacuum_ensemble(meanw,dtps,f0,cfg["n_samples"];rng,noise_scale=scale)
        samples = zeros(cfg["n_samples"],4)
        for j=1:cfg["n_samples"]
            du = fft(ens[:,:,j]-meanw,1)./sqrt(p0)
            samples[j,:] = project(du,0.,a)
        end
        out[scale==0.5 ? "vacuum_wigner_samples" : "vacuum_legacy_samples"] = samples
    end
    npzwrite(joinpath(raw,"source_checks.npz"),out)
end

function run_stochastic(cfg,raw)
    t0 = cfg["t0_ps"]
    gamma = cfg["gamma_W_m"]
    ld = t0^2/abs(cfg["beta2_ps2_m"])
    p0 = 1/(gamma*ld)
    rng = MersenneTwister(cfg["seed"])
    for source in cfg["sources"]
        delayed = source=="raman_delayed"
        a = setup(cfg["n"],cfg["window"],cfg["h"];raman=delayed,t0)
        q = HBAR*2pi*a.sim.f0*1e12/(p0*t0*1e-12)
        mean = propagate(a.s,a,cfg["zmax"],cfg["save_every"];fields=true)
        coords = zeros(length(mean.z),4,cfg["ntraj"])
        shadow_enabled = get(cfg,"shadow",false)
        shadow_saved = zeros(length(mean.z),4,cfg["ntraj"])
        stride = round(Int,cfg["save_every"]/a.h)
        nsteps = round(Int,cfg["zmax"]/a.h)
        # Explicit Wigner spectrum, using the solver's existing C_omega interface.
        cR = HBAR*2pi*a.sim.f0*1e12/gamma .* raman_psd(a.k,t0,cfg["temperature_K"])
        cG = fill(cfg["alpha_G"]*q/a.window,a.n,1)
        templates = Array{ComplexF64,3}(undef,a.n,4,length(mean.z))
        for (i,um) in enumerate(eachcol(mean.fields))
            if delayed
                energy = a.dt*sum(abs2,um)
                center = a.dt*sum(a.x.*abs2.(um))/energy
                velocity = a.dt*imag(dot(um,fft((-1im.*a.k).*ifft(um))))/energy
                xx = a.x .- center
                ss = sech.(xx)
                phase = angle(sum(ss.*um.*exp.(-1im.*velocity.*xx)))
                templates[:,:,i] = hcat(2ss,1im.*(1 .-xx.*tanh.(xx)).*ss,
                    xx.*ss,1im.*ss.*tanh.(xx)) .* exp.(1im.*(phase .+velocity.*xx))
            else
                templates[:,:,i] = a.g .* exp(0.5im*mean.z[i])
            end
        end
        start=time()
        for traj=1:cfg["ntraj"]
            if source=="vacuum"
                meanw = ifft(reshape(sqrt(p0).*a.s,a.n,1),1)
                initial = PP.photon_vacuum_ensemble(meanw,a.dt*t0,a.sim.f0,1;rng,noise_scale=0.5)
                aw = initial[:,:,1]./sqrt(p0)
            else
                aw = ifft(reshape(ComplexF64.(a.s),a.n,1),1)
            end
            u=fft(aw,1)
            coords[1,:,traj] = a.dt.*real.(templates[:,:,1]'*(vec(u)-mean.fields[:,1]))
            shadow = copy(coords[1,:,traj])
            shadow_saved[1,:,traj] = shadow
            cache=nothing
            for j=1:nsteps
                if shadow_enabled
                    shadow[2] += a.h*shadow[1]/2
                    shadow[3] += a.h*shadow[4]
                end
                aw,cache=step(aw,cache,a)
                if source=="gain"
                    kick = PP._sample_diagonal_kick(cG,a.h,rng)
                    aw .+= kick
                    shadow_enabled && (shadow .+= project(fft(kick,1),j*a.h,a))
                    cache=nothing
                elseif startswith(source,"raman")
                    u=fft(aw,1)
                    eta=PP.sample_real_raman_langevin_noise(cR,ld*a.h,a.dt*t0;rng)
                    # Same first-order multiplicative phase kick as the solver backend.
                    u .+= 1im*gamma.*u.*reshape(eta,:,1)
                    if shadow_enabled
                        # Leading stationary-soliton source; no fitted coefficient.
                        shadow .+= a.dt.*real.(a.g'*(1im*gamma.*a.s.*eta))
                    end
                    aw=ifft(u,1)
                    cache=nothing
                end
                if j%stride==0
                    idx=j÷stride+1
                    u=fft(aw,1)
                    coords[idx,:,traj] = a.dt.*real.(templates[:,:,idx]'*(vec(u)-mean.fields[:,idx]))
                    shadow_saved[idx,:,traj] = shadow
                end
            end
            if traj%256==0
                println("stochastic ",source," ",traj,"/",cfg["ntraj"]," elapsed=",round(time()-start,digits=1));flush(stdout)
            end
        end
        npzwrite(joinpath(raw,"stochastic_"*source*".npz"),Dict(
            "z"=>mean.z,"coordinates"=>coords,"q"=>q,"mean_fields"=>mean.fields,
            "shadow_coordinates"=>shadow_saved,"shadow_enabled"=>shadow_enabled,
            "wall_seconds"=>time()-start))
    end
end

function run_crosscheck(cfg,raw)
    rng=MersenneTwister(cfg["seed"])
    out=Dict{String,Any}()
    for method in ["rk4ip","splitstep"]
        a=setup(cfg["n"],cfg["window"],method=="rk4ip" ? cfg["h"] : cfg["h_splitstep"])
        # Repeat exactly the same independently drawn full-field probes for each method.
        rng=MersenneTwister(cfg["seed"])
        values=zeros(round(Int,cfg["zmax"]/cfg["save_every"])+1,4,cfg["nprobes"])
        initial=zeros(4,cfg["nprobes"])
        for j=1:cfg["nprobes"]
            v=(randn(rng,a.n).+1im.*randn(rng,a.n))./sqrt(2a.window)
            initial[:,j]=project(v,0.,a)
            ep=cfg["epsilon"]
            plus=propagate(a.s.+ep.*v,a,cfg["zmax"],cfg["save_every"];method)
            minus=propagate(a.s.-ep.*v,a,cfg["zmax"],cfg["save_every"];method)
            values[:,:,j]=transpose((plus.projected-minus.projected)/(2ep))
            out["z"]=plus.z
        end
        out[method]=values
        out["initial"]=initial
    end
    npzwrite(joinpath(raw,"crosscheck.npz"),out)
end

function main(path, raw_override=nothing)
    cfg=TOML.parsefile(path)
    raw=raw_override===nothing ? cfg["raw_location"] : raw_override
    mkpath(raw)
    any(name -> endswith(name,".npz"), readdir(raw)) && error(
        "Refusing to overwrite an existing run. Pass a fresh raw directory as the second argument.")
    started=time()
    for variant in get(cfg,"trace",[])
        run_trace(variant,raw)
    end
    haskey(cfg,"drift") && run_drift(cfg["drift"],raw)
    haskey(cfg,"source_checks") && run_source_checks(cfg["source_checks"],raw)
    haskey(cfg,"stochastic") && run_stochastic(cfg["stochastic"],raw)
    haskey(cfg,"crosscheck") && run_crosscheck(cfg["crosscheck"],raw)
    println("TOTAL_WALL_SECONDS=",time()-started)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS[1],length(ARGS)>1 ? ARGS[2] : nothing)
end
