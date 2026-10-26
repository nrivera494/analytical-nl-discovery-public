# agent: gpt-a; model: gpt-6-astra; family: gpt
# T-20261010-claude-interactive-03: full scalar spectral covariance from
# discrete RK4IP adjoint rows. No files in the solver submodule are changed.
using PulsePropagation, FFTW, LinearAlgebra, TOML, NPZ, Printf, SHA
const PP = PulsePropagation
const HBAR_R = 1.054571817e-34
const C_R = 2.99792458e-4 # m/ps
BLAS.set_num_threads(1)
FFTW.set_num_threads(1)
Threads.nthreads() <= 2 || error("At most two Julia threads are authorized")

# Opt-in evaluator adapter: the envelope/no-shock model uses a constant
# photon energy and has no artificial high-frequency nonlinear taper.
# The sampled Raman response itself is the package response, unchanged.
struct ReadoutResponse{R} <: PP.AbstractRamanResponse
    base::R
    fraction::Float64
end
ReadoutResponse(r) = ReadoutResponse(r, r isa NoRaman ? 0.0 : Float64(r.fraction))
function PP._mmgnlse_raman_kernels(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:ReadoutResponse}
    n = p.domain.time_grid.nt
    r = p.raman.base
    r isa NoRaman && return (ha=ComplexF64[], hb=ComplexF64[], fraction=0.0)
    dt = p.domain.time_grid.dt
    response = PP.raman_response(r, dt .* collect(0:n-1))
    (ha=ComplexF64.(ifft(response.ha) .* (n*dt)),
     hb=ComplexF64.(ifft(response.hb) .* (n*dt)), fraction=p.raman.fraction)
end
function PP._mmgnlse_solver_cache(p::PP.MMGNLSEParameters{D,T,A,G,B,O,N,W,R}) where {D,T,A,G,B,O,N,W,R<:ReadoutResponse}
    n,nm,np = PP._mmgnlse_public_shape(p)
    omega = PP._mmgnlse_raw_omega(p)
    beta_operator = PP._mmgnlse_beta_array(p.beta,n,nm,np,omega)
    nonlinear_prefactor = fill(1im*p.n2*p.omega0/C_R,n,1,1)
    nonlinear_active = any(!iszero,nonlinear_prefactor) && !PP._mmgnlse_overlap_iszero(p.S)
    (;omega,beta_operator,nonlinear_prefactor,nonlinear_active,raman=PP._mmgnlse_raman_kernels(p))
end

function readout_setup(c)
    n = Int(c["nt"]); window = c["window_ps"]; t0 = c["T0_ps"]
    grid = TimeGrid(n,window)
    domain = MMGNLSEDomain(degrees_of_freedom(:time),grid)
    omega0 = 2pi*C_R/(c["wavelength_nm"]*1e-9)
    gamma = c["gamma_per_W_m"]; n2 = get(c,"n2_m2_per_W",2.3e-20)
    overlap = gamma*C_R/(n2*omega0)
    response = get(c,"raman",false) ? AgarwalRaman() : NoRaman()
    public_model = get(c,"public_model",false)
    raman = public_model ? response : ReadoutResponse(response)
    beta = reshape([0.0,0.0,c["beta2_ps2_per_m"],get(c,"beta3_ps3_per_m",0.0)],:,1)
    pars = MMGNLSEParameters(domain;length=c["length_m"],beta=TaylorBeta(beta),
        S=overlap,n2,omega0,raman)
    t = time_axis(grid)
    profile = get(c,"pulse","gaussian") == "sech" ? sech.(t./t0) : exp.(-0.5 .* (t./t0).^2)
    a = reshape(ComplexF64.(sqrt(c["peak_power_W"]).*profile),n,1,1)
    weight = public_model ? photon_weights(grid,omega0) : fill(n*grid.dt*1e-12/(HBAR_R*omega0*1e12),n)
    all(isfinite,weight) && all(>(0),weight) || error("Nonpositive photon weight")
    (;n,grid,pars,a,t,t0,omega0,gamma,weight)
end

function covariance_case(c,out;only_columns=0)
    label=c["label"]; file=joinpath(out,label)
    isfile(file*".toml") && isfile(file*".npz") && get(c,"reuse",true) && return println("REUSE ",label)
    p=readout_setup(c); n=p.n; steps=Int(c["steps"]); dz=c["length_m"]/steps
    started=time()
    sol=solve_mmgnlse(p.a,p.pars,dz;saveat=:steps)
    aw=vec(get_spectral_field(sol)); phase=exp.(1im.*angle.(aw))
    nbar=p.weight.*abs2.(aw)
    bath=get(c,"raman",false)
    wanted=Int(get(c,"bath_intervals",32))
    sample=unique(round.(Int,range(1,length(sol.z);length=min(wanted+1,length(sol.z)))))
    zs=sol.z[sample]; zw=zeros(length(zs)); zw[1:end-1].+=diff(zs)./2; zw[2:end].+=diff(zs)./2
    Cw=bath ? raman_langevin_spectrum_coth(n,p.grid.dt,p.omega0/(2pi),p.gamma;temperature_K=300.0) : zeros(n)
    ncols=only_columns>0 ? min(only_columns,2n) : 2n
    G=zeros(ComplexF64,n,ncols)
    B=bath ? zeros(ComplexF64,n*length(zs),ncols) : zeros(ComplexF64,0,ncols)
    complete=Threads.Atomic{Int}(0)
    # A function scope is essential here: reusing names such as `terminal`
    # in the later scalar check would otherwise box/share them across threads.
    function fill_column(j)
        local bin, terminal, adj, lt, at, response, done
        bin=mod1(j,n); terminal=zeros(ComplexF64,n,1,1)
        terminal[bin]=sqrt(p.weight[bin])*phase[bin]*(j>n ? 1im : 1.0)
        adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,
            saveat=bath ? zs : [0.0,c["length_m"]],
            adjoint_mode=:discrete_rk4ip,checkpoint_stride=32)
        G[:,j].=vec(get_spectral_field(adj;units=:power))./sqrt.(p.weight)
        if bath
            maximum(abs.(adj.z.-zs)) < 1e-10 || error("Bath/adjoint grid mismatch")
            lt=reshape(get_temporal_field(adj;z=:all,units=:power),n,:)
            for k in eachindex(zs)
                at=vec(@view sol.fields[:,:,:,sample[k]])
                response=-2 .* imag.(at.*conj.(@view lt[:,k]))./n
                B[(k-1)*n+1:k*n,j].=fft(response).*sqrt.(Cw.*(p.gamma^2/(n*p.grid.dt*1e-12)*zw[k]))
            end
        end
        done=Threads.atomic_add!(complete,1)+1
        if done%32==0 || done==ncols
            @printf("ROWS %s %d/%d %.1fs\n",label,done,ncols,time()-started);flush(stdout)
        end
    end
    Threads.@threads :static for j in 1:ncols
        fill_column(j)
    end
    Vvac=real.(G'*G); Vbath=real.(B'*B); V=Vvac+Vbath
    # One independently contracted filter, using the same notebook observable
    # and public discrete-adjoint API. No covariance rows enter this contraction.
    mask=Float64.(abs.(frequency_axis(p.grid).*p.t0).<=1.5)
    mean_filter=dot(mask,nbar)
    terminal=reshape(p.weight.*mask.*aw,n,1,1)
    adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,
        saveat=bath ? zs : [0.0,c["length_m"]],adjoint_mode=:discrete_rk4ip,checkpoint_stride=32)
    direct_vac=sum(abs2.(vec(get_spectral_field(adj;units=:power)))./p.weight)/mean_filter
    direct_bath=0.0
    if bath
        lt=reshape(get_temporal_field(adj;z=:all,units=:power),n,:)
        for k in eachindex(zs)
            at=vec(@view sol.fields[:,:,:,sample[k]])
            b=-2 .* imag.(at.*conj.(@view lt[:,k]))
            direct_bath+=p.gamma^2*sum(abs2.(ifft(b)).*Cw)/(n*p.grid.dt*1e-12)*zw[k]/mean_filter
        end
    end
    report=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
        "config"=>c,"elapsed_seconds"=>time()-started,"rows"=>ncols,"dt_fs"=>p.grid.dt*1e3,
        "mean_photons"=>sum(nbar),"adjoint_mode"=>"discrete_rk4ip","bath_planes"=>length(zs),
        "direct_filter_F"=>direct_vac+direct_bath,"direct_filter_vacuum"=>direct_vac,
        "direct_filter_Raman"=>direct_bath,
        "temporal_edge_fraction"=>sum(abs2.(vec(sol.fields[:,:,:,end]))[abs.(p.t).>0.45c["window_ps"]])/sum(abs2,sol.fields[:,:,:,end]),
        "spectral_edge_fraction"=>sum(nbar[abs.(frequency_axis(p.grid)).>0.85maximum(abs,frequency_axis(p.grid))])/sum(nbar))
    if ncols==2n
        v=mask.*sqrt.(nbar); v./=norm(v)
        report["covariance_filter_F"]=dot(v,V[1:n,1:n]*v)
        report["filter_contraction_error"]=abs(report["covariance_filter_F"]-report["direct_filter_F"])
        report["lambda_min"]=eigmin(Symmetric(V))
        report["lambda_gen"]=eigmin(Symmetric(V[1:n,1:n]))
        report["full_count_F"]=dot(sqrt.(nbar),V[1:n,1:n]*sqrt.(nbar))/sum(nbar)
    end
    kernels=PP._mmgnlse_raman_kernels(p.pars)
    report["sampled_raman_integral"]=bath ? real(kernels.ha[1]+kernels.hb[1]) : 0.0
    npzwrite(file*".npz",Dict("V"=>V,"Vvac"=>Vvac,"Vbath"=>Vbath,"nbar"=>nbar,
        "mean_spectral"=>aw,"omega_rad_ps"=>frequency_axis(p.grid),"time_ps"=>p.t,
        "mean_temporal"=>vec(sol.fields[:,:,:,end]),"filter"=>mask,"Cw"=>Cw,"bath_z"=>zs))
    open(file*".toml","w") do io;TOML.print(io,report);end
    @printf("DONE %s seconds=%.1f directF=%.9g covarianceF=%.9g\n",label,time()-started,
        report["direct_filter_F"],get(report,"covariance_filter_F",NaN));flush(stdout)
    GC.gc();report
end

if abspath(PROGRAM_FILE)==@__FILE__
    config=TOML.parsefile(ARGS[1]); out=config["raw_location"];mkpath(out)
    include(joinpath(out,"raman_bath_spectrum.jl"))
    for c in config["cases"]
        covariance_case(c,out;only_columns=Int(get(config,"only_columns",0)))
    end
end
