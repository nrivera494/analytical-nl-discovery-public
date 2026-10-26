# agent: gpt-e; model: gpt-6-astra; family: gpt
# Independent harness for the unchanged agents' solver. API usage learned only
# from allowed evaluator code. Constant nonlinear prefactor selects precisely
# the no-shock, no-anti-alias-damping Kerr model being audited.
using PulsePropagation, FFTW, LinearAlgebra, NPZ, TOML
const PP=PulsePropagation
BLAS.set_num_threads(1);FFTW.set_num_threads(1)
Threads.nthreads()<=2 || error("JULIA_NUM_THREADS must be at most two")
struct AuditScalarKerr <: PP.AbstractRamanResponse end
function PP._mmgnlse_raman_kernels(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:AuditScalarKerr}
    (;ha=ComplexF64[],hb=ComplexF64[],fraction=0.)
end
function PP._mmgnlse_solver_cache(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:AuditScalarKerr}
    nt,nm,np=PP._mmgnlse_public_shape(p);omega=PP._mmgnlse_raw_omega(p)
    beta_operator=PP._mmgnlse_beta_array(p.beta,nt,nm,np,omega)
    nonlinear_prefactor=fill(1im*p.n2*p.omega0/2.99792458e-4,nt,1,1)
    nonlinear_active=true
    (;omega,beta_operator,nonlinear_prefactor,nonlinear_active,raman=PP._mmgnlse_raman_kernels(p))
end
function crosscheck(file,steps)
    start=time();data=npzread(file);t=vec(data["t"]);nt=length(t);dt=t[2]-t[1]
    phi=only(data["phi"]);dispersion=only(data["dispersion"])
    gain=haskey(data,"gain") ? only(data["gain"]) : 0.
    grid=TimeGrid(nt,nt*dt);domain=MMGNLSEDomain(degrees_of_freedom(:time),grid)
    @assert maximum(abs.(time_axis(grid).-t))<1e-11
    w0=1200.;p=MMGNLSEParameters(domain;length=1.,alpha=0.,gain=gain,beta=TaylorBeta([0.,0.,dispersion]),
        S=1.,n2=phi*2.99792458e-4/w0,omega0=w0,raman=AuditScalarKerr())
    initial=reshape(data["initial"],nt,1,1);h=1/steps
    sol=solve_mmgnlse(initial,p,h;method=RK4IP(),saveat=1.)
    mean=vec(sol.fields[:,:,:,end]);expected=vec(data["mean"])
    errors=Float64[];norms=Float64[]
    for j in axes(data["readouts"],2)
        q=data["readouts"][:,j]
        terminal=reshape(nt*dt.*fftshift(ifft(q)),nt,1,1)
        adj=solve_adjoint(terminal,p,h;forward_solution=sol,units=:power,saveat=(gain>0 ? h : 1.),
            adjoint_mode=:discrete_rk4ip,checkpoint_stride=25)
        field=get_temporal_field(adj;z=:all)
        gradient=vec(field[:,:,:,1])./(nt*dt)
        variance=sum(abs2,gradient)
        if gain>0
            vs=vec(sum(abs2,field;dims=(1,2,3)))./(nt*dt)^2
            variance+=gain*sum((vs[1:end-1].+vs[2:end]).*diff(adj.z)./2)
        end
        push!(norms,variance);push!(errors,variance/data["variances"][j]-1)
    end
    row=Dict("agent"=>"gpt-e","model"=>"gpt-6-astra","family"=>"gpt","file"=>file,
        "steps"=>steps,"phi"=>phi,"dispersion"=>dispersion,"gain"=>gain,"n"=>nt,
        "mean_relative_error"=>norm(mean-expected)/norm(expected),
        "adjoint_variances"=>norms,"relative_variance_errors"=>errors,"seconds"=>time()-start)
    outfile=replace(file,".npz"=>"_rk4ip_$(steps).toml")
    open(outfile,"w") do io;TOML.print(io,row);end
    TOML.print(stdout,row);flush(stdout)
end
crosscheck(ARGS[1],parse(Int,ARGS[2]))
