# Black-box measurement of solver nonlinear edge damping via four-wave mixing.
# gpt-d / gpt-6-astra / gpt. No implementation internals are read.
using PulsePropagation,FFTW,TOML,LinearAlgebra
BLAS.set_num_threads(1);FFTW.set_num_threads(2)
nt=512;dt=.003;grid=TimeGrid(nt,nt*dt);om=frequency_axis(grid);domain=MMGNLSEDomain(degrees_of_freedom(:time);time_grid=grid)
w0=2pi*2.99792458e-4/1.55e-6;n2=2.6e-20;Aeff=64.51341249011044e-12;h=1e-4
params=MMGNLSEParameters(domain;length=h,alpha=0.,gain=0.,beta=TaylorBeta([0.,0.,0.]),S=1/Aeff,n2=n2,omega0=w0,raman=NoRaman())
rows=Dict{String,Any}[];t0=time()
for fraction in [-.9,-.7,-.4,0.,.4,.7,.85,.95]
 j=clamp(nt÷2+1+round(Int,fraction*(nt÷2)),5,nt-4);Q=zeros(ComplexF64,nt);Q[j-1]=1.;Q[j-2]=1.
 A=reshape(fft(ifftshift(Q)),nt,1,1);sol=solve_mmgnlse(A,params,h;method=RK4IP(),precision=:float64,saveat=nothing)
 out=vec(get_spectral_field(sol));deriv=out[j]/h;expected=im*n2/Aeff*(w0+om[j])/(2.99792458e-4)
 push!(rows,Dict("relative_detuning"=>fraction,"Omega_rad_ps"=>om[j],"absolute_omega_rad_ps"=>w0+om[j],"measured_prefactor_ratio"=>real(deriv/expected),"imaginary_residual"=>imag(deriv/expected)))
end
result=Dict("agent"=>"gpt-d","model"=>"gpt-6-astra","family"=>"gpt","solver_commit"=>"b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa","dt_ps"=>dt,"nt"=>nt,"dz_m"=>h,"wall_s"=>time()-t0,"records"=>rows)
open(ARGS[1],"w") do io;TOML.print(io,result);end
println(rows)
