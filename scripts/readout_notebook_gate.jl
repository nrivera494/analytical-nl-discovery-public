# agent: gpt-a; model: gpt-6-astra; family: gpt
# Gate full-covariance normalization against the squeezing notebook's
# SpectralPhotonNumber terminal condition and discrete adjoint. Four disjoint
# pieces of its supplied binary filter are contracted separately, then summed.
using DelimitedFiles

function notebook_gate(out;nt=4096,window=12.288,steps=10000,bath_intervals=100)
    started=time(); label="notebook_discrete_gate"
    file=joinpath(out,label)
    isfile(file*".toml") && return println("REUSE ",label)
    wavelength=1550.0; omega0=2pi*C_R/(wavelength*1e-9)
    gamma=2.3e-20*omega0/C_R/(pi*(9.2e-6/2)^2)
    c=Dict{String,Any}("label"=>label,"nt"=>nt,"window_ps"=>window,
        "T0_ps"=>0.22/(2acosh(sqrt(2))),"wavelength_nm"=>wavelength,
        "gamma_per_W_m"=>gamma,"peak_power_W"=>3655.7,"length_m"=>10.0,
        "beta2_ps2_per_m"=>-0.0206,"beta3_ps3_per_m"=>8.1038e-5,
        "steps"=>steps,"raman"=>true,"public_model"=>true,"pulse"=>"sech")
    p=readout_setup(c); dz=10.0/steps
    zs=collect(range(0.0,10.0;length=bath_intervals+1))
    sol=solve_mmgnlse(p.a,p.pars,dz;saveat=zs)
    oldmask=zeros(4096)
    filterfile=joinpath(@__DIR__,"..","solver","example_notebooks","benchmark_data","squeezing_spectral_filter","optimal_filter.csv")
    oldmask[1196:2371].=reverse(vec(readdlm(filterfile)))
    # The notebook grid is 4096 points / 50 ps. Nearest old frequency pixel,
    # with zero transmission outside that grid, preserves its physical mask.
    omega=frequency_axis(p.grid)
    oldindex=round.(Int,omega./(2pi/50)).+2049
    mask=[1<=i<=4096 ? oldmask[i] : 0.0 for i in oldindex]
    passed=findall(>(0.5),mask)
    groups=[passed[round(Int,(j-1)*length(passed)/4)+1:round(Int,j*length(passed)/4)] for j in 1:4]
    masks=[Float64.(in.(collect(1:nt),Ref(ids))) for ids in groups]
    push!(masks,mask)
    G=zeros(ComplexF64,nt,5); B=zeros(ComplexF64,nt*length(zs),5); means=zeros(5)
    Cw=raman_langevin_spectrum_coth(nt,p.grid.dt,p.omega0/(2pi),p.gamma;temperature_K=300.0)
    zw=fill(10.0/bath_intervals,length(zs));zw[1]/=2;zw[end]/=2
    for j in 1:5
        obs=SpectralPhotonNumber(filter=masks[j])
        means[j]=value(obs,sol)
        terminal=terminal_condition(obs,sol)./sqrt(means[j])
        adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,
            saveat=zs,adjoint_mode=:discrete_rk4ip,checkpoint_stride=100)
        G[:,j].=vec(get_spectral_field(adj;units=:power))./sqrt.(p.weight)
        lt=reshape(get_temporal_field(adj;z=:all,units=:power),nt,:)
        for k in eachindex(zs)
            at=vec(@view sol.fields[:,:,:,k])
            response=-2 .* imag.(at.*conj.(@view lt[:,k]))./nt
            B[(k-1)*nt+1:k*nt,j].=fft(response).*sqrt.(Cw.*(p.gamma^2/(nt*p.grid.dt*1e-12)*zw[k]))
        end
        @printf("NOTEBOOK gate row %d/5 %.1fs\n",j,time()-started);flush(stdout)
    end
    Qvac=real.(G'*G);Qbath=real.(B'*B);Q=Qvac+Qbath
    u=sqrt.(means[1:4]./sum(means[1:4])); matrix_F=dot(u,Q[1:4,1:4]*u)
    report=Dict{String,Any}("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
        "config"=>c,"matrix_F"=>matrix_F,"notebook_direct_F"=>Q[5,5],
        "absolute_error"=>abs(matrix_F-Q[5,5]),"direct_vacuum_F"=>Qvac[5,5],
        "direct_Raman_F"=>Qbath[5,5],"dt_fs"=>p.grid.dt*1e3,
        "filter_bins"=>length(passed),"filter_source_sha256"=>bytes2hex(sha256(read(filterfile))),
        "bath_intervals"=>bath_intervals,"elapsed_seconds"=>time()-started,
        "status"=>"discrete normalization regression; this gate is not a converged reference-table point",
        "public_model_caveat"=>"public shock/taper; notebook's unshocked Raman coupling; retained only for API comparison")
    abs(matrix_F-Q[5,5]) < 1e-8 || error("Notebook covariance/direct gate failed")
    npzwrite(file*".npz",Dict("covariance"=>Q,"vacuum"=>Qvac,"bath"=>Qbath,"mean_photons"=>means,
        "omega_rad_ps"=>omega,"filter"=>mask))
    open(file*".toml","w") do io;TOML.print(io,report);end
    @printf("NOTEBOOK PASS F=%.10g error=%.3g %.1fs\n",matrix_F,report["absolute_error"],time()-started);flush(stdout)
    GC.gc()
end
