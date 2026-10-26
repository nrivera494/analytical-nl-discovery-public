# agent: gpt-d; model: gpt-6-astra; family: gpt
# Independent harness using the allowed evaluator's low-level RK4IP interface.
# No solver implementation source or proposer run script was read.
using PulsePropagation, FFTW, LinearAlgebra, NPZ, TOML, DelimitedFiles
const PP=PulsePropagation
BLAS.set_num_threads(1); FFTW.set_num_threads(1)

function run_case(name,N,fwhm;steps=4000,n=16384,dt=0.00075)
    pressure=read(`memory_pressure`,String)
    line=only(filter(x->occursin("free percentage",x),split(pressure,'\n')))
    println(line);flush(stdout)
    free=parse(Int,match(r"(\d+)%",line).captures[1]);free>=35 || error("Memory below threshold")
    raw=joinpath(homedir(),"analytical-nl-discovery-data","2026-10-17-gpt-d-raman-propagation")
    path=joinpath(raw,"julia_"*name*".toml")
    isfile(path) && error("Preserving completed Julia run: "*path)
    started=time(); T=fwhm/1000/(2acosh(sqrt(2.)))
    beta2,beta3=-.0217,.00012
    LD=T*T/abs(beta2);L=LD*(N==1 ? 2 : 3/N);h=L/steps
    lambda=1.55; n2=2.6e-20; area=64.5e-12;fr=.18
    omega0=2pi*299.792458/lambda
    gamma=2pi*n2/(lambda*1e-6*area)
    t=collect(-n÷2:n÷2-1).*dt
    O=PP.ifft_frequency_grid(n,dt)
    @assert maximum(abs.(O))>1000
    omega=omega0.+O;keep=omega.>.02omega0
    photon_weight=zeros(n);photon_weight[keep]=1 ./omega[keep]
    P=N*N*abs(beta2)/(gamma*T*T)
    initial=sqrt(P).*sech.(t./T)
    aw=reshape(ifft(ComplexF64.(initial)).*keep,n,1)
    a,b=1/.032,1/.0122;q=a*a+b*b
    H=q ./((a.-1im.*O).^2 .+ b*b)
    W=O.*imag.(H);kappa=gamma*fr/omega0*q/2
    sim=PP.Simulation{Float64}(lambda0=lambda*1e-6,dz=h,include_Raman=true,pulse_centering=false)
    fiber=PP.Fiber{Float64}(betas=reshape([0.,0.,beta2,beta3],4,1),sr=ones(1,1,1,1),L0=L,fr=fr)
    sr=PP.calc_srsk(fiber,sim,1)
    d=reshape(1im.*(beta2.*O.^2/2 .+beta3.*O.^3/6),n,1)
    pref=1im.*gamma.*(omega./omega0).*keep
    haw=fr.*H
    cache=nothing;window=n*dt
    E0=window*sum(abs2,aw);ph0=window*sum(abs2.(vec(aw)).*photon_weight)
    rows=zeros(steps+1,5);maxrho=0.;maxdrift=0.;minmargin=Inf
    for j=0:steps
        A=fft(vec(aw));I=abs2.(A);iw=ifft(I)
        E=window*sum(abs2,aw)
        rate=gamma*fr/omega0*window*sum(W.*abs2.(iw));rho=rate/(kappa*E*E)
        ph=window*sum(abs2.(vec(aw)).*photon_weight)
        maxrho=max(maxrho,rho);maxdrift=max(maxdrift,abs(ph/ph0-1))
        margin=E/E0-1/(1+kappa*E0*j*h);minmargin=min(minmargin,margin)
        rows[j+1,:]=[j*h,E,ph,rho,margin]
        if j<steps
            aw,cache,ok=PP.step_rk4ip_nogain(aw,sim,pref,sr,d,haw,ComplexF64[],nothing,cache)
            ok || error("RK4IP rejected fixed step")
        end
        if j%1000==0
            println("Julia ",name," ",j,"/",steps," rho_max=",maxrho);flush(stdout)
        end
    end
    out=Dict("agent"=>"gpt-d","model"=>"gpt-6-astra","family"=>"gpt",
        "case"=>name,"solver_commit"=>"b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa",
        "solver_dirty"=>false,"freeze_commit"=>"6df0927ef31369add037f36db21643b14d68bf51",
        "Eout_over_E0"=>rows[end,2]/E0,"max_accepted_rho"=>maxrho,
        "max_photon_drift"=>maxdrift,"min_retention_margin"=>minmargin,
        "h_m"=>h,"n"=>n,"dt_ps"=>dt,"wall_time_s"=>time()-started,
        "note"=>"Exact analytic response and shock prefactor supplied via low-level interface; no default blue-edge window. Saved rho evaluates the spectral identity on Julia fields, not the Julia RHS.")
    open(path,"w") do io; TOML.print(io,out);end
    writedlm(joinpath(raw,"julia_"*name*"_planes.csv"),rows,',')
    npzwrite(joinpath(raw,"julia_"*name*"_final.npz"),Dict("aw_final"=>vec(aw)))
    println(out);flush(stdout)
end

for name in ARGS
    if name=="core";run_case(name,3,100)
    elseif name=="h6_100";run_case(name,6,100;n=32768,dt=.000375)
    else;error("Unknown case "*name)
    end
    GC.gc()
end
