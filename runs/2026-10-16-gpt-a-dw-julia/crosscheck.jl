# agent: gpt-a; model: gpt-6-astra; family: gpt
# Independent harness using the pinned agents' solver, no solver source edits.
ENV["JULIA_NUM_PRECOMPILE_TASKS"]="1"
using PulsePropagation, FFTW, LinearAlgebra, NPZ, TOML
const PP=PulsePropagation
BLAS.set_num_threads(1)
FFTW.set_num_threads(1)
const SPAPER=835/(2pi*299.792458*50)

function memory_check()
    while true
        message=read(`memory_pressure`,String)
        matchval=match(r"free percentage: (\d+)%",message)
        free=parse(Int,matchval.captures[1])
        println("Memory free: ",free,"%");flush(stdout)
        free>=35 && return
        sleep(30)
    end
end

function response(w,model)
    model=="none" && return ComplexF64[],0.0
    fr,t1,t2=model=="M1" ? (.18,12.2/50,32/50) : (.245,12/50,32/50)
    a,b=1/t2,1/t1
    H=(a*a+b*b)./((a .-1im.*w).^2 .+b*b)
    if model=="roy"
        ab=50/96
        H=0.79 .* H .+ 0.21 .* (2ab ./ (ab .- 1im .* w) .- ab^2 ./ (ab .- 1im .* w).^2)
    end
    fr.*H,fr
end

function propagate(cfg,raw)
    memory_check()
    began=time();n=cfg["n"];window=cfg["window"];dt=window/n
    x=collect(-n÷2:n÷2-1).*dt
    w=PP.ifft_frequency_grid(n,dt)
    N=cfg["N"];delta=cfg["delta3"];h=cfg["h"]
    zmax=cfg["zmax"];nsteps=round(Int,zmax/h)
    @assert isapprox(nsteps*h,zmax)
    u0=cfg["shape"]=="sech" ? sech.(x) : exp.(-x.^2/2)
    q0=ifft(ComplexF64.(u0));q=reshape(copy(q0),:,1)
    haw,fr=response(w,cfg["raman"])
    sim=PP.Simulation{Float64}(lambda0=835e-9,dz=h,
        include_Raman=cfg["raman"]!="none",pulse_centering=false)
    fiber=PP.Fiber{Float64}(betas=reshape([0.,0.,-1.,6delta],4,1),
        sr=ones(1,1,1,1),L0=zmax,fr=fr)
    sr=PP.calc_srsk(fiber,sim,1)
    linear=reshape(1im .* (-w.^2 / 2 .+ delta .* w.^3),:,1)
    damping=cfg["damping"] ? Float64.(PP.damped_freq_window(n)) : ones(n)
    pref=1im * N^2 .* (1 .+ cfg["shock"] * SPAPER .* w) .* damping
    cache=nothing
    for j=1:nsteps
        q,cache,ok=PP.step_rk4ip_nogain(q,sim,pref,sr,linear,haw,ComplexF64[],nothing,cache)
        ok || error("RK4IP rejected step")
        if j%max(1,nsteps÷4)==0
            println(cfg["name"]," ",j,"/",nsteps," elapsed ",round(time()-began,digits=2),
                " peak RSS MiB ",round(Sys.maxrss()/1024^2,digits=1));flush(stdout)
            GC.gc(false)
        end
    end
    npzwrite(joinpath(raw,cfg["name"]*".npz"),Dict("q"=>vec(q),"q0"=>q0,"w"=>w,"t"=>x,
        "damping"=>damping,"z"=>zmax,"elapsed"=>time()-began,"peak_rss_mb"=>Sys.maxrss()/1024^2))
end

config=TOML.parsefile(ARGS[1]);raw=config["raw_location"];mkpath(raw)
for cfg in config["cases"]
    output=joinpath(raw,cfg["name"]*".npz")
    if isfile(output)
        println("Already done ",cfg["name"]);continue
    end
    propagate(cfg,raw)
    GC.gc()
end
