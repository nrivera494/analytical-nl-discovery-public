# agent: gpt-a; model: gpt-6-astra; family: gpt
# Material/overlap calibration only: no propagation or capture-law evaluation.
using PulsePropagation, LinearAlgebra, FFTW, TOML, NPZ
const PP = PulsePropagation
BLAS.set_num_threads(1)
FFTW.set_num_threads(1)
out = ARGS[1]
mkpath(out)
fiber = GRIN(;lambda0=1550e-9,core_radius=31.25e-6,NA=0.275)
material = Silica(;n2=2.3e-20,raman=NoRaman())
labels = [(family=:LP,l=0,m=j,p=j-1,order=2(j-1),parity=:axisymmetric) for j in 1:4]
offsets,omega0 = PP._dispersion_offsets(fiber.lambda0,5,35.,13)
x,y = PP._analytic_grid(fiber,labels;grid_size=129,grid_half_width=nothing)
fields = PP._grin_fields(fiber,material,labels,:LP,x,y)
samples = PP._analytic_beta_samples(fiber,material,labels,offsets,omega0)
beta = PP._fit_taylor_beta(offsets,samples,5,12).coefficients
S = PP._spatial_overlap(fields,x,y).values
T0 = 0.4/(2acosh(sqrt(2.)))
LD = T0^2/abs(beta[3,1])
gamma = material.n2*omega0/2.99792458e-4*S[1,1,1,1]
delta = (beta[2,2]-beta[2,1])*T0/abs(beta[3,1])
# Independent radial Simpson quadrature; x is the Laguerre radial coordinate.
xx=collect(range(0.,30.;length=120001)); dx=xx[2]-xx[1]
L=hcat(ones(length(xx)),1 .- xx,1 .- 2xx .+ xx.^2/2,1 .- 3xx .+ 1.5xx.^2 .- xx.^3/6)
sw=ones(length(xx));sw[2:2:end-1].=4;sw[3:2:end-2].=2
integ(v)=sum(sw.*v)*dx/3
ideal=zeros(4,4,4,4)
for a in 1:4,b in 1:4,c in 1:4,d in 1:4
    ideal[a,b,c,d]=2integ(exp.(-2xx).*L[:,a].*L[:,b].*L[:,c].*L[:,d])
end
d=Dict("agent"=>"gpt-a","model"=>"gpt-6-astra","family"=>"gpt",
 "T0_ps"=>T0,"LD_m"=>LD,"gamma_W_m"=>gamma,"P0_W"=>1/(gamma*LD),
 "delta_physical"=>delta,"omega0_rad_ps"=>omega0,"n2_m2_W"=>material.n2,
 "sigma_archive"=>2S[1,1,2,2]/S[1,1,1,1],"self02_archive"=>S[2,2,2,2]/S[1,1,1,1],
 "sigma_ideal_quadrature"=>2ideal[1,1,2,2],"self02_ideal_quadrature"=>ideal[2,2,2,2],
 "mixing_01030202_ideal"=>ideal[1,2,2,3],
 "beta2_ps2_m"=>vec(beta[3,:]),"beta1_ps_m"=>vec(beta[2,:]),
 "beta0_per_m"=>vec(beta[1,:]),"S01010101_per_m2"=>S[1,1,1,1],
 "beta0_residual_03_per_m"=>beta[1,3]-2beta[1,2]+beta[1,1],
 "beta0_residual_03_dimensionless"=>(beta[1,3]-2beta[1,2]+beta[1,1])*LD,
 "FWM_drive_mismatch_per_m"=>2beta[1,2]-beta[1,1]-beta[1,3],
 "profile_scope"=>"Archive analytic GRIN modes; no measured GIF625 profile supplied",
 "ideal_quadrature_max_error_vs_archive"=>maximum(abs.(ideal.-S./S[1,1,1,1])))
open(joinpath(out,"material.toml"),"w") do io;TOML.print(io,d);end
npzwrite(joinpath(out,"material.npz"),Dict("S"=>S,"ideal"=>ideal,"beta"=>beta,"x"=>x,"y"=>y,"fields"=>fields))
TOML.print(stdout,d)
