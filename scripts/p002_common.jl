# agent: gpt-a; model: gpt-6-astra; family: gpt
# Task-local model adapters; the solver source and pin are unchanged.
using PulsePropagation, FFTW, LinearAlgebra, TOML, NPZ, Printf, SHA
const PP = PulsePropagation
BLAS.set_num_threads(1); FFTW.set_num_threads(1)
const MATERIAL_RAW = "~/analytical-nl-discovery-data/2026-10-04-gpt-a-material"
const MAT = TOML.parsefile(joinpath(MATERIAL_RAW,"material.toml"))
const ARR = npzread(joinpath(MATERIAL_RAW,"material.npz"))
const T0 = MAT["T0_ps"]
const LD = MAT["LD_m"]
const P0 = MAT["P0_W"]
const W0 = MAT["omega0_rad_ps"]
const KAPPA = MAT["n2_m2_W"]*W0/2.99792458e-4
const HBAR = 6.62607015e-34/(2pi)

struct Round1Response{R} <: PP.AbstractRamanResponse
    base::R
    fraction::Float64
end
Round1Response(r) = Round1Response(r,r isa NoRaman ? 0. : Float64(r.fraction))

# Analytic Fourier transforms avoid under-resolving a 12.2 fs oscillator.
function PP._mmgnlse_raman_kernels(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:Round1Response}
    r=p.raman.base
    r isa NoRaman && return (ha=ComplexF64[],hb=ComplexF64[],fraction=0.)
    nt=p.domain.time_grid.nt; omega=PP._mmgnlse_raw_omega(p)
    aa=1/r.tau2 .- im .* omega
    osc=(1/r.tau1^2+1/r.tau2^2)./(aa.^2 .+ 1/r.tau1^2)
    if r isa AgarwalRaman
        ha=osc; hb=zeros(ComplexF64,nt)
    else
        ab=1/r.taub .- im .* omega
        boson=2 ./ (r.taub .* ab) .- 1 ./ (r.taub^2 .* ab.^2)
        ha=r.fa .* osc; hb=r.fc .* osc .+ r.fb .* boson
    end
    if iseven(nt)
        ha[nt÷2+1]=real(ha[nt÷2+1]);hb[nt÷2+1]=real(hb[nt÷2+1])
    end
    (;ha=ComplexF64.(ha),hb=ComplexF64.(hb),fraction=p.raman.fraction)
end

# Exact no-shock prefactor; no spectral damping. The cache is shared by the
# package's forward solver and analytic discrete adjoint.
function PP._mmgnlse_solver_cache(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:Round1Response}
    nt,nm,np=PP._mmgnlse_public_shape(p)
    omega=PP._mmgnlse_raw_omega(p)
    beta_operator=PP._mmgnlse_beta_array(p.beta,nt,nm,np,omega)
    nonlinear_prefactor=fill(1im*p.n2*p.omega0/2.99792458e-4,nt,1,1)
    nonlinear_active=any(!iszero,nonlinear_prefactor) && !PP._mmgnlse_overlap_iszero(p.S)
    (;omega,beta_operator,nonlinear_prefactor,nonlinear_active,raman=PP._mmgnlse_raman_kernels(p))
end

function setup(;r=.01,delta=1.,nm=2,nt=4096,window=320.,zeta=20.,response="none",physical=false,phase=0.,third=0.,thirdphase=0.,rwa=true)
    grid=TimeGrid(nt,window*T0)
    domain=MMGNLSEDomain(degrees_of_freedom(:time,:space),grid)
    S=copy(ARR["S"][1:nm,1:nm,1:nm,1:nm])
    if rwa
        for a in 1:nm,b in 1:nm,c in 1:nm,d in 1:nm
            b+c==a+d || (S[a,b,c,d]=0.)
        end
    end
    beta=zeros(3,nm); beta[3,:].=ARR["beta"][3,1]
    beta[2,:].=(0:nm-1).*delta*T0/LD
    if physical
        beta[3,:].=ARR["beta"][3,1:nm]
        beta[2,:].=ARR["beta"][2,1:nm].-ARR["beta"][2,1]
        gap=ARR["beta"][1,2]-ARR["beta"][1,1]
        beta[1,:].=ARR["beta"][1,1:nm].-ARR["beta"][1,1].-gap.*(0:nm-1)
    end
    ram=response=="none" ? NoRaman() : response=="agarwal" ? AgarwalRaman() : AnisotropicRaman()
    pars=MMGNLSEParameters(domain;length=zeta*LD,beta=TaylorBeta(beta),S,n2=MAT["n2_m2_W"],omega0=W0,raman=Round1Response(ram))
    tau=time_axis(grid)./T0
    a=zeros(ComplexF64,nt,nm,1); a[:,1,1].=sqrt(P0)./cosh.(tau)
    nm>=2 && (a[:,2,1].=sqrt(r*P0).*exp(im*phase)./cosh.(tau))
    nm>=3 && (a[:,3,1].=sqrt(third*P0).*exp(im*thirdphase)./cosh.(tau))
    (;pars,a,tau,grid,r,delta,nm,nt,window,zeta,response,physical,S,beta)
end

capture0(d)=iszero(d) ? 1. : (pi*d/(2sinh(pi*d/2)))^2
function fieldstats(a,p)
    aa=reshape(a,p.nt,p.nm)./sqrt(P0)
    dtau=p.grid.dt/T0
    energies=vec(sum(abs2,aa;dims=1)).*dtau
    peak=p.tau[argmax(abs2.(aa[:,1]))]
    w=fftshift(ifft(aa,1),1)
    se=round(Int,.05p.nt)
    de=Dict{String,Any}("energies"=>energies,"peak_tau"=>peak,
      "temporal_edge_fraction"=>sum(abs2,aa[abs.(p.tau).>.45p.window,:])/sum(abs2,aa),
      "spectral_edge_fraction"=>(sum(abs2,w[1:se,:])+sum(abs2,w[end-se+1:end,:]))/sum(abs2,w))
    if p.nm>=2 && p.r>0
        v=aa[:,2]
        de["mode2_energy_ratio"]=energies[2]/(2p.r)
        for radius in (4,5,6)
            de["capture_fixed_$radius"]=sum(abs2,v[abs.(p.tau).<radius])*dtau/(2p.r)
            de["capture_centered_$radius"]=sum(abs2,v[abs.(p.tau.-peak).<radius])*dtau/(2p.r)
        end
        psi=exp.(-im*p.delta.*p.tau)./cosh.(p.tau)./sqrt(2)
        de["bound_projection"]=abs2(dot(psi,v)*dtau)/(2p.r)
        if p.physical
            b=p.beta[3,2]/p.beta[3,1];sigma=2p.S[1,1,2,2]/p.S[1,1,1,1]
            nu=(sqrt(1+8sigma/b)-1)/2
            phi=exp.(-im*p.delta.*p.tau./b)./cosh.(p.tau).^nu
            phi./=sqrt(sum(abs2,phi)*dtau)
            de["physical_bound_projection"]=abs2(dot(phi,v)*dtau)/(2p.r)
        end
    end
    de
end

function run_capture(out,label;dz=.01,savezetas=[0.,10.,20.],method=RK4IP(),kwargs...)
    p=setup(;kwargs...)
    elapsed=@elapsed sol=solve_mmgnlse(p.a,p.pars,dz*LD;saveat=savezetas.*LD,method)
    rows=Dict{String,Any}[]
    for (j,z) in enumerate(sol.z)
        d=fieldstats(sol.fields[:,:,:,j],p);d["zeta"]=z/LD;push!(rows,d)
    end
    d=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
       "label"=>label,"r"=>p.r,"p2_total"=>p.r/(1+p.r),"delta"=>p.delta,
       "nm"=>p.nm,"nt"=>p.nt,"window_tau"=>p.window,"dzeta"=>dz,
       "response"=>p.response,"physical_dispersion"=>p.physical,"C0"=>capture0(p.delta),
       "elapsed_seconds"=>elapsed,"method"=>string(typeof(method)),"rows"=>rows)
    open(joinpath(out,label*".toml"),"w") do io;TOML.print(io,d);end
    npzwrite(joinpath(out,label*".npz"),Dict("tau"=>p.tau,"zeta"=>sol.z./LD,"fields"=>sol.fields))
    @printf("CAPTURE %s r=%.4g delta=%.6g C5=%.9g proj=%.9g time=%.1fs\n",label,p.r,p.delta,get(last(rows),"capture_fixed_5",NaN),get(last(rows),"bound_projection",NaN),elapsed);flush(stdout)
    GC.gc(); d
end
