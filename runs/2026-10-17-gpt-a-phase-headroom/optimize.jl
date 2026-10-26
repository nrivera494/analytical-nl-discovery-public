# agent: gpt-a; model: gpt-6-astra; family: gpt
# Independent objective/optimizer; pinned solver discrete adjoint.
using PulsePropagation, FFTW, LinearAlgebra, Random, Statistics, NPZ, TOML, DelimitedFiles
using Optim
const PP=PulsePropagation
BLAS.set_num_threads(1);FFTW.set_num_threads(1)
const OUT="~/analytical-nl-discovery-data/2026-10-17-gpt-a-phase-headroom"
const SRC=joinpath(@__DIR__,"..","2026-10-16-claude-a-raman-soliton-frontier")
struct AuditResponse <: PP.AbstractRamanResponse
    fraction::Float64
    t0_fs::Float64
end
# Evaluator-documented extension point, not a modification of the solver.
function PP._mmgnlse_raman_kernels(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:AuditResponse}
    nt=p.domain.time_grid.nt;r=p.raman;k=PP._mmgnlse_raw_omega(p)
    a=r.t0_fs/32.;b=r.t0_fs/12.2
    ha=(a*a+b*b)./((a .- im.*k).^2 .+ b*b)
    iseven(nt) && (ha[nt÷2+1]=real(ha[nt÷2+1]))
    (;ha=ComplexF64.(ha),hb=zeros(ComplexF64,nt),fraction=r.fraction)
end
function PP._mmgnlse_solver_cache(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:AuditResponse}
    nt,nm,np=PP._mmgnlse_public_shape(p);omega=PP._mmgnlse_raw_omega(p)
    beta_operator=PP._mmgnlse_beta_array(p.beta,nt,nm,np,omega)
    nonlinear_prefactor=fill(1im*p.n2*p.omega0/2.99792458e-4,nt,1,1)
    nonlinear_active=true
    (;omega,beta_operator,nonlinear_prefactor,nonlinear_active,raman=PP._mmgnlse_raman_kernels(p))
end

function matrices(q,z,dt)
    r=-z*z-abs2(q);b=sqrt(complex(r));C=cosh(b*dt);S=sinh(b*dt)/b
    C1=dt*S/2;S1=(dt*C-S)/(2r)
    A=ComplexF64[-im*z q;-conj(q) im*z]
    T=C*I+S*A;U=C1*I+S1*A
    T,(-2z*U+S*ComplexF64[-im 0;0 im]),(-2real(q)*U+S*ComplexF64[0 1;-1 0]),(-2imag(q)*U+S*ComplexF64[0 im;im 0])
end
function transfer(q,z,dt;grad=false)
    m=length(q)-1;Y=zeros(ComplexF64,2,m+1);Y[1,1]=1
    mats=Vector{Matrix{ComplexF64}}(undef,m);dzm=similar(mats);dxm=similar(mats);dym=similar(mats)
    yz=zeros(ComplexF64,2)
    for j in 1:m
        T,Tz,Tx,Ty=matrices((q[j]+q[j+1])/2,z,dt)
        yz=T*yz+Tz*Y[:,j];Y[:,j+1]=T*Y[:,j]
        mats[j]=T;dzm[j]=Tz;dxm[j]=Tx;dym[j]=Ty
    end
    a=Y[1,end];az=yz[1]
    if !grad;return a,az,norm(Y[:,end]);end
    row=ComplexF64[1 0];gx=zeros(length(q));gy=zeros(length(q))
    for j in m:-1:1
        ax=(row*dxm[j]*Y[:,j])[1];ay=(row*dym[j]*Y[:,j])[1]
        vx=imag(-ax/az)/2;vy=imag(-ay/az)/2
        gx[j]+=vx;gx[j+1]+=vx;gy[j]+=vy;gy[j+1]+=vy
        row=row*mats[j]
    end
    a,az,gx.+im.*gy
end
function zs_objective(u,t,N;gradient=true)
    dt=t[2]-t[1];ip=argmax(abs2.(u));center=t[ip];half=max(1.,8/(N*abs(u[ip])))
    inds=findall(abs.(t.-center).<=half)
    q=N.*u[inds];qpre=copy(q);tt=t[inds]
    k=2pi.*FFTW.fftfreq(length(q),1/dt);Q=fft(q);kc=sum(k.*abs2.(Q))/sum(abs2,Q)
    demod=exp.(-im*kc.*tt);q=q.*demod
    z=im*maximum(abs,q)/2;res=Inf
    for it in 1:20
        a,az,yn=transfer(q,z,dt);step=a/az;z-=step;res=abs(a)/max(yn,1e-30)
        abs(step)<1e-12 && break
    end
    0<imag(z)<maximum(abs,q)*1.2 || error("ZS root out of range: $z")
    f=2imag(z)/(N*N)
    gt=zeros(ComplexF64,length(u))
    if gradient
        a,az,gq=transfer(q,z,dt;grad=true)
        dk=real(dot(gq,-im.*tt.*q))
        gk=2 .* (ifft(k.*fft(qpre)).-kc.*qpre)./sum(abs2,qpre)
        gt[inds].=(2/N).*(gq.*conj.(demod).+dk.*gk)
    end
    f,gt,Dict("eta"=>imag(z),"real_zeta"=>real(z),"red_k"=>kc,"peak_t"=>center,
              "f_gate"=>dt*sum(abs2,u[inds])/2,"root_residual"=>res)
end
function legbasis(k,M,wc)
    x=clamp.(k./wc,-1,1);a=ones(length(k));b=copy(x);B=zeros(length(k),M)
    for m in 2:M+1
        c=((2m-1).*x.*b.-(m-1).*a)./m;B[:,m-1]=c;a=b;b=c
    end
    B
end
function run(N,T0,startname;maxiter=200,M=30,nt=8192,width=80.,hfac=1.,objective="zs",mode="opt")
    mkpath(OUT);started=time();grid=TimeGrid(nt,width);t=collect(time_axis(grid));dt=width/nt
    k=2pi.*FFTW.fftfreq(nt,1/dt) # standard FFT sign, unlike the solver spectrum
    Q=fft(ComplexF64.(sech.(t)));wc=maximum(abs.(k[abs.(Q).>1e-4maximum(abs,Q)]));B=legbasis(k,M,wc)
    z=4/N;steps=ceil(Int,z/(.4/(N*(2N-1))^2*hfac));dz=z/steps
    domain=MMGNLSEDomain(degrees_of_freedom(:time),grid);w0=1215.2590756831312
    pars=MMGNLSEParameters(domain;length=z,beta=TaylorBeta(reshape([0.,0.,-1.],3,1)),S=ones(1,1,1,1),
        n2=N*N*2.99792458e-4/w0,omega0=w0,raman=AuditResponse(.18,T0))
    function launch(c)
        V=Q.*exp.(im.*(B*c));reshape(ifft(V),nt,1,1),V
    end
    calls=Ref(0);best=Ref(-Inf);tag="opt_N$(Int(N))_T$(Int(T0))_$(startname)_$(objective)"
    history=joinpath(OUT,tag*"_history.csv")
    open(history,"w") do io;println(io,"evaluation,elapsed_s,f_zs,gradient_norm,peak_t,f_gate");end
    function evaluate(c;gradient=true,record=true)
        calls[] % 8 == 0 && GC.gc(false)
        initial,V=launch(c)
        sol=solve_mmgnlse(initial,pars,dz;method=RK4IP(),saveat=z/20)
        u=vec(sol.fields[:,:,:,end]);f,gt,diag=zs_objective(u,t,N;gradient)
        g=zeros(M)
        if gradient
            # gt is an ordinary Euclidean time-field derivative. Spectral
            # pairing introduces nt, with no dt: checked by central differences.
            terminal=reshape(nt.*fftshift(ifft(gt)),nt,1,1)
            adj=solve_adjoint(terminal,pars,dz;forward_solution=sol,units=:power,
                adjoint_mode=:discrete_rk4ip,checkpoint_stride=40,saveat=z)
            gspec=vec(ifftshift(get_spectral_field(adj;z=:initial)))
            # Solver spectrum = ifft(time); our Q = fft(time).
            for j in 1:M
                du=ifft(im.*V.*B[:,j]);dsp=ifft(du)
                g[j]=real(dot(gspec,dsp))
            end
        end
        if record
            calls[]+=1
            open(history,"a") do io
                println(io,join((calls[],time()-started,f,norm(g),diag["peak_t"],diag["f_gate"]),","))
            end
            if f>best[]
                best[]=f;writedlm(joinpath(OUT,tag*"_bestcoef.csv"),c,',')
                npzwrite(joinpath(OUT,tag*"_bestfield.npz"),Dict("t"=>t,"u"=>u,"c"=>c))
            end
            println(tag," eval=",calls[]," f=",f," |g|=",norm(g)," elapsed=",round(time()-started,digits=1));flush(stdout)
        end
        f,g,diag,u
    end
    c=zeros(M)
    if startname=="B"
        v=vec(readdlm(joinpath(SRC,"h4_adjoint_N4_T200_bestmask_coef.csv")))
        c[1:length(v)]=v.*((-1.).^(2:length(v)+1))
    elseif startswith(startname,"r")
        seed=2026101700+parse(Int,startname[2:end]);rng=MersenneTwister(seed)
        c.=randn(rng,M).*(startname=="r1" ? .2 : startname=="r2" ? .7 : 1.5)
    elseif startswith(startname,"warm")
        c.=vec(readdlm(ENV["WARM_MASK"],','))
    end
    if mode=="forward"
        initial,V=launch(c)
        sol=solve_mmgnlse(initial,pars,dz;method=RK4IP(),saveat=z/20)
        u=vec(sol.fields[:,:,:,end])
        npzwrite(joinpath(OUT,tag*"_forwardfield.npz"),Dict("t"=>t,"u"=>u,"c"=>c))
        record=Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
            "N"=>N,"T0_fs"=>T0,"nt"=>nt,"width"=>width,"h"=>dz,
            "mode"=>"selected-mask second-solver forward check", "elapsed_s"=>time()-started,
            "solver_commit"=>"b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa")
        open(joinpath(OUT,tag*"_forward.toml"),"w") do io;TOML.print(io,record);end
        TOML.print(stdout,record);return
    end
    baseval,basegrad,basediag,basefield=evaluate(c)
    if mode in ("check","checkopt")
        rng=MersenneTwister(2026101704);v=randn(rng,M);v./=norm(v);eps=1e-5
        fp=evaluate(c.+eps.*v;gradient=false,record=false)[1]
        fm=evaluate(c.-eps.*v;gradient=false,record=false)[1]
        fd=(fp-fm)/(2eps);pred=dot(basegrad,v)
        r=Dict("f_zs"=>baseval,"directional_fd"=>fd,"directional_adjoint"=>pred,
            "relative_error"=>abs(fd-pred)/max(abs(fd),abs(pred),1e-12),"gradient_norm"=>norm(basegrad),
            "elapsed_s"=>time()-started,"N"=>N,"T0_fs"=>T0,"nt"=>nt,"h"=>dz)
        open(joinpath(OUT,tag*"_check.toml"),"w") do io;TOML.print(io,r);end
        npzwrite(joinpath(OUT,tag*"_checkfield.npz"),Dict("t"=>t,"u"=>basefield))
        TOML.print(stdout,r);flush(stdout)
        r["relative_error"]<1e-4 || error("Failed directional derivative")
        mode=="check" && return
    end
    function fg!(F,G,x)
        val,gg,_,_=evaluate(x;gradient=G!==nothing)
        G!==nothing && (G.=-gg)
        F!==nothing ? -val : nothing
    end
    result=Optim.optimize(Optim.NLSolversBase.only_fg!(fg!),c,Optim.LBFGS(m=15),
        Optim.Options(iterations=maxiter,g_abstol=1e-5,f_reltol=0.,x_abstol=0.,show_trace=false))
    cfinal=Optim.minimizer(result);finval,fingrad,findiag,finfield=evaluate(cfinal)
    summary=Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
        "N"=>N,"T0_fs"=>T0,"start"=>startname,"f_zs"=>finval,"best_f_zs"=>best[],
        "gradient_norm"=>norm(fingrad),"gradient_max"=>maximum(abs,fingrad),"iterations"=>Optim.iterations(result),
        "calls"=>calls[],"converged"=>Optim.converged(result),"termination"=>string(result),
        "coefficients"=>M,"nt"=>nt,"width"=>width,"dt_fs"=>dt*T0,"h"=>dz,
        "elapsed_s"=>time()-started,"objective"=>"piecewise-constant ZS eigenvalue", "diag"=>findiag)
    open(joinpath(OUT,tag*"_summary.toml"),"w") do io;TOML.print(io,summary);end
    writedlm(joinpath(OUT,tag*"_finalcoef.csv"),cfinal,',')
    TOML.print(stdout,summary)
end
if abspath(PROGRAM_FILE)==@__FILE__
    N=parse(Float64,ARGS[1]);T=parse(Float64,ARGS[2]);start=ARGS[3];mode=length(ARGS)>3 ? ARGS[4] : "opt"
    run(N,T,start;mode,maxiter=parse(Int,get(ENV,"MAXITER","200")),nt=parse(Int,get(ENV,"NT","8192")),
        hfac=parse(Float64,get(ENV,"HFAC","1")))
end
