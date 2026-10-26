# agent: gpt-b; model: gpt-6-astra; family: gpt
# T-20261008-gpt-b-01. Material calibration; no stochastic propagation.
using PulsePropagation, LinearAlgebra, FFTW, TOML, NPZ
const PP = PulsePropagation
BLAS.set_num_threads(1); FFTW.set_num_threads(1)
out = ARGS[1]; mkpath(out)
material = Silica(;n2=2.3e-20,raman=NoRaman())
labels_grin = [(family=:LP,l=0,m=1,p=0,order=0,parity=:axisymmetric),
    (family=:LP,l=0,m=2,p=1,order=2,parity=:axisymmetric),
    (family=:LP,l=1,m=1,p=0,order=1,parity=:cos),
    (family=:LP,l=0,m=3,p=2,order=4,parity=:axisymmetric),
    (family=:LP,l=2,m=1,p=0,order=2,parity=:cos),
    (family=:LP,l=1,m=1,p=0,order=1,parity=:sin)]
if length(ARGS)>1 && ARGS[2]=="extended"
    append!(labels_grin,[(family=:LP,l=1,m=2,p=1,order=3,parity=:cos),
        (family=:LP,l=3,m=1,p=0,order=3,parity=:cos),
        (family=:LP,l=2,m=2,p=1,order=4,parity=:cos),
        (family=:LP,l=4,m=1,p=0,order=4,parity=:cos),
        (family=:LP,l=0,m=4,p=3,order=6,parity=:axisymmetric)])
end
rows = Dict{String,Any}()
for (name,fiber) in (("grin",GRIN(;lambda0=1550e-9,core_radius=31.25e-6,NA=.275)),
    ("step",StepIndex(;lambda0=1550e-9,core_radius=3.3*1550e-9/(2pi*.03),NA=.03)))
    labels = name=="grin" ? labels_grin : PP._step_labels(fiber,3)
    for nxy in (129,257)
        x,y=PP._analytic_grid(fiber,labels;grid_size=nxy,grid_half_width=nothing)
        fields=name=="grin" ? PP._grin_fields(fiber,material,labels,:LP,x,y) : PP._step_fields(fiber,labels,x,y)
        offsets,w0=PP._dispersion_offsets(fiber.lambda0,5,20.,13)
        bs=PP._analytic_beta_samples(fiber,material,labels,offsets,w0)
        beta=PP._fit_taylor_beta(offsets,bs,5,12).coefficients
        S=PP._spatial_overlap(fields,x,y).values
        t0=.5; ld=t0^2/abs(beta[3,1]); gamma=material.n2*w0/2.99792458e-4*S[1,1,1,1]
        label=name*"_"*string(nxy)
        groups=name=="grin" ? [l.order for l in labels] : [0,1,1]
        npzwrite(joinpath(out,label*".npz"),Dict("S"=>S,"beta"=>beta,"x"=>x,"y"=>y,"fields"=>fields,"groups"=>groups))
        rows[label]=Dict("labels"=>[string(l) for l in labels],"T0_ps"=>t0,"LD_m"=>ld,
            "gamma_W_m"=>gamma,"P0_W"=>1/(gamma*ld),"omega0_rad_ps"=>w0,
            "beta0_per_m"=>vec(beta[1,:]),"beta1_ps_m"=>vec(beta[2,:]),"beta2_ps2_m"=>vec(beta[3,:]),
            "delta"=>vec((beta[2,:].-beta[2,1]).*t0./abs(beta[3,1])),
            "b"=>vec(beta[3,:]./beta[3,1]),"S0_per_m2"=>S[1,1,1,1],
            "core_radius_m"=>fiber.core_radius,"NA"=>fiber.NA,
            "gram_error"=>maximum(abs.(PP._mode_gram(fields,x,y)-I)))
    end
end
rows["agent"]="gpt-b";rows["model"]="gpt-6-astra";rows["family"]="gpt"
open(joinpath(out,"material.toml"),"w") do io;TOML.print(io,rows);end
TOML.print(stdout,rows)
