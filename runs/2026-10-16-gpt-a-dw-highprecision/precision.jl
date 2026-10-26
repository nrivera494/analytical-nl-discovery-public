# agent: gpt-a; model: gpt-6-astra; family: gpt
# Independent Double64 RK4IP; current field only; no damping.
using DoubleFloats, GenericFFT, LinearAlgebra, TOML, Serialization, Dates
BLAS.set_num_threads(1)
const T=Double64
const CT=Complex{T}
const PI=T(BigFloat(pi))
const RAW="~/analytical-nl-discovery-data/2026-10-16-gpt-a-dw-highprecision"
function memory_check()
    while true
        free=parse(Int,match(r"free percentage: (\d+)%",read(`memory_pressure`,String)).captures[1])
        println("Memory free: ",free,"%");flush(stdout)
        free>=35 && return
        sleep(30)
    end
end
function exact(t,z)
    a=abs.(t)
    numerator=2*cis(z/2) .* ((exp.(-a).+exp.(-7a))/2 .+
        3cis(4z) .* (exp.(-3a).+exp.(-5a))/2)
    denominator=(1 .+exp.(-8a))/2 .+2 .* (exp.(-2a).+exp.(-6a)) .+3cos(4z).*exp.(-4a)
    numerator./denominator
end
function measure(q,q0,t,w,delta)
    norm0=sum(abs2,q0);u=fft(q)
    wz=inv(6delta);wr=inv(2delta)+18delta
    band=w.>=wz;resonant=(w.>=T(0.75)*wr).&(w.<=T(1.5)*wr)
    out=Dict{String,Any}("energy_drift"=>Float64(sum(abs2,q)/norm0-1),
        "eta_band"=>Float64(sum(abs2,q[band])/norm0),
        "eta_resonant"=>Float64(sum(abs2,q[resonant])/norm0))
    gated=Dict{String,Vector{CT}}()
    for R in (15,20,25)
        gate=1 ./ (1 .+exp.(-2 .* (t.-R))) .+1 ./ (1 .+exp.(2 .* (t.+R)))
        gq=ifft(u.*gate);gated[string(R)]=gq
        out["eta_gate"*string(R)]=Float64(sum(abs2,gq[band])/norm0)
        out["eta_resonant_gate"*string(R)]=Float64(sum(abs2,gq[resonant])/norm0)
    end
    out["roundtrip_relative_l2"]=Float64(norm(ifft(u)-q)/norm(q))
    out,gated
end
function run_case(name,delta_string,n,window,steps;benchmark=false,xi_string="")
    memory_check();began=time()
    delta=T(parse(BigFloat,delta_string))
    zmax=isempty(xi_string) ? 3PI/4 : T(parse(BigFloat,xi_string))
    h=zmax/steps
    dt=T(window)/n;t=T.(collect(-n÷2:n÷2-1)).*dt.+64
    w=T.(vcat(collect(0:n÷2-1),collect(-n÷2:-1))).*(2PI/T(window))
    u0=CT.(1 ./cosh.(t));q0=ifft(u0);q=copy(q0)
    half=cis.((-w.^2/2 .+delta.*w.^3)*h/2)
    nonlinear(q)=4im .* ifft((u=fft(q);abs2.(u).*u))
    function advance(q)
        v=half.*q;k1=half.*nonlinear(q)
        k2=nonlinear(v.+h/2 .*k1);k3=nonlinear(v.+h/2 .*k2)
        k4=nonlinear(half.*(v.+h.*k3))
        half.*(v.+h/6 .*(k1.+2k2.+2k3)).+h/6 .*k4
    end
    q=advance(q);GC.gc();started=time()
    limit=benchmark ? 20 : steps
    for j in 2:limit
        q=advance(q)
        if j%max(1,limit÷4)==0
            println(name," ",j,"/",limit," elapsed=",round(time()-started,digits=2),
                " RSS_MiB=",round(Sys.maxrss()/1024^2,digits=1));flush(stdout)
        end
        deadline=get(ENV,"AUDIT_DEADLINE","")
        !isempty(deadline) && now(UTC)>DateTime(deadline) && error("Reserved closeout time reached")
    end
    result=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
        "name"=>name,"delta3"=>Float64(delta),"n"=>n,"window"=>window,"center"=>64,
        "steps"=>steps,"completed_steps"=>limit,"h"=>Float64(h),"xi"=>Float64(zmax),
        "seconds_per_step"=>(time()-started)/(limit-1),"peak_rss_mb"=>Sys.maxrss()/1024^2)
    if benchmark
        result["fft_roundtrip_error"]=Float64(norm(fft(q0)-u0)/norm(u0))
        exactq=ifft(exact(t,zmax));m,g=measure(exactq,q0,t,w,delta)
        result["exact_TOD_free_null"]=m
    else
        measured_delta=iszero(delta) ? T(parse(BigFloat,"0.003")) : delta
        m,g=measure(q,q0,t,w,measured_delta);result["metrics"]=m
        result["measurement_delta3"]=Float64(measured_delta)
        if iszero(delta)
            result["breather_relative_l2_error"]=Float64(norm(fft(q)-exact(t,zmax))/norm(u0))
        end
        serialize(joinpath(RAW,name*".jls"),(q=q,q0=q0,t=t,w=w,gates=g))
        open(joinpath(RAW,name*"_spectrum.tsv"),"w") do io
            for j in eachindex(w)
                println(io,join(Float64.((w[j],real(q[j]),imag(q[j]),
                    real(g["15"][j]),imag(g["15"][j]),real(g["20"][j]),imag(g["20"][j]),
                    real(g["25"][j]),imag(g["25"][j]))),'\t'))
            end
        end
    end
    result["wall_seconds"]=time()-began
    open(joinpath(RAW,name*".toml"),"w") do io;TOML.print(io,result);end
    println(result);flush(stdout)
    result
end
mkpath(RAW)
if ARGS[1]=="pilot"
    run_case("pilot","0.003",16384,256,8192;benchmark=true)
elseif ARGS[1]=="precompression_grid"
    # Frozen before either grid-pair outcome. Both spatial resolutions use
    # the same coarser step; the baseline's time error is checked separately.
    # The already-running launcher retains its original argument until exit.
    println("Paired grid control: 4096 equal steps at n=16384 and n=32768; requested launcher steps ",ARGS[5]," interpreted by the frozen paired-grid design.")
    flush(stdout)
    if !isfile(joinpath(RAW,"precompression_grid_reference.toml"))
        run_case("precompression_grid_reference","0.003",16384,256,4096;xi_string="2.25")
        GC.gc()
    end
    run_case("precompression_grid","0.003",32768,256,4096;xi_string="2.25")
else
    run_case(ARGS[1],ARGS[2],parse(Int,ARGS[3]),parse(Int,ARGS[4]),parse(Int,ARGS[5]);xi_string=length(ARGS)>=6 ? ARGS[6] : "")
end
