# Extra check for run 2026-10-04-claude-b.1-prepared-sech-readout-20m (not in the archive).
# The archive compared the adjoint derivative dN_out/dN_signal (reference held fixed) with a central finite difference
# at a relative power step of 0.05 % and found a 1.7e-4 relative difference, which it attributed to the curvature of
# the interference response. A central difference has an O(step^2) truncation error, so if that attribution is right
# the difference falls by about 4 each time the step is halved. This script tests that on the standard grid.
#
# Usage: JULIA_NUM_THREADS=2 julia --project=solver fd_step_check.jl
include(joinpath(@__DIR__, "run_prepared_sech_readout.jl"))

function fd_step_check(kind;nt=4096,window=40.,dz=.01,steps=(.002,.001,.0005,.00025,.000125))
    p=problem(kind;nt,window)
    aw0=vec(fftshift(ifft(p.a,1),1))
    rw=R*exp(im*PHI).*aw0
    nin=sum(p.weights.*abs2.(aw0))
    sol=solve_mmgnlse(p.a,p.pars,dz)
    aw=vec(get_spectral_field(sol))
    cw,nout=mean_detected(p,aw,rw)
    terminal=reshape(sqrt(ETA).*p.weights.*cw,p.nt,1,1)
    adj=solve_adjoint(terminal,p.pars,dz;forward_solution=sol,units=:power,adjoint_mode=:discrete_rk4ip)
    g=vec(get_spectral_field(adj;units=:photon))
    b=sqrt.(p.weights).*aw0
    exact=real(dot(g,b./sqrt(nin)))/sqrt(nin)
    rows=Dict{String,Any}[]
    for epsilon in steps
        vals=Float64[]
        for scale in (1-epsilon,1+epsilon)
            ss=solve_mmgnlse(p.a.*sqrt(scale),p.pars,dz)
            _,nn=mean_detected(p,vec(get_spectral_field(ss)),rw)
            push!(vals,nn)
        end
        fd=(vals[2]-vals[1])/(2epsilon*nin)
        push!(rows,Dict{String,Any}("relative_power_step"=>epsilon,"finite_difference"=>fd,
            "adjoint"=>exact,"relative_difference_adjoint_minus_fd"=>(exact-fd)/fd))
        @printf("FD_STEP %s step=%.6g fd=%.15g adjoint=%.15g reldiff=%.6g\n",kind,epsilon,fd,exact,(exact-fd)/fd);flush(stdout)
    end
    d=Dict{String,Any}("run_id"=>RUN_ID,"kind"=>kind,"nt"=>nt,"window_ps"=>window,"dz_m"=>dz,"rows"=>rows,
        "driver_sha256"=>file_sha256(@__FILE__))
    write_toml(joinpath(RAW,"fd_step_check_"*kind*".toml"),d)
    d
end

if abspath(PROGRAM_FILE) == @__FILE__
    for kind in (isempty(ARGS) ? ["agarwal"] : ARGS)
        fd_step_check(kind)
    end
end
