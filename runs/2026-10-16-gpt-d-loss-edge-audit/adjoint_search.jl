# Auditor's spectral-mask search. gpt-d / gpt-6-astra / gpt.
# Fixed Float64 RK4IP, explicitly discrete adjoint, identical nominal step.
using PulsePropagation, FFTW, NPZ, TOML, LinearAlgebra, Random, Optim
BLAS.set_num_threads(1);FFTW.set_num_threads(2)
raw=ARGS[1];d=npzread(joinpath(raw,"inputs.npz"));scalar(k)=Float64(d[k])
A=ComplexF64.(d["A"]);nt=length(A);grid=TimeGrid(nt,scalar("window"));om=vec(d["Om"])
domain=MMGNLSEDomain(degrees_of_freedom(:time);time_grid=grid)
params=MMGNLSEParameters(domain;length=scalar("L"),alpha=vec(d["alpha"]),gain=0.,beta=SampledBeta(om,vec(d["beta"])),S=1/scalar("Aeff"),n2=scalar("n2"),omega0=scalar("omega0"),raman=AgarwalRaman(fraction=scalar("fR"),tau1=scalar("t1"),tau2=scalar("t2")))
Qbase=fftshift(ifft(A));omega=scalar("omega0").+om;dw=om[2]-om[1]
iw=map(w->w>0 ? 1/(1.054571817e-10*w) : 0.,omega);N0=scalar("dt")*nt*sum(abs2.(Qbase).*iw)
# Fractional occupancy of the bin intersecting the physical cutoff.
cutoff=2pi*299.792458/scalar("cutoff"); filt=clamp.((cutoff.-omega)./dw.+.5,0.,1.)
obs=SpectralPhotonNumber(filter=filt,modes=:all)
x=clamp.(om.*scalar("T"),-5.,5.)
B=hcat(x.^2 ./2,x.^3 ./6,x.^4 ./24,exp.(-((x.-1.5)./.8).^2),exp.(-((x.+1.5)./.8).^2))
C=hcat([exp.(-((x.-q)./.8).^2) for q in [-2.,-.7,.7,2.]]...)
softplus(q)=max(q,0.)+log1p(exp(-abs(q)));sigmoid(q)=q>=0 ? 1/(1+exp(-q)) : exp(q)/(1+exp(q))
function masked(v)
 phi=B*v[1:5];atten=C*softplus.(v[6:9]);Qbase.*exp.(im.*phi.-atten)
end
evaluations=Dict{String,Any}[];t0=time();bestJ=-Inf;bestv=zeros(9);bestQ=copy(Qbase)
function evaluate(v;gradient=true,stride=32)
 GC.gc()
 Q=masked(v);At=reshape(fft(ifftshift(Q)),nt,1,1)
 sol=solve_mmgnlse(At,params,scalar("h");method=RK4IP(),precision=:float64,saveat=nothing)
 J=value(obs,sol)/N0
 if !gradient;return J;end
 lam=terminal_condition(obs,sol)./N0
 adj=solve_adjoint(lam,params,scalar("h");forward_solution=sol,adjoint_mode=:discrete_rk4ip,checkpoint_stride=stride,units=:power,saveat=nothing)
 gq=vec(get_spectral_field(adj;z=:initial,units=:power));g=zeros(9)
 for k in 1:5;g[k]=2real(sum(conj.(gq).*im.*Q.*B[:,k]));end
 for k in 1:4;g[k+5]=-2real(sum(conj.(gq).*Q.*C[:,k]))*sigmoid(v[k+5]);end
 push!(evaluations,Dict("evaluation"=>length(evaluations)+1,"eta"=>J,"gradient_norm"=>norm(g),"elapsed_s"=>time()-t0))
 global bestJ,bestv,bestQ
 if J>bestJ;bestJ=J;bestv=copy(v);bestQ=copy(Q);npzwrite(joinpath(raw,"best_masked_input.npz"),Dict("Q"=>Q,"omega"=>omega,"v"=>v));end
 println("evaluation=",length(evaluations)," eta=",J," grad=",norm(g));flush(stdout)
 open(joinpath(raw,"progress.toml"),"w") do io
  TOML.print(io,Dict("evaluations"=>evaluations,"best_eta"=>bestJ,"best_coefficients"=>bestv,"completed"=>false))
 end
 return J,g
end
v0=vcat(zeros(5),fill(-20.,4));baseline=evaluate(v0;gradient=false)
rng=MersenneTwister(101);vt=vcat(.1randn(rng,5),fill(-5.,4));dir=randn(rng,9);dir./=norm(dir)
Jt,gt=evaluate(vt);epsfd=1e-4;fd=(evaluate(vt.+epsfd.*dir;gradient=false)-evaluate(vt.-epsfd.*dir;gradient=false))/(2epsfd)
ad=dot(gt,dir);rel=abs(fd-ad)/max(abs(fd),abs(ad),1e-12)
println("directional relative error=",rel);@assert rel<1e-3
_,g64=evaluate(vt;stride=64);checkpoint_difference=norm(gt-g64)/max(norm(gt),1e-15)
starts=Dict{String,Any}[]
for seed in [101,203,307]
 startrng=MersenneTwister(seed);v=vcat(seed==101 ? zeros(5) : .3randn(startrng,5),fill(seed==307 ? -4. : -6.,4))
 cached_v=Ref{Any}(nothing);cached_value=Ref{Any}(nothing)
 function cached(q)
  if cached_v[]===nothing || q!=cached_v[]
   cached_value[]=evaluate(q);cached_v[]=copy(q)
  end
  return cached_value[]
 end
 objective(q)=-cached(q)[1]
 gradient!(G,q)=(G.=-cached(q)[2])
 res=optimize(objective,gradient!,v,LBFGS(),Optim.Options(iterations=12,g_tol=1e-6,f_reltol=0.,x_abstol=0.,show_trace=false))
 push!(starts,Dict("seed"=>seed,"eta"=>-Optim.minimum(res),"iterations"=>Optim.iterations(res),"converged"=>Optim.converged(res),"minimizer"=>Optim.minimizer(res)))
end
out=Dict("agent"=>"gpt-d","model"=>"gpt-6-astra","family"=>"gpt","solver_commit"=>"b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa","baseline_eta"=>baseline,"best_eta"=>bestJ,"best_coefficients"=>bestv,"fractional_improvement"=>bestJ/baseline-1,"directional_fd"=>fd,"directional_adjoint"=>ad,"directional_relative_error"=>rel,"checkpoint_gradient_difference"=>checkpoint_difference,"starts"=>starts,"evaluations"=>evaluations,"wall_s"=>time()-t0,"adjoint_mode"=>"discrete_rk4ip","dz_forward"=>scalar("h"),"dz_adjoint"=>scalar("h"))
open(joinpath(raw,"metrics.toml"),"w") do io;TOML.print(io,out);end
println("Completed: baseline=",baseline," best=",bestJ)
