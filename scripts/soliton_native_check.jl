# Scalar soliton checks using the agents' solver and its discrete RK4IP adjoint.
# agent: gpt-b; model: gpt-6-astra; family: gpt
using PulsePropagation, FFTW, LinearAlgebra, DelimitedFiles, TOML, Printf
BLAS.set_num_threads(2)
cfg = TOML.parsefile(ARGS[1])
solver_commit = readchomp(`git -C solver rev-parse HEAD`)
solver_dirty = !isempty(readchomp(`git -C solver status --porcelain`))
solver_dirty && error("Native evidence requires a clean, recorded agents' solver checkout")
dest = cfg["raw_location"]; mkpath(dest)
include(cfg["raman_helper"])
nt = cfg["nt"]; T0 = cfg["T0_ps"]; window = cfg["window_over_T0"] * T0
zeta = cfg["z_over_LD"]; b2 = cfg["beta2_ps2_per_m"]
LD = T0^2/abs(b2); L = LD*zeta; dz=L/cfg["nsteps"]
c_light=2.99792458e-4; omega0=2π*c_light/(cfg["lambda0_nm"]*1e-9)
aeff=π*(9.2e-6/2)^2; n2=2.3e-20; gamma=n2*omega0/c_light/aeff
if get(cfg,"suppress_shock",false)
    n2 *= omega0/1e12; omega0=1e12
end
P0=1/(gamma*LD)
grid=TimeGrid(nt,window); t=time_axis(grid); omega=frequency_axis(grid)
domain=MMGNLSEDomain(degrees_of_freedom(:time),grid)
fr=cfg["raman_fraction"]
raman = fr == 0 ? NoRaman() : AgarwalRaman(fraction=fr)
beta=reshape([0.,0.,b2,cfg["beta3_ps3_per_m"]],:,1)
pars=MMGNLSEParameters(domain;length=L,beta=TaylorBeta(beta),S=1/aeff,n2,omega0,raman)
initial=zeros(ComplexF64,nt,1,1)
if get(cfg,"launch","sech") == "gaussian"
    initial[:,1,1] .= sqrt(P0)*get(cfg,"N",1.)*exp.(-0.5*(t/T0).^2)
else
    initial[:,1,1] .= sqrt(P0)*get(cfg,"N",1.)*sech.(t/T0)
end
cache=PulsePropagation._mmgnlse_solver_cache(pars)
C=fr==0 ? zeros(nt) : raman_langevin_spectrum_coth(nt,grid.dt,omega0/(2π),gamma;
    raman_fraction=fr,temperature_K=cfg["temperature_K"])
hbar=1.054571817e-34
S=C*gamma/(hbar*omega0*1e12)
R=fr==0 ? ones(ComplexF64,nt) : (1-fr).+fr.*(cache.raman.ha.+cache.raman.hb)
writedlm(joinpath(dest,"native_kernels.csv"),hcat(cache.omega*T0,real(R),imag(R),S,
    real(vec(cache.nonlinear_prefactor)/(1im*n2*omega0/c_light))),',')
if get(cfg,"export_only",false)
    println("exported kernels to ",dest);exit()
end
tstart=time()
nsave=get(cfg,"source_slices",200)
stride=max(1,cfg["nsteps"]÷nsave)
saveat=collect(0:stride:cfg["nsteps"]).*dz
last(saveat)!=L && push!(saveat,L)
sol=solve_mmgnlse(initial,pars,dz;saveat=saveat)
writedlm(joinpath(dest,"native_mean.csv"),hcat(t/T0,real(vec(sol.fields[:,:,:,end]))/sqrt(P0),imag(vec(sol.fields[:,:,:,end]))/sqrt(P0)),',')
maskfile=get(cfg,"mask_file","")
if isempty(maskfile)
    masks=hcat(ones(nt),Float64.(abs.(omega*T0).<get(cfg,"edge",.7368)))
else
    masks=readdlm(maskfile,',',Float64)
end
rows=Vector{Dict{String,Any}}()
for col in axes(masks,2)
    obs=SpectralPhotonNumber(filter=masks[:,col]); n=value(obs,sol)
    adj=solve_adjoint(terminal_condition(obs,sol),pars,dz;forward_solution=sol,
        saveat=saveat,adjoint_mode=:discrete_rk4ip)
    Fvac=sum(abs2,get_spectral_field(adj;units=:photon)[:,:,1])/n
    A=get_temporal_field(sol;z=:all,units=:power)
    lw=get_spectral_field(adj;z=:all,units=:power)
    lam=fft(ifftshift(lw.*reshape(1 .+omega/omega0,:,1,1,1),1),1)
    B=-2imag.(A.*conj.(lam))
    bw=ifft(B,1)
    # The helper already returns raw FFT ordering. Integrate with trapezoid
    # endpoint weights; the source quadrature is refined independently.
    profile=vec(sum(abs2.(bw).*reshape(C,:,1,1,1),dims=(1,2,3)))
    integral=sum(diff(adj.z).*(profile[1:end-1].+profile[2:end])/2)
    FR=gamma^2*integral*(1e12/window)/n
    row=Dict{String,Any}("mask_column"=>col,"mean_photons"=>n,"F_vacuum"=>Fvac,
        "F_Raman"=>FR,"F_total"=>Fvac+FR,"dB"=>10log10(Fvac+FR))
    push!(rows,row);println(row);flush(stdout)
end
out=Dict("agent"=>"gpt-b","model"=>"gpt-6-astra","family"=>"gpt",
    "solver_commit"=>solver_commit,"solver_dirty"=>solver_dirty,
    "wall_time_s"=>time()-tstart,"dt_fs"=>1000*grid.dt,"dz_m"=>dz,
    "adjoint_mode"=>"discrete_rk4ip","P0_W"=>P0,"L_m"=>L,"rows"=>rows)
open(joinpath(dest,"native_summary.toml"),"w") do io;TOML.print(io,out);end
