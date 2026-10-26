# agent: gpt-a; model: gpt-6-astra; family: gpt
# Directional finite differences of the actual filtered-count observable and
# an independent direct-space check of the rotating-wave reservoir Gram.
include(joinpath(@__DIR__,"p002_noise.jl"))
using Random
out=ARGS[1];mkpath(out);rng=MersenneTwister(20261004)
rows=Dict{String,Any}[]
for response in ("none","anisotropic")
    p=setup(;r=.003,delta=MAT["delta_physical"],response,zeta=2.,nt=1024,window=80.)
    dz=.01LD;sol=solve_mmgnlse(p.a,p.pars,dz)
    weight=p.nt*p.grid.dt*1e-12/(HBAR*W0*1e12)
    mask=Float64.(abs.(frequency_axis(p.grid).*T0).<=1)
    aw=get_spectral_field(sol);terminal=zeros(ComplexF64,size(aw))
    terminal[:,2,1].=weight.*mask.*aw[:,2,1]
    adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,adjoint_mode=:discrete_rk4ip)
    grad=get_spectral_field(adj;units=:power)
    direction=randn(rng,ComplexF64,size(p.a)).*reshape(exp.(-p.tau.^2/8),:,1,1)
    direction./=norm(direction);direction.*=norm(p.a)
    pred=2real(dot(grad,fftshift(ifft(direction,1),1)))
    f(a)=begin
        s=solve_mmgnlse(a,p.pars,dz);w=get_spectral_field(s)
        weight*sum(mask.*abs2.(w[:,2,1]))
    end
    for step in (1e-4,3e-5,1e-5)
        fd=(f(p.a.+step.*direction)-f(p.a.-step.*direction))/(2step)
        push!(rows,Dict("response"=>response,"relative_input_step"=>step,
            "predicted_derivative"=>pred,"finite_difference"=>fd,"relative_error"=>abs(pred-fd)/abs(fd)))
    end
end

# At one temporal sample, direct integration of the physical real-index noise
# susceptibility over transverse space and a uniformly sampled GRIN beat phase.
F=ARR["fields"][:,:,1:2];dx=ARR["x"][2]-ARR["x"][1];dy=ARR["y"][2]-ARR["y"][1]
a=ComplexF64[.7+.2im,-.1+.4im];l=ComplexF64[.3-.5im,.6+.1im]
pairs=[(m,n) for n in 1:2 for m in 1:2]
B=[im*(conj(l[m])*a[n]-l[n]*conj(a[m])) for (m,n) in pairs]
G=[n-m==q-v ? ARR["S"][m,n,v,q] : 0. for (m,n) in pairs,(v,q) in pairs]
contract=real(dot(B,G*B));direct=0.
for phi in (0:63).*2pi/64
    af=sum(F[:,:,m].*a[m].*exp(im*(m-1)*phi) for m in 1:2)
    lf=sum(F[:,:,m].*l[m].*exp(im*(m-1)*phi) for m in 1:2)
    susceptibility=-2imag.(conj.(lf).*af)
    global direct+=sum(abs2,susceptibility)*dx*dy/64
end
d=Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt","seed"=>20261004,
    "directional_count_checks"=>rows,"spatial_phase_averaged_Gram"=>contract,
    "direct_spatial_phase_average"=>direct,"Gram_relative_error"=>abs(contract-direct)/abs(direct),
    "scope"=>"Checks count adjoint and modal reservoir contractions; not an independent open-system quantum derivation.")
open(joinpath(out,"checks.toml"),"w") do io;TOML.print(io,d);end
TOML.print(stdout,d)
