# agent: gpt-a; model: gpt-6-astra; family: gpt
# Independent quantum-channel limit for the reservoir prefactor. No fitting.
include(joinpath(@__DIR__,"p002_noise.jl"))

function cw_check(response,sign,r,zeta,temperature)
    p=setup(;r,delta=0.,response,zeta,nt=64,window=40.)
    harmonic=4;omega_abs=2pi*harmonic/(p.window*T0)
    p.a[:,1,1].=sqrt(P0)
    p.a[:,2,1].=sqrt(r*P0).*exp.(sign*2pi*im*harmonic.*p.tau./p.window)
    dz=.0001LD;spacing=.001LD
    sol=solve_mmgnlse(p.a,p.pars,dz;saveat=spacing)
    weight=p.nt*p.grid.dt*1e-12/(HBAR*W0*1e12)
    initial=fftshift(ifft(p.a,1),1)
    aw=get_spectral_field(sol)
    n0=weight*sum(abs2,initial[:,2,1]);nout=weight*sum(abs2,aw[:,2,1]);gain=nout/n0
    terminal=zeros(ComplexF64,size(aw));terminal[:,2,1].=weight.*aw[:,2,1]./sqrt(nout)
    adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,
        saveat=spacing,adjoint_mode=:discrete_rk4ip,checkpoint_stride=20)
    optical=sum(abs2,get_spectral_field(adj;units=:power))/weight
    @assert maximum(abs.(adj.z.-sol.z))<1e-9
    at=reshape(sol.fields,p.nt,2,:);lt=reshape(get_temporal_field(adj;z=:all,units=:power),p.nt,2,:)
    pairs=[(m,n) for n in 1:2 for m in 1:2]
    G=[n-m==q-v ? ARR["S"][m,n,v,q] : 0. for (m,n) in pairs,(v,q) in pairs]
    ge=eigen(Symmetric(G));root=ge.vectors*Diagonal(sqrt.(max.(ge.values,0.)))
    C=bath_spectrum(p;temperature);zw=zeros(length(sol.z));zw[1:end-1].+=diff(sol.z)./2;zw[2:end].+=diff(sol.z)./2
    bath=0.;B=zeros(ComplexF64,p.nt,4)
    for iz in eachindex(sol.z)
        for (a,(m,n)) in enumerate(pairs)
            B[:,a].=im.*(conj.(lt[:,m,iz]).*at[:,n,iz].-lt[:,n,iz].*conj.(at[:,m,iz]))./p.nt
        end
        Bw=fft(B,1)*root
        bath+=sum(abs2.(Bw).*C)*(KAPPA^2/(p.nt*p.grid.dt)*1e12*zw[iz])
    end
    thermal=iszero(temperature) ? 0. : 1/expm1(HBAR*omega_abs*1e12/(1.380649e-23*temperature))
    # Bright coherent probe, undepleted classical CW pump, thermal bosonic
    # amplifier/attenuator: optical=G; bath=(2*n_th+1)*abs(G-1).
    expected_bath=(2thermal+1)*abs(gain-1)
    kernels=PP._mmgnlse_raman_kernels(p.pars)
    h=kernels.fraction.*(kernels.ha.+kernels.hb)
    k=argmin(abs.(abs.(PP._mmgnlse_raw_omega(p.pars)).-omega_abs))
    expected_abs_log_gain=2ARR["S"][1,1,2,2]/ARR["S"][1,1,1,1]*abs(imag(h[k]))*zeta
    Dict("response"=>response,"temporal_frequency_sign"=>sign,"r"=>r,"zeta"=>zeta,
        "omega_abs_rad_ps"=>omega_abs,"temperature_K"=>temperature,"thermal_occupation"=>thermal,"gain"=>gain,
        "F_optical"=>optical,"F_Raman"=>bath,"F_total"=>optical+bath,
        "predicted_F_Raman"=>expected_bath,"predicted_F_total"=>gain+expected_bath,
        "relative_bath_error"=>abs(bath-expected_bath)/expected_bath,
        "optical_minus_gain"=>optical-gain,"predicted_abs_log_gain"=>expected_abs_log_gain,
        "relative_gain_exponent_error"=>abs(abs(log(gain))-expected_abs_log_gain)/expected_abs_log_gain,
        "mean_photons_02_input"=>n0)
end

out=ARGS[1];mkpath(out);started=time();rows=Dict{String,Any}[]
for response in ("agarwal","anisotropic"),sign in (-1,1),r in (1e-6,1e-8),zeta in (.01,.02),temperature in (0.,300.)
    d=cw_check(response,sign,r,zeta,temperature);push!(rows,d)
    @printf("CW %s sign=%d r=%.1e z=%.3f T=%.0f gain=%.9f bath_relative_error=%.4g\n",response,sign,r,zeta,temperature,d["gain"],d["relative_bath_error"]);flush(stdout)
end
d=Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt","rows"=>rows,
    "elapsed_seconds"=>time()-started,"scope"=>"Periodic CW, two radial modes, undepleted-pump limit of a thermal bosonic amplifier/attenuator; not the pulsed soliton model.")
open(joinpath(out,"cw.toml"),"w") do io;TOML.print(io,d);end
